# This MCEdit filter is for writing ALife to the Raspberry Pi
# Implementation by @abrightmoore http://brightmoore.net

import minecraft.minecraft as minecraft # Martin O'Hanlon - http://raspberrypi.mythic-beasts.com/magpi/The-MagPi-issue-11-en.pdf
import minecraft.block as block

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *


inputs = (
	("abrightmoore@yahoo.com.au", "label"),
	("http://brightmoore.net", "label"),
	("Cell Material", alphaMaterials.BlockofIron),
	("Other Material", alphaMaterials.Glass),
	("Number of iterations", 1000),
	("Host:", ("string","value=localhost")),
	("Port:", 4711),
	("X:", 0),
	("Y:", 0),
	("Z:", 0),
#	("Clear to Read, Check to Write:", False),

)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt((int)(x),(int)(y),(int)(z))
    if tempBlock == 0:
	setBlock(level, (block, data), (int)(x),(int)(y),(int)(z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, (int)(y)):
    	setBlockIfEmpty(level, (block, data), (int)(x),(int)(iterY),(int)(z))
    	

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def fix(angle):
	while angle > pi:
		angle = angle - 2 * pi
	while angle < -pi:
		angle = angle + 2 * pi
	return angle

def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			scratchpad.setBlockAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockID)
			scratchpad.setBlockDataAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	ALIFEMCPI(level, box, options)		
	level.markDirtyBox(box)


def ALIFEMCPI(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "ALIFEMCPI"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	host = options["Host:"]
	port = options["Port:"]
	#rw = options["Clear to Read, Check to Write:"]
	X = options["X:"]
	Y = options["Y:"]
	Z = options["Z:"]

	# http://en.wikipedia.org/wiki/Conway's_Game_of_Life#Rules
	# The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead. Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:
	# Any live cell with fewer than two live neighbours dies, as if caused by under-population.
	# Any live cell with two or three live neighbours lives on to the next generation.
	# Any live cell with more than three live neighbours dies, as if by overcrowding.
	# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
	
	MATERIAL = options["Cell Material"] # This is the cell block when alive. When dead, it is other (below)
	OTHERMATERIAL = options["Other Material"] #
	ITERATIONS = options["Number of iterations"]

	# Reading from the Pi with getBlock is far too expensive currently. Until getBlocks() is available, write only.
	WIDTH = width
	DEPTH = depth
	HEIGHT = height
	HEIGHTOFFSET = -1 # Clouds. Sort of.
	DEAD = -1

	Q = zeros((WIDTH,DEPTH,HEIGHT,2)) # -1 = dead, otherwise the number indicates the number of neighbours
	
	fieldIndex = 0
	
	# Seed the field with the blocks from the MCEdit selection
	for iterY in xrange(0, HEIGHT):
		for iterX in xrange(0, WIDTH):
			for iterZ in xrange(0, DEPTH):
				if level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ) != 0: # Not air
					Q[iterX,iterZ,iterY,fieldIndex] = 0
				else:
					Q[iterX,iterZ,iterY,fieldIndex] = DEAD

	print 'Connecting to %s:%s' % (host, port)
	mc = minecraft.Minecraft.create(host, port)
	print 'Connected to %s:%s' % (host, port)
	print 'Fetching the player position'
	playerPos = mc.player.getPos()
	print 'Player is at %s %s %s' % (playerPos.x, playerPos.y, playerPos.z)
	
	mc.postToChat("ALIFE_CraftPI is starting.")
	
	theBlock = block.AIR
	theBlock.id = options["Cell Material"].ID
	theBlock.data = options["Cell Material"].blockData
	
	theOtherBlock = block.GLASS
	theOtherBlock.id = options["Other Material"].ID
	theOtherBlock.data = options["Other Material"].blockData

	for cycling in xrange(0, ITERATIONS):
		# print '%s: %s Iteration of %s' % (method, cycling, ITERATIONS)
		
		countAlive = 0
		countDeath = 0
		countBirth = 0
		# First pass - re-scan the current field. 
		for iterY in xrange(0, HEIGHT):
			for iterX in xrange(0,WIDTH):
				for iterZ in xrange(0,DEPTH):
					# Count Neighbours here
					neighbourCount = 0
					for ix in xrange(-1,2):
						for iz in xrange(-1,2):
							if ix == 0 and iz == 0:
								t = 0
							else: #if ix != 0 or iz != 0: # Don't count the current cell
								if Q[(iterX+ix)%WIDTH,(iterZ+iz)%DEPTH,iterY,fieldIndex%2] != DEAD:
									#print 'Found a neighbour at %s %s' % ((iterX+ix)%WIDTH,(iterZ+iz)%DEPTH)								
									neighbourCount = neighbourCount +1
					# print 'NeighbourCount %s' % (neighbourCount)
					# Conway's ALife logic
					if Q[iterX,iterZ, iterY, fieldIndex%2] != DEAD: # It's alive!
						if neighbourCount < 2 or neighbourCount > 3:
							Q[iterX, iterZ, iterY, (fieldIndex+1)%2] = DEAD
							#print 'killing %s %s' % (iterX, iterZ)
							countDeath = countDeath +1
						elif neighbourCount == 2 or neighbourCount ==3:
							Q[iterX, iterZ, iterY, (fieldIndex+1)%2] = neighbourCount
							#print 'leaving alive %s %s' % (iterX, iterZ)
							countAlive = countAlive +1
					else: # It is dead
						if neighbourCount == 3:
							Q[iterX, iterZ, iterY, (fieldIndex+1)%2] = neighbourCount # It's alive!
							#print 'new baby at %s %s' % (iterX, iterZ)
							countBirth = countBirth +1
						else:
							Q[iterX, iterZ, iterY, (fieldIndex+1)%2] = DEAD # Set it dead on the target field.
		print 'Generation %s: Born %s, Alive %s, Dead %s' % (cycling, countBirth, countAlive, countDeath)
		# Now we have a newly calculated field. Let's use it
		fieldIndex = (fieldIndex +1)%2 # Swap buffers
				
		# Write out the new blocks, get rid of the dead blocks. Do as little by way of writing to the remote API as possible
		for iterY in xrange(0, HEIGHT):
			for iterX in xrange(0,WIDTH):
				for iterZ in xrange(0,DEPTH):
					if Q[iterX,iterZ,iterY,fieldIndex] != DEAD: # Now alive. Set to material
						mc.setBlock((int)(playerPos.x+iterX),(int)(playerPos.y+iterY+HEIGHTOFFSET),(int)(playerPos.z+iterZ),theBlock) # ToDo: Use setBlocks for a boost
					elif Q[iterX,iterZ,iterY,fieldIndex] == DEAD and Q[iterX,iterZ,iterY,(fieldIndex+1)%2] != DEAD: # Was alive, now dead. Set to air
						#else: # is Dead
						mc.setBlock((int)(playerPos.x+iterX),(int)(playerPos.y+iterY+HEIGHTOFFSET),(int)(playerPos.z+iterZ),theOtherBlock) # ToDo: Use setBlocks for a boost
	
	print 'Copying field of cells back to MCEdit'
					
	for iterY in xrange(0, HEIGHT):
		for iterX in xrange(0,WIDTH):
			for iterZ in xrange(0,DEPTH):
				if Q[iterX,iterZ,iterY,fieldIndex] != DEAD: # Now alive. Set to material
					#print '%s %s' % (iterX, iterZ)
					setBlock(level,(theBlock.id,theBlock.data),(int)(box.minx+iterX),(int)(box.miny+iterY),(int)(box.minz+iterZ)) # ToDo: Use setBlocks for a boost
					#setBlock(level,(1,0),(int)(box.minx+iterX),(int)(box.miny),(int)(box.minz+iterZ)) # ToDo: Use setBlocks for a boost
				else: # Was alive, now dead. Set to air
					setBlock(level,(0,0),(int)(box.minx+iterX),(int)(box.miny+iterY),(int)(box.minz+iterZ)) # ToDo: Use setBlocks for a boost
						
	mc.postToChat("ALIFE_CraftPI is now complete.")
	
	print '%s: Ended at %s' % (method, time.ctime())		
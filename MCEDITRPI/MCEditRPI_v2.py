# This MCEdit filter is for reading and writing regions to the Raspberry Pi
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
	("Host:", ("string","value=rpi314")),
	("Port:", 4711),
	("X:", 0),
	("Y:", 0),
	("Z:", 0),
	("Clear to Read, Check to Write:", False),

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
	MCPI(level, box, options)		
	level.markDirtyBox(box)


def MCPI(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "MCPI"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	host = options["Host:"]
	port = options["Port:"]
	rw = options["Clear to Read, Check to Write:"]
	X = options["X:"]
	Y = options["Y:"]
	Z = options["Z:"]
	
	if width > 255: width = 255
	if height > 255: height = 255
	if depth > 255: depth = 255

	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	
	mc = minecraft.Minecraft.create(host, port)
	playerPos = mc.player.getPos()
	print 'Player is at %s %s %s' % (playerPos.x, playerPos.y, playerPos.z)
	
	count = 0
	if rw == False:

		mc.postToChat("Reading MCPI world from MCEdit...")	
		
		for iterX in xrange(0,width):
			for iterY in xrange(0,height):
				for iterZ in xrange(0,depth):
					theBlock = mc.getBlockWithData((int)(-centreWidth+iterX+X),(int)(-centreHeight+iterY+Y),(int)(-centreDepth+iterZ+Z)) # read from RPI. TODO - use getBlocks instead for a boost
					count = count +1
					if count %10 == 0:
						print 'Read MCPI to MCEdit Progress: %s %s %s = %s:%s' % (iterX, iterY, iterZ, theBlock.id, theBlock.data)
					setBlock(level, (theBlock.id, theBlock.data), box.minx+iterX, box.miny+iterY, box.minz+iterZ) # write to MCEdit
		mc.postToChat("MCPI world read complete.")
	else: # Write back
		theBlock = block.AIR
		mc.postToChat("Writing MCPI world from MCEdit...")
		for iterX in xrange(0,width):
			for iterY in xrange(0,height):
				for iterZ in xrange(0,depth):
					count = count +1
					if count %10 == 0:
						print 'Write MCPI to MCEdit Progress: %s %s %s' % (iterX, iterY, iterZ)
					theBlock.id = level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ)
					theBlock.data = level.blockDataAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ)
					mc.setBlock((int)(-centreWidth+iterX+X),(int)(-centreHeight+iterY+Y),(int)(-centreDepth+iterZ+Z),theBlock) # Use setBlocks for a boost
		
		mc.postToChat("MCPI world write complete.")
	
	print '%s: Ended at %s' % (method, time.ctime())		
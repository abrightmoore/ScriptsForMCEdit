# This filter creates cubes in the selection box.
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
	  ("CUBES", "label"),
	  ("Pick a block:", "blocktype"),
	  ("Floors?", False),
	  ("Floor block:", "blocktype"),
	  ("Floor chance:", 100),
	  ("Walls?", False),
	  ("Wall block:", "blocktype"),
	  ("Wall chance:", 100),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label")
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
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Cubes(level, box, options)		
	level.markDirtyBox(box)

def Cube(level, block, (x1,y1,z1),(x2,y2,z2), floors, floorBlock, floorChance, walls, wallBlock, wallChance):
	# Draws a cube
	method = "CUBE"
	print '%s: Started at %s' % (method, time.ctime())

	# Render all the verteces
	
	drawLine(level, block, (x1, y1, z1), (x2, y1, z1) )
	drawLine(level, block, (x1, y1, z1), (x1, y2, z1) )
	drawLine(level, block, (x1, y1, z1), (x1, y1, z2) )
	drawLine(level, block, (x2, y2, z1), (x2, y2, z2) )
	drawLine(level, block, (x2, y2, z1), (x1, y2, z1) )
	drawLine(level, block, (x2, y2, z1), (x2, y1, z1) )
	drawLine(level, block, (x1, y2, z2), (x1, y2, z1) )
	drawLine(level, block, (x1, y2, z2), (x1, y1, z2) )
	drawLine(level, block, (x1, y2, z2), (x2, y2, z2) )
	drawLine(level, block, (x2, y1, z2), (x1, y1, z2) )
	drawLine(level, block, (x2, y1, z2), (x2, y2, z2) )
	drawLine(level, block, (x2, y1, z2), (x2, y1, z1) )
	
	if floors == True:
		if randint(0,100) < floorChance:
			for iterX in xrange(x1+1,x2):
				drawLine(level, floorBlock, (iterX, y1, z1+1), (iterX, y1, z2-1) )
		if randint(0,100) < floorChance:
			for iterX in xrange(x1+1,x2):
				drawLine(level, floorBlock, (iterX, y2, z1+1), (iterX, y2, z2-1) )

	if walls == True:
		if randint(0,100) < wallChance:
			for iterY in xrange(y1+1,y2):
				drawLine(level, wallBlock, (x1, iterY, z1+1), (x1, iterY, z2-1) )
	if walls == True:
		if randint(0,100) < wallChance:
			for iterY in xrange(y1+1,y2):
				drawLine(level, wallBlock, (x2, iterY, z1+1), (x2, iterY, z2-1) )
	if walls == True:
		if randint(0,100) < wallChance:
			for iterY in xrange(y1+1,y2):
				drawLine(level, wallBlock, (x1+1, iterY, z1), (x2-1, iterY, z1) )
	if walls == True:
		if randint(0,100) < wallChance:
			for iterY in xrange(y1+1,y2):
				drawLine(level, wallBlock, (x1+1, iterY, z2), (x2-1, iterY, z2) )
			
	print '%s: Ended at %s' % (method, time.ctime())	
	
def CubeIter(level, block, (x1,y1,z1), (x2,y2,z2), floors, floorBlock, floorChance, walls, wallBlock, wallChance):
	MAXSIZE = 2
	CHANCE = 2

	halfWidth = (int)((x2-x1)/2)
	halfHeight = (int)((y2-y1)/2)
	halfDepth = (int)((z2-z1)/2)

	if x2-x1 > MAXSIZE and y2-y1 > MAXSIZE and z2-z1 > MAXSIZE: # If the cube isn't too small
		Cube(level, block, (x1,y1,z1), (x2,y2,z2), floors, floorBlock, floorChance, walls, wallBlock, wallChance) # Draw this cube
	
		# For each octet of the cube, randomly go deeper, until a limit is reached.
		
		if randint(0,CHANCE) == 1:
			CubeIter(level, block, (x1,y1,z1), (x1+halfWidth, y1+halfHeight, z1+halfDepth), floors, floorBlock, floorChance, walls, wallBlock, wallChance)
		if randint(0,CHANCE) == 1:
			CubeIter(level, block, (x1+halfWidth,y1,z1), (x2, y1+halfHeight, z1+halfDepth), floors, floorBlock, floorChance, walls, wallBlock, wallChance)
		if randint(0,CHANCE) == 1:
			CubeIter(level, block, (x1,y1+halfHeight,z1), (x1+halfWidth, y2, z1+halfDepth), floors, floorBlock, floorChance, walls, wallBlock, wallChance)
		if randint(0,CHANCE) == 1:
			CubeIter(level, block, (x1,y1,z1+halfDepth), (x1+halfWidth, y1+halfHeight, z2), floors, floorBlock, floorChance, walls, wallBlock, wallChance)
		if randint(0,CHANCE) == 1:
			CubeIter(level, block, (x1+halfWidth,y1+halfHeight,z1), (x2, y2, z1+halfDepth), floors, floorBlock, floorChance, walls, wallBlock, wallChance)
		if randint(0,CHANCE) == 1:
			CubeIter(level, block, (x1,y1+halfHeight,z1+halfDepth), (x1+halfWidth, y2, z2), floors, floorBlock, floorChance, walls, wallBlock, wallChance)
		if randint(0,CHANCE) == 1:
			CubeIter(level, block, (x1+halfWidth,y1,z1+halfDepth), (x2, y1+halfHeight, z2), floors, floorBlock, floorChance, walls, wallBlock, wallChance)
		if randint(0,CHANCE) == 1:
			CubeIter(level, block, (x1+halfWidth,y1+halfHeight,z1+halfDepth), (x2, y2, z2), floors, floorBlock, floorChance, walls, wallBlock, wallChance)

def Cubes(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "CUBES"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	blockID = options["Pick a block:"].ID
	blockData = options["Pick a block:"].blockData
	floors = options["Floors?"]
	floorBlock = (options["Floor block:"].ID,options["Floor block:"].blockData)
	floorChance = options["Floor chance:"]
	walls = options["Walls?"]
	wallBlock = (options["Wall block:"].ID,options["Wall block:"].blockData)
	wallChance = options["Wall chance:"]
	# END CONSTANTS

	CubeIter(level, (blockID,blockData), (box.minx, box.miny, box.minz), (box.maxx, box.maxy, box.maxz), floors, floorBlock, floorChance, walls, wallBlock, wallChance)
	
	print '%s: Ended at %s' % (method, time.ctime())
	

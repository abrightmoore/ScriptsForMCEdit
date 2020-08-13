# This filter extends the base block of a tree into the soil
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
		("DROP THE BASE", "label"),
		("Material to drop:", alphaMaterials.Wood),
		("Material to replace:", alphaMaterials.Dirt),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
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
	DropTheBase(level, box, options)		
	level.markDirtyBox(box)

def DropTheBase(level, box, options): 
	
	method = "DROP THE BASE"
	print '%s: Started at %s' % (method, time.ctime())	
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	
	materialToReplace = (options["Material to replace:"].ID, options["Material to replace:"].blockData)
	material = (options["Material to drop:"].ID, options["Material to drop:"].blockData)

	iterY = box.maxy
	while iterY >= box.miny:
		iterY = iterY -1
	#for iterY in xrange(box.miny,box.maxy): #Height
		print '%s: Layer %s of %s' % (method, iterY-box.miny+1, height)
		for iterZ in xrange(box.minz,box.maxz): #Depth
			for iterX in xrange(box.minx,box.maxx): #Width
				tempBlock = (level.blockAt( iterX, iterY, iterZ),level.blockDataAt( iterX, iterY, iterZ))
				if tempBlock == material: # Only randomise the selected material
					belowBlock = (level.blockAt( iterX, iterY-1, iterZ),level.blockDataAt( iterX, iterY-1, iterZ))
					if belowBlock == materialToReplace:
						belowBlock1 = level.blockAt( iterX-1, iterY-1, iterZ)
						belowBlock2 = level.blockAt( iterX+1, iterY-1, iterZ)
						belowBlock3 = level.blockAt( iterX, iterY-1, iterZ-1)
						belowBlock4 = level.blockAt( iterX, iterY-1, iterZ+1)
						if belowBlock1 == 0 or belowBlock2 == 0 or belowBlock3 == 0 or belowBlock4 == 0:
							setBlock(level, material, iterX, iterY-1, iterZ)
							print '%s: Replaced material at %s %s %s' % (method, iterX, iterY-1, iterZ)
		
		
	print '%s: Ended at %s' % (method, time.ctime())


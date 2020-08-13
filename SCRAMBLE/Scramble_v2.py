# This filter randomises the data values of blocks in the selection box within defined limits
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
		("SCRAMBLE", "label"),
		("Material to replace:", alphaMaterials.StoneBricks),
		("Material:", alphaMaterials.StoneBrickStairs),
		("Data Range:", ("string","value=0 15")),
		("Chance:", 10),
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
	Scramble(level, box, options)		
	level.markDirtyBox(box)

def Scramble(level, box, options): 
	
	method = "SCRAMBLE"
	print '%s: Started at %s' % (method, time.ctime())	
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	
	materialToReplace = options["Material to replace:"].ID
	material = options["Material:"].ID #, options["Material:"].blockData)
	dataRange = options["Data Range:"].split()
	dataRangeList = map(int, dataRange)
	dataMin = dataRangeList[0]
	dataMax = dataRangeList[1]
	chance = options["Chance:"]

	# for iterY in xrange(0,height): #Height

	for iterY in xrange(box.miny,box.maxy): #Height
		print '%s: Layer %s of %s' % (method, iterY-box.miny+1, height)
		for iterZ in xrange(box.minz,box.maxz): #Depth
			for iterX in xrange(box.minx,box.maxx): #Width
				if randint(0,99) < chance:
					tempBlock = level.blockAt( iterX, iterY, iterZ)
					if tempBlock == materialToReplace and tempBlock != 0: # Only randomise the selected material
							newValue = randint(dataMin, dataMax)
							setBlock(level, (material, newValue), iterX, iterY, iterZ)
					
				#		level.blockDataAt( box.minx + iterX, box.miny+iterY, box.minz+iterZ) )

	
	print '%s: Ended at %s' % (method, time.ctime())


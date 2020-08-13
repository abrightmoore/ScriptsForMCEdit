# This MCEdit filter is from an idea by @tomutwit on Twitter to randomly redistribute all blocks in a chunk
# Implementation by @abrightmoore http://brightmoore.net

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
	("abrightmoore@yahoo.com.au", "label"),
	("http://brightmoore.net", "label"),
	("Select a region, run the filter.", "label"),

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
	porridge(level, box, options)		
	level.markDirtyBox(box)


def porridge(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "PORRIDGE"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Scan the box and create a list of all the valid locations with non-air blocks
	
	QLoc = []
	QBlock = []
	for iterX in xrange(0,width):
		for iterY in xrange(0,height):
			for iterZ in xrange(0,depth):
				theBlock = level.blockAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				if theBlock != 0: # current block is not air
					theBlockData = level.blockDataAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					QLoc.append( (iterX, iterY, iterZ) )
					QBlock.append( (theBlock, theBlockData) )

	# ... then write out random blocks to the region to valid locations previously placed on the list.
		
	count = 0
	for (x, y, z) in QLoc:
		count = count + 1
		if count % 10 == 0:
			print '%s: %s Progress %s of %s' % (method, time.ctime(), count, len(QLoc))		
		
		index = randint(0, len(QBlock)-1 )
		
		newBlock = QBlock.pop( index )
		
		setBlock(level, newBlock, box.minx+x, box.miny+y, box.minz+z)

	

	print '%s: Ended at %s' % (method, time.ctime())		
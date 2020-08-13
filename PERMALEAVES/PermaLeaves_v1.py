# This MCEdit filter is from an idea by Hypixel to convert leaves in a map to permanent, as if the player had placed them, preventing decay.
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
	("Confirm?", False),
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
	permaLeaves(level, box, options)		
	level.markDirtyBox(box)


def permaLeaves(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "PERMALEAVES"
	print '%s: Started at %s' % (method, time.ctime())
	width = box.maxx-box.minx
	printBlockDetails = options["Confirm?"]

	count = 0
	for iterX in xrange(box.minx, box.maxx):
		count = count + 1
		if count % 10 == 0:
			print '%s: %s Progress %s of %s' % (method, time.ctime(), count, width)		

		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				theBlock = level.blockAt(iterX, iterY, iterZ)
				if theBlock == 18:
					theBlockData = level.blockDataAt(iterX, iterY, iterZ)
					if printBlockDetails == True:
						print '%s: %s found %s:%s at %s %s %s' % (method, time.ctime(), theBlock, theBlockData, iterX, iterY, iterZ)
					changed = False
					if theBlockData > -1 and theBlockData < 4:
						theBlockData = theBlockData + 4
						changed = True
					elif theBlockData > 7 and theBlockData < 12:
						theBlockData = theBlockData - 4
						changed = True
					if changed == True:
						setBlock(level, (theBlock, theBlockData), iterX, iterY, iterZ)

	print '%s: Ended at %s' % (method, time.ctime())		
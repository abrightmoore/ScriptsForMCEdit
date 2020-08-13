# This filter lays down a smooth undulating sheet of fresh white snow.
# Requested by @Anistuffs
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials

inputs = (
	  ("BOS", "label"),
	  ("Ignore block IDs:", ("string","value=0 6 7 8 9 10 11 12 13 27 28 30 31 32 37 38 39 40 50 51 52 55 59 63 64 65 66 68 69 70 71 72 78 83 93 94 96 104 105 106 115 116 118 119 127 131 132 140 141 142 143 145 147 148 149 150 151 154 157") ),
	  ("Radius:", 4),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt(x,y,z)
    if tempBlock == 0:
	setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
    	level.setBlockDataAt(x, y, z, data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, y):
    	setBlockIfEmpty(level, (block, data), x, iterY, z)
    	

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def fix(angle):
	while angle > pi:
		angle = angle - 2 * pi
	while angle < -pi:
		angle = angle + 2 * pi
	return angle

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	BOS(level, box, options)		
	level.markDirtyBox(box)
	
def BOS(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "BOS"
	print '%s: Started at %s' % (method, time.ctime())
	ignore = options["Ignore block IDs:"].split()
	ignoreList = map(int, ignore)
	radius = options["Radius:"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	theField = zeros((width,depth)) # a 2D array of heights, seeded with 0

	# First pass - identify heights
	for iterX in xrange(0, width):
		for iterZ in xrange(0, depth):		
			iterY = height -1	
			while iterY >= 0:
				tempBlock = level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ)
				if tempBlock != 0 and not (tempBlock in ignoreList):
					theField[iterX][iterZ] = iterY
					iterY = 0 # break
				iterY = iterY - 1

	theSnowField = zeros((width,depth)) # a 2D array of heights, seeded with 0

	# Second pass - Scan the surface and determine the slope height at each point as an average of the surrounding blocks heights. Identify maxima and minima.
	for iterX in xrange(0, width):
		for iterZ in xrange(0, depth):
			localSum = 0
			numberOfPoints = 0
			for x in xrange(0,radius*2): # Improve on this - make it circular
				for z in xrange(0,radius*2):
					px = radius-x+iterX
					pz = radius-z+iterZ
							
					if px >= 0 and px < width and pz >=0 and pz < depth:	
						localSum = localSum + theField[px][pz] # Add the height at this point
						# print 'u %s' % (localSum)
						numberOfPoints = numberOfPoints + 1
			if numberOfPoints > 0:
				theSnowField[iterX][iterZ] = (float)(localSum / numberOfPoints) # simple average
				print 's %s' % theSnowField[iterX][iterZ]
				
	# Third pass - plot
	for iterX in xrange(0, width):
		for iterZ in xrange(0, depth):
			snowHeightHere = abs(((float)(theSnowField[iterX][iterZ]) - (float)(theField[iterX][iterZ]))*100/16)
			if snowHeightHere > 7:
				snowHeightHere = 7
			elif snowHeightHere < -7:
				snowHeightHere = -7 
			print 'v %s' % ((int)(snowHeightHere))
			setBlock(level, (78, (int)(8+snowHeightHere)), box.minx+iterX, box.miny+theField[iterX][iterZ]+1, box.minz+iterZ)


	print '%s: Ended at %s' % (method, time.ctime())
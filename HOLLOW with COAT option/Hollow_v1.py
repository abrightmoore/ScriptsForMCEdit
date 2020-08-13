# This filter hollows out a solid shape.
# Suggested by @Jigarbov on Twitter.
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("HOLLOW", "label"),
	  ("Material:", alphaMaterials.Air),
	  ("Coat:", False),
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
	Hollow(level, box, options)		
	level.markDirtyBox(box)
	
def Hollow(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Hollow"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	PURGEAMOUNT = 9+8+9
	material = (options["Material:"].ID, options["Material:"].blockData)
	coat = options["Coat:"]
	# END CONSTANTS


	# First pass, scan and count neighbours
	F = zeros( (width, height, depth) ) # This field holds the count of how many neighbour blocks there are

	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				thisBlock = level.blockAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				if thisBlock != AIRBLOCK: # Now I need to push this block's contribution into all the neighbour blocks in a 3x3 grid
					for dx in xrange(-1,2):
						for dy in xrange(-1,2):
							for dz in xrange(-1,2):
								if dx == 0 and dy == 0 and dz == 0:  # Ignore the current block as it is not a neighbour to itself
									T = 0 # ignore
								else:
									(x, y, z) = (iterX + dx, iterY + dy, iterZ + dz)
									if x > 0 and x < (width-1) and y > 0 and y < (height-1) and z > 0 and z < (depth-1):
										F[x][y][z] = F[x][y][z] + 1

	# Pass 2 - purge anywhere the neighbour count indicates the block is completely encased in other blocks
	for iterX in xrange(1, width-1):
		for iterY in xrange(1, height-1):
			for iterZ in xrange(1, depth-1):
				# print '%s' % (F[iterX][iterY][iterZ])
				
				if coat == False:
					if F[iterX][iterY][iterZ] >= PURGEAMOUNT:
						setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				else:
					if F[iterX][iterY][iterZ] < PURGEAMOUNT and F[iterX][iterY][iterZ] > 0:
						setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					
	print '%s: Ended at %s' % (method, time.ctime())
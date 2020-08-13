# This filter sheaths all blocks in a selection box in cladding.
# Requested by @Jigarbov
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("SHEATH", "label"),
	  ("Sheath Material:", alphaMaterials.Cobblestone),
	  ("Base Material:", alphaMaterials.Stone),
	  ("Radius:", 3),
	  ("Round:", False),
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
	Sheath(level, box, options)		
	level.markDirtyBox(box)
	
def Sheath(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Sheath"
	print '%s: Started at %s' % (method, time.ctime())
	materialSheath = (options["Sheath Material:"].ID, options["Sheath Material:"].blockData)
	materialBase = (options["Base Material:"].ID, options["Base Material:"].blockData)
	radius = options["Radius:"]
	round = options["Round:"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	MASKBLOCK = 200
	MASKIGNORE = -100
	# END CONSTANTS

	theField = zeros((width,height,depth))

	# First pass - blocks, air and base masking
	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				tempBlock = (level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ), level.blockDataAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ))
				if tempBlock != AIR:
					if tempBlock == materialBase:
						theField[iterX][iterY][iterZ] = MASKIGNORE # ignore 
					else:
						theField[iterX][iterY][iterZ] = MASKBLOCK # is a block

	# Second pass - mask out the region around each block					
	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				mask = theField[iterX][iterY][iterZ]
				if mask >= MASKBLOCK: # is a block, apply the mask!
					zippedyDooDax = -radius
					while zippedyDooDax <= radius:
						zippedyDooDay = -radius
						while zippedyDooDay <= radius:
							zippedyDooDaz = -radius
							while zippedyDooDaz <= radius:
								x = iterX + zippedyDooDax
								y = iterY + zippedyDooDay
								z = iterZ + zippedyDooDaz
								if x >= 0 and x < width and y >= 0 and y < height and z >= 0 and z < depth: # array bounds check
									if round == False:
										theField[x][y][z] = theField[x][y][z] + 1
									else: # roundlish
										x1 = zippedyDooDax * zippedyDooDax
										y1 = zippedyDooDay * zippedyDooDay
										z1 = zippedyDooDaz * zippedyDooDaz
										r1 = radius * radius
										
										if ((x1 + y1) <= r1) and ((y1 + z1) <= r1) and ((x1 + z1) <= r1):
											theField[x][y][z] = theField[x][y][z] + 1
										
										
								zippedyDooDaz = zippedyDooDaz + 1
							zippedyDooDay = zippedyDooDay + 1
						zippedyDooDax = zippedyDooDax + 1

	# Third pass - plot
	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				# print '%s1: %s %s %s is %s' % (method, iterX, iterY, iterZ, theField[iterX][iterY][iterZ])
				if theField[iterX][iterY][iterZ] == 0: # is unmasked, replace!
					setBlockIfEmpty(level, materialSheath, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
	



	print '%s: Ended at %s' % (method, time.ctime())
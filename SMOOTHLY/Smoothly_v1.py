# This filter rounds out jaggedy height variation within a selection box.
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("SMOOTHLY", "label"),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

def perform(level, box, options):
    ''' Feedback to abrightmoore@yahoo.com.au '''
    Smoothly(level, box, options)
    level.markDirtyBox(box)

def Smoothly(level, box, options):
	method = "SMOOTHLY"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	
	# approach -
	# identify the heights at each x/z location (the 'Y')
	# for each range of cells in the area, determine a new average height.
	# Adjust the height of each block to the new average height. If going up, replicate the top block. If down, cut the stack by setting with air
	
	# Pass 1 - stolen from my Drape filter
	HEIGHTMAP = zeros((width,depth)) #  Height map. I should probably get this from chunk data instead of brute-forcing it.
	MAX = 0
	MIN = 9999999
	for iterX in xrange(box.minx, box.maxx):
		print '%s: Scanning column %s of %s' % (method, iterX-box.minx, width)
		for iterZ in xrange(box.minz, box.maxz):
			# start from the base of the selection, find the top of the landscape. That's the point to redraw the object at.
			topY = box.maxy
			keepGoing = 1
			while topY > box.miny-1 and keepGoing == 1:
				tempBlock = (level.blockAt(iterX,topY,iterZ), level.blockDataAt(iterX,topY,iterZ))
				if tempBlock <> AIR: # found a block. Must be the top!
					keepGoing = 0
					HEIGHTMAP[iterX-box.minx,iterZ-box.minz] = topY #
					if topY > MAX:
						MAX = topY
					if topY < MIN:
						MIN = topY
				else:
					topY = topY -1

	# Pass 2 - math!
	HEIGHTMAPTGT = zeros((width,depth)) # target map

	MIDPOINT = box.miny + height/2
	
	for iterX in xrange(1, width-1):
		print '%s: Recalculating column height %s of %s' % (method, iterX, width)
		for iterZ in xrange(1, depth-1):
			HEIGHTMAPTGT[iterX][iterZ] = HEIGHTMAP[iterX-1][iterZ-1] + HEIGHTMAP[iterX-1][iterZ] + HEIGHTMAP[iterX-1][iterZ+1] + HEIGHTMAP[iterX][iterZ-1] + HEIGHTMAP[iterX][iterZ] + HEIGHTMAP[iterX][iterZ+1] + HEIGHTMAP[iterX+1][iterZ-1] + HEIGHTMAP[iterX+1][iterZ] + HEIGHTMAP[iterX+1][iterZ+1]
			HEIGHTMAPTGT[iterX][iterZ] = HEIGHTMAPTGT[iterX][iterZ] / 9 # average the local set of blocks to find the new height.
			
	# Pass 3 - apply
	for iterX in xrange(1, width-1):
		print '%s: Applying changes to column height %s of %s' % (method, iterX, width)
		for iterZ in xrange(1, depth-1):		
			delta = (int)(HEIGHTMAPTGT[iterX][iterZ] - HEIGHTMAP[iterX][iterZ])
			if delta > 0: # Go higher!
				tempBlock = (level.blockAt(box.minx+iterX,HEIGHTMAP[iterX][iterZ],box.minz+iterZ), level.blockDataAt(box.minx+iterX,HEIGHTMAP[iterX][iterZ],box.minz+iterZ))
				for iterY in xrange(1,delta):
					setBlock(level,tempBlock,iterX+box.minx,HEIGHTMAP[iterX][iterZ]+iterY,iterZ+box.minz)
			elif delta < 0: # Remove blocks
				for iterY in xrange(0,-delta):
					setBlock(level,AIR,iterX+box.minx,HEIGHTMAP[iterX][iterZ]-iterY,iterZ+box.minz) # air
			# elif delta == 0: # do nothing
				
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)
		
def getBoxSize(box):
    return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
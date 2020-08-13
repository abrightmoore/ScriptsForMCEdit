# This filter replaces a bunch of block with other blocks. Requested by /u/Ridddle
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, materials
from mcplatform import *

inputs = (
	  ("BLOCK FLIPPER", "label"),
	  # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Map From List:", ("string","value=16 14 21 73 56 37 38 31 85 52 30 8 9 3 50 39 40 54") ),
	  ("Map To List:", ("string","value=153 89 89 11 88 0 0 0 113 133 13 0 0 11 0 0 0 0") ),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

# Utility methods

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)
   	
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
		
def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	blockFlipper(level, box, options)		
	level.markDirtyBox(box)
	
def blockFlipper(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "BLOCK FLIPPER"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	mapFrom = options["Map From List:"].split()
	mapFromList = map(int, mapFrom)
	mapTo = options["Map To List:"].split()
	mapToList = map(int, mapTo)

	print '%s: %s' % (method, box)
	for i,x in enumerate(mapFromList):
		print '%s: Swapping %s to %s at %s' % (method, level.materials[x], level.materials[mapToList[i]], time.ctime())
		level.fillBlocks(box, level.materials[mapToList[i]], [level.materials[x]])
	print("filled %d blocks" % box.volume )
	

	print '%s: Ended at %s' % (method, time.ctime())
	

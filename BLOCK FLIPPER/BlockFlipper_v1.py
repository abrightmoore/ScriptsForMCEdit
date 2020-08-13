# This filter replaces a bunch of block with other blocks. Requested by /u/Ridddle
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
	  ("BLOCK FLIPPER", "label"),
	  # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Map From List:", ("string","value=2 3 1") ),
	  ("Map To List:", ("string","value=41 42 57") ),
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

	# END CONSTANTS
	COUNTER = 0
	for iterX in xrange(box.minx, box.maxx):
		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				COUNTER = COUNTER+1
				if COUNTER % 10000 == 0:
					print '%s: Step %s - %s of %s' % (method, COUNTER, iterX-box.minx,width)
				theBlock = level.blockAt(iterX,iterY,iterZ)
				index = [i for i,x in enumerate(mapFromList) if x == theBlock]
				for i in index:
					setBlock(level, (mapToList[i], 0), iterX, iterY, iterZ)

	print '%s: Ended at %s' % (method, time.ctime())
	

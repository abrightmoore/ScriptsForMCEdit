# This filter replaces a bunch of block with other blocks. Requested by /u/Ridddle
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, materials
from mcplatform import *

inputs = [
	(
	  ("1-5", "title"),
	  ("BLOCK FLIPPER", "label"),
	  ("Click each tab", "label"),
	  ("Map from 1", alphaMaterials.BlockofIron),
	  ("Map to 1", alphaMaterials.BlockofIron),
	  ("Map from 2", alphaMaterials.BlockofIron),
	  ("Map to 2", alphaMaterials.BlockofIron),
	  ("Map from 3", alphaMaterials.BlockofIron),
	  ("Map to 3", alphaMaterials.BlockofIron),
	  ("Map from 4", alphaMaterials.BlockofIron),
	  ("Map to 4", alphaMaterials.BlockofIron),
	  ("Map from 5", alphaMaterials.BlockofIron),
	  ("Map to 5", alphaMaterials.BlockofIron),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),

    ),
	(
	  ("6-10", "title"),
	  ("BLOCK FLIPPER", "label"),
	  ("Click each tab", "label"),
	  ("Map from 6", alphaMaterials.BlockofIron),
	  ("Map to 6", alphaMaterials.BlockofIron),
	  ("Map from 7", alphaMaterials.BlockofIron),
	  ("Map to 7", alphaMaterials.BlockofIron),
	  ("Map from 8", alphaMaterials.BlockofIron),
	  ("Map to 8", alphaMaterials.BlockofIron),
	  ("Map from 9", alphaMaterials.BlockofIron),
	  ("Map to 9", alphaMaterials.BlockofIron),
	  ("Map from 10", alphaMaterials.BlockofIron),
	  ("Map to 10", alphaMaterials.BlockofIron),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),

  ),
]	  
	  

   	
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
	
	mapList = [ options["Map from 1"],
				options["Map to 1"],
				options["Map from 2"],
				options["Map to 2"],
				options["Map from 3"],
				options["Map to 3"],
				options["Map from 4"],
				options["Map to 4"],
				options["Map from 5"],
				options["Map to 5"],
				options["Map from 6"],
				options["Map to 6"],
				options["Map from 7"],
				options["Map to 7"],
				options["Map from 8"],
				options["Map to 8"],
				options["Map from 9"],
				options["Map to 9"],
				options["Map from 10"],
				options["Map to 10"] ]

	print '%s: %s' % (method, box)
	listPos = 0
	while listPos < len(mapList):
		blockFrom = mapList[listPos]
		blockTo = mapList[listPos+1]
		if blockFrom != blockTo: # Only take an action if the blocks are different
			print '%s: Swapping %s to %s at %s' % (method, blockFrom, blockTo, time.ctime())
			level.fillBlocks(box, blockTo, [blockFrom])
		else:
			print "Skipping "+str((listPos>>1))+" "+str(blockFrom)
		listPos += 2
	print("filled %d blocks" % box.volume )

	print '%s: Ended at %s' % (method, time.ctime())
	

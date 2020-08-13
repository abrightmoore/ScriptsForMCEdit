# This filter deforms the terrain in the selection box by creating a gash in the surface of the world
#
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob

inputs = (
	  ("Drop the Bass", False),
	  ("Embed depth", 0),
	  ("Endermess?", False),
	  ("DRAPE abrightmoore@yahoo.com.au http://brightmoore.net", "label"),
	  ("Use defaults to lay your creation on the ground.", "label"),
	  ("Set Drop the Bass to checked to extend the base block to the floor, leaving the creation in place.", "label"),
	  ("Increase or decrease the Embed depth to adjust the depth of filtered blocks.", "label"),
	  ("Or... simulate an army of Endermen picking apart your world block-by-block with Endermess.", "label"),
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

def Drape(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Drape"
	print '%s: Started at %s' % (method, time.ctime())
	mode = options["Drop the Bass"]
	EMBED_DEPTH = options["Embed depth"]
	ENDERMESS = options["Endermess?"] # Endermess

	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	ENDERMAP = zeros((width,depth)) # Endermess Height map. I should probably get this from chunk data instead of brute-forcing it.
	
	# Pass 1
	for iterX in xrange(box.minx, box.maxx):
		print '%s: Fall %s of %s' % (method, iterX-box.minx, width)
		for iterZ in xrange(box.minz, box.maxz):
			# start from the base of the selection, find the top of the landscape. That's the point to redraw the object at.
			topY = box.miny-1
			keepGoing = 1
			while topY > 0 and keepGoing == 1:
				tempBlock = (level.blockAt(iterX,topY,iterZ), level.blockDataAt(iterX,topY,iterZ))
				if tempBlock <> AIR: # found a block. Must be the top!
					keepGoing = 0
					ENDERMAP[iterX-box.minx,iterZ-box.minz] = topY # Endermess
				else:
					topY = topY -1
			
			if mode == False:
				# transpose all the blocks from the selection down, starting at the new top position
				for iterY in xrange(0,height):
					setBlock(level, 
						 (level.blockAt(iterX,box.miny+iterY,iterZ), level.blockDataAt(iterX,box.miny+iterY,iterZ)),
						 iterX,
						 topY+1+iterY-EMBED_DEPTH,
						 iterZ
						)
			else:
				# Extend the base block to the surface
				setBlockToGround(level, 
						 (level.blockAt(iterX,box.miny,iterZ), level.blockDataAt(iterX,box.miny,iterZ)),
						 iterX,box.miny,iterZ,topY-EMBED_DEPTH
						)
					
	# Endermess - Second pass 
	if ENDERMESS == True:
		ENDERMESS_AMT = randint(width, width*depth)
		print '%s: Endermessing' % (method)
		logger = 0
		for iter in xrange(0,ENDERMESS_AMT):
			logger = logger +1
			if logger%1000 == 0:
				print '%s: Endermessing around %s' % (method, iter)
			
			sourceX = 0
			sourceZ = 0
			targetX = 0
			targetZ = 0
			while sourceX == targetX and sourceZ == targetZ: # Prevent vertical block transposition.
				(sourceX, sourceZ) = (randint(0,width-1),randint(0,depth-1))
				(targetX, targetZ) = (randint(0,width-1),randint(0,depth-1))
			# transpose!
			setBlock(level, 
					 (level.blockAt(sourceX+box.minx,ENDERMAP[sourceX,sourceZ],sourceZ+box.minz), level.blockDataAt(sourceX+box.minx,ENDERMAP[sourceX,sourceZ],sourceZ+box.minz)),
					 targetX+box.minx,
					 ENDERMAP[targetX,targetZ]+1,
					 targetZ+box.minz
					)
		
			setBlock(level, 
					 AIR,
					 sourceX+box.minx,
					 ENDERMAP[sourceX,sourceZ],
					 sourceZ+box.minz
					)
			
			ENDERMAP[sourceX,sourceZ] = ENDERMAP[sourceX,sourceZ]-1
			ENDERMAP[targetX,targetZ] = ENDERMAP[targetX,targetZ]+1
	
	print '%s: Complete at %s' % (method, time.ctime())

def perform(level, box, options):
	''' This script is used to erode the contents of a selected box. Feedback to abrightmoore@yahoo.com.au '''

	Drape(level, box, options)		
	
	level.markDirtyBox(box)
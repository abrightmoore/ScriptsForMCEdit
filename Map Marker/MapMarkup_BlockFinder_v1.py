# This filter provides an in game pointer in the sky to blocks of interest
# Requested by @Helen269 on the forums
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials

# Global constants
METHOD = "MAP MARKER"

inputs = (
	  ("MAPMARKER", "label"),
          ("Choose the block to locate:", "blocktype"),
          ("What should I look for?", ("Match Block Type Only", "Match Block Data") ),
#	  ("Ignore block IDs:", ("string","value=0 6 7 8 9 10 11 12 13 27 28 30 31 32 37 38 39 40 50 51 52 55 59 63 64 65 66 68 69 70 71 72 78 83 93 94 96 104 105 106 115 116 118 119 127 131 132 140 141 142 143 145 147 148 149 150 151 154 157") ),
          ("Main Material:", alphaMaterials.Stone),
          ("Secondary Material:", alphaMaterials.Cobblestone),
          ("Highlight Material:", alphaMaterials.WoodPlanks),
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
	mapMarker(level, box, options)		
	level.markDirtyBox(box)

def mapMarker(level, box, options):
	# CONSTANTS
	print '%s: Started at %s' % (METHOD, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	baseBlock = options["Choose the block to locate:"].ID
	baseBlockData = options["Choose the block to locate:"].blockData


	# First pass - search down-up for the block of interest. On the first hit at x/z, place a marker and move on with the search

	modeMatchBlockData = False
	if options["What should I look for?"] == "Match Block Data":
		modeMatchBlockData = True

	found = 0
	
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			y = box.miny
			while y < box.maxy:
				if modeMatchBlockData == True:
					if level.blockAt(x,y,z) == baseBlock and level.blockDataAt(x,y,z) == baseBlockData:
						print 'I found your block %s at %s %s %s with data value %s' % (baseBlock, x, y, z, baseBlockData)
						buildATower(x,y,z, level, box, options)
						found = found +1
						y = box.maxy # end search at this x/z coord
					
				else:
					if level.blockAt(x,y,z) == baseBlock:
						print 'I found your block %s at %s %s %s' % (baseBlock, x, y, z)
						buildATower(x,y,z, level, box, options)
						found = found +1
						y = box.maxy # end search at this x/z coord

				y = y+1

	print '%s: %s. Found %s' % (METHOD, time.ctime(), found)
	print '%s: Ended at %s' % (METHOD, time.ctime())
	
	
	
def buildATower(x, y, z, level, box, options):
	method = "buildATower"
	HEIGHTOFWALLS = 13
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	#ignore = options["Ignore block IDs:"].split()
	#ignoreList = map(int, ignore)
	AIR=(0,0)
	
	# Find a candidate surface
	iterY = 250
	miny = y
	foundy = y
	while iterY > miny:
		block = level.blockAt(x,iterY,z)
		if block != 0: # not AIR
			#if (block not in ignoreList):
			foundy = iterY
			iterY = miny # end search, block found was a legitimate candidate for the surface				
		iterY = iterY -1
	y = foundy

	print '%s: Started at %s. Position %s %s %s' % (method, time.ctime(), x, y, z)
	


	TURRETWIDTH = 10 + randint(0,8)*2
	TURRETHEIGHT = HEIGHTOFWALLS + randint(6,16)
	TURRETDIAMETER = (int)(pi * TURRETWIDTH)+1 # the number of blocks around the circumference that need to be drawn.
	TURRETRADIUS = (int)(TURRETWIDTH/2)
	TURRETANGLE = (float)(2*pi / TURRETDIAMETER)
	
	startX = (int)(x) # Centre of the turret
	startZ = (int)(z)				

	for turretCircumferenceIter in xrange (0,TURRETDIAMETER):
		wallX = (int)(TURRETRADIUS * cos(TURRETANGLE*turretCircumferenceIter))
		wallZ = (int)(TURRETRADIUS * sin(TURRETANGLE*turretCircumferenceIter))
		window = False

		for iterY in xrange(0, TURRETHEIGHT):
			if randint(0,100) <= 4:
				block = materialSecondary
			else:				
				block = materialMain

			if iterY%6 == 2 and randint(0,100) == 1:
				window = True
				block = AIR
			elif window == True:
				block = AIR
				window = False


			if iterY == 0:
				setBlockToGround(level, block,  
					(int)(startX+wallX),
					(int)(iterY+y),
					(int)(startZ+wallZ),
					y-8
				)
			else:
				setBlock(level, block,  
					(int)(startX+wallX),
					(int)(iterY+y),
					(int)(startZ+wallZ)
				)

	for iterY in xrange(0, TURRETHEIGHT): # Now place flooring
		if (iterY%6) == 0:
			# Drop in a floor
			for floorRadius in xrange(0, TURRETRADIUS):
				floorCircumference = (int)(2 * floorRadius * pi)+1
				floorAngle = 2*pi/floorCircumference
				for floorIter in xrange(0, floorCircumference):
					floorX = (int)(floorRadius * cos(floorAngle * floorIter))
					floorZ = (int)(floorRadius * sin(floorAngle * floorIter))
					block = materialHighlight
					setBlockIfEmpty(level, block,  
						(int)(floorX+startX),
						(int)(iterY+y),
						(int)(floorZ+startZ)
						)
	
	print '%s: Ended at %s' % (method, time.ctime())
	
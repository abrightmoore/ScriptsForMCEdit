# This filter replaces a particular block type with a selection of other blocks at the specified percentage
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# Relay out requested by Mader.

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

inputs = [

	(
	  ("1-2", "title"),
	  ("Click each tab", "label"),
	  ("Material to Replace", alphaMaterials.Stone),
	  ("Replace Chance", 50),
	  ("Material 1", alphaMaterials.BlockofIron),
	  ("Chance 1", 10),
	  ("Material 2", alphaMaterials.BlockofIron),
	  ("Chance 2", 5),

    ),
	(
	  ("3-5", "title"),
	  ("Material 3", alphaMaterials.BlockofIron),
	  ("Chance 3", 0),
	  ("Material 4", alphaMaterials.BlockofIron),
	  ("Chance 4", 0),
	  ("Material 5", alphaMaterials.BlockofIron),
	  ("Chance 5", 0),
	),

	(
	  ("6-8", "title"),
	  ("Material 6", alphaMaterials.BlockofIron),
	  ("Chance 6", 0),
	  ("Material 7", alphaMaterials.BlockofIron),
	  ("Chance 7", 0),
	  ("Material 8", alphaMaterials.BlockofIron),
	  ("Chance 8", 0),
	),
	(
	  ("9-10", "title"),
	  ("Material 9", alphaMaterials.BlockofIron),
	  ("Chance 9", 0),
	  ("Material 10", alphaMaterials.BlockofIron),
	  ("Chance 10", 0)
    ),
]
	  

#	  ("abrightmoore@yahoo.com.au", "label"),
#	  ("http://brightmoore.net", "label"),

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

def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), ((int)(x),(int)(y),(int)(z)), ((int)(x1),(int)(y1),(int)(z1)), 0 )

def drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z
	# print 'dlc - (%s %s %s) (%s %s %s)' % (x,y,z, x1,y1,z1)
	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			scratchpad.setBlockAt(x+(int)(iter*cos(theta)*cos(phi)), y+(int)(iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt(x+(int)(iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.

def	copyBlocksFromDBG(level,schematic, A, cursorPosn):
	(x1,y1,z1,x2,y2,z2) = (A.minx,A.miny,A.minz,A.maxx,A.maxy,A.maxz)
	(width, height, depth) = getBoxSize(schematic.bounds)

	if x2 > width or y2 > height or z2 > depth:
		return False
	else:
		level.copyBlocksFrom(schematic, A, cursorPosn)
	return True
			
def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	#print 'ANALYSE %s %s %s' % (width, height, depth)

	minX = width
	minY = height
	minZ = depth
	maxX = 0
	maxY = 0
	maxZ = 0
	found = False
	
	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depth):
				if level.blockAt(iterX, iterY, iterZ) != 0:
					#print 'ANALYSING %s %s %s' % (iterX, iterY, iterZ)
					if iterX > maxX:
						maxX = iterX
					if iterY > maxY:
						maxY = iterY
					if iterZ > maxZ:
						maxZ = iterZ
				
					if iterX < minX:
						minX = iterX
					if iterY < minY:
						minY = iterY
					if iterZ < minZ:
						minZ = iterZ
						
					found = True

	#print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	#print '%s: Ended at %s' % (method, time.ctime())
	
	if found == False:
		return BoundingBox((0, 0, 0), (width, height, depth))	
	else:
		return BoundingBox((minX, 0, minZ), (maxX+1, maxY+1, maxZ+1))
	

def findSurface(x, y, z, level, box, options):
	# Find a candidate surface
	iterY = 250
	miny = y
	foundy = y
	while iterY > miny:
		block = level.blockAt(x,iterY,z)
		if block != 0: # not AIR
			foundy = iterY
			iterY = miny # end search, block found was a legitimate candidate for the surface				
		iterY = iterY -1
	return foundy

def printBoundingBox(A):
	print 'BoundingBox %s %s %s %s %s %s' % (A.minx,A.miny,A.minz,A.maxx,A.maxy,A.maxz)


def checkBoundingBoxIntersect(A, B):
	#print 'Checking BB A/B intersection '
	#printBoundingBox(A)
	#printBoundingBox(B)
	# Check for A completely to the left of B. https://github.com/mcedit/pymclevel/blob/master/box.py
	# http://www.toymaker.info/Games/html/3d_collisions.html
	if A.maxx < B.minx:
	    return False
	# Check for A to the right of B
	if A.minx > B.maxx:
	    return False
	# Check for A in front of B
	if A.maxz < B.minz:
	    return False
	# Check for A behind B
	if A.minz > B.maxz:
	    return False
	# Check for A above B
	if A.miny > B.maxy:
	    return False
	# Check for A below B
	if A.maxy < B.miny:
	   return False
	   
	# Collision has occurred
	#print 'Collision occurred'
	return True

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Alchemy(level, box, options)		
	level.markDirtyBox(box)
	
def Alchemy(level, box, options):
	# CONSTANTS
	method = "ALCHEMY"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIR = (0,0)
	
	material = (options["Material to Replace"].ID, options["Material to Replace"].blockData)

	replaceChance = options["Replace Chance"]
	Material = []
	Chance = []
	
	Material.append((options["Material 1"].ID, options["Material 1"].blockData))
	Chance.append(options["Chance 1"])
	Material.append((options["Material 2"].ID, options["Material 2"].blockData))
	Chance.append(options["Chance 2"])
	Material.append((options["Material 3"].ID, options["Material 3"].blockData))
	Chance.append(options["Chance 3"])
	Material.append((options["Material 4"].ID, options["Material 4"].blockData))
	Chance.append(options["Chance 4"])
	Material.append((options["Material 5"].ID, options["Material 5"].blockData))
	Chance.append(options["Chance 5"])
	Material.append((options["Material 6"].ID, options["Material 6"].blockData))
	Chance.append(options["Chance 6"])
	Material.append((options["Material 7"].ID, options["Material 7"].blockData))
	Chance.append(options["Chance 7"])
	Material.append((options["Material 8"].ID, options["Material 8"].blockData))
	Chance.append(options["Chance 8"])
	Material.append((options["Material 9"].ID, options["Material 9"].blockData))
	Chance.append(options["Chance 9"])
	Material.append((options["Material 10"].ID, options["Material 10"].blockData))
	Chance.append(options["Chance 10"])
	
	ChanceTotal = 0
	for value in Chance:
		ChanceTotal = ChanceTotal + value
	
	for iterY in xrange(box.miny, box.maxy): # scan for all blocks that are force-carrying
		print '%s: Layer %s of %s' % (method, iterY-box.miny, height-2)
		for iterX in xrange(box.minx, box.maxx):
			for iterZ in xrange(box.minz, box.maxz):
				if (level.blockAt(iterX, iterY, iterZ),level.blockDataAt(iterX, iterY, iterZ)) == material: # Found a block to consider swapping out
					if randint(0,100) <= replaceChance: # We should replace this block
						# But with which one?!?!
						aRandomNumber = randint(0,ChanceTotal)
						# Select the right one
						index = 0
						runningTotal = 0
						for c in Chance:
							runningTotal = runningTotal + c
							if aRandomNumber < runningTotal: # the random number is within the bounds defined for this block type.
								setBlock(level, Material[index], iterX, iterY, iterZ)
								break
							index = index + 1
	print '%s: Ended at %s' % (method, time.ctime())

	
	
# This filter provides a way to find a block and replace that block with a schematic.
# Requested by james22402 on the forums: http://www.minecraftforum.net/topic/213853-mcedit-filter-scripts/page__st__300#entry22658577
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


# MCSchematic access method @TexelElf
# Texelelf's guidance:
#	from pymclevel import MCSchematic, mclevel
#	deformation = pymclevel.MCSchematic((width, height, length), mats=self.editor.level.materials)
#	deformation.setBlockAt(x,y,z,blockID)
#	deformation.setBlockDataAt(x,y,z,blockData)
#	deformation.Blocks[::4] = 57
#	schematic_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir? or mcplatform.schematicsDir, "Save Schematic As...", "", "Schematic\0*.schematic\0\0", ".schematic")
#	deformation.saveToFile(schematic_file)
# And from Codewarrior0's filterdemo.py:
#	level.copyBlocksFrom(temp, temp.bounds, box.origin)

# Global constants

inputs = (
	  ("BlockSchematicSwapper", "label"),
          ("Choose the block to locate:", "blocktype"),
          ("What should I look for?", ("Match Block Type Only", "Match Block Data") ),
		  ("What is the schematic to use?", ("string","value=BlockSchematicSwapper_CowSpawner.schematic")),
		  ("Random Schematics?", False),
		  ("Schematic Set:", ("string","value=")),
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

	
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

	
def drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			scratchpad.setBlockAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockID)
			scratchpad.setBlockDataAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.

def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	print 'ANALYSE %s %s %s' % (width, height, depth)

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
					print 'ANALYSING %s %s %s' % (iterX, iterY, iterZ)
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

	print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	print '%s: Ended at %s' % (method, time.ctime())
	
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
			#if (block not in ignoreList):
			foundy = iterY
			iterY = miny # end search, block found was a legitimate candidate for the surface				
		iterY = iterY -1
	return foundy


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	blockSchematicSwapper(level, box, options)		
	level.markDirtyBox(box)

def blockSchematicSwapper(level, box, options):
	# CONSTANTS
	method = "blockSchematicSwapper"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	SHAPE = (200,200,200)
	# END CONSTANTS

	baseBlock = options["Choose the block to locate:"].ID
	baseBlockData = options["Choose the block to locate:"].blockData
	theFileName = "filters/"+options["What is the schematic to use?"]
	randomSchemas = options["Random Schematics?"]
	DIRPATH = options["Schematic Set:"]
	StartSchematicFiles = []
	if randomSchemas == True:
		# Prefill a list of schematic file names which we will choose from later on
		StartSchematicFiles = glob.glob("filters/"+DIRPATH+"/*.schematic")
		for fileName in StartSchematicFiles:
			print fileName
		print 'Found %s start schematic files' % (len(StartSchematicFiles))
	else:
		# import the corresponding MCSchematic to the supplied filename
		print 'Loading schematic from file - %s' % (theFileName)
		print os.getcwd()
		charSchematic = MCSchematic(shape=SHAPE,filename=theFileName)
	
	modeMatchBlockData = False
	if options["What should I look for?"] == "Match Block Data":
		modeMatchBlockData = True

	# First pass - search down-up for the block of interest. On the first hit at x/z, import schematic and move on with the search
	
	# END CONSTANTS



	found = 0
	
	counter = 0
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.miny, box.maxy):
				counter = counter +1
				if counter%10000 == 0:
					print '%s %s: Searching at x=%s y=%s z=%s' % (method, time.ctime(), x, y, z)
		
				if modeMatchBlockData == True:
					if level.blockAt(x,y,z) == baseBlock and level.blockDataAt(x,y,z) == baseBlockData:
						print 'I found your block %s at %s %s %s with data value %s' % (baseBlock, x, y, z, baseBlockData)
						# level.copyBlocksFrom(charSchematic, BoundingBox((0,0,0),(1,1,1)), (x, y, z))
						if randomSchemas == False:
							placeASchematic(x,y,z, theFileName, level, box, options)
						else:
							chosenSchematic = randint(0,len(StartSchematicFiles)) % len(StartSchematicFiles)
							placeASchematic(x,y,z, StartSchematicFiles[chosenSchematic], level, box, options)
						found = found +1
					
				else:
					if level.blockAt(x,y,z) == baseBlock:
						print 'I found your block %s at %s %s %s' % (baseBlock, x, y, z)
						# level.copyBlocksFrom(charSchematic, BoundingBox((0,0,0),(2,2,2)), (x, y, z))
						if randomSchemas == False:
							placeASchematic(x,y,z, theFileName, level, box, options)
						else:
							chosenSchematic = randint(0,len(StartSchematicFiles)) % len(StartSchematicFiles)
							placeASchematic(x,y,z, StartSchematicFiles[chosenSchematic], level, box, options)
						found = found +1

	print '%s: %s. Found %s' % (method, time.ctime(), found)
	print '%s: Ended at %s' % (method, time.ctime())
	
def placeASchematic(x,y,z, theFileName, level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "placeASchematic"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	SHAPE = (32,32,32)
	# END CONSTANTS

	# cursorPosn = box.origin
	# import the corresponding MCSchematic to the supplied filename
	print 'Loading schematic from file - %s' % (theFileName)
	charSchematic = MCSchematic(shape=SHAPE,filename=theFileName)

	cursorPosn = (x, y, z)		
	bb = analyse(charSchematic)
	level.copyBlocksFrom(charSchematic, bb, cursorPosn)

	print '%s: Ended at %s' % (method, time.ctime())
	

# @TheWorldFoundry
# This version centres the schematic on the block position and also doesn't force files into the filters directory



import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import *
from os import listdir
from os.path import isfile, join
import glob

inputs = (
	  ("BlockSchematicSwapper", "label"),
          ("Choose the block to locate:", "blocktype"),
          ("What should I look for?", ("Match Block Type Only", "Match Block Data") ),
		  ("What is the schematic to use?", ("string","value=BlockSchematicSwapper_CowSpawner.schematic")),
		  ("Random Schematics?", False),
		  ("Schematic Set:", ("string","value=")),
		  ("Remove air?", False),
 	  ("adrian@TheWorldFoundry.com", "label"),
	  ("http://TheWorldFoundry.com", "label"),
)


def perform(level, box, options):
	blockSchematicSwapper(level, box, options)		
	level.markDirtyBox(box)
	
	
def blockSchematicSwapper(level, box, options):
	# CONSTANTS
	method = "blockSchematicSwapper"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width >>1 
	centreHeight = height >>1
	centreDepth = depth >>1
	AIR = (0,0)
	SHAPE = (200,200,200)
	# END CONSTANTS

	baseBlock = options["Choose the block to locate:"].ID
	baseBlockData = options["Choose the block to locate:"].blockData
	theFileName = options["What is the schematic to use?"]
	randomSchemas = options["Random Schematics?"]
	DIRPATH = options["Schematic Set:"]
	StartSchematicFiles = []
	if randomSchemas == True:
		# Prefill a list of schematic file names which we will choose from later on
		StartSchematicFiles = glob.glob(DIRPATH+"/*.schematic")
		for fileName in StartSchematicFiles:
			print fileName
		print 'Found %s start schematic files' % (len(StartSchematicFiles))
	else:
		# import the corresponding MCSchematic to the supplied filename
		print 'Loading schematic from file - %s' % (theFileName)
		print os.getcwd()
		charSchematic = MCSchematic(filename=theFileName)
	
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
	centreWidth = width >>1
	centreHeight = height >>1
	centreDepth = depth >>1
	removeAir = options["Remove air?"]
	
	# END CONSTANTS

	# cursorPosn = box.origin
	# import the corresponding MCSchematic to the supplied filename
	print 'Loading schematic from file - %s' % (theFileName)
	charSchematic = MCSchematic(filename=theFileName)
	schemWidthOffset = charSchematic.Width>>1
	schemDepthOffset = charSchematic.Length>>1
	cursorPosn = (x-schemWidthOffset, y, z-schemDepthOffset)
	blocksIDs = range(level.materials.id_limit)
	if removeAir:
		blocksIDs.remove(0) 		
	level.copyBlocksFrom(charSchematic, BoundingBox((0,0,0),(charSchematic.Width,charSchematic.Height,charSchematic.Length)), cursorPosn, blocksToCopy=blocksIDs)

	print '%s: Ended at %s' % (method, time.ctime())
	
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
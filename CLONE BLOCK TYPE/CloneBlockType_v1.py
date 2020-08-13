# This filter is to move all blocks of only a certain type by an offset
# Requested by @Dragnoz (Twitter) / https://www.youtube.com/user/Dragnoz (YouTube)
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, cosh
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from copy import deepcopy
import bresenham # @Codewarrior0

# YOUR CODE GOES HERE \/ \/ \/ \/ \/ \/ \/ \/ \/
inputs = (
		("CLONE BLOCK TYPE", "label"),
		("Material 1:", alphaMaterials.Rail),
		("Material 2:", alphaMaterials.PoweredRail),
		("Material 3:", alphaMaterials.DetectorRail),
		("Material 4:", alphaMaterials.ActivatorRail),
		("Offset X:", 0),
		("Offset Y:", -10),
		("Offset Z:", 0),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def cloneByBlockType(originalLevel,originalBox,level,box,options):
	method = "cloneByBlockType"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	(M1_ID,M1_DATA) = getBlockFromOptions(options, "Material 1:")
	(M2_ID,M2_DATA) = getBlockFromOptions(options, "Material 2:")
	(M3_ID,M3_DATA) = getBlockFromOptions(options, "Material 3:")
	(M4_ID,M4_DATA) = getBlockFromOptions(options, "Material 4:")

	ox = options["Offset X:"]
	oy = options["Offset Y:"]
	oz = options["Offset Z:"]

	# scan the selection box, locate blocks of the desired type, and copy them to the specified offset from their current location
	for iterY in xrange(0,height):
		print iterY
		for iterZ in xrange(0,depth):
			for iterX in xrange(0,width):
				(blockHereID,blockHereData) = getBlock(originalLevel, originalBox.minx+iterX, originalBox.miny+iterY, originalBox.minz+iterZ)
				if blockHereID == M1_ID or blockHereID == M2_ID or blockHereID == M3_ID or blockHereID == M4_ID: # Match type, ignore data
					setBlock(level, (blockHereID,blockHereData), iterX+ox, iterY+oy, iterZ+oz) # Clone the block
	FuncEnd(level,box,options,method) # Log end
					
def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	# Operations go here - switch to the function based on selected operation
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	cloneByBlockType(originalLevel,originalBox,level,box,options)
	
	SUCCESS = True
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end
	
############# METHOD HELPERS #############
	
def FuncStart(level, box, options, method):
	# abrightmoore -> shim to prepare a function.
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	
	# other initialisation methods go here
	return (method, (width, height, depth), (centreWidth, centreHeight, centreDepth))

def FuncEnd(level, box, options, method):
	print '%s: Ended at %s' % (method, time.ctime())

############# WORLD ACCESS HELPERS #############

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

############# GFX PRIMITIVES #############

def setBlockIfEmpty(level, (block, data), x, y, z):
	tempBlock = level.blockAt(x,y,z)
	if tempBlock == 0:
		setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

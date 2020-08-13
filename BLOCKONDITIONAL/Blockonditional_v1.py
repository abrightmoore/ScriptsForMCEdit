# This filter is for conditionally replacing blocks in a selection area per @cocoamix86.
# 21/9/2015 - init
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
from random import Random # @Codewarrior0

inputs = (
		("BLOCKONDITIONAL", "label"),
		("Find block:", alphaMaterials.Grass),
		("Place block:", alphaMaterials.Stone),
		("Place block offset X:", 0),
		("Place block offset Y:", -1),
		("Place block offset Z:", 0),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
		)

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM BLOCKONDITIONAL"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	SUCCESS = blockonditional(level, box, options)
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,originalBox,options,method) # Log end
	
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

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
def blockonditional(level,box,options):
	# Local variables
	method = "BLOCKONDITIONAL"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	SUCCESS = False	

	FINDBLOCK = getBlockFromOptions(options,"Find block:")
	PLACEBLOCK = getBlockFromOptions(options,"Place block:")
	PBOX = options["Place block offset X:"]
	PBOY = options["Place block offset Y:"]
	PBOZ = options["Place block offset Z:"]
	
	for y in xrange(0,height):
		print y
		for x in xrange(0,width):
			for z in xrange(0,depth):
				curBlock = getBlock(level, x, y, z)
				if curBlock == FINDBLOCK:
					setBlock(level, PLACEBLOCK, x+PBOX, y+PBOY, z+PBOZ)
					#print curBlock, FINDBLOCK
					SUCCESS = True
	
	FuncEnd(level,box,options,method) # Log end
	return SUCCESS
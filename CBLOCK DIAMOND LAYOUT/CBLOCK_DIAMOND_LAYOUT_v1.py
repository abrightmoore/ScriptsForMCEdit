# This filter is to layout Command Blocks in a 'star' pattern, suitable for v1.7 triggering
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors:
#    @Texelelf
#    @Sethbling
#    @CodeWarrior0
#    @Podshot_

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

inputs = (
		("CBLOCK DIAMOND LAYOUT", "label"),
		("Execution mode:", ("Scan Command Blocks","Re-layout Command Blocks")),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
		("Requested by SPIDER", "label"),
)

def getCommandBlocks(level, box, options):
	command = []

	for (chunk, slices, point) in level.getChunkSlices(box):
		
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if t["id"].value == "Control":
					command.append(t["Command"].value)
					
					print("Command At: " +str(x)+"(x)"+" "+str(y)+"(y)"+" "+str(z)+ "(z)" + " " +"is: " + t["Command"].value + "													")

	return command

def CBlockDiamondLayout(level, box, options, commands):
	method = "CBLOCK_DIAMOND_LAYOUT"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	# Redraw the supplied commands as a diamond within the selection box. Quick and dirty is OK - doesn't need to worry about selection box size / etc
	# The diamond is 29 blocks across each major axis.
	
	startX = 0
	startY = 0
	startZ = centreDepth
	pathLength = 1
	rowLength = 1
	rowPos = 1
	rowNumber = 1
	for command in commands:
		y = startY+int(floor(pathLength / 422)) # blocks in a Layer count
		x = startX + rowNumber
		z = startZ - int(floor(rowLength/2)) + rowPos
		createCmdBlock(level, box.minx+x, box.miny+y, box.minz+z, command)
		# Work out where to put the next block
		pathLength += 1
		rowPos += 1
		if rowNumber < 15:
			if rowPos > rowLength:
				rowLength += 2
				rowPos = 1
				rowNumber += 1
		elif rowNumber < 29:
			if rowPos > rowLength:
				rowLength -= 2
				rowPos = 1
				rowNumber += 1
		elif rowNumber == 29:
			if rowPos > rowLength:
				rowLength = 1
				rowPos = 1
				rowNumber = 1
		else: # Finished this layer, move up!
			rowPos = 1
			rowNumber = 1
	
	FuncEnd(level,box,options,method) # Log end
	return True

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM CBLOCK_DIAMOND_LAYOUT"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	global commands
	if options["Execution mode:"] == "Scan Command Blocks":
		commands = getCommandBlocks(level,box,options)
		SUCCESS = False
	elif options["Execution mode:"] == "Re-layout Command Blocks":
		SUCCESS = CBlockDiamondLayout(level, box, options, commands)
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end
	
############# METHOD HELPERS #############

def createCmdBlock(level, x, y, z, command): #abrightmoore - convenience method.
	COMMANDBLOCK = 137
	CHUNKSIZE = 16

	level.setBlockAt(x, y, z, COMMANDBLOCK)
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command)
	control["SuccessCount"] = TAG_Int(0)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	chunka.TileEntities.append(control)
	chunka.dirty = True
	
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

def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
	
############# GFX PRIMITIVES #############

def setBlockIfEmpty(level, (block, data), x, y, z):
	tempBlock = level.blockAt(x,y,z)
	if tempBlock == 0:
		setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

############# GFX  #############			
			
def distance( (x1,y1,z1), (x2,y2,z2) ):
	p = x1 * x2 + z1 * z2
	return sqrt( p + y1 * y2 )


# This filter is to create Tartan-style patterns/designs.
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

inputs = (
		("TARTAN", "label"),
		("Block type:", alphaMaterials.WhiteWool),
		("15 Black:", False),
		("7  Dark Grey:", False),
		("8  Light Grey:", False),
		("0  White:", True),
		("6  Pink:", False),
		("14 Red:", True),
		("12 Brown:", False),
		("1  Orange:", True),
		("4  Yellow:", True),
		("5  Lime Green:", False),
		("13 Dark Green:", True),
		("9  Cyan:", False),
		("3  Light Blue:", False),
		("11 Dark Blue:", False),
		("2  Magenta:", False),
		("10 Purple:", False),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def Tartan(level, box, options):
	method = "TARTAN"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	# This is the base block type, with data values variants to be determined from the clickable checkboxes.
	(matID,matData) = getBlockFromOptions(options,"Block type:")
	
	# Data values for the block in a friendly clickable list
	o = [ options["0  White:"],
			options["1  Orange:"],
			options["2  Magenta:"],
			options["3  Light Blue:"],
			options["4  Yellow:"],
			options["5  Lime Green:"],
			options["6  Pink:"],
			options["7  Dark Grey:"],
			options["8  Light Grey:"],
			options["9  Cyan:"],
			options["10 Purple:"],
			options["11 Dark Blue:"],
			options["12 Brown:"],
			options["13 Dark Green:"],
			options["14 Red:"],
			options["15 Black:"]
		]
	#print o
	c = []
	for i in xrange(0,16): # initialise
		#print i
		if o[i] == True:
			c.append(i)
	if len(c) == 0:
		c.append(matData)	
	
	# TODO: Randomise the order of the list
	
	# 1. for each block variant, work out a sinusoidal period
	# 2. build at each row and column an ordered list of block types
	# 3. draw each 
	period = []
	for b in c:
		period.append(randint(1,len(c)*4))
	
	matrix = zeros((width,depth))
	
	twoPi = 2*pi
	for x in xrange(0,width):
		maxXValue = 0
		maxZValue = 0
		maxXBlock = c[0]
		maxZBlock = c[0]
		theBlock = c[0]
		for i in xrange(0,len(c)):
			valueX = sin(x/centreWidth*period[i]*twoPi)
			if valueX > maxXValue:
				maxXValue = valueX
				maxXBlock = i
		theBlock = maxXBlock
				
		for z in xrange(0,depth):
			matrix[x][z] = theBlock
			setBlock(level, (matID, c[theBlock%(len(c)-1)]), x, theBlock, z)
			setBlock(level, (matID, c[theBlock%(len(c)-1)]), z, theBlock, x)
	
	FuncEnd(level,box,options,method) # Log end
	return True
	
def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM CRYSTALS"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	SUCCESS = Tartan(level, box, options)
		
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

def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLine1(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ): # @ CodeWarrior
	for px, py, pz in bresenham.bresenham((x,y,z),(x1,y1,z1)): # @ CodeWarrior
		setBlock(scratchpad,(blockID, blockData),px,py,pz) # @ CodeWarrior 
	setBlock(scratchpad,(blockID, blockData),x1,y1,z1) # @ CodeWarrior
	
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
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.

############# GFX  #############			
			
def distance( (x1,y1,z1), (x2,y2,z2) ):
	p = x1 * x2 + z1 * z2
	return sqrt( p + y1 * y2 )

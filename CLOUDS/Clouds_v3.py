# This filter is for playing with Clouds for SQORED
# 30/8/2015 - init
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
		("CLOUDS", "label"),
		("Seed:", 42),
		("Threshold:", 0.1),
		("Material:", alphaMaterials.Glass),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
		("Requested by @Sqored", "label"),
		)
		
def getSeed(level, options):
	if options["Seed:"] != 0:
		return seed
	else:
		return level.RandomSeed

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

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
	
def Clouds(level, box, options):
	method = "CLOUDS"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	twopi = pi*2
	CHUNKSIZE = 8
#	if height > CHUNKSIZE:
#		CHUNKSIZE = height
	BIGCHUNKSIZE = CHUNKSIZE*CHUNKSIZE
	MATERIAL = getBlockFromOptions(options,"Material:")
	THRESHOLD = options["Threshold:"]
	# Create random pattern
	# Render it into the world at box height-1 using the nominated material, but only replace air
	
	r = Random(getSeed(level,options)) # reproducible based on the seed provided.

	b_quant = r.randint(CHUNKSIZE,2*BIGCHUNKSIZE) # Complexity of the scenery
	b_origins = []
	b_amplitudes = []
	sum_amplitudes = 0
	b_freq = []
	for i in xrange(0,b_quant): # setup
		b_origins.append( (r.randint(0,width-1),r.randint(0,height-1)))
		amp = r.randint(int(height/16)+2,height+3)
		b_amplitudes.append( amp )
		sum_amplitudes += amp
		b_freq.append( r.randint(CHUNKSIZE,BIGCHUNKSIZE))

	y = box.maxy-1
	for x in xrange(box.minx,box.maxx):
		for z in xrange(box.minz,box.maxz):
			amp = 0
			drx = x - (box.minx+centreWidth)
			drz = z - (box.minz+centreDepth)
			ddist = float(sqrt(drx*drx+drz*drz))
			
			for i in xrange(0,b_quant):
				(rx, rz) = b_origins[i]
				dx = x - rx # to each of the origins
				dz = z - rz
				dist = float(sqrt(dx*dx + dz*dz))
				amp += b_amplitudes[i] * cos( twopi*(float(dist%b_freq[i]))/b_freq[i] )
			amp = float(amp/sum_amplitudes) # Normalise to account for the world height.
			if ddist/((width+depth)/2) > 1:
				amp = -1000000
			else:
				amp  = amp*cos(pi/2*ddist/((width+depth)/2)) 
			print amp
			if amp > THRESHOLD:
				setBlock(level,MATERIAL,x,y,z)

	return True

def setBlockIfEmpty(level, (block, data), x, y, z):
	tempBlock = level.blockAt(x,y,z)
	if tempBlock == 0:
		setBlock(level, (block, data), x, y, z)
	
def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM AdroitBiomes"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	SUCCESS = Clouds(level, box, options)
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,originalBox,options,method) # Log end
	
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

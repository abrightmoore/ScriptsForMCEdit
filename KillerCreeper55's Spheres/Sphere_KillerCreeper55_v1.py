# This filter creates Command Blocks that create Minecart spawners with projected blocks - ala KillerCreeper55
# http://www.youtube.com/watch?v=706Wg2uHAes
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)
# Example:
# /summon MinecartRideable ~ ~1 ~ {CustomDisplayTile:1,DisplayTile:159,DisplayData:4,DisplayOffset:84,Rotation:[90f,20f]}

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf


# These imports by @SethBling (http://youtube.com/SethBling)
from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Float
from pymclevel import TAG_Double
from pymclevel import TAG_String

inputs = (
	  ("Parameterised Spheres", "label"),
	  ("Radius", 84),
	  ("Material", alphaMaterials.WhiteWool),
	  ("Horizontal step degrees", 5),
	  ("Vertical step degrees", 5),
	  ("Offset", 1),
	  ("Generator Width", 16),
	  ("Layer Separation", 2),
	  ("Command Blocks X", 0),
	  ("Command Blocks Y", 0),
	  ("Command Blocks Z", 0),
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
	
def createCommandBlockData(x, y, z, theCommand):
	e = TileEntity.Create("Control")
	e["Command"] = TAG_String(theCommand)
	TileEntity.setpos(e, (x, y, z))
	return e


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	ParamSpheres(level, box, options)		
	level.markDirtyBox(box)
	
def ParamSpheres(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "PARAMETERISED SPHERES"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	O_RADIUS = options["Radius"]
	OFFSET = options["Offset"]
	O_STEP_H = options["Horizontal step degrees"]
	O_STEP_V = options["Vertical step degrees"]
	baseX = options["Command Blocks X"]
	baseY = options["Command Blocks Y"]
	baseZ = options["Command Blocks Z"]
	O_MATERIAL_ID = options["Material"].ID
	O_MATERIAL_DATA = options["Material"].blockData
	
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16
	PACKEDCHUNKSIZE = options["Generator Width"]
	if PACKEDCHUNKSIZE == 0:
		PACKEDCHUNKSIZE = CHUNKSIZE
	LAYERGAP = options["Layer Separation"]+1
	# END CONSTANTS
	packedSpawnerCount = 0
	
	
	if baseX == 0 and baseY == 0 and baseZ == 0:
		baseX = box.maxx-(box.minx % CHUNKSIZE)
		baseZ = box.maxz-(box.maxz % CHUNKSIZE)
		baseY = box.maxy+1*CHUNKSIZE

	iterH = 0
	while iterH <= 360:
		print '%s: Processing %s of 360' % (method, iterH)
		iterV = 0
		while iterV <= 180:
			spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
			spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
			spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
			chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)

			theCommand = "/summon MinecartRideable "+str(box.minx)+" "+str(box.miny)+" "+str(box.minz)+" {CustomDisplayTile:1,DisplayTile:"+str(O_MATERIAL_ID)+",DisplayData:"+str(O_MATERIAL_DATA)+",DisplayOffset:"+str(O_RADIUS)+",Rotation:["+str(iterH)+"f,"+str(iterV)+"f]}"
			
			setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
			chunk.TileEntities.append( 	createCommandBlockData(spawnerX, 
										spawnerY, 
										spawnerZ, 
										theCommand
										))

			packedSpawnerCount = packedSpawnerCount+1
			chunk.dirty = True
			iterV = iterV + O_STEP_V
		iterH = iterH + O_STEP_H
		
	print '%s: Ended at %s' % (method, time.ctime())
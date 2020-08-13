# This filter creates a Command Blocks that create blocks in the selection area
# Suggested by WHAKru on YouTube
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

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
	  ("BLOCKCOMMAND", "label"),
	  ("Offset", 1),
	  ("Relative coordinates?", False),
	  ("Specify Generator Properties?", False),
	  ("Generator X", 0),
	  ("Generator Y", 0),
	  ("Generator Z", 0),
	  ("Generator Width", 16),
	  ("Layer Separation", 0),
	  ("All Air?", False),
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
	BlockCommand(level, box, options)		
	level.markDirtyBox(box)
	
def BlockCommand(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	TICKSPERSEC = 20
	method = "BLOCKCOMMAND"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	OFFSET = options["Offset"]+1
	COORDS = options["Relative coordinates?"]
	ALLAIR = options["All Air?"]
	GENPROPS = options["Specify Generator Properties?"]
	baseX = options["Generator X"]
	baseY = options["Generator Y"]
	baseZ = options["Generator Z"]
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
		baseX = box.minx-(box.minx % CHUNKSIZE)
		baseZ = box.minz-(box.maxz % CHUNKSIZE) #-5*CHUNKSIZE
		baseY = box.maxy+1*CHUNKSIZE

	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depth):
				tempBlock = (	level.blockAt( box.minx + iterX, box.miny+iterY, box.minz+iterZ), 
						level.blockDataAt( box.minx + iterX, box.miny+iterY, box.minz+iterZ) )
				if ALLAIR == True:
					tempBlock = AIR
				(ID, Data) = tempBlock
				if tempBlock != AIR or ALLAIR == True:
					spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
					spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
					spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
					setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
					chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
					
					
					cX = box.minx+iterX
					cY = box.miny+iterY
					cZ = box.minz+iterZ
					
					if COORDS == True:
						cX = cX - spawnerX
						cY = cY - spawnerY
						cZ = cZ - spawnerZ 
						theCommand = "/setblock ~"+str(cX)+" ~"+str(cY)+" ~"+str(cZ)+" "+str(ID)+" "+str(Data)+" replace"
					else:
						theCommand = "/setblock "+str(cX)+" "+str(cY)+" "+str(cZ)+" "+str(ID)+" "+str(Data)+" replace"
					
					chunk.TileEntities.append( 	createCommandBlockData(spawnerX, 
									spawnerY, 
									spawnerZ, 
									theCommand
									))
					packedSpawnerCount = packedSpawnerCount+1
					chunk.dirty = True
				

	print '%s: Ended at %s' % (method, time.ctime())
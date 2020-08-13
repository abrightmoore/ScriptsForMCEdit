# This filter creates a spawner animation
# Spawner function by @SethBling (http://youtube.com/SethBling), Animation method by /u/Sralam (http://www.youtube.com/user/SralamVids)
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)
# v10 - configurable TICKS

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials

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
	  ("Framination", "label"),
	  ("Frame Width (Blocks):", 3),
	  ("Seconds between animations:", 0),
	  ("Seconds Delay before animation:", 0),
	  ("Animation X position (0 for default):", 0),
	  ("Animation Y position (0 for default):", 0),
	  ("Animation Z position (0 for default):", 0),
	  ("Animation X end position:", 0),
	  ("Animation Y end position:", 0),
	  ("Animation Z end position:", 0),
	  ("Ticks:", 2),
	  ("Life:", 0),
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

# createSandSpawner() function by @SethBling (http://youtube.com/SethBling)
# hacks by @abrightmoore
def createSandSpawner(x, y, z, (block, data), frameNum, numFrames, tx, ty, tz, interval, delay, TICKS, life):
	
	spawner = TAG_Compound()
	spawner["id"] = TAG_String("MobSpawner")
	spawner["Items"] = TAG_List()
	spawner["x"] = TAG_Int(x)
	spawner["y"] = TAG_Int(y)
	spawner["z"] = TAG_Int(z)
	spawner["Delay"] = TAG_Short(TICKS*frameNum+delay)
	spawner["MinSpawnDelay"] = TAG_Short(interval+TICKS*numFrames)
	spawner["MaxSpawnDelay"] = TAG_Short(interval+TICKS*numFrames+1)
	spawner["SpawnCount"] = TAG_Short(1)
	spawner["SpawnData"] = createSandEntity(tx, ty, tz, block, data, life)
	spawner["MaxNearbyEntities"] = TAG_Short(10000)
	spawner["RequiredPlayerRange"] = TAG_Short(128)
	spawner["EntityId"] = TAG_String("FallingSand")					
	return spawner


# createSandEntity() function by @SethBling (http://youtube.com/SethBling)	
# hacks by @abrightmoore
def createSandEntity(x, y, z, block, data, life):
	sand = TAG_Compound()
	sand["Motion"] = TAG_List()
	sand["Motion"].append(TAG_Double(0))
	sand["Motion"].append(TAG_Double(0))
	sand["Motion"].append(TAG_Double(0))
	sand["OnGround"] = TAG_Byte(1)
	sand["DropItem"] = TAG_Byte(0)
	sand["Dimension"] = TAG_Int(0)
	sand["Air"] = TAG_Short(300)
	sand["Pos"] = TAG_List()
	sand["Pos"].append(TAG_Double(x+0.5))
	sand["Pos"].append(TAG_Double(y+0.5))
	sand["Pos"].append(TAG_Double(z+0.5))
	sand["Data"] = TAG_Byte(data)
	sand["TileID"] = TAG_Int(block)
	sand["Tile"] = TAG_Byte(block)
	sand["Time"] = TAG_Byte(life)
	sand["Fire"] = TAG_Short(-1)
	sand["FallDistance"] = TAG_Float(0)
	sand["Rotation"] = TAG_List()
	sand["Rotation"].append(TAG_Float(0))
	sand["Rotation"].append(TAG_Float(0))
	return sand

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Framination(level, box, options)		
	level.markDirtyBox(box)
	
def Framination(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	TICKSPERSEC = 20
	method = "Framination"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	frameWidth = options["Frame Width (Blocks):"]
	interval = options["Seconds between animations:"] * TICKSPERSEC
	delay = options["Seconds Delay before animation:"] * TICKSPERSEC
	targetX = options["Animation X position (0 for default):"]
	targetY = options["Animation Y position (0 for default):"]
	targetZ = options["Animation Z position (0 for default):"]
	endX = options["Animation X end position:"]
	endY = options["Animation Y end position:"]
	endZ = options["Animation Z end position:"]
	TICKS = options["Ticks:"]
	life = options["Life:"]

	deltaX = 0.0
	deltaY = 0.0
	deltaZ = 0.0

	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	BLOCKSPAWNER = (52,0)
	CHUNKSIZE = 16

	# END CONSTANTS

	numFrames = (int)(width / frameWidth)

	packedSpawnerCount = 0
	baseX = box.minx-(box.minx % CHUNKSIZE)
	baseZ = box.maxz-(box.maxz % CHUNKSIZE)+CHUNKSIZE # one chunk deeper
	baseY = box.miny

	if targetX == 0 and targetY == 0 and targetZ == 0:
		targetX = baseX
		targetY = baseY
		targetZ = baseZ + CHUNKSIZE # Default is to offset the animation one chunk from the spawners
		deltaX = 0.0
		deltaY = 0.0
		deltaZ = 0.0
	else: # slope is rise over run. Steps is slope / number of frames!
		deltaX = (float)((float)(endX)-(float)(targetX))/numFrames
		deltaY = (float)((float)(endY)-(float)(targetY))/numFrames
		deltaZ = (float)((float)(endZ)-(float)(targetZ))/numFrames

	for iterFrames in xrange(0, numFrames):
		for iterX in xrange(0, frameWidth):
			x = iterFrames*frameWidth+iterX
			for iterY in xrange(0, height):
				for iterZ in xrange(0, depth):
					tempBlock = (	level.blockAt( box.minx + x, box.miny+iterY, box.minz+iterZ), 
							level.blockDataAt( box.minx + x, box.miny+iterY, box.minz+iterZ) )
					if tempBlock != AIR:
						spawnerX = baseX + packedSpawnerCount%CHUNKSIZE
						spawnerY = baseY + (int)(packedSpawnerCount/(CHUNKSIZE*CHUNKSIZE))
						spawnerZ = baseZ + (int)(packedSpawnerCount/CHUNKSIZE)%CHUNKSIZE
						setBlock(level, BLOCKSPAWNER, spawnerX, spawnerY, spawnerZ)
						chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE) # revisit this - should now be constant
						chunk.TileEntities.append( 	createSandSpawner(spawnerX, 
										spawnerY, 
										spawnerZ, 
										tempBlock, 
										iterFrames, 
										numFrames, 
										(int)(deltaX*iterFrames+targetX+iterX), # This is where the animation goes 
										(int)(deltaY*iterFrames+targetY+iterY), 
										(int)(deltaZ*iterFrames+targetZ+iterZ),
										interval,
										delay,
										TICKS,
										life))
						packedSpawnerCount = packedSpawnerCount+1
						chunk.dirty = True
				

	print '%s: Ended at %s' % (method, time.ctime())
# This filter creates invisible skeletons wearing things on their heads. Crazy? A little...
# /summon Skeleton ~ ~2 ~ {Equipment:[{},{},{},{},{id:78}],ActiveEffects:[{Id:14,Amplifier:2,Duration:10000000}]}
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
	  ("SKELETEST", "label"),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt((int)(x),(int)(y),(int)(z))
    if tempBlock == 0:
	setBlock(level, (block, data), (int)(x),(int)(y),(int)(z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, (int)(y)):
    	setBlockIfEmpty(level, (block, data), (int)(x),(int)(iterY),(int)(z))
    	

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


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	SkeleTest(level, box, options)		
	level.markDirtyBox(box)
	
def SkeleTest(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "SKELETEST"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	MATERIAL = (35, 0)
	scratchpad = level.extractSchematic(box)
	# END CONSTANTS

	# The following structure is from @Texelelf - http://www.elemanser.com/filters.html
	for (chunk, slices, point) in level.getChunkSlices(box):
		(cx,cz) = chunk.chunkPosition
		cposx = cx * 16
		cposz = cz * 16
		y = box.miny
		for x in range((cposx if (cposx > box.minx) else box.minx),(cposx+16 if ((cposx+16) < box.maxx) else box.maxx),1):
			for z in range((cposz if (cposz > box.minz) else box.minz),(cposz+16 if((cposz+16) < box.maxz) else box.maxz),1):
				theCommand = "/summon Skeleton ~ ~2 ~ {Equipment:[{},{},{},{},{id:"+str(x)+"}],ActiveEffects:[{Id:14,Amplifier:2,Duration:10000000}]}"
					
				level.setBlockAt(x, y, z, 137)
				e = TileEntity.Create("Control")
				e["Command"] = TAG_String(theCommand)
				TileEntity.setpos(e, (x, y, z))
				chunk.TileEntities.append(e)
		chunk.dirty = True
	
	print '%s: Ended at %s' % (method, time.ctime())
	

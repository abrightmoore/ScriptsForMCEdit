# This filter creates an enumeration of all the blocks in the world with all the data values, like a Minecraft Particle Collider
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

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
	  ("SUPER BLOCK/DATA COLLIDER", "label"),
	  ("Become a mad Minecraft scientist.", "label"),
	  ("Make a selection and run the filter.", "label"),
	  ("Pore over the data, publish your results.", "label"),
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

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	ParticleCollider(level, box, options)		
	level.markDirtyBox(box)
	
def ParticleCollider(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "ParticleCollider"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	MAXDATAVAL = 16
	MAXBLOCKIDVAL = 4096
	# END CONSTANTS

	BLOCKID = 0
	DATAVALUE = 0

	for iterBLOCKID in xrange(0,MAXBLOCKIDVAL):
		for iterDATAVALUE in xrange(0,MAXDATAVAL):
			setBlock(level, (iterBLOCKID, iterDATAVALUE), box.minx+iterDATAVALUE*2, box.miny+2, box.minz+iterBLOCKID*2)

	print '%s: Ended at %s' % (method, time.ctime())
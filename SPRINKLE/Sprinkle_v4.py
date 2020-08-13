# This filter randomly distributes a number of blocks of the type you specify throughout the selection region
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("SPRINKLE", "label"),
	  ("Material:", alphaMaterials.Cobblestone),
	  ("How many blocks?", 10),
	  ("Overwrite Blocks?", False),
	  ("Only Overwrite Blocks?", False),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt(x,y,z)
    if tempBlock == 0:
		setBlock(level, (block, data), x, y, z)

def setBlockIfNotEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt(x,y,z)
    if tempBlock != 0:
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
	Sprinkle(level, box, options)		
	level.markDirtyBox(box)
	
def Sprinkle(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Sprinkle"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	PURGEAMOUNT = 0
	material = (options["Material:"].ID, options["Material:"].blockData)
	QTY = options["How many blocks?"]
	OVERWRITE = options["Overwrite Blocks?"]
	ONLYOVERWRITE = options["Only Overwrite Blocks?"]
	# END CONSTANTS

	for iterQty in xrange(0, QTY):
		(x, y, z) = (randint(0, width-1), randint(0, height-1), randint(0, depth-1) )

		if OVERWRITE == False:
			print 'setBlock1'
			setBlockIfEmpty(level, material, box.minx+x, box.miny+y, box.minz+z)
		else:
			if ONLYOVERWRITE == True:
				print 'setBlock2'
				setBlockIfNotEmpty(level, material, box.minx+x, box.miny+y, box.minz+z)
			else:
				print 'setBlock3'
				setBlock(level, material, box.minx+x, box.miny+y, box.minz+z)
		
						
	print '%s: Ended at %s' % (method, time.ctime())
# This filter creates thing.
# abrightmoore@yahoo.com.au
# http://brightmoore.net

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("HEMI", "label"),
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
	Hemi(level, box, options)		
	level.markDirtyBox(box)
	
def Hemi(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Hemi"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS

	radius = centreWidth
	angleDelta = pi/180
	for theta in xrange(0,360):
		for phi in xrange(0,90):
			angle = angleDelta * theta
			setBlock(level, (1,0), 
					(int)(box.minx+centreWidth + radius*( cos(angle)*cos(phi*angleDelta)) ),
					(int)(box.miny+centreWidth + radius*( sin(angle)*sin(phi*angleDelta)) ),
					(int)(box.minz+centreWidth + radius*( sin(angle)*cos(phi*angleDelta)) ),
					)
	
	print '%s: Ended at %s' % (method, time.ctime())
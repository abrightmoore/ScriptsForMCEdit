# This filter creates a type of hollow sphere using the surface you select in Minecraft.
# abrightmoore@yahoo.com.au
# http://brightmoore.net

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("SPHERIFY", "label"),
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
	Spherify(level, box, options)		
	level.markDirtyBox(box)
	
def Spherify(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Spherify"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	destY = 127
	destX = 0
	destZ = 0
	# END CONSTANTS

	PanelWidth = (int)(width/4)
	PanelDepth = (int)(depth/3)
	
	radius = width/2/pi


	for sx in xrange(0,width):
		print '%s: %s of %s' % (method, sx, width-1)
		theta = (float)(pi *2 * sx / width) # angle around the sphere (latitude) is the ratio of distance traveled in the source blocks to a full revolution.

		for sz in xrange(0,depth):

			phi = (float)(pi/2 - pi * sz / depth) # longitude is the ratio of distance traveled in the source blocks to a half revolution

			polarX = (float)(cos(theta) * cos(phi))
			polarZ = (float)(sin(theta) * cos(phi))

			for sy in xrange(0,height):

				tempBlockSource = level.blockAt(box.minx+sx,box.miny+sy,box.minz+sz) # What is the source block? Ignore air
				if tempBlockSource <> 0: # Ignore air

					dX = (float)(polarX * (radius+sy) + destX)
					dZ = (float)(polarZ * (radius+sy) + destZ)
					dY = (float)(sin(phi) * (radius+sy) + destY)

					# print '%s: polarX %s polarZ %s theta %s phi %s' % (method, (float)(polarX), (float)(polarZ),(float)(theta),(float)(phi))

					#We are mapping the source block onto a sphere where the y position is the layer from the core, and x and z are mapped onto the surface in a grid

					if level.blockAt((int)(dX), (int)(dY), (int)(dZ)) == 0: #Do nothing if a block already exists at the target location 
						level.setBlockAt((int)(dX), (int)(dY), (int)(dZ), tempBlockSource)
						level.setBlockDataAt((int)(dX), (int)(dY), (int)(dZ), level.blockDataAt(box.minx+sx, box.miny+sy, box.minz+sz))


					
	print '%s: Ended at %s' % (method, time.ctime())
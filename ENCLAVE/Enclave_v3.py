# @TheWorlfdFoundry - getting around to fixing the tearing bug by following @CodeWarrior0's advice to map back instead of forward

# This MCEDIT filter creates a round wall to an arbitrary radius using your selection area as a repeating wall section around the origin with the specified radius
# 
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

# PSEUDO CODE
# Select wall section (3D selection box) - width, depth, height
# Circumferenace = 2 x pi x (radius+depth/2) (Number of blocks around the circumference at the midpoint of the template section)
#
# Goal is to re-map blocks from the selection to the circumference.
#
# Work out the angle step size based on a full revolution divided by the step size.
#
# for each step around the circumference:
#  for each step along the depth:
#   calculate the target position for the new x,z placement of blocks.
#   for each step along the height:
#
#    If the source block is not air or "Copy air" is true: 
#     copy, modulo the source template, the source block to the target position.
#     if the gap from the previous array of blocks is too large (x2-x1 > 1 and z2-z1 > 1), fill the blocks between (maybe a line from source to target?)
#     remember this position for the next circumference step gap checking..
#     !!! Block type at source and target? Half/half? What about handling air? 
#
# Can I do anything to fit the shape into the circumference?


import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials # https://github.com/mcedit/pymclevel/blob/master/materials.py
from pymclevel import MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob

inputs = (
	  ("ENCLAVE", "label"),
#	  ("Radius", 40), 
	  ("Centre X", 0), 
	  ("Centre Z", 0),
	  ("Base Y", 64),
	  ("To use, mark a wall section width-wise and run the filter.", "label"),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Enclave(level, box, options)		
	level.markDirtyBox(box)

def Enclave(level, box, options):
	# CONSTANTS
	method = "ENCLAVE"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIR = (0,0)
	#RADIUS = options["Radius"]
	CENTREX = options["Centre X"]
	CENTREZ = options["Centre Z"]
	BASEY = options["Base Y"]
	
	CIRCUMFERENCE = 2.0 * pi * float(depth) # Offset by mid-way through the template depth to minimise distortion?
	# ANGLESTEPSIZE = 2 * pi / CIRCUMFERENCE # Radians (i.e. 1/RADIUS)

	plotMinx = CENTREX-(int(CIRCUMFERENCE)>>1)
	plotMinz = CENTREZ-(int(CIRCUMFERENCE)>>1)
	
	R = int(CIRCUMFERENCE/2)

	for x in xrange(0,int(CIRCUMFERENCE)):
		print x," of ",int(CIRCUMFERENCE)
		dx = x-R
		for z in xrange(0,int(CIRCUMFERENCE)):
			dz = z-R
			dist = sqrt(dx**2+dz**2)
			angle = atan2(dz,dx)
			angleRatio = (angle+pi)/(2.0*pi)
			#widthRatio = float(x)/float(CIRCUMFERENCE)
			depthRatio = float(dist)/float(depth)

			px = box.minx + int(angleRatio*(width-1))
			pz = box.minz + int(depthRatio*(depth-1))
			if depthRatio <= 1.0:
				for y in xrange(0, height):
					# Here we plot into this position the block we find in the source selection at the ratios we're at here
					thisBlock = level.blockAt(px,box.miny+y,pz) # read from template
					if thisBlock != 0: # ignore air
						thisBlockData = level.blockDataAt(px,box.miny+y,pz)
						setBlock(level, (thisBlock, thisBlockData), plotMinx+x, BASEY+y, plotMinz+z)
	
	# level.markDirtyBox(BoundingBox((plotMinx,BASEY,plotMinz),(int(CIRCUMFERENCE),height,int(CIRCUMFERENCE))))
	
	print '%s: Ended at %s' % (method, time.ctime())


# UTILITIES
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
    	level.setBlockDataAt(x, y, z, data)

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
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.

def drawLineLength(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	(theta,phi,distance) = getDistanceVector( (x,y,z), (x1,y1,z1))

	iter = 0
	while iter <= maxLength:
		dx = (int)(x+iter*cos(theta)*cos(phi))
		dy = (int)(y+iter*sin(phi))
		dz = (int)(z+iter*cos(theta)*cos(phi))
	
		scratchpad.setBlockAt(dx, dy, dz, blockID)
		scratchpad.setBlockDataAt(dx, dy, dz, blockData)
		iter = iter+1.0 # slightly oversample because I lack faith.
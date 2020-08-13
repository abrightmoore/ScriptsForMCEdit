# This filter creates a crater subsidence in the selection box - the surface of the world is preserved
# Suggested by SmeltScape on YouTube
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
	  ("CRATER", "label"),
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
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Crater(level, box, options)		
	level.markDirtyBox(box)

def Crater(level, box, options):
	method = "Crater"
	print '%s: Started at %s' % (method, time.ctime())	

	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	
	radius = centreDepth
	if width > depth:
		radius = centreWidth
	R = radius
	
	# For a circle described by the width and height, lower the hemisphere of blocks by an amount that corresponds with the position of the hemisphere at that point
	
	for iterX in xrange (0, width):
		for iterZ in xrange(0, depth):
			PW = centreWidth - iterX # Where is this position on the circle centred within the selection box?
			PD = centreDepth - iterZ 
			rHere = sqrt(PW*PW + PD*PD) # Pythagoras
			if rHere <= R:
				# Get the depth of the hemisphere here. R is the hypotenuse, we're after the Opposite of this right angle triangle
				opp = (int)(sqrt(R * R - rHere * rHere)) # Pythagoras
				# This opp is the amount to shift the blocks down by at this point
				if opp > 0: # Work to do
					for iterY in xrange(0,height):
						if iterY+opp < height:
							setBlock(level,
								(level.blockAt(box.minx+iterX, box.miny+iterY+opp, box.minz+iterZ), level.blockDataAt(box.minx+iterX, box.miny+iterY+opp, box.minz+iterZ)),
								box.minx+iterX, box.miny+iterY, box.minz+iterZ)
							setBlock(level,	AIR,box.minx+iterX, box.miny+iterY+opp, box.minz+iterZ) # Delete the copied block
						else:
							iterY = height # break out of loop
	
#	for iterY in xrange(1, height):
#		# at each layer, drop the blocks in the circle by one block
#		r2 = (int)(radius*radius)
#		print '%s %s Step %s of %s %s %s %s' % (method, time.ctime(), iterY, height-1, cos(((pi/2)/height)*iterY), radius, r2)
#		for iterX in xrange (0, width):
#			for iterZ in xrange(0, depth):
#				# if within the hemisphere of interest
#				PW = centreWidth - iterX # Where is this position on the circle centred within the selection box?
#				PD = centreDepth - iterZ 
#				if PW*PW+PD*PD < r2: # blit block downward
#					for iterV in xrange(iterY+1, height): # move this column down one block.
#						setBlock(level,
#								(level.blockAt(box.minx+iterX, box.miny+iterV, box.minz+iterZ), level.blockDataAt(box.minx+iterX, box.miny+iterV, box.minz+iterZ)),
#								box.minx+iterX, box.miny+iterV-1, box.minz+iterZ)
#						setBlock(level,	AIR,box.minx+iterX, box.miny+iterV, box.minz+iterZ)
#
#		radius = (int)(R * cos(((pi/2)/height)*iterY))
					
	print '%s: Ended at %s' % (method, time.ctime())	

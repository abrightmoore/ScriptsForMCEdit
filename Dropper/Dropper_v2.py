# This filter lets you generate Dropper towers
# Development was prompted by @TheQMagnet
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

# MCSchematic access method @TexelElf
# Texelelf's guidance:
#	from pymclevel import MCSchematic, mclevel
#	deformation = pymclevel.MCSchematic((width, height, length), mats=self.editor.level.materials)
#	deformation.setBlockAt(x,y,z,blockID)
#	deformation.setBlockDataAt(x,y,z,blockData)
#	deformation.Blocks[::4] = 57
#	schematic_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir? or mcplatform.schematicsDir, "Save Schematic As...", "", "Schematic\0*.schematic\0\0", ".schematic")
#	deformation.saveToFile(schematic_file)
# And from Codewarrior0's filterdemo.py:
#	level.copyBlocksFrom(temp, temp.bounds, box.origin)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
	  ("DROPPER", "label"),
	  ("Simplicity:", 10),
	  ("Perpendicular:", False),
	  ("Highlight 1:", alphaMaterials.Wood), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Highlight 2:", alphaMaterials.WoodPlanks), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Highlight 3:", alphaMaterials.BlockofIron), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Water:", alphaMaterials.Water), # https://github.com/mcedit/pymclevel/blob/master/materials.py
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

def drawLineLength(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)

	iter = 0
	while iter <= maxLength:
		dx = (int)(x+iter*cos(theta)*cos(phi))
		dy = (int)(y+iter*sin(phi))
		dz = (int)(z+iter*cos(theta)*cos(phi))
	
		scratchpad.setBlockAt(dx, dy, dz, blockID)
		scratchpad.setBlockDataAt(dx, dy, dz, blockData)
		iter = iter+1.0 # slightly oversample because I lack faith.

def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
		
	
def drawSphere(level,(x,y,z), r, material):
	RSQUARED = r*r
	for iterX in xrange(-r,r):
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			for iterY in xrange(-r,r):
				if XSQUARED + ZSQUARED + iterY*iterY <= RSQUARED:
					setBlock(level, material, XOFFSET, y+iterY, ZOFFSET)

def drawSphereSprinkles(level, (x,y,z), r, materialBase, materialOption, chance):
	RSQUARED = r*r
	for iterX in xrange(-r,r):
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			for iterY in xrange(-r,r):
				if XSQUARED + ZSQUARED + iterY*iterY <= RSQUARED:
					if randint(0,100) < chance:
						setBlock(level, materialBase, XOFFSET, y+iterY, ZOFFSET)
					else:
						setBlock(level, materialOption, XOFFSET, y+iterY, ZOFFSET)
		
def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Dropper(level, box, options)		
	level.markDirtyBox(box)
	
def Dropper(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "DROPPER"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	dx = (int)(centreWidth / 3)
	dz = (int)(centreDepth / 3)
	HL1 = (options["Highlight 1:"].ID, options["Highlight 1:"].blockData)
	HL2 = (options["Highlight 2:"].ID, options["Highlight 2:"].blockData)
	HL3 = (options["Highlight 3:"].ID, options["Highlight 3:"].blockData)
	WATER = (options["Water:"].ID, options["Water:"].blockData)
	SIMPLICITY = options["Simplicity:"]
	PERPENDICULAR = options["Perpendicular:"]
	# END CONSTANTS

	# Pseudo code
	# Make the walls
	# Create a start spot
	# Generate obstacles randomly down to the bottom
	# Create a target water pool to land in

	for y in xrange(0, height):
		print '%s: Layer %s of %s' % (method, y, height)
		for x in xrange(0, width):
			for z in xrange(0, depth):
				if y == 0: # Base
					setBlock(level, HL1, box.minx+x, box.miny+y, box.minz+z)
				else:
					if x == 0 or z == 0 or x == width-1 or z == depth-1:
						setBlock(level, HL1, box.minx+x, box.miny+y, box.minz+z)
					if ((z == 1 or z == depth-2) and x%dx == 0) or ((x ==1 or x == width-2) and z%dz == 0):
						setBlock(level, HL2, box.minx+x, box.miny+y, box.minz+z)
					
					if y == 1 and (x > centreWidth-2 and x < centreWidth+2 and z > centreDepth-2 and z < centreDepth+2): # Pool
						setBlock(level, WATER, box.minx+x, box.miny+y, box.minz+z)
					elif (y == 1 or y == height-1) and (x == centreWidth-2 or x == centreWidth+2 or z == centreDepth-2 or z == centreDepth+2): # Pool edge and launch pad
						setBlock(level, HL3, box.minx+x, box.miny+y, box.minz+z)
		if y > 4 and y < height - 8:
			if randint(0,SIMPLICITY) == 1:
				vx1 = randint(2, width-3)
				vx2 = randint(2, width-3)
				vz1 = randint(2, depth-3)
				vz2 = randint(2, depth-3)
				if randint(0,1) == 1:
					if PERPENDICULAR == False:
						drawLine(level, HL3, (box.minx+vx1,box.miny+y,box.minz), (box.minx+vx2,box.miny+y,box.minz+depth-1) )
					else:
						drawLine(level, HL3, (box.minx+vx1,box.miny+y,box.minz), (box.minx+vx1,box.miny+y,box.minz+depth-1) )
				else:
					if PERPENDICULAR == False:
						drawLine(level, HL3, (box.minx,box.miny+y,box.minz+vz1), (box.minx+width-1,box.miny+y,box.minz+vz2) )
					else:
						drawLine(level, HL3, (box.minx,box.miny+y,box.minz+vz1), (box.minx+width-1,box.miny+y,box.minz+vz1) )
					
	print '%s: Ended at %s' % (method, time.ctime())

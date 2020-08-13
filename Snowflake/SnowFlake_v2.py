# This filter creates Snowflakes
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
	  ("SNOWFLAKE", "label"),
	  ("Material:", alphaMaterials.Stone),
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
		dz = (int)(z+iter*sin(theta)*cos(phi))
	
		scratchpad.setBlockAt(dx, dy, dz, blockID)
		scratchpad.setBlockDataAt(dx, dy, dz, blockData)
		iter = iter+0.5 # slightly oversample because I lack faith.

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Snowflake(level, box, options)		
	level.markDirtyBox(box)
	
def Snowflake(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "SNOWFLAKE"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (options["Material:"].ID, options["Material:"].blockData)
	(blockID, blockData) = material
	Colours = [0, 0, 0,11,3,10, 14,1,4,5]
	CHANCETOFORM = 9 # Intended to add variability to the chance to form a block 
	# END CONSTANTS

	# Make a 2D snowflake with34 lines of symmetry (i.e. 6 equal arcs)
	# So.. do it once, then rotate into position at 60 degrees, then replicate in the other 3 quadrants.
	
	SnowFlake = zeros ( (width, depth) ) # Snowflake template. This field holds the blocks that are empty or full
	# Rotate 60 degrees and mirror within the same quadrant
		
	piDivThree = pi/3
	complexity = randint(2,7)
	
	widthHere = (int)(width/2.1)
	for iterX in xrange(0,widthHere):
		if True: # ditch this in final edit ;]
		#if randint(0,10) < complexity:
			depthHere = (int)(randint(0, depth)/8)
			for iterZ in xrange(-depthHere, depthHere):
				print '%s' % iterZ
				if iterZ == 0 or randint(0,10) < CHANCETOFORM: 
					print '%s' % iterZ
					SnowFlake[centreWidth+iterX, centreDepth+iterZ] = SnowFlake[centreWidth+iterX, centreDepth+iterZ]+1
					SnowFlake[centreWidth-iterX, centreDepth-iterZ] = SnowFlake[centreWidth-iterX, centreDepth-iterZ]+1

				if iterZ == 0 or randint(0,10) < CHANCETOFORM:
					r = sqrt(iterX*iterX + iterZ*iterZ)
					phi = piDivThree-atan2(iterZ,iterX)
					x = (int)(r*cos(phi))
					z = (int)(r*sin(phi))
					SnowFlake[centreWidth+x, centreDepth+z] = SnowFlake[centreWidth+x, centreDepth+z]+1

				if iterZ == 0 or randint(0,10) < CHANCETOFORM:
					r = sqrt(iterX*iterX + iterZ*iterZ)
					phi = piDivThree*2-atan2(iterZ,iterX)
					x = (int)(r*cos(phi))
					z = (int)(r*sin(phi))
					SnowFlake[centreWidth+x, centreDepth+z] = SnowFlake[centreWidth+x, centreDepth+z]+1

				if iterZ == 0 or randint(0,10) < CHANCETOFORM:
					r = sqrt(iterX*iterX + iterZ*iterZ)
					phi = piDivThree*4-atan2(iterZ,iterX)
					x = (int)(r*cos(phi))
					z = (int)(r*sin(phi))
					SnowFlake[centreWidth+x, centreDepth+z] = SnowFlake[centreWidth+x, centreDepth+z]+1
					
				if iterZ == 0 or randint(0,10) < CHANCETOFORM:
					r = sqrt(iterX*iterX + iterZ*iterZ)
					phi = piDivThree*5-atan2(iterZ,iterX)
					x = (int)(r*cos(phi))
					z = (int)(r*sin(phi))
					SnowFlake[centreWidth+x, centreDepth+z] = SnowFlake[centreWidth+x, centreDepth+z]+1
	# Tilt
	if(height > 1):
		# random tilt
		inclineX = ((float)(height)/(float)(width))
		inclineZ = 0.0
		if randint(1,10) < 5:
			inclineX = ((float)(height)/(float)(width))
		else:
			inclineZ = ((float)(height)/(float)(depth))
		if randint(1,10) < 5:
			inclineX = -inclineX
		if randint(1,10) < 5:
			inclineZ = -inclineZ
		print '%s: Tilting x %s z %s' % (method, inclineX, inclineZ)

		deltaY = abs(inclineX)
		if abs(inclineZ) > deltaY:
			deltaY = abs(inclineZ)
		
		for iterX in xrange(0,width):
			for iterZ in xrange(0,depth):
				if SnowFlake[iterX,iterZ] > 0: #and SnowFlake[iterX,iterZ] < complexity:
					if blockID == 35: # Wool - special colour handling
						setBlock(level, (blockID, Colours[(int)(SnowFlake[iterX,iterZ]%len(Colours))]), box.minx+iterX+ box.miny+(iterX*inclineX+iterZ*inclineZ)+deltaY, box.minz+iterZ) # Wool has colours.
					else:
						setBlock(level, material, box.minx+iterX, box.miny+(iterX*inclineX+iterZ*inclineZ)+deltaY, box.minz+iterZ)
	else:
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depth):
				if SnowFlake[iterX,iterZ] > 0: #and SnowFlake[iterX,iterZ] < complexity:
					if blockID == 35: # Wool - special colour handling
						setBlock(level, (blockID, Colours[(int)(SnowFlake[iterX,iterZ]%len(Colours))]), box.minx+iterX, box.miny, box.minz+iterZ) # Wool has colours.
					else:
						setBlock(level, material, box.minx+iterX, box.miny, box.minz+iterZ)

	print '%s: Ended at %s' % (method, time.ctime())
	

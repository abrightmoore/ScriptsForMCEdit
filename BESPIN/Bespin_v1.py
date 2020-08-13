# This filter lets you make the panel highlights as in the Bespin cloud city from Star Wars V: The Empire Strikes Back
# NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOoooooooooooooooooooooooooooooooo!!!!!!!!!!!!!!!!!!!!!!!
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
	  ("BESPIN", "label"),
	  ("Highlight 1:", alphaMaterials.Wood), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Highlight 2:", alphaMaterials.WoodPlanks), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Highlight 3:", alphaMaterials.WoodPlanks), # https://github.com/mcedit/pymclevel/blob/master/materials.py
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
	Bespin(level, box, options)		
	level.markDirtyBox(box)
	
def Bespin(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "BESPIN"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	HL1 = (options["Highlight 1:"].ID, options["Highlight 1:"].blockData)
	HL2 = (options["Highlight 2:"].ID, options["Highlight 2:"].blockData)
	HL3 = (options["Highlight 3:"].ID, options["Highlight 3:"].blockData)
	# END CONSTANTS

	# Pseudo code
	# Define a few segment sizes that most panels will be
	# Then pack in an occasional composite panel of smaller sizes
	# The highlights are the lights around the edges.
	
	PANELSIZE_X = 8 + randint(0,8)
	PANELSIZE_Y = 8 + randint(0,8)
	
	y = 0
	while y < height:
		print 'Progress: %s of %s' % (y, height)
		h = PANELSIZE_Y
		w = PANELSIZE_X
		if randint(0,5) < 2: # Standard panel
			h = (int)(PANELSIZE_Y / randint(1,4))
			w = (int)(PANELSIZE_X * randint(1,5))
		elif randint(0,5) < 2: # Standard panel
			h = (int)(PANELSIZE_Y * randint(1,3))
			w = (int)(PANELSIZE_X / randint(1,5))
		elif randint(0,5) < 2: # Standard panel
			h = (int)(PANELSIZE_Y * randint(1,3))
			w = (int)(PANELSIZE_X * randint(1,5))
		elif randint(0,5) < 2: # Standard panel
			h = (int)(PANELSIZE_Y / randint(1,4))
			w = (int)(PANELSIZE_X / randint(1,5))

			
		x = 0
		while x < width:
			LIGHTS = HL2
			if randint(0,5) == 1:
				LIGHTS = HL3
			drawLine(level, HL1, (box.minx + x, box.miny + y, box.minz), (box.minx + x, box.miny + y + h -1, box.minz))
			drawLine(level, HL1, (box.minx + x, box.miny + y + h-1, box.minz), (box.minx + x + w-1, box.miny + y + h-1, box.minz))
			if randint(0,5) < 3:
				drawLine(level, HL1, (box.minx + x, box.miny + y + h -2, box.minz), (box.minx + x + w-1, box.miny + y + h -2, box.minz))
				if randint(0,5) < 3:
					drawLine(level, HL1, (box.minx + x, box.miny + y + h -3, box.minz), (box.minx + x + w-1, box.miny + y + h -3, box.minz))
			drawLine(level, HL1, (box.minx + x + w-1, box.miny + y + h-1, box.minz), (box.minx + x + w-1, box.miny + y, box.minz))
			drawLine(level, HL1, (box.minx + x + w-1, box.miny + y, box.minz), (box.minx + x, box.miny + y, box.minz))
			for x1 in xrange(x,x+w):
				for y1 in xrange(y,y+h):
					if w > 4 and h > 4:
						if x1%w == 2 or x1%w == w-3 or y1%h == 2 or y1%h == h-3:
							if randint(0,4) == 1:
								setBlock(level, LIGHTS, box.minx+x1, box.miny+y1, box.minz)
					
			x = x + w 
		y = y + h
						
	print '%s: Ended at %s' % (method, time.ctime())
	

# This filter lets you make cratered moons and other stuff
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
	  ("That's No Moon!", "label"),
	  ("Atmosphere:", alphaMaterials.Ice), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Material:", alphaMaterials.BlockofIron), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Layers?", False),
	  ("Layers:", ("string","value=2 3 1 16 1 1 11 42")),
	  ("Chance of Layer Material:", 100),
	  ("Chance of Ring Material:", 0),
	  ("Crescent?", False),
	  ("Swiss Cheese?", False),
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
	thatsNoMoon(level, box, options)		
	level.markDirtyBox(box)
	
def thatsNoMoon(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "THATSNOMOON"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (options["Material:"].ID, options["Material:"].blockData)
	atmosphere = (options["Atmosphere:"].ID, options["Atmosphere:"].blockData)
	RING = options["Chance of Ring Material:"]
	CRESCENT = options["Crescent?"]
	SWISSCHEESE = options["Swiss Cheese?"]
	LAYERFLAG = options["Layers?"]
	LAYER = options["Layers:"].split()
	LAYERS = map(int, LAYER)
	LAYERCHANCE = options["Chance of Layer Material:"]
	ANGLESTEP = pi/180
	# END CONSTANTS

	radius = centreWidth
	if centreHeight < radius:
		radius = centreHeight
	if centreDepth < radius:
		radius = centreDepth
	
	(ox, oy, oz) = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
	
	# Base sphere - solid
	print '%s: Atmosphere' % (method)
	drawSphere(level, (ox, oy, oz), radius, atmosphere)
	
	# Draw interior
	if LAYERFLAG == True:
		print '%s: Layering it like an onion.' % (method)
		posn = 0
		layerSize = (int)(radius/(len(LAYERS)+1))
		for layerIter in LAYERS:
			posn = posn +1
			drawSphereSprinkles(level, (ox, oy, oz), radius-(posn*layerSize), (layerIter, 0), material, LAYERCHANCE)
		
	
	
	# Impact craters
	
	maxCraters = randint(1,10*radius)
	for craterIter in xrange(0,maxCraters):
		print '%s: Cratering %s of %s' % (method, craterIter, maxCraters)
		craterSize = randint(radius/10+1, radius/5+2)
		theta = randint(0,360)*ANGLESTEP
		phi = randint(0,360)*ANGLESTEP
		if SWISSCHEESE == True:
			r = randint((int)(radius/3),radius)
		else:
			r = radius+(craterSize*3/4)
		(x, y, z) = getRelativePolar((ox, oy, oz), (theta,phi, r))
		drawSphere(level, (x, y, z), craterSize, (0,0))
		# Then draw the depression
#		(x, y, z) = getRelativePolar((ox, oy, oz), (theta,phi, radius-(craterSize*2/3+craterSize/2)))
#		drawSphere(level, (x, y, z), craterSize*2/3, (0,0))
	
	if CRESCENT == True:
		print '%s: Crescent' % (method)
		craterSize = (int)(radius*2)
		theta = randint(0,360)*ANGLESTEP
		phi = randint(0,360)*ANGLESTEP
		(x, y, z) = getRelativePolar((ox, oy, oz), (theta,phi, craterSize))
		drawSphere(level, (x, y, z), craterSize, (0,0))
	
	# Rings
	if RING > 0:
		print '%s: Ring ring...' % (method)
		if(height > 1):
			# Rings with a random tilt
			inclineX = ((float)(height)/(float)(width))
			inclineZ = ((float)(width)/(float)(height))
			if randint(1,10) < 5:
				inclineX = ((float)(2.0)/(float)(randint(1,100)))
			else:
				inclineZ = ((float)(2.0)/(float)(randint(1,100)))
			if randint(1,10) < 5:
				inclineX = -inclineX
			if randint(1,10) < 5:
				inclineZ = -inclineZ
			print '%s: Tilting x %s z %s' % (method, inclineX, inclineZ)

			deltaY = abs(inclineX)
			if abs(inclineZ) > deltaY:
				deltaY = abs(inclineZ)
			
			minR = (int)(width)
			minRd = minR-(width/4)
			minRSq = minR*minR
			minRdSq = minRd * minRd
			for iterX in xrange(-minR,minR):
				XSQUARED = iterX*iterX
				for iterZ in xrange(-minR,minR):
					t = XSQUARED + iterZ * iterZ
					if t >= minRdSq and t <= minRSq and randint(0,100) <= RING:
						setBlock(level, material, box.minx+centreWidth+iterX, box.miny+centreHeight+(iterX*inclineX+iterZ*inclineZ)+deltaY, box.minz+centreDepth+iterZ) # Wool has colours.

	print '%s: Ended at %s' % (method, time.ctime())
	

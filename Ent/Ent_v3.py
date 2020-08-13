# This filter lets you make Giant Trees
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
	  ("ENT", "label"),
	  ("Bark:", alphaMaterials.Wood), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Wood:", alphaMaterials.WoodPlanks), # https://github.com/mcedit/pymclevel/blob/master/materials.py
#	  ("Leaves:", alphaMaterials.Leaves), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Years of Growth:", 3),
	  ("Floor Each:", 1),
	  ("Randomness:", 1),
	  ("Termites?", False),
#	  ("Branches?", False),
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
	Ent(level, box, options)		
	level.markDirtyBox(box)
	
def Ent(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "ENT"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	BARK = (options["Bark:"].ID, options["Bark:"].blockData)
	WOOD = (options["Wood:"].ID, options["Wood:"].blockData)
#	LEAVES = (options["Leaves:"].ID, options["Leaves:"].blockData)
	RANDOMNESS = options["Randomness:"]
	RINGS = options["Years of Growth:"]
	FLOOR = options["Floor Each:"]
	SWISSCHEESE = options["Termites?"]
#	BRANCHES = options["Branches?"]
	ANGLESTEP = pi/180
	TwoPI = 2*pi
	# END CONSTANTS

	# Pseudo code
	# start with a square base of a random orientation
	# Draw a square in the current layer with bark on the outside and wood material on the inside
	# Randomly rotate the base slightly and decrease the size a little
	# Draw the next layer up.
	
	SideLength = centreWidth
	Orientation = randint(0,45)
	
	offsetX = 0
	offsetZ = 0
	
	angle = TwoPI/360
	
	# Growth rings - suggested by Chandler Gloyd
	
	numSides = 3+randint(0,15)
	
	for y in xrange(0, height):
		print '%s: %s of %s' % (method, y, height)
		radius = (int)(SideLength)
		
		for r in xrange(1,radius):
			MATERIAL = WOOD
			ringR = (int)(SideLength/RINGS)
			if ringR == 0:
				ringR == 2
			if r == radius-1 or r%ringR == 0: # Growth rings and bark
				MATERIAL = BARK
			
			if (MATERIAL == WOOD and y%FLOOR == 0) or (MATERIAL == BARK):
				x = r * cos(Orientation*angle)
				z = r * sin(Orientation*angle)
				
				for sides in xrange(0,numSides+1):
					x1 = r * cos((Orientation+360/numSides*sides)*angle)
					z1 = r * sin((Orientation+360/numSides*sides)*angle)
					drawLine(level, MATERIAL, (box.minx+centreWidth+x+offsetX,box.miny+y,box.minz+offsetZ+centreDepth+z), (box.minx+centreWidth+x1+offsetX,box.miny+y,box.minz+centreDepth+z1+offsetZ) )
					x = x1
					z = z1
		
		if(randint(0,3) == 0):
			SideLength = SideLength - 1
			if RANDOMNESS > 0:
				offsetX = offsetX+randint(0,2*RANDOMNESS+1)-RANDOMNESS
				offsetZ = offsetZ+randint(0,2*RANDOMNESS+1)-RANDOMNESS
		if SideLength < 1:
			break
		if(randint(0,4) == 0):
			Orientation = Orientation + randint(1,5)

#	if BRANCHES == True:
#		for y in xrange(0, height):
#			print '%s: %s of %s' % (method, y, height)
#			if randint(1,100) < 5:
#				(ox, oy, oz) = (box.minx+centreWidth, box.miny+y, box.minz+centreDepth)
#				theta = randint(0,360)*ANGLESTEP
#				phi = randint(0,45)*ANGLESTEP
#				MATERIAL = BARK
#				maxLength = height-y
#				distance = 0
#				while distance < maxLength:
#					(x, y, z) = getRelativePolar((ox, oy, oz), (theta,phi, distance))
#					drawSphere(level, (x,y,z), centreWidth/8, MATERIAL )
#					distance = distance + (maxLength-distance)/3 +2
				
	if SWISSCHEESE == True:
		radius = centreWidth
		if centreHeight < radius:
			radius = centreHeight
		if centreDepth < radius:
			radius = centreDepth
		(ox, oy, oz) = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
		maxCraters = randint(1,10*radius)
		for craterIter in xrange(0,maxCraters):
			print '%s: Cratering %s of %s' % (method, craterIter, maxCraters)
			craterSize = randint(radius/10+1, radius/5+2)
			theta = randint(0,360)*ANGLESTEP
			phi = randint(0,360)*ANGLESTEP
			r = randint((int)(radius/3),radius)
			(x, y, z) = getRelativePolar((ox, oy, oz), (theta,phi, r))
			drawSphere(level, (x, y, z), craterSize, (0,0))
		
						
	print '%s: Ended at %s' % (method, time.ctime())
	

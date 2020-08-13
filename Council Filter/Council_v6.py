# This filter makes roads and bridges.
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
	  ("COUNCIL WORKS", "label"),
	  ("Material:", alphaMaterials.Brick), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Mix Material:", alphaMaterials.Gravel), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Edge Material:", alphaMaterials.StoneBricks), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Support Material:", alphaMaterials.MossyCobblestoneWall), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Support Gap:", 0),
	  ("Start X:", 0),
	  ("Start Y:", 64),
	  ("Start Z:", 0),
	  ("End X:", 100),
	  ("End Y:", 64),
	  ("End Z:", 28),
	  ("Width:", 8),
	  ("Height:", 6),
	  ("... Or Automatic Mode?", False),
	  ("Mix Material Chance 0-100:", 0),
	  ("No Material Chance 0-100:", 0),
	  ("Meander?", False),
	  ("Tunnel Support?", False),
	  ("Arches?", False),
	  
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
	(theta,phi,distance) = getDistanceVector( (x,y,z), (x1,y1,z1))

	iter = 0
	while iter <= maxLength:
		dx = (int)(x+iter*cos(theta)*cos(phi))
		dy = (int)(y+iter*sin(phi))
		dz = (int)(z+iter*cos(theta)*cos(phi))
	
		scratchpad.setBlockAt(dx, dy, dz, blockID)
		scratchpad.setBlockDataAt(dx, dy, dz, blockData)
		iter = iter+1.0 # slightly oversample because I lack faith.

def getDistanceVector( (x,y,z), (x1,y1,z1) ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)
	
	return (theta, phi, distance)
		
def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
		
		
def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	councilWorks(level, box, options)		
	level.markDirtyBox(box)
	
def councilWorks(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "COUNCIL WORKS"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (options["Material:"].ID, options["Material:"].blockData)
	edgeMaterial = (options["Edge Material:"].ID, options["Edge Material:"].blockData)
	supportMaterial = (options["Support Material:"].ID, options["Support Material:"].blockData)
	mixMaterial = (options["Mix Material:"].ID, options["Mix Material:"].blockData)
	MIXMATERIALCHANCE = options["Mix Material Chance 0-100:"]
	NOMATERIALCHANCE = options["No Material Chance 0-100:"]
	TUNNELSUPPORT = options["Tunnel Support?"]
	ARCHES = options["Arches?"]
	MEANDER = options["Meander?"]
	AUTOMATIC = options["... Or Automatic Mode?"]
	supportGap = options["Support Gap:"]
	(startX, startY, startZ) = (options["Start X:"], options["Start Y:"], options["Start Z:"] )
	(endX, endY, endZ) = (options["End X:"], options["End Y:"], options["End Z:"] )
	bWidth = options["Width:"]
	bHeight = options["Height:"]
	STEPSIZE = 0.25
	AIR = (0,0)
	# END CONSTANTS

	if AUTOMATIC == True:
		bHeight = height
		startY = box.miny
		endY = startY
		MEANDER = False
		if width < depth:
			bWidth = width
			startX = (int)(box.minx+width/2)
			endX = startX
			startZ = box.minz
			endZ = box.maxz
		else:
			bWidth = depth
			startX = box.minx
			endX = box.maxx
			startZ = (int)(box.minz+depth/2)
			endZ = startZ
	
	if supportGap < 1:
		supportGap = randint(2,16)
	
	squiggliness = 20 * randint(1,10)
	squiggleCounter = 0
	(basePosX, basePosY, basePosZ) = (startX,startY,startZ)
	(theta,phi,distance) = getDistanceVector( (basePosX, basePosY, basePosZ), (endX,endY,endZ))
	
	hWidth = (int)(bWidth / 2)
	for pathIter in xrange(0,(int)(distance/STEPSIZE)):
		ARCH = (int)(pathIter/STEPSIZE)%supportGap
		SUPPORTBLOCK = level.blockAt((int)(basePosX), (int)(basePosY+bHeight), (int)(basePosZ))
		for iter in xrange(-hWidth,hWidth):
			 # start block
			squiggleCounter = squiggleCounter+1
			if MEANDER == True and squiggleCounter % squiggliness == 0:
				theta = theta + randint(-1,1)*pi/32
			
			(x1, y1, z1) = getRelativePolar( (basePosX, basePosY, basePosZ), (theta+pi/2, 0, iter) )
			
			for iterY in xrange(0,bHeight):
				theMaterial = AIR
				if iterY == 0:
					if abs(iter) >= hWidth-1:
						theMaterial = edgeMaterial
					else:
						if randint(0,100) < NOMATERIALCHANCE:
							theMaterial = AIR
						elif randint(0,100) < MIXMATERIALCHANCE:
							theMaterial = mixMaterial
						else:
							theMaterial = material
				else:
					if ARCH == 0 and (ARCHES == True or (TUNNELSUPPORT == True and SUPPORTBLOCK != 0)):
						if abs(iter) >= hWidth-1 or iterY >= bHeight-1 or (bHeight - iterY) <= abs(iter*2):
							theMaterial = supportMaterial
						

				setBlock(level, theMaterial, x1, y1+iterY, z1)
		(basePosX, basePosY, basePosZ) = getRelativePolar( (basePosX, basePosY, basePosZ), (theta, phi, 0.25)) # oversample to prevent columns of missed blocks.
	
	print '%s: Ended at %s' % (method, time.ctime())
	

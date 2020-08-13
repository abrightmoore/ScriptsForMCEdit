# This filter makes Villager heads. I know.
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
	  ("VILLAGER HEADS", "label"),
	  ("Material:", alphaMaterials.Cobblestone), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Mix Material:", alphaMaterials.Stone), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Edge Material:", alphaMaterials.StoneBricks), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Eye:", alphaMaterials.WoodPlanks), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Iris:", alphaMaterials.Leaves), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Mix Material Chance 0-100:", 10),
	  ("No Edge Material Chance 0-100:", 0),
	  ("Hollow?", True),
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
	villagerHead(level, box, options)		
	level.markDirtyBox(box)
	
def villagerHead(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "VILLAGER HEAD"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (options["Material:"].ID, options["Material:"].blockData)
	edgeMaterial = (options["Edge Material:"].ID, options["Edge Material:"].blockData)
	eyeMaterial = (options["Eye:"].ID, options["Eye:"].blockData)
	irisMaterial = (options["Iris:"].ID, options["Iris:"].blockData)
	mixMaterial = (options["Mix Material:"].ID, options["Mix Material:"].blockData)
	MIXMATERIALCHANCE = options["Mix Material Chance 0-100:"]
	NOMATERIALCHANCE = options["No Edge Material Chance 0-100:"]
	HOLLOW = options["Hollow?"]
	AIR = (0,0)
	WIDTHRADIUS = 4
	HEIGHTRADIUS = 5
	# END CONSTANTS

	# exterior planes
	for x1 in xrange(-1,2):
		for y1 in xrange(-1,2):
			for z1 in xrange(-1,2):
				if x1 != 0 and y1 != 0 and z1 != 0:
					for x in xrange(0,WIDTHRADIUS+1):
						for y in xrange(0,HEIGHTRADIUS+1):
							for z in xrange(0,WIDTHRADIUS+1):
								theMaterial = material
								if (x == WIDTHRADIUS and y == HEIGHTRADIUS) or (z == WIDTHRADIUS and y == HEIGHTRADIUS) or (z == WIDTHRADIUS and x == WIDTHRADIUS):
									theMaterial = edgeMaterial
									if randint(0,99) < NOMATERIALCHANCE:
										theMaterial = AIR
								if randint(0,99) < MIXMATERIALCHANCE:
									theMaterial = mixMaterial
								if HOLLOW == True:
									if x == WIDTHRADIUS or z == WIDTHRADIUS or y == HEIGHTRADIUS:
										theMaterial = theMaterial
									else:
										theMaterial = AIR
								setBlock(level, theMaterial, box.minx+centreWidth+x*x1, box.miny+centreHeight+y*y1, box.minz+centreHeight+z*z1)

	# Nose
	for y in xrange(0,HEIGHTRADIUS+1):
		for x in xrange(-1,2):
			for z in xrange(-1,2):
				setBlock(level, edgeMaterial, box.minx+centreWidth+WIDTHRADIUS+x+1, box.miny+centreHeight-1-y, box.minz+centreHeight+z)
	
	# Eyes
	for z in xrange(-1,2):
		if z != 0:
			setBlock(level, irisMaterial, box.minx+centreWidth+WIDTHRADIUS, box.miny+centreHeight, box.minz+centreHeight+WIDTHRADIUS/2*z)
			setBlock(level, eyeMaterial, box.minx+centreWidth+WIDTHRADIUS, box.miny+centreHeight, box.minz+centreHeight+(WIDTHRADIUS/2+1)*z)

	# Monobrow
	for z in xrange(-WIDTHRADIUS+1,WIDTHRADIUS):
			setBlock(level, edgeMaterial, box.minx+centreWidth+WIDTHRADIUS+1, box.miny+centreHeight+1, box.minz+centreHeight+z)
		
	# Mouth
	for z in xrange(-WIDTHRADIUS+2,WIDTHRADIUS-1):
			setBlock(level, AIR, box.minx+centreWidth+WIDTHRADIUS, box.miny+centreHeight-HEIGHTRADIUS+2, box.minz+centreHeight+z)
			
	print '%s: Ended at %s' % (method, time.ctime())
	

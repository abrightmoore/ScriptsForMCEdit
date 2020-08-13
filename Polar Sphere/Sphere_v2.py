# This filter lets you muck about with spheres in MCEdit.
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
	  ("POLARSPHERE", "label"),
	  ("Material:", alphaMaterials.BlockofIron), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Start Horiz Angle (Degrees):", 0),
	  ("End Horiz Angle (Degrees):", 360),
	  ("Start Vert Angle (Degrees):", 0),
	  ("End Vert Angle (Degrees):", 360),
	  ("Path Length:", 1000),
	  ("Horizontal Period:", 1.5),
	  ("Vertical Period:", 2.3),
	  ("Radius Period:", 0.0),
	  ("Radius Percent Gap:", 0.0),
	  ("Terminating Block:", False),
	  ("Compound Angles:", False),
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
		
		
def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	SpherePolar(level, box, options)		
	level.markDirtyBox(box)
	
def SpherePolar(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "SPHEREPOLAR"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (options["Material:"].ID, options["Material:"].blockData)
	pathLength = options["Path Length:"]
	horizPeriod = options["Horizontal Period:"]
	vertPeriod = options["Vertical Period:"]
	radiusPeriod = options["Radius Period:"]
	radiusPercentGap = options["Radius Percent Gap:"]
	termBlock = options["Terminating Block:"]
	compoundAngles = options["Compound Angles:"]
	startHorizAngle = options["Start Horiz Angle (Degrees):"]*pi/180
	endHorizAngle = options["End Horiz Angle (Degrees):"]*pi/180
	startVertAngle = options["Start Vert Angle (Degrees):"]*pi/180
	endVertAngle = options["End Vert Angle (Degrees):"]*pi/180
	TwoPI = 2*pi
	
	# END CONSTANTS

	radius = centreWidth
	if centreHeight < radius:
		radius = centreHeight
	if centreDepth < radius:
		radius = centreDepth
	
	radiusPercentGap = radiusPercentGap / 100
	
	angleSize = pi/180
	
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
	period1 = horizPeriod
	period2 = vertPeriod
	
	horizAngle = 0
	vertAngle = 0
	
	displayCounter=0
	
	for iterPath in xrange(0, pathLength):
		if displayCounter % 500 == 0:
			print '%s: %s step %s of %s' % (method, time.ctime(), iterPath+1, pathLength)
		
		displayCounter = displayCounter+1
		if compoundAngles == False:
			horizAngle = horizAngle + angleSize*period1
			vertAngle = vertAngle + angleSize*period2
		else:
			horizAngle = horizAngle + iterPath*angleSize*period1
			vertAngle = vertAngle + iterPath*angleSize*period2
		
		
		if horizAngle%TwoPI > startHorizAngle and horizAngle%TwoPI < endHorizAngle and vertAngle%TwoPI > startVertAngle and vertAngle%TwoPI < endVertAngle: # bounds check
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, radius*cos(iterPath*radiusPeriod)))
			
			if termBlock == False:
				if radiusPercentGap == 0:
					drawLine(level, material, p1, p2)
				else:
					p3 = getRelativePolar(p1, ( horizAngle, vertAngle, radius*cos(iterPath*radiusPeriod)*radiusPercentGap))
					drawLine(level, material, p3, p2)
			else:
				(x,y,z) = p2
				setBlock(level, material, x,y,z)
		
	print '%s: Ended at %s' % (method, time.ctime())
	

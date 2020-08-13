# This filter is to create crystal growths in caves and tunnels
# Requested by @theCommonPeople 
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, cosh
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from copy import deepcopy
import bresenham # @Codewarrior0

# YOUR CODE GOES HERE \/ \/ \/ \/ \/ \/ \/ \/ \/
inputs = (
		("CRYSTALS", "label"),
		("Block type:", alphaMaterials.BlockofQuartz),
		("Number of Crystals:", 15),
		("Cast Rays:", False),
		("15 Black:", True),
		("7  Dark Grey:", True),
		("8  Light Grey:", True),
		("0  White:", True),
		("6  Pink:", True),
		("14 Red:", True),
		("12 Brown:", True),
		("1  Orange:", True),
		("4  Yellow:", True),
		("5  Lime Green:", True),
		("13 Dark Green:", True),
		("9  Cyan:", True),
		("3  Light Blue:", True),
		("11 Dark Blue:", True),
		("2  Magenta:", True),
		("10 Purple:", True),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)


def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM CRYSTALS"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	SUCCESS = Crystals(level, box, options)
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end

def Crystals(level, box, options):
	method = "CRYSTALS"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	# The user has passed us a box with a centre and some walls of varying thickness
	# Method - cast rays out from the centre to the edge and where a wall is, grow a crystal
	template = level.extractSchematic(box) # Copy the cave
	AIR = (0,0)
	ANGLES = 360
	angle = pi/ANGLES*2
	RANGE = 45
	(matID,matData) = getBlockFromOptions(options,"Block type:")
	numOutCroppings = options["Number of Crystals:"]
	castRays = options["Cast Rays:"]
	
	# Data values for the block in a friendly clickable list
	o = [ options["0  White:"],
			options["1  Orange:"],
			options["2  Magenta:"],
			options["3  Light Blue:"],
			options["4  Yellow:"],
			options["5  Lime Green:"],
			options["6  Pink:"],
			options["7  Dark Grey:"],
			options["8  Light Grey:"],
			options["9  Cyan:"],
			options["10 Purple:"],
			options["11 Dark Blue:"],
			options["12 Brown:"],
			options["13 Dark Green:"],
			options["14 Red:"],
			options["15 Black:"]
		]
	print o
	c = []
	for i in xrange(0,16): # initialise
		print i
		if o[i] == True:
			c.append(i)
	if len(c) == 0:
		c.append(matData)
		
	if numOutCroppings < 1: numOutCroppings = randint(5, 50)
	for i in xrange(1,numOutCroppings):
		print 'Outcroppings %s of %s' % (i,numOutCroppings)
		theta = randint(0,ANGLES) * angle
		phi = randint(0,ANGLES) * angle
		material = (matID, c[randint(0,len(c)-1)])
		
		raylength = 2.0
		keepGoing = True
		while keepGoing == True:
			(t,u,v) = getRelativePolar( (centreWidth, centreHeight, centreDepth), (theta, phi, raylength) ) # Which way will we walk?
			(x,y,z) = (int(t),int(u),int(v))
			print '%s %s %s len %s: %s %s %s %s' % (x,y,z,raylength,width,height,depth,keepGoing)
			if castRays == True: setBlock(level, (matID,matData), x,y,z)
			block = getBlock(template, x, y, z) # Check the cave topology
			if block != AIR:
			
				# Choose a pattern
				type = randint(1,3)
				# type = 3 #test
				if type == 1: # Line to centre
					llength = randint(3,10)
					theta2 = theta
					phi2 = phi-pi #reverse direction
					(x1,y1,z1) = getRelativePolar( (x,y,z), (theta2, phi2, llength) ) # Which way will we draw?
					drawLine(level, material, (x,y,z),(x1,y1,z1))
				elif type == 2: # sphere
					theta2 = theta
					phi2 = phi-pi #reverse direction
					spokes = randint(3,7)
					spokeAngle = 2*pi/spokes
					llength = randint(5,10)
					for j in 0,spokes:
						theta2 = theta
						for k in 0,spokes:
							(x1,y1,z1) = getRelativePolar( (x,y,z), (theta2, phi2, llength) )
							drawLine(level, material, (x,y,z),(x1,y1,z1))
							theta2 = theta2+spokeAngle
						phi2 = phi2+spokeAngle
				
				else: # random splodge
					numShards = randint(3,11)
					for j in 0,numShards: # per @CodeWarrior0
						print '%s of %s' % (j,numShards)
						llength = randint(3,10)
						theta2 = theta #+pi+randint(-RANGE,RANGE)*angle
						phi2 = phi - pi +randint(-RANGE,RANGE)*angle
						(x1,y1,z1) = getRelativePolar( (x,y,z), (theta2, phi2, llength) ) # Which way will we draw?
						drawLine(level, material, (x,y,z),(x1,y1,z1))
				
				keepGoing = False
			if x < 0: keepGoing = False
			if y < 0: keepGoing = False
			if z < 0: keepGoing = False
			if x > width-1: keepGoing = False
			if y > height-1: keepGoing = False
			if z > depth-1: keepGoing = False
			if raylength > 1000.0: keepGoing = False
			raylength = raylength + 1.0
	
	FuncEnd(level,box,options,method) # Log end
	return True

	
############# METHOD HELPERS #############
	
def FuncStart(level, box, options, method):
	# abrightmoore -> shim to prepare a function.
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	
	# other initialisation methods go here
	return (method, (width, height, depth), (centreWidth, centreHeight, centreDepth))

def FuncEnd(level, box, options, method):
	print '%s: Ended at %s' % (method, time.ctime())

############# WORLD ACCESS HELPERS #############

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
	
############# GFX PRIMITIVES #############

def setBlockIfEmpty(level, (block, data), x, y, z):
	tempBlock = level.blockAt(x,y,z)
	if tempBlock == 0:
		setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLine1(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ): # @ CodeWarrior
	for px, py, pz in bresenham.bresenham((x,y,z),(x1,y1,z1)): # @ CodeWarrior
		setBlock(scratchpad,(blockID, blockData),px,py,pz) # @ CodeWarrior 
	setBlock(scratchpad,(blockID, blockData),x1,y1,z1) # @ CodeWarrior
	
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

############# GFX  #############			
			
def Bridge(level, box, options):
	method = options["Operation"]
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	TENSION = options["Tension:"]
	WIDTH = options["Width:"]
	MARKERBLOCK = getBlockFromOptions(options,"Marker block:")
	PATHBLOCK = getBlockFromOptions(options,"Path block:")
	FENCEBLOCK = getBlockFromOptions(options,"Fence block:")
	RAILINGBLOCK = getBlockFromOptions(options,"Railing block:")
	ANCHORBLOCK = getBlockFromOptions(options,"Anchor block:")
	SUCCESS = False
	Q = [] # A queue of locations where the marker blocks have been found
	# 1. find all the marker blocks in the selection. These are the bridge endpoints
#	for iterY in xrange(box.miny, box.maxy):
#		for iterZ in xrange(box.minz, box.maxz):
#			for iterX in xrange(box.minx, box.maxx):
	for (iterX, iterY, iterZ) in box.positions: #@naor2012 
		if getBlock(level,iterX,iterY,iterZ) == MARKERBLOCK:
			Q.append( (iterX, iterY, iterZ) )
			print Q
	
	# 2. draw a bridge between each set of markers.
	if len(Q) > 1:
		p = Q[0]	
		for i in xrange(1,len(Q)):
			n = Q[i]
			# drawLine(level, PATHBLOCK, p, n) # Simple test - draw a line between two points
				
			# 2a. let's draw a bridge as a Catenary arc y = a cosh( x/a )
			saggyPath(level, PATHBLOCK, FENCEBLOCK, RAILINGBLOCK, ANCHORBLOCK, p, n, TENSION, WIDTH )
			
			p = n # Current point becomes the previous point
		
		SUCCESS = True
	
	FuncEnd(level,box,options,method) # Log end
	return SUCCESS

def distance( (x1,y1,z1), (x2,y2,z2) ):
	p = x1 * x2 + z1 * z2
	return sqrt( p + y1 * y2 )
	
def saggyPath(level, PATHBLOCK, FENCEBLOCK, RAILINGBLOCK, ANCHORBLOCK, (x,y,z), (x1,y1,z1), tension, WIDTH ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)
	toTheRight = theta + pi/2
	toTheLeft = theta - pi/2
	(lx,lz) = (x+(WIDTH/2)*cos(toTheLeft) , z+(WIDTH/2)*sin(toTheLeft) )
	(rx,rz) = (x+(WIDTH/2)*cos(toTheRight) , z+(WIDTH/2)*sin(toTheRight) )
	
	ddx = rx - lx
	ddz = rz - lz
	dist = ceil(sqrt( ddx * ddx + ddz *ddz))
	print dist

	# Draw lines to make a path of the specified width from the start location to the end
	i = 0
	while i <= dist: #
		dthetax = cos(toTheRight)
		dthetaz = sin(toTheRight)
		startx = lx + dthetax*float(i)
		startz = lz + dthetaz*float(i)
		drawSaggyArc(level, PATHBLOCK, (startx,y,startz), theta, phi, distance, tension, WIDTH)
		i = i + 0.5
	for iterY in xrange(1,2):
		drawSaggyArc(level, FENCEBLOCK, (lx,y+iterY,lz), theta, phi, distance, tension, 1)
		drawSaggyArc(level, FENCEBLOCK, (lx+dthetax*dist,y+iterY,lz+dthetaz*dist), theta, phi, distance, tension, 1)
	for iterY in xrange(2,3):
		drawSaggyArc(level, RAILINGBLOCK, (lx,y+iterY,lz), theta, phi, distance, tension, 1)
		drawSaggyArc(level, RAILINGBLOCK, (lx+dthetax*dist,y+iterY,lz+dthetaz*dist), theta, phi, distance, tension, 1)
	# Anchor points
	drawLine(level, ANCHORBLOCK, (lx,y,lz),(lx,y+2,lz))
	drawLine(level, ANCHORBLOCK, (lx+dthetax*dist,y,lz+dthetaz*dist),(lx+dthetax*dist,y+2,lz+dthetaz*dist))
	drawLine(level, ANCHORBLOCK, ((int)(lx+distance*cos(theta)*cos(phi)), (int)(y+distance*sin(phi)), (int)(lz+distance*sin(theta)*cos(phi))),((int)(lx+distance*cos(theta)*cos(phi)), (int)(y+distance*sin(phi)+3), (int)(lz+distance*sin(theta)*cos(phi))))
	drawLine(level, ANCHORBLOCK, ((int)(lx+dthetax*dist+distance*cos(theta)*cos(phi)), (int)(y+distance*sin(phi)), (int)(lz+dthetaz*dist+distance*sin(theta)*cos(phi))),((int)(lx+dthetax*dist+distance*cos(theta)*cos(phi)), (int)(y+distance*sin(phi)+3), (int)(lz+dthetaz*dist+distance*sin(theta)*cos(phi))))
	
def drawSaggyArc(level, material, (x,y,z), theta, phi, distance, tension, width):
	midPoint = distance/2
	scale = distance / tension

	p = (0,0,0)
	iter = 0
	while iter <= distance:
		xx = (iter - midPoint)/midPoint
		ddy = xx*xx*scale
		n = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)+ddy-scale), (int)(z+iter*sin(theta)*cos(phi)))
		if p != (0,0,0):
			drawLine(level, material, p, n)
		p = n
		iter = iter+0.5 # slightly oversample because I lack faith.
	
def saggyLine_v1(scratchpad, PATHBLOCK, (x,y,z), (x1,y1,z1), tension, width,  ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)
	toTheRight = theta + pi/2
	toTheLeft = theta - pi/2
	(lx,lz) = (x+(width/2)*cos(toTheLeft) , y+(width/2)*sin(toTheLeft) )
	(rx,rz) = (x+(width/2)*cos(toTheRight) , y+(width/2)*sin(toTheRight) )
	
	ddx = rx - lx
	ddz = rz - lz
	dist = ceil(sqrt( ddx * ddx + ddz *ddz))
	print dist
	midPoint = distance/2
	scale = distance / tension

	# Draw lines to make a path of the specified width from the start location to the end
	i = 0
	while i < dist: #
		startx = lx + cos(toTheLeft)*float(i)
		startz = lz + sin(toTheLeft)*float(i)
		print startx
		print startz
		p = (0,0,0)
		iter = 0
		while iter <= distance:
			xx = (iter - midPoint)/midPoint
			ddy = xx*xx*scale
			n = ((int)(startx+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)+ddy-scale), (int)(startz+iter*sin(theta)*cos(phi)))
			if p != (0,0,0):
				drawLine(scratchpad, PATHBLOCK, p, n)
			p = n
			iter = iter+0.5 # slightly oversample because I lack faith.
		i = i + 0.5

# This filter is to create suspension bridges
# Requested by @SirVladymir (Twitter) / https://www.youtube.com/user/SirVladimyr (YouTube)
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
		("SUSPENSION BRIDGES", "label"),
		("Operation", (
			"Suspension Bridge",
			"Suspension Bridge"
  		    )),
		("Tension:", 5.0),
		("Width:", 5.0),
		("Marker block:", alphaMaterials.BlockofQuartz),
		("Path block:", alphaMaterials.BlockofQuartz),
		("Fence block:", alphaMaterials.Brick),
		("Railing block:", alphaMaterials.Stone),
		("Anchor block:", alphaMaterials.GlassPane), # Randomly assigned
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

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
	
	shuffle(Q)
	
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
		
def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = options["Operation"]
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	SUCCESS = Bridge(level, box, options)
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end

	
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

############# GFX PRIMATIVES #############

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
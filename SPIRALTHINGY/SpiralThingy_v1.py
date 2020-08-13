# A spiral tower thingy
# abrightmoore@yahoo.com.au

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0

inputs = (
	  ("SPIRALLY THINGY", "label"),
	  ("Material:", alphaMaterials.Stone),
	  ("Fill Material:", alphaMaterials.Stone),
	  ("Slab Material:", alphaMaterials.StoneSlab),
	  ("Quick?", True),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

def SpiralThingyQuick(level,box,options):
	method = "SpiralThingy"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	MATERIAL = getBlockFromOptions(options,"Material:")
	SLAB = getBlockFromOptions(options,"Slab Material:")
	
	# Start at the centre of the box, and at the top of the selection, 
	x1=centreWidth
	y1=height-1
	z1=centreDepth
	x=x1
	y=y1
	z=z1
	xold = x
	yold = y
	zold = z
	pathLength = 0
	angle = pi/180
	while y > 0:
		for iterY in xrange(0,y):
			setBlock(level,MATERIAL,box.minx+x,box.miny+iterY,box.minz+z)
		drawLine(level,MATERIAL,(box.minx+x,box.miny+iterY,box.minz+z),(box.minx+xold,box.miny+yold,box.minz+zold))
		pathLength = pathLength+1
		revolutions = pathLength/(90)
		xold = x
		yold = y
		zold = z
		x = x1 + sin(angle*pathLength) * revolutions
		z = z1 + cos(angle*pathLength) * revolutions
		y = y1 - 1 - revolutions
		
		
	
	FuncEnd(level,box,options,method)

def SpiralThingy(level,box,options):
	method = "SpiralThingy"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	MATERIAL = getBlockFromOptions(options,"Material:")
	FILLMATERIAL = getBlockFromOptions(options,"Fill Material:")
	(SLABID,SLABDATA) = getBlockFromOptions(options,"Slab Material:")
	
	# Start at the centre of the box, and at the top of the selection, 
	iteration = 1
	while iteration <= 2:
		x1=centreWidth
		y1=(float)(height-1)
		z1=centreDepth
		x=x1
		y=float(y1)
		z=z1
		xold = x
		yold = y
		zold = z
		pathLength = 0
		angle = pi/180
		while y > 0:
			halfY = (int)(y/2)
			print '%s' % (y)

			if iteration == 1:
				drawTriangle(level, box, options, (box.minx+x,box.miny+y,box.minz+z), (box.minx+xold,box.miny+y,box.minz+zold), (x1,y,z1), MATERIAL, FILLMATERIAL)
				for iterY in xrange(0,int(y)):
					setBlock(level,FILLMATERIAL,box.minx+x,box.miny+iterY,box.minz+z)
			else:
				data = SLABDATA
				print '%s %s' % (y,float(y)-int(y))
				if (float(y)-int(y)) >= 0.5:
					data = data+8
				drawLine(level,(SLABID,data),(box.minx+x,box.miny+y,box.minz+z),(box.minx+xold,box.miny+(int)(yold),box.minz+zold))
			pathLength = pathLength+1
			revolutions = float(pathLength/31.0)
			xold = x
			yold = y
			zold = z
			x = x1 + sin(angle*pathLength) * (revolutions)
			z = z1 + cos(angle*pathLength) * (revolutions)
			y = float(y1 - 1 - revolutions)
		iteration += 1

	FuncEnd(level,box,options,method)

	
	
def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	if options["Quick?"] == True:
		SpiralThingyQuick(level,box,options)	
	else:
		SpiralThingy(level,box,options)	

	SUCCESS = True
		
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
	
def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLine1(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	for px, py, pz in bresenham.bresenham((x,y,z),(x1,y1,z1)):
		setBlock(scratchpad,(blockID, blockData),px,py,pz)
	setBlock(scratchpad,(blockID, blockData),x1,y1,z1)
	
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

def drawLineConstrainedRandom(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), frequency ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)


	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)

	iter = 0
	while iter <= distance:
		if randint(0,99) < frequency:
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
		iter = iter+0.5 # slightly oversample because I lack faith.

def drawTriangle(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
	if materialFill != (0,0):
		# for each step along the 'base' draw a line from the apex
		dx = p3x - p2x
		dy = p3y - p2y
		dz = p3z - p2z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)
		
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
			
			iter = iter+0.5 # slightly oversample because I lack faith.
			drawLine(level, materialFill, (px, py, pz), (p1x, p1y, p1z) )
	
	
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )
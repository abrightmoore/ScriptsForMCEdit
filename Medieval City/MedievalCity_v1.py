# This filter is to create a Medieval style city
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
from random import Random # @Codewarrior0

inputs = (
		("MEDIEVAL CITY", "label"),
		("Quick render?", True),
		("Seed:", 42),
		("Fill Material:", alphaMaterials.BlockofQuartz),
		("Edge Material:", alphaMaterials.BlockofQuartz),
		("Floor Material:", alphaMaterials.BlockofQuartz),
		("Roof Slab Material:", alphaMaterials.BlockofQuartz),
		("Glass Material:", alphaMaterials.BlockofQuartz),
		("Max Iterations:", 10000),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def areaOfPolygon(points): # http://www.mathopenref.com/coordpolygonarea2.html
	area = 0
	xl = 0
	zl = 0
	for index in xrange(0,len(points)-2):
		(x1,y1) = points[index]
		(x,y) = points[(index+1)%len(points)]
		area = area + (x1+x) * (y1+y)
	area = area /2
	return area

def MedievalCity(level, box, options):
	method = "MEDIEVALCITY"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start	
	
	# Layout the city using a network of roads and plots. Honour the supplied selection box.
	# Prototype - draw roads and plots at low/quick detail. 
	random = Random(options["Seed:"])
	# a = random.random()
	# print '%s' % (a)
	
	# CityLayoutMap = MCSchematic((width,1,depth)) # This is a 2D map of the city elements using block types to mark the elements from an above view.
	CityLayout = [] # A collection of Polygons. Each Polygon is a collection of points defining the boundary of the shape
	entireBoxShape = ((0,0),(width,0),(width,depth),(0,depth))
#	print 'Area: %s' % (areaOfPolygon(entireBoxShape))
	
	CityLayout.append( ("Potential",entireBoxShape) ) # starting shape is the entire shape of the selection box
	counter = 100
	keepGoing = True # Main city layout loop
	while keepGoing == True:
		counter -= 1
		
		# find a free space
		(type,place) = CityLayout[randint(0,len(CityLayout)-1)]
		area = areaOfPolygon(place)
		print 'Area of %s is %s' % (type,area)
		
		if counter == 0:
			keepGoing = False
	
	
	
	
	
	
	
	
	
	
	FuncEnd(level,box,options,method) # Log end
	return True

def MedievalWallSection(box, options, fillMaterial, edgeMaterial, glassMaterial):
	method = "MedievalWallSection"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 

	# Wall
	drawRectangle(level, box, options,
					(box.minx,box.miny,box.minz+1),
					(box.maxx-1,box.miny,box.minz+1),
					(box.maxx-1,box.maxy-1,box.minz+1),
					(box.minx,box.maxy-1,box.minz+1),
					fillMaterial)
	# Edge around wall
	drawLine(level, edgeMaterial, (box.minx,box.miny,box.minz+1),(box.maxx-1,box.miny,box.minz+1))
	drawLine(level, edgeMaterial, (box.maxx-1,box.miny,box.minz+1),(box.maxx-1,box.maxy-1,box.minz+1))
	drawLine(level, edgeMaterial, (box.maxx-1,box.maxy-1,box.minz+1),(box.minx,box.maxy-1,box.minz+1))
	drawLine(level, edgeMaterial, (box.minx,box.maxy-1,box.minz+1),(box.minx,box.miny,box.minz+1))
	# Edge proper
	drawLine(level, edgeMaterial, (box.minx,box.miny,box.minz),(box.maxx-1,box.miny,box.minz))
	drawLine(level, edgeMaterial, (box.maxx-1,box.miny,box.minz),(box.maxx-1,box.maxy-1,box.minz))
	drawLine(level, edgeMaterial, (box.maxx-1,box.maxy-1,box.minz),(box.minx,box.maxy-1,box.minz))
	drawLine(level, edgeMaterial, (box.minx,box.maxy-1,box.minz),(box.minx,box.miny,box.minz))
	# Braces
	drawLine(level, edgeMaterial, (box.minx,box.miny,box.minz),(box.maxx-1,box.maxy-1,box.minz))
	drawLine(level, edgeMaterial, (box.minx,box.maxy-1,box.minz),(box.maxx-1,box.miny,box.minz))
	
	return level
	
def MedievalRoom(level, box, options):
	method = "MEDIEVALROOM"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start	
	b=range(4096); b.remove(0)

	# A room is floor, walls, one with door, some with Windows, roof, and interior dressing. Dimensions are the supplied box.
	getBlockFromOptions(options,"Floor Material:")
	# Floor
	drawRectangle(level, box, options,
					(box.minx+2,box.miny,box.minz+2),
					(box.maxx-3,box.miny,box.minz+2),
					(box.maxx-3,box.miny,box.maxz-3),
					(box.minx+2,box.miny,box.maxz-3),
					getBlockFromOptions(options,"Floor Material:"))
	
	# First wall
	wallBox = BoundingBox((0,0,0),(width,height,2)) 
	wallSchematic = MedievalWallSection(wallBox, options, getBlockFromOptions(options,"Fill Material:"), getBlockFromOptions(options,"Edge Material:"), getBlockFromOptions(options,"Glass Material:"))
	level.copyBlocksFrom(wallSchematic, wallBox, (box.minx,box.miny,box.minz),b)

	# Second wall
	wallBox2 = BoundingBox((0,0,0),(depth,height,2)) 
	wallSchematic2 = MedievalWallSection(wallBox2, options, getBlockFromOptions(options,"Fill Material:"), getBlockFromOptions(options,"Edge Material:"), getBlockFromOptions(options,"Glass Material:"))
	wallSchematic2.rotateLeft()
	r90BBox = BoundingBox((0,0,0),(2,height,depth))
	level.copyBlocksFrom(wallSchematic2, r90BBox, (box.minx,box.miny,box.minz),b)
	
	# Third wall
	wallSchematic.rotateLeft()
	wallSchematic.rotateLeft()
	level.copyBlocksFrom(wallSchematic, wallBox, (box.minx,box.miny,box.maxz-2),b)
	
	# Fourth wall
	wallSchematic2.rotateLeft()
	wallSchematic2.rotateLeft()
	level.copyBlocksFrom(wallSchematic2, r90BBox, (box.maxx-2,box.miny,box.minz),b)

	# Roof
#	for x in xrange(0,int(width/2)+1):
#		for z in xrange(0,int(depth/2)+1):
#			y = x
#			if z < y: y = z
#			(blockID,blockData) = getBlockFromOptions(options,"Roof Slab Material:")
#			if y%2 == 1: blockData += 8 # Upper slab
#			y = int(y/2)
#			if y >= height-1: y = height-1
#			setBlock(level, (blockID,blockData), x, y, z)
#			setBlock(level, (blockID,blockData), width-x-1, y, z)
#			setBlock(level, (blockID,blockData), x, y, depth-z-1)
#			setBlock(level, (blockID,blockData), width-x-1, y, depth-z-1)
	
	FuncEnd(level,box,options,method) # Log end
	return True
	
def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM MEDIEVALCITY"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	SUCCESS = MedievalRoom(level, box, options)
		
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
			
def distance( (x1,y1,z1), (x2,y2,z2) ):
	p = x1 * x2 + z1 * z2
	return sqrt( p + y1 * y2 )

def drawRectangle(level,box,options,p1,p2,p3,p4,material):
	drawTriangle(level, box, options, p1, p2, p3,material, material)
	drawTriangle(level, box, options, p1, p4, p3,material, material)
	
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
		
def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	#print 'ANALYSE %s %s %s' % (width, height, depth)

	minX = width
	minY = height
	minZ = depth
	maxX = 0
	maxY = 0
	maxZ = 0
	found = False
	
	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depth):
				if level.blockAt(iterX, iterY, iterZ) != 0:
					#print 'ANALYSING %s %s %s' % (iterX, iterY, iterZ)
					if iterX > maxX:
						maxX = iterX
					if iterY > maxY:
						maxY = iterY
					if iterZ > maxZ:
						maxZ = iterZ
				
					if iterX < minX:
						minX = iterX
					if iterY < minY:
						minY = iterY
					if iterZ < minZ:
						minZ = iterZ
						
					found = True

	#print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	#print '%s: Ended at %s' % (method, time.ctime())
	
	if found == False:
		return BoundingBox((0, 0, 0), (width, height, depth))	
	else:
		return BoundingBox((minX, 0, minZ), (maxX+1, maxY+1, maxZ+1))

def checkBoundingBoxIntersect(A, B):
	#print 'Checking BB A/B intersection '
	#printBoundingBox(A)
	#printBoundingBox(B)
	# Check for A completely to the left of B. https://github.com/mcedit/pymclevel/blob/master/box.py
	# http://www.toymaker.info/Games/html/3d_collisions.html
	if A.maxx < B.minx:
	    return False
	# Check for A to the right of B
	if A.minx > B.maxx:
	    return False
	# Check for A in front of B
	if A.maxz < B.minz:
	    return False
	# Check for A behind B
	if A.minz > B.maxz:
	    return False
	# Check for A above B
	if A.miny > B.maxy:
	    return False
	# Check for A below B
	if A.maxy < B.miny:
	   return False
	   
	# Collision has occurred
	#print 'Collision occurred'
	return True
	

# This filter creates WALLS with different materials you specify
# 
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob


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

inputs = (
	  ("WALLS", "label"),
	  ("Strut", alphaMaterials.Stone),
	  ("Lintel", alphaMaterials.StoneBricks),
	  ("Wall", alphaMaterials.Wood),
	  ("Wall Edge", alphaMaterials.Wood),
	  ("Window", alphaMaterials.Glass),
	  ("Floor", alphaMaterials.Cobblestone),
	  ("Roof", alphaMaterials.Stone),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt(x,y,z)
    if tempBlock == 0:
	setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
    	level.setBlockDataAt(x, y, z, data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, y):
    	setBlockIfEmpty(level, (block, data), x, iterY, z)
    	

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
			scratchpad.setBlockAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockID)
			scratchpad.setBlockDataAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.

def	copyBlocksFromDBG(level,schematic, A, cursorPosn):
	(x1,y1,z1,x2,y2,z2) = (A.minx,A.miny,A.minz,A.maxx,A.maxy,A.maxz)
	(width, height, depth) = getBoxSize(schematic.bounds)

	if x2 > width or y2 > height or z2 > depth:
		return False
	else:
		level.copyBlocksFrom(schematic, A, cursorPosn)
	return True
			
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
	

def findSurface(x, y, z, level, box, options):
	# Find a candidate surface
	iterY = 250
	miny = y
	foundy = y
	while iterY > miny:
		block = level.blockAt(x,iterY,z)
		if block != 0: # not AIR
			foundy = iterY
			iterY = miny # end search, block found was a legitimate candidate for the surface				
		iterY = iterY -1
	return foundy

def printBoundingBox(A):
	print 'BoundingBox %s %s %s %s %s %s' % (A.minx,A.miny,A.minz,A.maxx,A.maxy,A.maxz)


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

def retrieveSelectedSchematic(theFileName): # Load a schematic, analyse it (find the bounds) and return the schematic and bounding box
	# ... todo: Cache schematics so I don't need to analyse on each access
	method = "retrieveSelectedSchematic"
	print '%s: Started at %s' % (method, time.ctime())
	SHAPE = (32,32,32)
	print 'Loading schematic from file - %s' % (theFileName)
	charSchematic = MCSchematic(shape=SHAPE,filename=theFileName)
	print '%s: Ended at %s' % (method, time.ctime())
	return (charSchematic, analyse(charSchematic))

	
# ------------------------------- End utility methods ---------------------
	
def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Walls(level, box, options)		
	level.markDirtyBox(box)

# Filter script
	
def Walls(level, box, options):
	# CONSTANTS
	method = "WALLS"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIR = (0,0)

	MATERIAL_STRUT = (options["Strut"].ID, options["Strut"].blockData)
	MATERIAL_LINTEL = (options["Lintel"].ID, options["Lintel"].blockData)
	MATERIAL_WALL = (options["Wall"].ID, options["Wall"].blockData)
	MATERIAL_WALLEDGE = (options["Wall Edge"].ID, options["Wall Edge"].blockData)
	MATERIAL_WINDOW = (options["Window"].ID, options["Window"].blockData)
	MATERIAL_FLOOR = (options["Floor"].ID, options["Floor"].blockData)
	MATERIAL_ROOF = (options["Roof"].ID, options["Roof"].blockData)
	
	# WALL COMPONENT DIMENSIONS
	STRUT_WIDTH = randint(1,3)
	WINDOW_WIDTH = randint(2,width-4)
	WINDOW_HEIGHT = randint(2,height-4)
	
	# Draw the floor
	for iterX in xrange(STRUT_WIDTH, width-STRUT_WIDTH):
		for iterZ in xrange(0,depth):
			setBlock(level, MATERIAL_FLOOR, box.minx+iterX,box.miny,box.minz+iterZ)

	# Draw the upright struts
	for iterX in xrange(0,STRUT_WIDTH):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				setBlock(level, MATERIAL_STRUT, box.minx+iterX,box.miny+iterY,box.minz+iterZ)
				setBlock(level, MATERIAL_STRUT, box.minx+width-1-iterX,box.miny+iterY,box.minz+iterZ)
		
	# Draw the roof edge 
	for iterX in xrange(STRUT_WIDTH, width-STRUT_WIDTH):
		for iterZ in xrange(0,depth):
			setBlock(level, MATERIAL_ROOF, box.minx+iterX,box.miny+height-1,box.minz+iterZ)
			
	# Draw the wall sheet
	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			setBlock(level, MATERIAL_WALL, box.minx+iterX,box.miny+iterY,box.minz+1)
	
	# Draw the wall edge
	for iterY in xrange(0, height):
		setBlock(level, MATERIAL_WALLEDGE, box.minx+STRUT_WIDTH,box.miny+iterY,box.minz+1)
		setBlock(level, MATERIAL_WALLEDGE, box.minx+width-1-STRUT_WIDTH,box.miny+iterY,box.minz+1)
	
	# Draw the window
	WINDOW_STARTX = (int)((width-WINDOW_WIDTH)/2)
	WINDOW_STARTY = (int)((height-WINDOW_HEIGHT)/2)
	print '%s: WINDOW_STARTX / Y %s %s %s %s' % (method, WINDOW_STARTX, WINDOW_STARTY, WINDOW_WIDTH, WINDOW_HEIGHT)
	for iterX in xrange(WINDOW_STARTX, WINDOW_STARTX+WINDOW_WIDTH):
		for iterY in xrange(WINDOW_STARTY, WINDOW_STARTY+WINDOW_HEIGHT):
			setBlock(level, MATERIAL_WINDOW, box.minx+iterX,box.miny+iterY,box.minz+1)

	# Draw the lintel
	for iterX in xrange(0, width):
		setBlock(level, MATERIAL_LINTEL, box.minx+iterX,box.miny+height-1,box.minz+1)

			
	print '%s: Ended at %s' % (method, time.ctime())

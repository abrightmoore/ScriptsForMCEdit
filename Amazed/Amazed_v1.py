# This filter makes a 3D maze in your selection box
# Algorithm overview - depth first spanning tree, adapted to 3D by me: http://en.wikipedia.org/wiki/Maze_generation_algorithm
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
	  ("AMAZED", "label"),
  	  ("Material:", alphaMaterials.Cobblestone),
	  ("Cell Size:", 4),
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

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Amazed(level, box, options)		
	level.markDirtyBox(box)

def Amazed(level, box, options):
	# CONSTANTS
	method = "AMAZED"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIR = (0,0)
	NOTVISITED = 0
	VISITED = 1
	WALL = 0
	NOWALL = 1
	WALLSIZE = options["Cell Size:"]
	material = (options["Material:"].ID, options["Material:"].blockData)
	# END CONSTANTS

	cells = zeros((width,height,depth,7)) #
	
	Q = [] # traversed paths
	
	x = 0
	y = centreHeight
	z = centreDepth
	
	startCell = (x,y,z)
	
	logger = 0
	
	print '%s: Generating maze at %s, starting at %s %s %s' % (method, time.ctime(), x, y, z)
	keepGoing = True
	while keepGoing == True:
		logger = logger +1
		if logger%1000 == 0:
			print '%s: Cell %s %s %s' % (method, x, y, z)
			
		if cells[x,y,z,0] == NOTVISITED:
			cells[x,y,z,0] = VISITED
			Q.append( (x,y,z) )
			
		# Create an iterable list of neighbouring cells that have not yet been visited
		P = []
		for dP in xrange(-1,2):
			if dP != 0:
				d = x+dP
				if d > -1 and d < width:
					if cells[d,y,z,0] == NOTVISITED:
						P.append( (d,y,z,dP,0,0) )
				d = y+dP
				if d > -1 and d < height:
					if cells[x,d,z,0] == NOTVISITED:
						P.append( (x,d,z,0,dP,0) )
				d = z+dP
				if d > -1 and d < depth:
					if cells[x,y,d,0] == NOTVISITED:
						P.append( (x,y,d,0,0,dP) )
		
		Plen = len(P)
		if Plen > 0:
			print 'Choosing a neighbour'
			# Select a cell at random
			(x1,y1,z1,dx,dy,dz) = P[randint(0, Plen-1)]
			# Remove the wall between this cell and the neighbour
			if dx == -1:
				cells[x,y,z,1] = NOWALL
				cells[x1,y1,z1,2] = NOWALL
			elif dx == 1:
				cells[x,y,z,2] = NOWALL
				cells[x1,y1,z1,1] = NOWALL
			elif dy == -1:
				cells[x,y,z,3] = NOWALL
				cells[x1,y1,z1,4] = NOWALL
			elif dy == 1:
				cells[x,y,z,4] = NOWALL
				cells[x1,y1,z1,3] = NOWALL
			elif dz == -1:
				cells[x,y,z,5] = NOWALL
				cells[x1,y1,z1,6] = NOWALL
			elif dz == 1:
				cells[x,y,z,6] = NOWALL
				cells[x1,y1,z1,5] = NOWALL
			
			# Move along to process the neighbour
			x = x1
			y = y1
			z = z1
			# This is the next cell
		else: # Backtrack
			print 'Backtracking'
			(x1, y1, z1) = startCell
			if x == x1 and y == y1 and z == z1: #or len(Q) == 0: # We're at the start and there is nowhere else to go
				print 'Generation completed'
				keepGoing = False
			else: # Find me another cell
				print 'Stepping backwards'
				if len(Q) > 0:
					(x,y,z) = Q.pop()
					print 'Popped %s %s %s' % (x,y,z)
				else:
					print 'Pop not possible'
	
	print '%s: Rendering maze at %s' % (method, time.ctime())
	
	# Now, render unto the maze that which is Caeser's. Draw the walls.
	for iterX in xrange(0,width):
		for iterY in xrange(0,height):
			for iterZ in xrange(0,depth):
				logger = logger + 1
				if logger%1000 == 0:
					print 'Drawing cell %s %s %s' % (iterX, iterY, iterZ)
				if cells[iterX, iterY, iterZ, 1] == WALL:
					for iY in xrange(0,WALLSIZE):
						for iZ in xrange(0,WALLSIZE):
							setBlock(level, material, box.minx+(iterX*WALLSIZE),box.miny+(iterY*WALLSIZE)+iY,box.minz+(iterZ*WALLSIZE)+iZ)
				if cells[iterX, iterY, iterZ, 2] == WALL:
					for iY in xrange(0,WALLSIZE):
						for iZ in xrange(0,WALLSIZE):
							setBlock(level, material, box.minx+(iterX*WALLSIZE)+WALLSIZE-1,box.miny+(iterY*WALLSIZE)+iY,box.minz+(iterZ*WALLSIZE)+iZ)
				if cells[iterX, iterY, iterZ, 3] == WALL:
					for iX in xrange(0,WALLSIZE):
						for iZ in xrange(0,WALLSIZE):
							setBlock(level, material, box.minx+(iterX*WALLSIZE)+iX,box.miny+(iterY*WALLSIZE),box.minz+(iterZ*WALLSIZE)+iZ)
				if cells[iterX, iterY, iterZ, 4] == WALL:
					for iX in xrange(0,WALLSIZE):
						for iZ in xrange(0,WALLSIZE):
							setBlock(level, material, box.minx+(iterX*WALLSIZE)+iX,box.miny+(iterY*WALLSIZE)+WALLSIZE-1,box.minz+(iterZ*WALLSIZE)+iZ)
				if cells[iterX, iterY, iterZ, 5] == WALL:
					for iX in xrange(0,WALLSIZE):
						for iY in xrange(0,WALLSIZE):
							setBlock(level, material, box.minx+(iterX*WALLSIZE)+iX,box.miny+(iterY*WALLSIZE)+iY,box.minz+(iterZ*WALLSIZE))
				if cells[iterX, iterY, iterZ, 6] == WALL:
					for iX in xrange(0,WALLSIZE):
						for iY in xrange(0,WALLSIZE):
							setBlock(level, material, box.minx+(iterX*WALLSIZE)+iX,box.miny+(iterY*WALLSIZE)+iY,box.minz+(iterZ*WALLSIZE)+WALLSIZE-1)

	print '%s: Ended at %s' % (method, time.ctime())

def retrieveSelectedSchematic(theFileName): # Load a schematic, analyse it (find the bounds) and return the schematic and bounding box
	# ... todo: Cache schematics so I don't need to analyse on each access
	method = "retrieveSelectedSchematic"
	print '%s: Started at %s' % (method, time.ctime())
	SHAPE = (32,32,32)
	print 'Loading schematic from file - %s' % (theFileName)
	charSchematic = MCSchematic(shape=SHAPE,filename=theFileName)
	print '%s: Ended at %s' % (method, time.ctime())
	return (charSchematic, analyse(charSchematic))


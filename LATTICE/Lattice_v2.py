# This filter removes blocks leaving a frame-like landscape or object, with surfaces preserved.
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
	  ("Lattice", "label"),
	  ("Gap Size", 5),
	  ("Surface Only?", False),
  	  ("Honeycomb?", False),
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
	Lattice(level, box, options)		
	level.markDirtyBox(box)

def Lattice(level, box, options):
	# CONSTANTS
	method = "LATTICE"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIR = (0,0)
	GAPSIZE = options["Gap Size"]
	SURFACEONLY = options["Surface Only?"]
	HONEYCOMB = options["Honeycomb?"]
	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Mirror the blocks - in memory working read only copy
	maskSchematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Mirror the blocks - in memory mask.
	
	for iterY in xrange(1, height-1): # scan for all blocks that are adjacent to air
		print '%s: Locating surface blocks, step %s of %s' % (method, iterY-box.miny, height-2)
		for iterX in xrange(1, width-1):
			for iterZ in xrange(1, depth-1):
				temp = schematic.blockAt(iterX, iterY, iterZ)
				print 'Checking block %s at %s %s %s' % (temp, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				if temp != 0: # Found a block - check if it is a surface. Note all non-air is considered a block for surface checking.
					if schematic.blockAt(iterX-1, iterY, iterZ) == 0 or schematic.blockAt(iterX+1, iterY, iterZ) == 0 or schematic.blockAt(iterX, iterY-1, iterZ) == 0 or schematic.blockAt(iterX, iterY+1, iterZ) == 0 or schematic.blockAt(iterX, iterY, iterZ-1) == 0 or schematic.blockAt(iterX, iterY, iterZ+1) == 0 or schematic.blockAt(iterX-1, iterY-1, iterZ) == 0 or schematic.blockAt(iterX-1, iterY+1, iterZ) == 0 or schematic.blockAt(iterX-1, iterY, iterZ-1) == 0 or schematic.blockAt(iterX-1, iterY, iterZ+1) == 0 or schematic.blockAt(iterX+1, iterY-1, iterZ) == 0 or schematic.blockAt(iterX+1, iterY+1, iterZ) == 0 or schematic.blockAt(iterX+1, iterY, iterZ-1) == 0 or schematic.blockAt(iterX+1, iterY, iterZ+1) == 0 or schematic.blockAt(iterX, iterY-1, iterZ-1) == 0 or schematic.blockAt(iterX, iterY-1, iterZ+1) == 0 or schematic.blockAt(iterX, iterY+1, iterZ-1) == 0 or schematic.blockAt(iterX, iterY+1, iterZ+1) == 0:
							print 'Keeping surface block %s %s %s' % (box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					else:
						print 'Purging block %s %s %s' % (box.minx+iterX, box.miny+iterY, box.minz+iterZ)
						setBlock(maskSchematic, AIR, iterX, iterY, iterZ) # purge this block, it has no air around it and is therefore a surface

	# Out of the prior step there is a set of surface blocks defined in the mask set.
	# Now I need to purge all blocks NOT on the lattice and not part of the surface, keeping all others.
	# Then copy back into the world

	if SURFACEONLY == True:
		level.copyBlocksFrom(maskSchematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
	elif HONEYCOMB == True: # Lattice of blocks too!
		for iterY in xrange(0, height): # scan for all blocks that are adjacent to air
			print '%s: Purging blocks off the honeycomb, step %s of %s' % (method, iterY-box.miny, height-2)
			for iterX in xrange(0, width):
				for iterZ in xrange(0, depth):
					if maskSchematic.blockAt(iterX, iterY, iterZ) == 0 and not (iterX%GAPSIZE == 0 or iterY%GAPSIZE == 0 or iterZ%GAPSIZE == 0):
						setBlock(schematic, AIR, iterX, iterY, iterZ) # purge this block, it has no air around it and is therefore a surface
		level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
	else: # Lattice of blocks too!
		for iterY in xrange(0, height): # scan for all blocks that are adjacent to air
			print '%s: Purging blocks off the lattice, step %s of %s' % (method, iterY-box.miny, height-2)
			for iterX in xrange(0, width):
				for iterZ in xrange(0, depth):
					if not (maskSchematic.blockAt(iterX, iterY, iterZ) != 0 or ((iterX%GAPSIZE == 0 and iterY%GAPSIZE == 0 and iterZ%GAPSIZE != 0) or (iterX%GAPSIZE != 0 and iterY%GAPSIZE == 0 and iterZ%GAPSIZE == 0) or (iterX%GAPSIZE == 0 and iterY%GAPSIZE != 0 and iterZ%GAPSIZE == 0) or (iterX%GAPSIZE == 0 and iterY%GAPSIZE == 0 and iterZ%GAPSIZE == 0))):
						setBlock(schematic, AIR, iterX, iterY, iterZ) # purge this block, it has no air around it and is therefore a surface
		level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
					
	print '%s: Ended at %s' % (method, time.ctime())
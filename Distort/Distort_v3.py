# This filter calculates and deforms blocks in space by their proximity to a specific mass
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
	  ("Distort", "label"),
	  ("Unit Force", 100),
	  ("Force", ("Attract","Repel")),
	  ("Material", alphaMaterials.BlockofIron),
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
	Distort(level, box, options)		
	level.markDirtyBox(box)

def Distort(level, box, options):
	# CONSTANTS
	method = "DISTORT"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIR = (0,0)
	material = (options["Material"].ID, options["Material"].blockData)
	unitForce = options["Unit Force"]
	force = options["Force"]
	forceDirection = 1
	if force == "Repel":
		forceDirection = -1
	
	Q = [] # The list of force carrying blocks
	
	for iterY in xrange(box.miny, box.maxy): # scan for all blocks that are force-carrying
		print '%s: Locating force carrier blocks, step %s of %s' % (method, iterY-box.miny, height-2)
		for iterX in xrange(box.minx, box.maxx):
			for iterZ in xrange(box.minz, box.maxz):
				if (level.blockAt(iterX, iterY, iterZ),level.blockDataAt(iterX, iterY, iterZ)) == material: # Found a force carrier
					Q.append( (iterX, iterY, iterZ) )
					print '%s: found a force block at (%s %s %s)' % (method, iterX, iterY, iterZ)
	
	# S = zeros((width,height,depth))
	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Mirror the blocks
	
	for iterY in xrange(box.miny, box.maxy): # Construct a model of the forces at play on each block in space
		print '%s: Calculating force vectors, step %s of %s' % (method, iterY-box.miny, height-2)
		for iterX in xrange(box.minx, box.maxx):
			for iterZ in xrange(box.minz, box.maxz):
				tempBlock = (schematic.blockAt(iterX-box.minx, iterY-box.miny, iterZ-box.minz),schematic.blockDataAt(iterX-box.minx, iterY-box.miny, iterZ-box.minz))
				# print '%s: checking block at (%s %s %s)' % (method, iterX, iterY, iterZ)
				if tempBlock != AIR and tempBlock != material: # Found a force subject
					print '%s: found a block at (%s %s %s)' % (method, iterX, iterY, iterZ)
					# Here I need to calculate the force vectors at play attributed to each of the force carrying blocks...
					dx = (float)(0.0)
					dy = (float)(0.0)
					dz = (float)(0.0)
					fdx = (float)(0.0)
					fdy = (float)(0.0)
					fdz = (float)(0.0)
					for (px, py, pz) in Q:
						dx = (float)(px - iterX)
						dy = (float)(py - iterY)
						dz = (float)(pz - iterZ)
						distanceSquared = dx * dx + dz * dz + dy * dy
						force = (float)(0.0)
						if distanceSquared != 0:
							force = (float)(unitForce*forceDirection*1/distanceSquared)
							ratio = force / sqrt(distanceSquared) # The force vector is a fraction of the distances involved. What fraction lets us work out the force components
							fdx = fdx+(dx * ratio)
							fdy = fdy+(dy * ratio)
							fdz = fdz+(dz * ratio)

					print '%s: force at (%s %s %s) is %s. dx=%s dy=%s dz=%s' % (method, iterX, iterY, iterZ, force, fdx, fdy, fdz)
						
					#L = len(Q)
					#if L > 0: # average of the force vector components
					#	dx = (float)(dx/L)
					#	dy = (float)(dy/L)
					#	dz = (float)(dz/L)
					# S[iterX-box.minx,iterY-box.miny,iterZ-box.minz] = ( dx, dy, dz ) # Average distance vector at this point
	
					# force is inversely proportional to the square of the distance between the objects
						
					# Move tempBlock in the target zone
					setBlock(level, AIR, iterX, iterY, iterZ) # Clear the original block to air
					setBlock(level, tempBlock, iterX+(int)(fdx), iterY+(int)(fdy), iterZ+(int)(fdz)) # to fix - components of force vector
					# Move the block to a new target location
	print '%s: Ended at %s' % (method, time.ctime())
# This filter carves blocks out of the selection box, like an air brush in MCEdit
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
	  ("CARVER", "label"),
	  ("Shape", ("Sphere","SphereN","Cylinder (Vertical)","CylinderN (Vertical)","Boulder","Diagonal VerticalPP","Diagonal VerticalPN","Diagonal VerticalNN","Diagonal VerticalNP","Diagonal WidthPP","Diagonal WidthPN","Diagonal WidthNN","Diagonal WidthNP","Diagonal DepthPP","Diagonal DepthPN","Diagonal DepthNN","Diagonal DepthNP","CornerPPP","CornerPPN","CornerPNP","CornerPNN","CornerNPP","CornerNPN","CornerNNP","CornerNNN")), #
	  ("Cladding", alphaMaterials.Air),
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
	Carver(level, box, options)		
	level.markDirtyBox(box)

def Carver(level, box, options):
	# CONSTANTS
	method = "Carver"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIR = (0,0)

	POSTSHAPE = options["Shape"]
	CLADDING = (options["Cladding"].ID, options["Cladding"].blockData)
	
	# END CONSTANTS

	displaycounter = 0
	if POSTSHAPE == "Cylinder (Vertical)": # Trim away the exterior
		print 'Carving the selection into a cylinder.'
		rD = centreWidth
		if centreDepth < rD:
			rD = centreDepth
		for iterY in xrange(0,height):
			displaycounter = displaycounter + 1
			if displaycounter%1 == 0:
				print 'Cladding %s of %s' % (iterY, height+1)
			for iterZ in xrange(0,depth):
				for iterX in xrange(0,width):
					iz = iterZ - rD
					ix = iterX - rD
					pd = (int)(sqrt(ix*ix + iz*iz))
					# print '%s %s' % (pd,rD)
					if pd == (rD-1):
						setBlock(level, CLADDING, box.minx+iterX,box.miny+iterY,box.minz+iterZ)
					elif pd >= rD:
						setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	if POSTSHAPE == "CylinderN (Vertical)": # Trim away the exterior
		print 'Carving the selection into a cylinder-.'
		rD = centreWidth
		if centreDepth < rD:
			rD = centreDepth
		for iterY in xrange(0,height):
			displaycounter = displaycounter + 1
			if displaycounter%1 == 0:
				print 'Cladding %s of %s' % (iterY, height+1)
			for iterZ in xrange(0,depth):
				for iterX in xrange(0,width):
					iz = iterZ - rD
					ix = iterX - rD
					pd = (int)(sqrt(ix*ix + iz*iz))
					# print '%s %s' % (pd,rD)
					if pd == (rD+1):
						setBlock(level, CLADDING, box.minx+iterX,box.miny+iterY,box.minz+iterZ)
					elif pd <= rD+1:
						setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)
						
						
	elif POSTSHAPE == "Sphere": # Carve out the core
		print 'Carving the selection into a sphere.'
		rD = centreWidth
		if centreDepth < rD:
			rD = centreDepth
		if centreHeight < rD:
			rD = centreHeight
		for iterY in xrange(0,height):
			displaycounter = displaycounter + 1
			if displaycounter%100 == 0:
				print 'Cladding %s of %s' % (iterY, height+1)
			for iterZ in xrange(0,depth):
				for iterX in xrange(0,width):
					dX = iterX - rD
					dZ = iterZ - rD
					dY = iterY - rD
					pd = (int)(sqrt(dX*dX + dZ*dZ + dY*dY))
					
					if pd == rD-1:
						setBlock(level, CLADDING, box.minx+iterX,box.miny+iterY,box.minz+iterZ)
					elif pd > rD-1:
						setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "SphereN": # Carve out the core
		print 'Carving the selection into a sphere-.'
		rD = centreWidth
		if centreDepth < rD:
			rD = centreDepth
		if centreHeight < rD:
			rD = centreHeight
		for iterY in xrange(0,height):
			displaycounter = displaycounter + 1
			if displaycounter%100 == 0:
				print 'Cladding %s of %s' % (iterY, height+1)
			for iterZ in xrange(0,depth):
				for iterX in xrange(0,width):
					dX = iterX - rD
					dZ = iterZ - rD
					dY = iterY - rD
					pd = (int)(sqrt(dX*dX + dZ*dZ + dY*dY))
					
					if pd == rD-1:
						setBlock(level, CLADDING, box.minx+iterX,box.miny+iterY,box.minz+iterZ)
					elif pd < rD-1:
						setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)
						
	elif POSTSHAPE == "Boulder":
		Boulder(level, box, options)

	elif POSTSHAPE == "Diagonal VerticalPP":
		slope = (float)((float)(depth)/(float)(width))
		for iterX in xrange(0,width):
			for iterZ in xrange(0,depth):
				if (float)(iterX) == 0.0 or (float)(iterZ)/(float)(iterX) > slope:
					for iterY in xrange(0,height):
						setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "Diagonal VerticalPN":
		slope = (float)((float)(depth)/(float)(width))
		for iterX in xrange(0,width):
			for iterZ in xrange(0,depth):
				if (float)(iterX) != 0.0:
					if (float)(iterZ)/(float)(iterX) <= slope:
						for iterY in xrange(0,height):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "Diagonal VerticalNP":
		slope = -1.0*((float)(depth)/(float)(width))
		print '%s: Slope %s' % (method, slope)
		for iterX in xrange(0,width):
			for iterZ in xrange(0,depth):
				if (float)(iterX) != 0.0:
					if -1.0*(float)(depth-iterZ)/(float)(iterX) > slope:
						for iterY in xrange(0,height):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "Diagonal VerticalNN":
		slope = -1.0*(float)(depth)/(float)(width)
		for iterX in xrange(0,width):
			for iterZ in xrange(0,depth):
				if (float)(iterX) == 0.0 or -1.0*((float)(depth)-(float)(iterZ))/(float)(iterX) <= slope:
					for iterY in xrange(0,height):
						setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

						
	elif POSTSHAPE == "Diagonal WidthPN":
		slope = (float)((float)(height)/(float)(width))
		for iterX in xrange(0,width):
			for iterY in xrange(0,height):
				if (float)(iterX) != 0.0:
					if (float)((float)(iterY)/(float)(iterX)) <= slope:
						for iterZ in xrange(0,depth):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "Diagonal WidthPP":
		slope = (float)((float)(height)/(float)(width))
		for iterX in xrange(0,width):
			for iterY in xrange(0,height):
				if (float)(iterX) == 0.0 or (float)((float)(iterY)/(float)(iterX)) > slope:
						for iterZ in xrange(0,depth):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "Diagonal WidthNP":
		slope = -1.0*(float)((float)(height)/(float)(width))
		for iterX in xrange(0,width):
			for iterY in xrange(0,height):
				if (float)(iterX) != 0.0:
					if -1.0*(float)((float)((float)(height)-(float)(iterY))/(float)(iterX)) <= slope:
						for iterZ in xrange(0,depth):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "Diagonal WidthNN":
		slope = -1.0*(float)((float)(height)/(float)(width))
		for iterX in xrange(0,width):
			for iterY in xrange(0,height):
				if (float)(iterX) != 0.0: 
					if -1.0*(float)((float)((float)(height)-(float)(iterY))/(float)(iterX)) > slope:
						for iterZ in xrange(0,depth):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

							
	elif POSTSHAPE == "Diagonal DepthPP":
		slope = (float)((float)(height)/(float)(depth))
		for iterZ in xrange(0,depth):
			for iterY in xrange(0,height):
				if (float)(iterZ) == 0.0 or (float)((float)(iterY)/(float)(iterZ)) > slope:
						for iterX in xrange(0,width):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "Diagonal DepthPN":
		slope = (float)((float)(height)/(float)(depth))
		for iterZ in xrange(0,depth):
			for iterY in xrange(0,height):
				if (float)(iterZ) != 0.0:
					if (float)((float)(iterY)/(float)(iterZ)) <= slope:
						for iterX in xrange(0,width):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "Diagonal DepthNN":
		slope = -1.0*(float)((float)(height)/(float)(depth))
		for iterZ in xrange(0,depth):
			for iterY in xrange(0,height):
				if (float)(iterZ) != 0.0:
					if -1.0*(float)((float)(height)-(float)(iterY))/(float)(iterZ) > slope:
						for iterX in xrange(0,width):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)
							
	elif POSTSHAPE == "Diagonal DepthNP":
		slope = -1.0*(float)((float)(height)/(float)(depth))
		for iterZ in xrange(0,depth):
			for iterY in xrange(0,height):
				if (float)(iterZ) != 0.0:
					if -1.0*(float)((float)(height)-(float)(iterY))/(float)(iterZ) <= slope:
						for iterX in xrange(0,width):
							setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

# ------------
	elif POSTSHAPE == "CornerPPP":
		widthP = width
		depthP = depth
		heightP = height
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "CornerPPN":
		widthP = width
		depthP = depth
		heightP = height
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					setBlock(level, AIR, box.minx+iterX,box.miny+iterY,box.minz+depth-1-iterZ)

	elif POSTSHAPE == "CornerPNP":
		widthP = width
		depthP = depth
		heightP = height
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					setBlock(level, AIR, box.minx+iterX,box.miny+height-1-iterY,box.minz+iterZ)

	elif POSTSHAPE == "CornerPNN":
		widthP = width
		depthP = depth
		heightP = height
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					setBlock(level, AIR, box.minx+iterX,box.miny+height-1-iterY,box.minz+depth-1-iterZ)

	elif POSTSHAPE == "CornerNPP":
		widthP = width
		depthP = depth
		heightP = height
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					setBlock(level, AIR, box.minx+width-1-iterX,box.miny+iterY,box.minz+iterZ)

	elif POSTSHAPE == "CornerNPN":
		widthP = width
		depthP = depth
		heightP = height
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					setBlock(level, AIR, box.minx+width-1-iterX,box.miny+iterY,box.minz+depth-1-iterZ)

	elif POSTSHAPE == "CornerNNP":
		widthP = width
		depthP = depth
		heightP = height
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					setBlock(level, AIR, box.minx+width-1-iterX,box.miny+height-1-iterY,box.minz+iterZ)

	elif POSTSHAPE == "CornerNNN":
		widthP = width
		depthP = depth
		heightP = height
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					setBlock(level, AIR, box.minx+width-1-iterX,box.miny+height-1-iterY,box.minz+depth-1-iterZ)
							
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

def Boulder(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "BOULDER"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	destY = 127
	destX = 0
	destZ = 0
	# END CONSTANTS

	boulder = zeros( (width, height, depth) )

	# choose three points on the edges of the box - defines a plane. Mark the blocks to delete from this corner

	numIterations = randint(1,4)

	for iters in xrange(0, numIterations):
		# Corners
		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[iterX][iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[iterX][height-1-iterY][iterZ] = 1 # denotes an air block	


		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[iterX][height-1-iterY][depth-1-iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[width-1-iterX][iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[width-1-iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[width-1-iterX][height-1-iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[width-1-iterX][height-1-iterY][depth-1-iterZ] = 1 # denotes an air block	

		# long vertical edges
		widthP = randint(1, centreWidth)
		depthP = randint(1, centreDepth)
		for iterY in xrange(0, height):
			for iterX in xrange(0, widthP):
				depthHere = depthP - (iterX*depthP/widthP)
				for iterZ in xrange(0, (int)(depthHere)):
					boulder[iterX][iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, centreWidth)
		depthP = randint(1, centreDepth)
		for iterY in xrange(0, height):
			for iterX in xrange(0, widthP):
				depthHere = depthP - (iterX*depthP/widthP)
				for iterZ in xrange(0, (int)(depthHere)):
					boulder[width-1-iterX][iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, centreWidth)
		depthP = randint(1, centreDepth)
		for iterY in xrange(0, height):
			for iterX in xrange(0, widthP):
				depthHere = depthP - (iterX*depthP/widthP)
				for iterZ in xrange(0, (int)(depthHere)):
					boulder[iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		widthP = randint(1, centreWidth)
		depthP = randint(1, centreDepth)
		for iterY in xrange(0, height):
			for iterX in xrange(0, widthP):
				depthHere = depthP - (iterX*depthP/widthP)
				for iterZ in xrange(0, (int)(depthHere)):
					boulder[width-1-iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		# long horizontal edges
		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][height-1-iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][height-1-iterY][depth-1-iterZ] = 1 # denotes an air block	


		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, depth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, depth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][height-1-iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, depth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[width-1-iterX][iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, depth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[width-1-iterX][height-1-iterY][iterZ] = 1 # denotes an air block	
	
	
	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				if boulder[iterX][iterY][iterZ] == 1:
					setBlock(level, (0,0), box.minx+iterX, box.miny+iterY, box.minz+iterZ)
	
					
	print '%s: Ended at %s' % (method, time.ctime())
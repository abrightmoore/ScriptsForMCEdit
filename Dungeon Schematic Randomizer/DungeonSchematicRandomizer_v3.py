# This filter randomly places a schematic in the map "underground" except for a bit at the top, which isn't
# Requested by /u/StezzerLolz
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
	  ("Dungeon Schematic Randomizer", "label"),
	  ("Approx. Number of Tiles", 50),
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

def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	print 'ANALYSE %s %s %s' % (width, height, depth)

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

	print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	print '%s: Ended at %s' % (method, time.ctime())
	
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
	print 'Checking BB A/B intersection '
	printBoundingBox(A)
	printBoundingBox(B)
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
	print 'Collision occurred'
	return True

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	dungeonSchematicRandomizer(level, box, options)		
	level.markDirtyBox(box)

def dungeonSchematicRandomizer(level, box, options):
	# CONSTANTS
	method = "DungeonSchematicRandomizer"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	TILELIMIT = options["Approx. Number of Tiles"]
	# END CONSTANTS

	DUNGEONQ = []

	# Prefill a list of schematic file names which we will choose from later on
	StartSchematicFiles = glob.glob("filters/DungeonSchematics/Start/*.schematic")
	for fileName in StartSchematicFiles:
		print fileName
	print 'Found %s start schematic files' % (len(StartSchematicFiles))

	print 'Scanning available schematics...'
	EncounterSchematicFiles = glob.glob("filters/DungeonSchematics/*.schematic")
	for fileName in EncounterSchematicFiles:
		print fileName
	print 'Found %s dungeon schematic files' % (len(EncounterSchematicFiles))
	# End cached file names

	# Choose start block
	x = randint(0, width) + box.minx
	z = randint(0, depth) + box.minz
	y = 0
	y = findSurface(x, y, z, level, box, options) # find a block on the top of the map
	STARTY = y-8
	chosenSchematic = randint(0,len(StartSchematicFiles)) % len(StartSchematicFiles)
	(schematicNext , bbLast) = retrieveSelectedSchematic(StartSchematicFiles[chosenSchematic])
	
	cursorPosn = (x, y, z)
	level.copyBlocksFrom(schematicNext, bbLast, cursorPosn) # blit schematic in
	print 'bbLast'
	printBoundingBox(bbLast)
	B = BoundingBox( (x+bbLast.minx+1,y+bbLast.miny+1,z+bbLast.minz+1), (bbLast.maxx-1,bbLast.maxy-1,bbLast.maxz-1)  )
	print 'B'
	printBoundingBox(B)
	DUNGEONQ.append( B ) # Starter bounding box

	direction = 0 # down. 1,2,3,4 is N,E,S,W. 5 is up,
	
	counter = 10 + TILELIMIT+randint(0,TILELIMIT)# This many 'rooms' off the entrance
	
	# Loop until finished
	while counter > 0:
		chosenSchematic = randint(0,len(EncounterSchematicFiles)) % len(EncounterSchematicFiles)
		bbNext = BoundingBox((0,0,0),(0,0,0)) # Dummy assignment to clear out references
		(schematicNext , bbNext) = retrieveSelectedSchematic(EncounterSchematicFiles[chosenSchematic])
		centreXSchematic = (int)(bbNext.width / 2) # Centre of the floor
		centreZSchematic = (int)(bbNext.length / 2) # Centre of the floor
		centreYSchematic = (int)(bbNext.height / 2) # Centre of the height
		print 'bbLast:'
		printBoundingBox(bbLast)
		print 'bbNext:'
		printBoundingBox(bbNext)
		(sx, sy, sz) = (x, y, z) # last blit coords
				
		# based on the direction, the start posn is shifted and then the schematic is placed.
		placedATile = False
		
		if direction == 0: # Down. New position is in line with the centre of the floor, offset by the height of the new schematic
			x = sx+(int)(bbLast.width / 2)-centreXSchematic # Centre of the floor
			z = sz+(int)(bbLast.length / 2)-centreZSchematic
			y = sy-bbNext.height
			cursorPosn = (x, y, z)		

			A = BoundingBox((x+bbNext.minx+1,y+bbNext.miny+1,z+bbNext.minz+1), (bbNext.maxx-1,bbNext.maxy-1,bbNext.maxz-1) )
			result = False
			for B in DUNGEONQ:
				if checkBoundingBoxIntersect(A, B) == True:
					result = True
			if result == False and y > 8:
				level.copyBlocksFrom(schematicNext, bbNext, cursorPosn) # blit schematic in
				DUNGEONQ.append(A)
				placedATile = True
			else:
				d1 = 0
				d2 = randint(0,5)
				direction = d1 + d2 # 1 to 5, prefer 1,2,3,4
		
		if direction == 1: # North
			x = sx+(int)(bbLast.width / 2)-centreXSchematic # Centre of the floor
			z = sz+bbLast.length
			y = sy
			cursorPosn = (x, y, z)		

			A = BoundingBox((x+bbNext.minx+1,y+bbNext.miny+1,z+bbNext.minz+1), (bbNext.maxx-1,bbNext.maxy-1,bbNext.maxz-1) )
			print 'BB A:'
			printBoundingBox(A)
			result = False
			for B in DUNGEONQ:
				if checkBoundingBoxIntersect(A, B) == True:
					result = True
			if result == False:
				level.copyBlocksFrom(schematicNext, bbNext, cursorPosn) # blit schematic in
				DUNGEONQ.append(A)
				placedATile = True
			else:
				d1 = 0
				d2 = randint(0,5)
				direction = d1+d2 # 2 to 5, prefer 2,3,4

		if direction == 2: # East
			x = sx+bbLast.width # Centre of the floor
			z = sz+(int)(bbLast.length/2)-centreZSchematic
			y = sy
			cursorPosn = (x, y, z)		
			A = BoundingBox((x+bbNext.minx+1,y+bbNext.miny+1,z+bbNext.minz+1), (bbNext.maxx-1,bbNext.maxy-1,bbNext.maxz-1) )
			result = False
			for B in DUNGEONQ:
				if checkBoundingBoxIntersect(A, B) == True:
					result = True
			if result == False:
				level.copyBlocksFrom(schematicNext, bbNext, cursorPosn) # blit schematic in
				DUNGEONQ.append(A)
				placedATile = True
			else:
				d1 = 0
				d2 = randint(0,5)
				direction = d1 + d2 # 1 to 5, prefer 1,2,3,4
		
		if direction == 3: # South
			x = sx+(int)(bbLast.width / 2)-centreXSchematic # Centre of the floor
			z = sz-bbNext.length
			y = sy
			cursorPosn = (x, y, z)		
			A = BoundingBox((x+bbNext.minx+1,y+bbNext.miny+1,z+bbNext.minz+1), (bbNext.maxx-1,bbNext.maxy-1,bbNext.maxz-1) )
			result = False
			for B in DUNGEONQ:
				if checkBoundingBoxIntersect(A, B) == True:
					result = True
			if result == False:
				level.copyBlocksFrom(schematicNext, bbNext, cursorPosn) # blit schematic in
				DUNGEONQ.append(A)
				placedATile = True
			else:
				d1 = 0
				d2 = randint(0,5)
				direction = d1 + d2 # 1 to 5, prefer 1,2,3,4

		if direction == 4: # West
			x = sx-bbNext.width # Centre of the floor
			z = sz+(int)(bbLast.length/2)-centreZSchematic
			y = sy
			cursorPosn = (x, y, z)		
			A = BoundingBox((x+bbNext.minx+1,y+bbNext.miny+1,z+bbNext.minz+1), (bbNext.maxx-1,bbNext.maxy-1,bbNext.maxz-1) )
			result = False
			for B in DUNGEONQ:
				if checkBoundingBoxIntersect(A, B) == True:
					result = True
			if result == False:
				level.copyBlocksFrom(schematicNext, bbNext, cursorPosn) # blit schematic in
				DUNGEONQ.append(A)
				placedATile = True
			else:
				d1 = 0
				d2 = randint(0,5)
				direction = d1 + d2 # 1 to 5, prefer 1,2,3,4
						
		if direction == 5: # Up
			x = sx+(int)(bbLast.width / 2)-centreXSchematic # Centre of the floor
			z = sz+(int)(bbLast.length / 2)-centreZSchematic
			y = sy+bbLast.height
			cursorPosn = (x, y, z)		
			# A = BoundingBox((x+bbNext.minx+1,y+bbNext.miny+1,z+bbNext.minz+1), (x+bbNext.maxx-1,y+bbNext.maxy-1,z+bbNext.maxz-1) )
			A = BoundingBox((x+bbNext.minx+1,y+bbNext.miny+1,z+bbNext.minz+1), (bbNext.maxx-1,bbNext.maxy-1,bbNext.maxz-1) )
			result = False
			for B in DUNGEONQ:
				if checkBoundingBoxIntersect(A, B) == True:
					result = True
			if result == False and y <= STARTY:
				level.copyBlocksFrom(schematicNext, bbNext, cursorPosn) # blit schematic in
				DUNGEONQ.append(A)
				placedATile = True

		# Roll two dice	
		d1 = randint(0,5)
		d2 = 0
		direction = d1 + d2 # 0 to 5, prefer 1,2,3,4
		print 'Placed a tile = %s' % (placedATile)
		print 'Direction chosen = %s'% (direction)
		
		if placedATile == True:		
			bbLast = bbNext # Preserve prior selection bounding box
		else:
			x = sx # roll back
			y = sy
			z = sz
		
		counter = counter - 1
			
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

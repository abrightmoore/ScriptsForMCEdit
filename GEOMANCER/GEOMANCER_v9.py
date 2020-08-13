# This filter lets you manipulate the land within the selection box
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)
# http://www.planetminecraft.com/mod/geomancer---an-mcedit-filter-for-landscape-manipulation/

import time # for timing
import pymclevel
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials

inputs = (
	  ("GEOMANCER", "label"),
	    ("Operation", (
	    		    "Yellow Brick Road",
	    		    "Rainbow Road",
	    		    "Mt Ring",
	    		    "Mt Range",
	    		    "Mt",
	    		    "Jaggedy Mountain",
	    		    "Mount",
	    		    "Spire",
	    		    "Tower",
	    		    "Conamid",
	    		    "Gully",
	    		    "Boulder",
	    		    "Farm Maker",
			    "Flyland",
			    "Gash",
	    		    "Mound",
	    		    "Butte",
	    		    "Raise",
	    		    "Subside",
			    "Rainbow",
			    "Foam",
			    "Hollow",
			    "Zipper Canyon",
  		    )),
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

def findMaxAbsHeight(level, box):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "GEOMANCER - findMaxAbsoluteHeight"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS

	currentMaxHeight = 0
	for iterY in xrange(1,height-1):
		testHeight = box.maxy-iterY # scanning top down
		if testHeight > currentMaxHeight:
			for iterX in xrange(0,width):
				for iterZ in xrange(0,depth):
					if level.blockAt( box.minx + iterX, box.maxy-iterY, box.minz+iterZ) != AIRBLOCK:
						currentMaxHeight = testHeight
						# stop searching, we've found the top-most block in the selection area
						iterX = width 
						iterZ = depth
						iterY = height-1					
	print '%s: Ended at %s, returning %s' % (method, time.ctime(), currentMaxHeight)
	return currentMaxHeight

def drawJaggedyPath(level, box, options, DEM):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Draw Jeggedy Path"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS
	
	# Draw a jaggedy path

	directionX = 0
	directionZ = 0
	xload = 0
	zload = 0
	posX = 0
	posZ = 0

	if width > depth:
		directionX = 1
		posX = 0
		posZ = (int)(depth/2) #randint(1,depth)
	else:
		directionZ = 1
		posX = (int)(width/2) #randint(1,width)
		posZ = 0

	while posX < (width-1) and posZ < (depth-1):
		# wander
		posX = posX + directionX # guided step forward
		posZ = posZ + directionZ

		if xload > 0:
			posX = posX + 1
			xload = xload -1
		elif xload < 0:
			posX = posX - 1
			xload = xload +1
		elif zload > 0:
			posZ = posZ + 1
			zload = zload -1
		elif zload < 0:
			posZ = posZ - 1
			zload = zload +1
		else:
			posX = posX + (randint(0,2)-1) * directionZ # clever clogs way of adjusting the position perpendicular to the direction of travel
			posZ = posZ + (randint(0,2)-1) * directionX
			if xload == 0 and randint(0,5) == 3:
				xload = (randint(0,(int)(width/6))-(int)(width/12))*directionZ
			if zload == 0 and randint(0,5) == 3:
				zload = (randint(0,(int)(depth/6))-(int)(depth/12))*directionX

		if directionX == 1: # bounds check
			if posZ >= (depth-1):
				posZ = depth-2
				zload = -3
			elif posZ <= 0:
				posZ = 1
				zload = 3

		elif directionZ == 1:
			if posX >= (width-1):
				posX = width-2
				xload = -3
			elif posX <= 0:
				posX = 1
				xload = 3
		DEM[posX, posZ] = DEM[posX, posZ]+1
	return (DEM, directionX, directionZ)

def drawCircularPath(level, box, options, DEM):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Draw Circular Path"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS
	
	# Draw a circular path - suggested by Bhima

	directionX = 0
	directionZ = 0
	xload = 0
	zload = 0
	posX = 0
	posZ = 0

	if width > depth:
		directionX = 1
	else:
		directionZ = 1

	distance = centreWidth / 3
	r = (width-2*distance)/2
	for iterX in xrange(distance, (int)(width-distance)):
		pZ = sqrt(r*r - (centreWidth-abs(iterX))*(centreWidth-abs(iterX)))
		DEM[iterX, (int)(centreDepth+pZ)] = DEM[iterX, (int)(centreDepth+pZ)]+1
		DEM[iterX, (int)(centreDepth-pZ)] = DEM[iterX, (int)(centreDepth-pZ)]+1

	distance = centreWidth / 4
	r = (width-2*distance)/2
	for iterX in xrange(distance, (int)(width-distance)):
		pZ = sqrt(r*r - (centreWidth-abs(iterX))*(centreWidth-abs(iterX)))
		DEM[iterX, (int)(centreDepth+pZ)] = DEM[iterX, (int)(centreDepth+pZ)]+1
		DEM[iterX, (int)(centreDepth-pZ)] = DEM[iterX, (int)(centreDepth-pZ)]+1


	return (DEM, directionX, directionZ)



def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	
	method = options["Operation"]
	
	if method == "Raise":
		Raise(level, box, options)
	elif method == "Yellow Brick Road":
			yellowBrickRoad(level, box, options, colours = [ 4, 4, 4, 4, 4 ])
	elif method == "Rainbow Road":
			yellowBrickRoad(level, box, options, colours = [ 14, 14, 1, 1, 4, 4, 5, 5, 3, 3, 11, 11, 10, 10 ])
	elif method == "Mt Ring":
			MtRing(level, box, options)
	elif method == "Mt Range":
			MtRange(level, box, options)
	elif method == "Jaggedy Mountain":
			Mt1(level, box, options)
	elif method == "Mt":
			Mt(level, box, options)
	elif method == "Conamid":
			Conamid(level, box, options)
#	elif method == "Range":
#		Range(level, box, options)
	elif method == "Gully":
		Gully(level, box, options)
	elif method == "Zipper Canyon":
		ZipperCanyon(level, box, options)
	elif method == "Mound":
		Mound(level, box, options)
	elif method == "Boulder":
		Boulder(level, box, options)
	elif method == "Subside":
		Subside(level, box, options)
	elif method == "Farm Maker":
		Voronoi(level, box, options)
	elif method == "Rainbow":
		Rainbow(level, box, options)
	elif method == "Hollow":
		Hollow(level, box, options)
	elif method == "Gash":
		Gash(level, box, options)
	elif method == "Foam":
		Foam(level, box, options)
	elif method == "Flyland":
		Flyland(level, box, options)
	elif method == "Spire":
		Mountain(level, box, options, [ (8,1), (6,2), (3,3), (2,6), (1,8)]) # OK - size of box matters.
	elif method == "Mount":
		# Mountain(level, box, options, [ (6,1), (5,2), (4,3), (3,3), (2,4), (1,5)])
		Mountain(level, box, options, [ (12,1), (11,1), (10,1), (9,1), (8,1), (7,1), (6,1), (5,1), (4,1), (3,1), (2,1), (1,1)])
	elif method == "Butte":
		#Mountain(level, box, options, [ (7,1), (6,2), (1,3)]) # OK 
		#Mountain(level, box, options, [ (6,1), (5,1), (4,1), (3,2), (2,2), (1,3)])
		Mountain(level, box, options, [ (12,1), (11,1.1), (10,1.2), (9,1.3), (8,1.4), (7,1.5), (6,1.6), (5,1.7), (4,1.8), (3,1.9), (2,2), (1,2.1)])
	elif method == "Tower":
		Mountain(level, box, options, [ (2,1),(1,1)])
		
	level.markDirtyBox(box)


def yellowBrickRoad(level, box, options, colours):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "YellowBrickRoad"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS
	material = (41,0) # Gold!
	duplicates = 0

	roadWidth = len(colours)

	print '%s: Rendering the Road into the world at %s' % (method, time.ctime())

	for iter in xrange(0,roadWidth):
		phaseOffset = 0 #(float)(pi/1440*(float)(iter))
		scale = 0.5
		iterX = 0
		iterZ = 0
		lastX = -99999
		lastZ = -99999
		steps = 0
		angleSize = pi/1440
		# Spiral out from the centre
		while (centreWidth+iterX) < width and (centreWidth+iterX) >= 0 and (centreDepth+iterZ) >=0 and (centreDepth+iterZ) < depth:
			#if ((int)(iterX) == (int)(lastX)) and ((int)(iterZ) == (int)(lastZ)): # Optimise writes to the world
			#	duplicates = duplicates+1
			#else:
			setBlock(level, (35,colours[iter]), (int)(box.minx+centreWidth+iterX), box.miny, (int)(box.minz+centreDepth+iterZ)) 
			steps = steps+angleSize
			lastX = iterX
			lastZ = iterZ
			iterX = steps*cos(steps)*scale
			iterZ = steps*sin(steps)*scale
			scale=scale*(1.0001+iter*(0.000001))

	for iter in xrange(0,roadWidth):
		phaseOffset = pi #(float)(pi/1440*(float)(iter))
		scale = 0.5
		iterX = 0
		iterZ = 0
		lastX = -99999
		lastZ = -99999
		steps = 0
		angleSize = pi/1440
		# Spiral out from the centre
		while (centreWidth+iterX) < width and (centreWidth+iterX) >= 0 and (centreDepth+iterZ) >=0 and (centreDepth+iterZ) < depth:
			#if ((int)(iterX) == (int)(lastX)) and ((int)(iterZ) == (int)(lastZ)): # Optimise writes to the world
			#	duplicates = duplicates+1
			#else:
			setBlock(level, (35,colours[iter]), (int)(box.minx+centreWidth+iterX), box.miny, (int)(box.minz+centreDepth+iterZ)) 
			steps = steps+angleSize
			lastX = iterX
			lastZ = iterZ
			iterX = steps*cos(phaseOffset+steps)*scale
			iterZ = steps*sin(phaseOffset+steps)*scale
			scale=scale*(1.0001+iter*(0.000001))

		
	print '%s: Ended at %s with %s duplicates suppressed' % (method, time.ctime(), duplicates)


def spiral(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Spiral"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS
	material = (41,0) # Gold!
	scale = 2


	AREA = zeros( (width, height, depth) )

	print '%s: Rendering the Road into the world at %s' % (method, time.ctime())

	iterX = 0
	iterZ = 0
	lastX = -1
	lastZ = -1
	steps = 0

	angleSize = pi/1440
	
	# Spiral out from the centre
	while (centreWidth+iterX) < width and (centreWidth+iterX) >= 0 and (centreDepth+iterZ) >=0 and (centreDepth+iterZ) < depth:
		if iterX != lastX and iterZ != lastZ: # Optimise writes to the world
			setBlock(level, material, (int)(box.minx+centreWidth+iterX), box.miny, (int)(box.minz+centreDepth+iterZ)) 
			steps = steps+angleSize
		lastX = iterX
		lastZ = iterZ
		iterX = steps*cos(steps)*scale
		iterZ = steps*sin(steps)*scale
		
	print '%s: Ended at %s' % (method, time.ctime())

def MtRing(level, box, options):
	method = "MtRing"
	print '%s: Started at %s' % (method, time.ctime())
	SIZE = 7
	material = (1,0)

	(width, height, depth) = getBoxSize(box)

	AREA = zeros( (width, height, depth) )

	(MTPath, directionX, directionZ) = drawCircularPath( level, box, options, zeros( (width, depth) ) )


	for iterX in xrange(0, width):
		for iterZ in xrange(0, depth):
			
			if MTPath[iterX, iterZ] > 0 and randint(0,5) == 1:
				#twosize = 10*SIZE
				MTWidth = 20 #randint(SIZE, twosize)
				MTDepth = MTWidth

				# Height is determined by distance from the box edges

				#nearestX = iterX
				#if width-iterX < iterX:
				#	nearestX = width-iterX
				#nearestZ = iterZ
				#if depth - iterZ < iterZ:
				#	nearestZ = width-iterZ

				#ratioZ = (float)((float)(nearestZ) / (float)(depth/2))
				#ratioX = (float)((float)(nearestX) / (float)(width/2))
				#print '%s %s' % (ratioX, ratioZ)
				#MTHeight = abs((float)(ratioZ * ratioX * height))
				MTHeight = height/2+randint(0, (int)(height/2))

				mountain = zeros( (2*MTWidth, MTHeight, 2*MTDepth) )
				MtA(mountain, options, ((int)(2*MTWidth), (int)(MTHeight), (int)(2*MTDepth)))
		
				# copy mountain into the region
				x = 0
				while x < (int)(2*MTWidth):
					y = 0
					while y < (int)(MTHeight):
						z = 0
						while z < (int)(2*MTDepth):
							px = iterX-(int)(MTWidth)+x
							pz = iterZ-(int)(MTDepth)+z
							if px >= 0 and px < width and pz >= 0 and pz < depth and y < height:
								if mountain[x][y][z] > 0:
									AREA[px][y][pz] = mountain[x][y][z]
							z = z +1
						y = y +1
					x = x +1
				
	print '%s: Rendering the Range into the world at %s' % (method, time.ctime())

	for iterX in xrange(0, width): # Hollow render? Make this modular?
		for iterZ in xrange(0, depth):
			iterY = height-1
			while iterY >= 0:
				if AREA[iterX][iterY][iterZ] == 1:
					setBlockIfEmpty(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ) 
					# iterY = -1 # stop scan. Plot surface block only. Overhangs? Draft for visualisation.
				iterY = iterY -1


	print '%s: Ended at %s' % (method, time.ctime())


def MtRange(level, box, options):
	method = "MtRange"
	print '%s: Started at %s' % (method, time.ctime())
	SIZE = 7
	material = (1,0)

	(width, height, depth) = getBoxSize(box)

	AREA = zeros( (width, height, depth) )

	(MTPath, directionX, directionZ) = drawJaggedyPath( level, box, options, zeros( (width, depth) ) )
	(MTPath, directionX, directionZ) = drawJaggedyPath( level, box, options, MTPath )


	for iterX in xrange(0, width):
		for iterZ in xrange(0, depth):
			
			if MTPath[iterX, iterZ] > 0 and randint(0,5) == 1:
				twosize = 10*SIZE
				MTWidth = randint(SIZE, twosize)
				MTDepth = 1.3 * MTWidth

				# Height is determined by distance from the box edges

				nearestX = iterX
				if width-iterX < iterX:
					nearestX = width-iterX
				nearestZ = iterZ
				if depth - iterZ < iterZ:
					nearestZ = width-iterZ

				ratioZ = (float)((float)(nearestZ) / (float)(depth/2))
				ratioX = (float)((float)(nearestX) / (float)(width/2))
				print '%s %s' % (ratioX, ratioZ)
				MTHeight = abs((float)(ratioZ * ratioX * height))

				mountain = zeros( (2*MTWidth, MTHeight, 2*MTDepth) )
				MtA(mountain, options, ((int)(2*MTWidth), (int)(MTHeight), (int)(2*MTDepth)))

				# copy mountain into the region
				x = 0
				while x < (int)(2*MTWidth):
					y = 0
					while y < (int)(MTHeight):
						z = 0
						while z < (int)(2*MTDepth):
							px = iterX-(int)(MTWidth)+x
							pz = iterZ-(int)(MTDepth)+z
							if px >= 0 and px < width and pz >= 0 and pz < depth and y < height:
								if mountain[x][y][z] > 0:
									AREA[px][y][pz] = mountain[x][y][z]
							z = z +1
						y = y +1
					x = x +1
				
	print '%s: Rendering the Range into the world at %s' % (method, time.ctime())

	for iterX in xrange(0, width): # Hollow render? Make this modular?
		for iterZ in xrange(0, depth):
			iterY = height-1
			while iterY >= 0:
				if AREA[iterX][iterY][iterZ] == 1:
					setBlockIfEmpty(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ) 
					# iterY = -1 # stop scan. Plot surface block only. Overhangs? Draft for visualisation.
				iterY = iterY -1


	print '%s: Ended at %s' % (method, time.ctime())


def MtA(DEM, options, (width, height, depth)):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "MtA"
	print '%s: Started at %s' % (method, time.ctime())
	# (width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS

	randset = [2, 2, 2, 2]
	
	minim = False
	for i in xrange(0,4):
		if minim == False:
			if randint(0,3) == 1:
				randset[i] = randint(4,7)
				minim = True

	radii = [ -randint((int)(centreWidth/randset[0]),centreWidth-1), 
		  -randint((int)(centreDepth/randset[1]),centreDepth-1), 
		   randint((int)(centreWidth/randset[2]),centreWidth-1),
		   randint((int)(centreDepth/randset[3]),centreDepth-1)]
	
	for iterY in xrange(0, height):
		# for each layer, draw a squishdisc
		vertScale = (float)(((float)(height)-(float)(iterY))/(float)(height))
		
		
		startX = (float)(vertScale*radii[0])
		endX = (float)(vertScale*radii[2])
		startZ = (float)(vertScale*radii[1])
		endZ = (float)(vertScale*radii[3])
		
		# print '%s %s %s %s %s %s' % (iterY, vertScale, startX, endX, startZ, endZ)
		
		if startX != 0:
			angleStepSize = pi/2/abs(startX)
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(startZ*cos(+angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
				
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ +1
				iterX = iterX +1

		if endX != 0:
			angleStepSize = pi/2/abs(endX)
			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(startZ*cos(angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1

			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
		
		# Re-arrange the Radii
		
		for i in xrange(0,4):
			oldradius = radii[i]
			dice = randint(0,10)
			if dice == 1:
				if radii[i] > 0:
					radii[i] = radii[i] +1
				else:
					radii[i] = radii[i] -1	
			elif dice == 2:
				if radii[i] > 0:
					radii[i] = radii[i] -1
				else:
					radii[i] = radii[i] +1	
			elif dice == 3:
				if radii[i] > 0:
					radii[i] = radii[i] -2
				else:
					radii[i] = radii[i] +2	
			elif dice == 4:
				if radii[i] > 0:
					radii[i] = radii[i] +2
				else:
					radii[i] = radii[i] -2

	
			if abs(radii[i]) < 1 or (radii[i] * oldradius) < 0:
				radii[i] = oldradius # restore if I went too far


		if radii[0] < -centreWidth+1:
			radii[0] = -centreWidth+1
		if radii[1] < -centreDepth+1:
			radii[1] = -centreDepth+1
		if radii[2] > centreWidth-1:
			radii[2] = centreWidth-1
		if radii[3] > centreDepth-1:
			radii[3] = centreDepth-1

	print '%s: Ended at %s' % (method, time.ctime())
		

def Mt(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Mt"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS

	randset = [2, 2, 2, 2]
	
	minim = False
	for i in xrange(0,4):
		if minim == False:
			if randint(0,3) == 1:
				randset[i] = randint(4,7)
				minim = True

	DEM = zeros( (width, height, depth) )
	radii = [ -randint(centreWidth/randset[0],centreWidth-1), -randint(centreDepth/randset[1],centreDepth-1), randint(centreWidth/randset[2], centreWidth-1), randint(centreDepth/randset[3],centreDepth-1)]
	
	for iterY in xrange(0, height):
		# for each layer, draw a squishdisc
		vertScale = (float)(((float)(height)-(float)(iterY))/(float)(height))
		
		
		startX = (float)(vertScale*radii[0])
		endX = (float)(vertScale*radii[2])
		startZ = (float)(vertScale*radii[1])
		endZ = (float)(vertScale*radii[3])
		
		print '%s %s %s %s %s %s' % (iterY, vertScale, startX, endX, startZ, endZ)
		
		if startX != 0:
			angleStepSize = pi/2/abs(startX)
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(startZ*cos(+angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
				
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ +1
				iterX = iterX +1

		if endX != 0:
			angleStepSize = pi/2/abs(endX)
			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(startZ*cos(angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1

			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
		
		# Re-arrange the Radii
		
		for i in xrange(0,4):
			oldradius = radii[i]
			dice = randint(0,10)
			if dice == 1:
				if radii[i] > 0:
					radii[i] = radii[i] +1
				else:
					radii[i] = radii[i] -1	
			elif dice == 2:
				if radii[i] > 0:
					radii[i] = radii[i] -1
				else:
					radii[i] = radii[i] +1	
			elif dice == 3:
				if radii[i] > 0:
					radii[i] = radii[i] -2
				else:
					radii[i] = radii[i] +2	
			elif dice == 4:
				if radii[i] > 0:
					radii[i] = radii[i] +2
				else:
					radii[i] = radii[i] -2

	
			if abs(radii[i]) < 1 or (radii[i] * oldradius) < 0:
				radii[i] = oldradius # restore if I went too far


		if radii[0] < -centreWidth+1:
			radii[0] = -centreWidth+1
		if radii[1] < -centreDepth+1:
			radii[1] = -centreDepth+1
		if radii[2] > centreWidth-1:
			radii[2] = centreWidth-1
		if radii[3] > centreDepth-1:
			radii[3] = centreDepth-1
		
	for iterX in xrange(0, width): # Hollow render. Make this modular?
		for iterZ in xrange(0, depth):
			iterY = height-1
			while iterY >= 0:
				if DEM[iterX][iterY][iterZ] == 1:
					setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ) # plot surface block only. Overhangs? Draft for visualisation.
					# iterY = -1 # stop scan.
				iterY = iterY -1

	print '%s: Ended at %s' % (method, time.ctime())

def Mt2(level, box, options): # Conic
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Mt"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS

	DEM = zeros( (width, height, depth) )
	radii = [ -randint(centreWidth-1,centreWidth-1), -randint(centreDepth-1,centreDepth-1), randint(centreWidth-1, centreWidth-1), randint(centreDepth-1,centreDepth-1)]
	
	for iterY in xrange(0, height):
		# for each layer, draw a squishdisc
		vertScale = (float)(((float)(height)-(float)(iterY))/(float)(height))
		
		
		startX = (float)(vertScale*radii[0])
		endX = (float)(vertScale*radii[2])
		startZ = (float)(vertScale*radii[1])
		endZ = (float)(vertScale*radii[3])
		
		print '%s %s %s %s %s %s' % (iterY, vertScale, startX, endX, startZ, endZ)
		
		if startX != 0:
			angleStepSize = pi/2/abs(startX)
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(startZ*cos(+angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
				
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ +1
				iterX = iterX +1

		if endX != 0:
			angleStepSize = pi/2/abs(endX)
			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(startZ*cos(angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1

			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
		
		# Re-arrange the Radii
		
		for i in xrange(0,4):
			oldradius = radii[i]
			dice = randint(0,10)
			if dice == 1:
				if radii[i] > 0:
					radii[i] = radii[i] +1
				else:
					radii[i] = radii[i] -1	
			elif dice == 2:
				if radii[i] > 0:
					radii[i] = radii[i] -1
				else:
					radii[i] = radii[i] +1	
			elif dice == 3:
				if radii[i] > 0:
					radii[i] = radii[i] -2
				else:
					radii[i] = radii[i] +2	
			elif dice == 4:
				if radii[i] > 0:
					radii[i] = radii[i] +2
				else:
					radii[i] = radii[i] -2

	
			if abs(radii[i]) < 1 or (radii[i] * oldradius) < 0:
				radii[i] = oldradius # restore if I went too far


		if radii[0] < -centreWidth+1:
			radii[0] = -centreWidth+1
		if radii[1] < -centreDepth+1:
			radii[1] = -centreDepth+1
		if radii[2] > centreWidth-1:
			radii[2] = centreWidth-1
		if radii[3] > centreDepth-1:
			radii[3] = centreDepth-1
		
			

	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				if DEM[iterX][iterY][iterZ] == 1:
					setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)

	print '%s: Ended at %s' % (method, time.ctime())

def Mt1(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Mt"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	destY = 127
	destX = 0
	destZ = 0
	# END CONSTANTS

	DEM = zeros( (width, height, depth) )
	radii = [ -randint(centreWidth-1,centreWidth-1), -randint(centreDepth-1,centreDepth-1), randint(centreWidth-1, centreWidth-1), randint(centreDepth-1,centreDepth-1)]
	
	for iterY in xrange(0, height):
		# for each layer, draw a squishdisc
		vertScale = (float)(((float)(height)-(float)(iterY))/(float)(height))
		
		
		startX = (float)(vertScale*radii[0])
		endX = (float)(vertScale*radii[2])
		startZ = (float)(vertScale*radii[1])
		endZ = (float)(vertScale*radii[3])
		
		print '%s %s %s %s %s %s' % (iterY, vertScale, startX, endX, startZ, endZ)
		
		if startX != 0:
			angleStepSize = pi/2/abs(startX)
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(startZ*cos(+angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
				
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ +1
				iterX = iterX +1

		if endX != 0:
			angleStepSize = pi/2/abs(endX)
			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(startZ*cos(angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1

			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
		
		# Re-arrange the Radii
		
		for i in xrange(0,4):
			oldradius = radii[i]
			dice = randint(0,10)
			if dice == 1:
				radii[i] = radii[i] +1
			elif dice == 2:
				radii[i] = radii[i] -1
			elif dice == 3:
				radii[i] = radii[i] -2
			elif dice == 4:
				radii[i] = radii[i] -3
			elif dice == 5:
				radii[i] = radii[i] -4
	
			if abs(radii[i]) < 1 or (radii[i] * oldradius) < 0:
				radii[i] = oldradius # restore if I went too far


		if radii[0] < -centreWidth+1:
			radii[0] = -centreWidth+1
		if radii[1] < -centreDepth+1:
			radii[1] = -centreDepth+1
		if radii[2] > centreWidth-1:
			radii[2] = centreWidth-1
		if radii[3] > centreDepth-1:
			radii[3] = centreDepth-1


	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				if DEM[iterX][iterY][iterZ] == 1:
					setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)

	print '%s: Ended at %s' % (method, time.ctime())

def Conamid(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Conamid"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	destY = 127
	destX = 0
	destZ = 0
	# END CONSTANTS

	DEM = zeros( (width, height, depth) )
	radii = [ -randint(centreWidth-1,centreWidth-1), -randint(centreDepth-1,centreDepth-1), randint(centreWidth-1, centreWidth-1), randint(centreDepth-1,centreDepth-1)]
	
	for iterY in xrange(0, height):
		# for each layer, draw a squishdisc
		vertScale = (float)(((float)(height)-(float)(iterY))/(float)(height))
		
		
		startX = (float)(vertScale*radii[0])
		endX = (float)(vertScale*radii[2])
		startZ = (float)(vertScale*radii[1])
		endZ = (float)(vertScale*radii[3])
		
		print '%s %s %s %s %s %s' % (iterY, vertScale, startX, endX, startZ, endZ)
		
		if startX != 0:
			angleStepSize = pi/2/abs(startX)
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(startZ*cos(+angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1
				
			angleStepSize = pi/2/abs(startX)
			iterX = startX
			while iterX <= 0:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ +1
				iterX = iterX +1

		if endX != 0:
			angleStepSize = pi/2/abs(endX)
			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(startZ*cos(angleStepSize*iterX))
				iterZ = Z
				while iterZ <= 0:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1

			iterX = 0
			while iterX <= endX:
				# draw an arc		
				Z = (int)(endZ*cos(angleStepSize*iterX))
				iterZ = 0
				while iterZ <= Z:
					DEM[iterX+centreWidth, iterY, iterZ+centreDepth] = 1
					iterZ = iterZ+1
				iterX = iterX +1



	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				if DEM[iterX][iterY][iterZ] == 1:
					setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)

	print '%s: Ended at %s' % (method, time.ctime())



def Gully(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Gully"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS
	
	# Creates a canyon in the selection box
	
	DEM = zeros( (width, depth) )
	
	# Draw a jaggedy path

	directionX = 0
	directionZ = 0
	xload = 0
	zload = 0
	posX = 0
	posZ = 0



	if width > depth:
		directionX = 1
		posX = 0
		posZ = randint(0,depth-1)
	else:
		directionZ = 1
		posX = randint(0,width-1)
		posZ = 0
		
	while posX < (width-1) and posZ < (depth-1):
		# wander
		posX = posX + directionX # guided step forward
		posZ = posZ + directionZ
		
		if xload > 0:
			posX = posX + 1
			xload = xload -1
		elif xload < 0:
			posX = posX - 1
			xload = xload +1
		elif zload > 0:
			posZ = posZ + 1
			zload = zload -1
		elif zload < 0:
			posZ = posZ - 1
			zload = zload +1
		else:
			posX = posX + (randint(0,2)-1) * directionZ # clever clogs way of adjusting the position perpendicular to the direction of travel
			posZ = posZ + (randint(0,2)-1) * directionX
			if xload == 0 and randint(0,5) == 3:
				xload = (randint(0,(int)(width/6))-(int)(width/12))*directionZ
			if zload == 0 and randint(0,5) == 3:
				zload = (randint(0,(int)(depth/6))-(int)(depth/12))*directionX

		if directionX == 1: # bounds check
			if posZ >= (depth-1):
				posZ = depth-2
				zload = -3
			elif posZ <= 0:
				posZ = 1
				zload = 3
				
		elif directionZ == 1:
			if posX >= (width-1):
				posX = width-2
				xload = -3
			elif posX <= 0:
				posX = 1
				xload = 3
		DEM[posX, posZ] = DEM[posX, posZ]+1
				
	# I now have a jaggedy random path from one edge to the other.
	
	wavelength1 = randint(0,180)*pi/180
	wavelength1AngleStepSize = 1
	if directionX == 1:
		wavelength1AngleStepSize = (int)(width/wavelength1)
	elif directionZ ==1:
		wavelength1AngleStepSize = (int)(depth/wavelength1)
	
	for iterX in xrange(0, width):
		for iterZ in xrange(0, depth):
			iterY = height-1
			while iterY >= 0:
				if DEM[iterX,iterZ] > 0:
					for iterWidth in xrange(0,(int)(iterY/4)+1):
						if directionX == 1:
							setBlock(level, AIR, box.minx+iterX, box.miny+iterY, (int)(box.minz+iterZ+(iterWidth-(int)(iterY/8))))
						elif directionZ == 1:
							setBlock(level, AIR, (int)(box.minx+iterX+(iterWidth-(int)(iterY/8))), box.miny+iterY, box.minz+iterZ)
				iterY = iterY - 1


	print '%s: Ended at %s' % (method, time.ctime())


def ZipperCanyon(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "ZipperCANYON"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	# END CONSTANTS
	
	# Creates a canyon in the selection box
	
	DEM = zeros( (width, depth) )
	
	# Draw a jaggedy path

	directionX = 0
	directionZ = 0
	xload = 0
	zload = 0
	posX = 0
	posZ = 0

	if width > depth:
		directionX = 1
		posX = 0
		posZ = randint(0,depth-1)
	else:
		directionZ = 1
		posX = randint(0,width-1)
		posZ = 0
		
	while posX < (width-1) and posZ < (depth-1):
		# wander
		posX = posX + directionX # guided step forward
		posZ = posZ + directionZ
		
		if xload > 0:
			posX = posX + 1
			xload = xload -1
		elif xload < 0:
			posX = posX - 1
			xload = xload +1
		elif zload > 0:
			posZ = posZ + 1
			zload = zload -1
		elif zload < 0:
			posZ = posZ - 1
			zload = zload +1
		else:
			posX = posX + (randint(0,2)-1) * directionZ # clever clogs way of adjusting the position perpendicular to the direction of travel
			posZ = posZ + (randint(0,2)-1) * directionX
			if xload == 0 and randint(0,5) == 3:
				xload = (randint(0,(int)(width/6))-(int)(width/12))*directionZ
			if zload == 0 and randint(0,5) == 3:
				zload = (randint(0,(int)(depth/6))-(int)(depth/12))*directionX

			
		
#		print '%s: %s %s %s %s' % (method, posX, posZ, directionX, directionZ)
		
		if directionX == 1: # bounds check
			if posZ >= (depth-1):
				posZ = depth-2
				zload = -3
			elif posZ <= 0:
				posZ = 1
				zload = 3
				
		elif directionZ == 1:
			if posX >= (width-1):
				posX = width-2
				xload = -3
			elif posX <= 0:
				posX = 1
				xload = 3
		DEM[posX, posZ] = DEM[posX, posZ]+1
				
	# I now have a jaggedy random path from one edge to the other.
	
	wavelength1 = randint(0,180)*pi/180
	wavelength1AngleStepSize = 1
	if directionX == 1:
		wavelength1AngleStepSize = (int)(width/wavelength1)
	elif directionZ ==1:
		wavelength1AngleStepSize = (int)(depth/wavelength1)
	
	for iterX in xrange(0, width):
		for iterZ in xrange(0, depth):
			iterY = height-1
			while iterY >= 0:
				if DEM[iterX,iterZ] > 0:
					for iterWidth in xrange(0,(int)(iterY/4)+1):
						if directionX == 1:
							setBlock(level, AIR, box.minx+iterX, box.miny+iterY, (int)(box.minz+iterZ+(iterWidth-(int)(iterY/8))*sin((iterZ+iterY)*wavelength1AngleStepSize)))
						elif directionZ == 1:
							setBlock(level, AIR, (int)(box.minx+iterX+(iterWidth-(int)(iterY/8))*sin((iterZ+iterY)*wavelength1AngleStepSize)), box.miny+iterY, box.minz+iterZ)
				iterY = iterY - 1


	print '%s: Ended at %s' % (method, time.ctime())

def Mountain(level, box, options, dimensionList):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "MOUNTAIN"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	destY = 127
	destX = 0
	destZ = 0
	# END CONSTANTS

	
	currentHeight = 0
	currentDepth = 0
	currentWidth = 0
	
	for (heightDivisor, widthDivisor) in dimensionList:
	# choose three points on the edges of the box - defines a plane. Mark the blocks to delete from this corner

		(width, height, depth) = getBoxSize(box)
		width = (int)(width / widthDivisor)
		depth = (int)(depth / widthDivisor)
		height = (int)(height / heightDivisor)
		centreWidth = width / 2
		centreHeight = height / 2
		centreDepth = depth / 2

		boulder = zeros( (width, height, depth) )

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
					boulder[iterX][height-1-iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][height-1-iterY][(int)(depth/widthDivisor)-1-iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, centreDepth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][height-1-iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, centreDepth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[width-1-iterX][height-1-iterY][iterZ] = 1 # denotes an air block	


		(mwidth, mheight, mdepth) = getBoxSize(box)
		xOffset = (int)((mwidth - width)/2)
		zOffset = (int)((mdepth - depth)/2)

		for iterX in xrange(0, width):
			for iterY in xrange(0, height):
				for iterZ in xrange(0, depth):
					if boulder[iterX][iterY][iterZ] == 0:
						setBlock(level, material, box.minx+iterX+xOffset, box.miny+iterY, box.minz+iterZ+zOffset)
		
		currentHeight = currentHeight + height	
		currentWidth = currentWidth + width
		currentDepth = currentDepth + depth
	print '%s: Ended at %s' % (method, time.ctime())


def Flyland(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Flyland"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	# The scan region is a vertical cylinder in the selection box

	ANGLESTEPSIZEX = pi/width 	# I like to shout when it comes to constants. For each step in the width direction, this is how much rotation around a unit circle occurs

	# Step 1 - find the maximum height of the blocks in the area. The difference between that height and the top of the box is how much the blocks will be moved.
	myBox = zeros( (width,height,depth,2) )
	surfaceLayer = height
	lastBlockCount = 0
	currentBlockCount = 0
	highestBlockLayer = 0

	iterY = height-1
	while iterY >= 0:
		currentBlockCount = 0

		for iterX in xrange(0, width):

			angleX = ANGLESTEPSIZEX*iterX
			minMaxZ = (int)(sin(angleX)*centreDepth)
			
			iterZ = -minMaxZ
			while iterZ < minMaxZ:  # This method is slightly better than rotation mapping for speed and leaving no holes due to rounding

				(block, blockData) = (level.blockAt(box.minx + iterX, box.miny + iterY, box.minz + centreDepth + iterZ), level.blockDataAt(box.minx + iterX, box.miny + iterY, box.minz + centreDepth + iterZ))
				myBox[iterX, iterY, iterZ+centreDepth, 0] = block
				myBox[iterX, iterY, iterZ+centreDepth, 1] = blockData # cache a copy. We'll bring it back when wrenching it from the ground into the sky later.
				# print 'Block = %s, BlockData = %s' % (myBox[iterX, iterY, iterZ+centreDepth,0], myBox[iterX, iterY, iterZ+centreDepth,1])
				if block != 0:
					currentBlockCount = currentBlockCount + 1 # found a non-air block.
					if currentBlockCount > lastBlockCount:  # new candidate for the surface height! Lock it in.
						surfaceLayer = iterY
						lastBlockCount = currentBlockCount

					if highestBlockLayer == 0: # we haven't seen a non-air block yet
						highestBlockLayer = iterY # ... and now we have seen our first, therefore highest, non-air block
						# print 'Highest block layer found at %s' % (highestBlockLayer)
				iterZ = iterZ +1
		iterY = iterY - 1
				
	# Coming out of step 1 the surface of the land has been located and is in "surfaceLayer". The highest block has been identified and is in "highestBlockLayer".

	amountToRaiseTheChunk = height - highestBlockLayer

	print '%s: Surface at %s, Highest block at %s, Amount to raise the land is %s' % (method, surfaceLayer, highestBlockLayer, amountToRaiseTheChunk)

	# Step 2 - shift the region of interest upwards! Take everything in a sort of conical section below the surface.
	
	typeOfSubsurface = randint(0,5)  # randomly upheave different shapes from the land
	
	RANDMULTIPLIER = randint(1,8)
	
	
	
	for iterX in xrange(0, width):
		angleX = ANGLESTEPSIZEX*iterX
		minMaxZ = (int)(sin(angleX)*centreDepth)
		radiusMax = ( sqrt(centreWidth * centreWidth + minMaxZ * minMaxZ))	
		ANGLE = pi/2/radiusMax
		ANGLE2 = ANGLE/8*RANDMULTIPLIER
		iterZ = -minMaxZ
		while iterZ < minMaxZ:  # This method is slightly better than rotation mapping for speed and leaving no holes due to rounding
			deltaX = centreWidth - iterX
			localRadius = sqrt(deltaX*deltaX + iterZ*iterZ)
			
			if typeOfSubsurface == 0:
				depthToCopy = localRadius /  radiusMax * surfaceLayer  # Magic math for the subsurface column at this x,z point
			elif typeOfSubsurface == 1:
				depthToCopy = localRadius /  radiusMax * surfaceLayer - randint(0,2)  # Magic math for the subsurface column at this x,z point
			elif typeOfSubsurface == 2:
				depthToCopy = sin(localRadius * ANGLE) * surfaceLayer
			elif typeOfSubsurface == 3:
				depthToCopy = (localRadius * localRadius)
				if depthToCopy > surfaceLayer:
					depthToCopy = surfaceLayer
				depthToCopy = depthToCopy - randint(0,(surfaceLayer/3))
			else:
				depthToCopy = sin(localRadius * ANGLE2) * surfaceLayer
						
			depthToCopyTo = (int)( depthToCopy ) # Depending on where we are on the disc of land, the depth under the surface to be copied varies
			if depthToCopyTo < 0:
				depthToCopyTo = 0
			elif depthToCopyTo > surfaceLayer:
				depthToCopyTo = surfaceLayer
				
			# print 'depthToCopyTo is %s' % (depthToCopyTo)
			iterY = highestBlockLayer
			while iterY > depthToCopyTo: # for each vertical column of blocks, shift up by amountToRaiseTheChunk.
				setBlock(level, (myBox[iterX, iterY, iterZ+centreDepth,0],myBox[iterX, iterY, iterZ+centreDepth,1]), box.minx+iterX, box.miny+iterY + amountToRaiseTheChunk, box.minz+centreDepth+iterZ) # copy
				setBlock(level, AIR, box.minx+iterX, box.miny+iterY, box.minz+centreDepth+iterZ) # ... then clear

				iterY = iterY - 1
			iterZ = iterZ +1


	print '%s: Ended at %s' % (method, time.ctime())

def Foam(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Foam"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	PURGEAMOUNT = 0
	# END CONSTANTS

	# First pass, scan and count neighbours. Blocks with different neighbours are retained. Those with no different neighbour are discarded
	F = zeros( (width, height, depth) ) # This field holds the count of how many neighbour blocks there are

	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				if F[iterX][iterY][iterZ] == 0: # if the counter is higher then we've already determined this block is a cell wall
					thisBlock = (level.blockAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ), level.blockDataAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ))
					if thisBlock != AIRBLOCK: # Now check all the neighbour blocks. If one is found that is different, then a wall goes up. Otherwise - discard.
						for dx in xrange(-1,2):
							for dy in xrange(-1,2):
								for dz in xrange(-1,2):
									if dx == 0 and dy == 0 and dz == 0:  # Ignore the current block as it is not a neighbour to itself
										T = 0 # ignore
									else:
										(x, y, z) = (iterX + dx, iterY + dy, iterZ + dz)
										if x > 0 and x < (width-1) and y > 0 and y < (height-1) and z > 0 and z < (depth-1):
											thatBlock = (level.blockAt(box.minx+x, box.miny+y, box.minz+z), level.blockDataAt(box.minx+x, box.miny+y, box.minz+z) )
											if thisBlock != thatBlock:
												F[iterX][iterY][iterZ] = F[iterX][iterY][iterZ] + 1  # This block is a cell wall
												F[x][y][z] = F[x][y][z] + 1  # and so is that block.

	# Pass 2 - purge anywhere the neighbour count indicates the block is not a cell wall.
	for iterX in xrange(1, width-1):
		for iterY in xrange(1, height-1):
			for iterZ in xrange(1, depth-1):
				# print '%s' % (F[iterX][iterY][iterZ])
				if F[iterX][iterY][iterZ] == PURGEAMOUNT:
						setBlock(level, AIR, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
						
	print '%s: Ended at %s' % (method, time.ctime())

	
def Raise(level, box, options): # Request from the forums - MinecraftvsCreepers
	# CONSTANTS AND GLOBAL VARIABLES
	TICKSPERSEC = 20
	method = "GEOMANCER - Raise"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	BLOCKSPAWNER = (52,0)
	CHUNKSIZE = 16
	# END CONSTANTS

	# Scan for height to raise the map
	
	currentMaxHeight = findMaxAbsHeight(level, box)
	
	# we now have currentMaxHeight. Raise all blocks by this amount. Leave the original blocks where they were to 'fill' the void that would otherwise be created.
	# Future - should I slope the edges smoothly?

	deltaHeight = box.maxy-currentMaxHeight # this is the amount by which the landscape must be lifted
	
	iterY = currentMaxHeight
	while iterY >= 0:  # top-down scanning again. Copying as we go this time. Start at the top-most layer of the landscape
		for iterX in xrange(0,width):
			for iterZ in xrange(0,depth):
				
				tempBlock = level.blockAt( box.minx+iterX, box.miny+iterY, box.minz+iterZ)
						
				if tempBlock != AIRBLOCK: # do I need to copy at all?
					tempData = level.blockDataAt( box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					setBlock(level, (tempBlock,tempData), box.minx+iterX, box.miny+iterY+deltaHeight, box.minz+iterZ)
		iterY = iterY -1

	print '%s: Ended at %s' % (method, time.ctime())

def Gash(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Gash"
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS


	if depth > width: # The gash runs the length of the selection box, whichever the orientation
	
		angleStart = randint(0,100)
		angleEnd = randint(100,200)
		angleStepSizeZ = (pi/50*(angleEnd-angleStart))/depth # describes the arc of the gash
		gashAngleStart = pi/50*angleStart
		gashStepSize = pi/depth # one full revolution
		
		for iterZ in xrange(0, depth):
			iterX = (int)(centreWidth*sin(gashAngleStart+angleStepSizeZ * iterZ))
			
			gashWidth = (int)(centreWidth*sin(gashStepSize*iterZ)/2)

			for iterY in xrange(0, height):			
				heightBand = 2 - (int)((iterY / (height / 2)))

				for sizeX in xrange(-gashWidth+heightBand,gashWidth-heightBand):
					posX = (float)(iterX+sizeX)

					gashWidthMultiplier = (float)(iterY/height)
										
					setBlock(level, 
						 AIR,
						 box.minx+centreWidth+(int)(posX),
						 box.miny+iterY,
						 box.minz+iterZ
						)				
		
	
	else:
		angleStart = randint(0,100)
		angleEnd = randint(100,200)
		angleStepSizeX = (pi/50*(angleEnd-angleStart))/width # describes the arc of the gash
		gashAngleStart = pi/50*angleStart
		gashStepSize = pi/width # one full revolution
		
		for iterX in xrange(0, width):
			iterZ = (int)(centreDepth*sin(gashAngleStart+angleStepSizeX * iterX))
			
			gashWidth = (int)(centreDepth*sin(gashStepSize*iterX)/2)

			for iterY in xrange(0, height):
				heightBand = 2 - (int)((iterY / (height / 2)))
				
				for sizeZ in xrange(-gashWidth+heightBand,gashWidth-heightBand):
					posZ = (float)(iterZ+sizeZ)
					
					setBlock(level, 
						 AIR,
						 box.minx+iterX,
						 box.miny+iterY,
						 box.minz+centreDepth+(int)(posZ)
						)			

def Hollow(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Hollow"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	PURGEAMOUNT = 9+8+9
	material = AIR
	coat = False
	# END CONSTANTS


	# First pass, scan and count neighbours
	F = zeros( (width, height, depth) ) # This field holds the count of how many neighbour blocks there are

	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				thisBlock = level.blockAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				if thisBlock != AIRBLOCK: # Now I need to push this block's contribution into all the neighbour blocks in a 3x3 grid
					for dx in xrange(-1,2):
						for dy in xrange(-1,2):
							for dz in xrange(-1,2):
								if dx == 0 and dy == 0 and dz == 0:  # Ignore the current block as it is not a neighbour to itself
									T = 0 # ignore
								else:
									(x, y, z) = (iterX + dx, iterY + dy, iterZ + dz)
									if x > 0 and x < (width-1) and y > 0 and y < (height-1) and z > 0 and z < (depth-1):
										F[x][y][z] = F[x][y][z] + 1

	# Pass 2 - purge anywhere the neighbour count indicates the block is completely encased in other blocks
	for iterX in xrange(1, width-1):
		for iterY in xrange(1, height-1):
			for iterZ in xrange(1, depth-1):
				# print '%s' % (F[iterX][iterY][iterZ])
				
				if coat == False:
					if F[iterX][iterY][iterZ] >= PURGEAMOUNT:
						setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				else:
					if F[iterX][iterY][iterZ] < PURGEAMOUNT and F[iterX][iterY][iterZ] > 0:
						setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					
	print '%s: Ended at %s' % (method, time.ctime())


def Rainbow(level, box, options): 	
	colours = [ 14, 1, 4, 5, 11, 3, 10 ]
	radius = (box.maxx - box.minx) / 2
	fidelity = radius * 20 # arbitrary based on leaving no gaps.

	depth = (box.maxz - box.minz)
	bandwidth = radius / 16
	if bandwidth < 1:
		bandwidth = 1

	deg = pi/fidelity
	
	heightscale = 1.0 * (box.maxy - box.miny) / radius # squish the arc based on box height
	
	
	for z in range(0, depth):
		for t in range(0, fidelity):
			offset = 0
			for c in colours:
				for i in range(0, bandwidth):
					x = (radius-offset) * cos(t * deg)
					y = heightscale * (radius-offset) * sin(t * deg)
					setBlock(level, (35, c), (int)(box.minx + radius + x), (int)(box.miny + y), box.minz+z)
					offset = offset + 1
		
	level.markDirtyBox(box)
	
def Mound(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	TICKSPERSEC = 20
	method = "GEOMANCER - Mound"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	BLOCKSPAWNER = (52,0)
	CHUNKSIZE = 16
	# END CONSTANTS

	currentMaxHeight = findMaxAbsHeight(level, box)
	deltaHeight = box.maxy-currentMaxHeight # this is the amount by which the landscape must be lifted at the centre of the selection box

	for x in range(-centreWidth,centreWidth):
		print '%s: Iteration %s of %s' % (method, x, width)
		for z in range(-centreDepth,centreDepth):
			r = (float)(sqrt(x*x + z*z)) # distance from selection box centre on the horizontal plane
			t = r/centreWidth
			c = cos(t)
			h = abs((float)(deltaHeight)*c) # height at this point
			print '%s: %s %s %s %s %s %s' % (method, x, z, r, h, c, t)
			if h > 0:
				y = currentMaxHeight
				while y >= box.miny:
					setBlock(level, (level.blockAt((int)(box.minx+centreWidth+x),(int)(y),(int)(box.minz+centreDepth+z)),level.blockDataAt((int)(box.minx+centreWidth+x),(int)(y),(int)(box.minz+centreDepth+z))), (int)(box.minx+centreWidth+x),(int)(y+h),(int)(box.minz+centreDepth+z)) # blit block up
					y = y - 1 # process the next layer down.

	print '%s: Ended at %s' % (method, time.ctime())
	
def Boulder(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "BOULDER"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (1,0)
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
				if boulder[iterX][iterY][iterZ] == 0:
					setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
	
					
	print '%s: Ended at %s' % (method, time.ctime())	
	
def Subside(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Subside"
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	# Pass 1 - mark and replace
	for iterX in xrange(box.minx, box.maxx):
		print '%s: Subside %s of %s' % (method, iterX-box.minx, width-1)
		for iterZ in xrange(box.minz, box.maxz):
			# Pass 1, fall
			iterY = box.miny
			lastSolidY = iterY-1
			
			x = iterX - box.minx - centreWidth
			z = iterZ - box.minz - centreDepth
			
			if x*x + z*z < centreDepth*centreWidth:
				lastSolidY = lastSolidY+1 # hunt for next available position, start above the block just placed
				keepGoing = 1
				while keepGoing == 1:
					if level.blockAt(iterX, lastSolidY, iterZ) == 0:
						lastSolidY = lastSolidY-1
						keepGoing = 0
					lastSolidY = lastSolidY+1
					if lastSolidY == box.maxy: # No air?
						keepGoing = 0 # give up, no free air found within the current pile.			
					else: # There is air
						while iterY < box.maxy:
							tempB = level.blockAt(iterX,iterY,iterZ)
							if (tempB <> 0 and level.blockAt(iterX,iterY-1,iterZ) == 0):
								# print '%s: Fall %s of %s at block %s' % (method, iterY, box.maxy, tempBlock)
								# fall! Where to?				
								if iterY > lastSolidY:
									tempBlock = (tempB, level.blockDataAt(iterX,iterY,iterZ))
									setBlockIfEmpty(level, tempBlock, iterX, lastSolidY, iterZ) # Place block at lowest air position
									setBlock(level, AIR, iterX, iterY, iterZ) # Replace original block position with AIR						
									level.markDirtyBox(box)
									lastSolidY = lastSolidY+1 # hunt for next available position, start above the block just placed
									keepGoing = 1
									while keepGoing == 1:
										if level.blockAt(iterX, lastSolidY, iterZ) == 0:
											lastSolidY = lastSolidY-1	
											keepGoing = 0
										lastSolidY = lastSolidY+1
										if lastSolidY == box.maxy:
											keepGoing = 0 # give up, no free air found within the current pile.
											iterY = box.maxy # break hunt
								# else:
								#	print 'Subside error - air block was missed! %s %s %s' % (iterY, lastSolidY, iterZ)
							iterY = iterY + 1

def Voronoi(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Voronoi"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	Q = []
	# Pass 1 - identify the location and type of each block in the selection box (use sparse regions)
	for iterX in xrange(box.minx, box.maxx):
		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				thisBlock = (level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ))
				if thisBlock != AIR:
					Q.append( (thisBlock, iterX, iterY, iterZ )  )

	# Pass 2 - identify the closest block to each point in space.
	for iterX in xrange(box.minx, box.maxx):
		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				thisBlock = (level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ))
				if thisBlock == AIR:
					# Work out the distance of this block from each of the anchor blocks.
					newBlock = AIR
					lastDistance = 999999999
					for iterQ in xrange(0, len(Q)):
						(controlBlock, x, y, z) = Q[iterQ]
						deltaX = x - iterX
						deltaY = y - iterY
						deltaZ = z - iterZ
						thisDistance = deltaX*deltaX + deltaY*deltaY + deltaZ*deltaZ
						if thisDistance < lastDistance:
							newBlock = controlBlock
							lastDistance = thisDistance # New champion to be beaten
					if newBlock != AIR:
						setBlock(level, newBlock, iterX, iterY, iterZ)
						
	print '%s: Ended at %s' % (method, time.ctime())
	
def ImpactCrater(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	TICKSPERSEC = 20
	method = "GEOMANCER - ImpactCrater"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	BLOCKSPAWNER = (52,0)
	CHUNKSIZE = 16
	# END CONSTANTS

	currentMaxHeight = findMaxAbsHeight(level, box)
	deltaHeight = box.maxy-currentMaxHeight # this is the amount by which the landscape must be lifted at the centre of the selection box

	for x in range(-centreWidth,centreWidth):
		print '%s: Iteration %s of %s' % (method, x, width)
		for z in range(-centreDepth,centreDepth):
			r = (float)(sqrt(x*x + z*z)) # distance from selection box centre on the horizontal plane
			h = abs((float)(deltaHeight)*cos(r/centreWidth*3)) # height at this point
			print '%s: %s %s %s %s' % (method, x, z, r, h)
			y = currentMaxHeight
			while y >= box.miny:
				setBlock(level, (level.blockAt((int)(box.minx+centreWidth+x),(int)(y),(int)(box.minz+centreDepth+z)),level.blockDataAt((int)(box.minx+centreWidth+x),(int)(y),(int)(box.minz+centreDepth+z))), (int)(box.minx+centreWidth+x),(int)(y+h),(int)(box.minz+centreDepth+z)) # blit block up
				y = y - 1 # process the next layer down.

	print '%s: Ended at %s' % (method, time.ctime())
	

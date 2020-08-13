# This filter is to create buildings in the style of Andreas Palladio
# Requested by @BlockWorksYT (Twitter) / https://www.youtube.com/user/BlockWorksYT (YouTube)
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
		("PALLADIO for BLOCKWORKS", "label"),
		("Operation", (
			"Palladio",
			"Palladio"
  		    )),
		("Wall:", alphaMaterials.BlockofQuartz),
		("Slab:", alphaMaterials.StoneSlab),
		("Roof:", alphaMaterials.Brick),
		("Roof Slab:", alphaMaterials.BrickSlab),

#		("Marker block:", alphaMaterials.BlockofQuartz),
#		("Path block:", alphaMaterials.BlockofQuartz),
#		("Fence block:", alphaMaterials.Brick),
#		("Railing block:", alphaMaterials.Stone),
#		("Anchor block:", alphaMaterials.GlassPane), # Randomly assigned
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)


def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = options["Operation"]
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	
#	shape = primitive_arch(box, int(ceil(height/9*8)), int(ceil(width/5*2)), getBlockFromOptions(options,"Marker block:"))
	shape = PalladioBuilding(box,options)
	bbox = BoundingBox((0,0,0),(width,height,depth))
	level.copyBlocksFrom(shape, bbox, (box.minx,box.miny,box.minz))
	SUCCESS = True
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end

def PalladioBuildingInterior(level, buildingBox, roomBox, options, wallMaterial, groundFloorHeight, upperLevelHeight, foundationHeight, roofHeight ):
	method = "PalladioBuildingInterior"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,roomBox,options,method) # Log start

	# Palladio's room ratios
	# Circle
	# Square
	# 1:1.25
	# 1:1.414
	# 1:1.5
	# 1:1.667
	# 1:2
	
	# 1. Determine the room layout
	P = [] # width wise room partitions
	Q = [] # depth wise room partitions
	# Work out how to 'pack' each side?
	pos = 0
	posDepth = 0
	while pos < centreWidth and posDepth < centreDepth:
		roomWidth = randint(8,16)
		pos += roomWidth
		if pos < centreWidth and posDepth < centreDepth:
			P.append(roomWidth)
			ratio = randint(1,6)
			if ratio == 1:
				Q.append(roomWidth)
				posDepth += roomWidth
			elif ratio == 2:
				Q.append(int(roomWidth*1.25))
				posDepth += int(roomWidth*1.25)
			elif ratio == 3:
				Q.append(int(roomWidth*1.414))
				posDepth += int(roomWidth*1.414)
			elif ratio == 4:
				Q.append(int(roomWidth*1.5))
				posDepth += int(roomWidth*1.5)
			elif ratio == 5:
				Q.append(int(roomWidth*1.667))
				posDepth += int(roomWidth*1.667)
			elif ratio == 6:
				Q.append(int(roomWidth*2))
				posDepth += int(roomWidth*2)
	
	# 1.a. Render room and floor partitions
	floor = groundFloorHeight
	while floor < height:
		for x in xrange(0,width):
			for z in xrange(0,depth):
				setBlock(level, wallMaterial, roomBox.minx+x, foundationHeight+floor, roomBox.minz+z)
		floor += upperLevelHeight
	
	posx = 0
	posz = 0
	index = 0
	while posx < centreWidth and posz < centreDepth and index < len(P) and index < len(Q):
		posx += P[index]
		posz += Q[index]
		z = posz
		for x in xrange(0,width):
			for y in xrange(0,height):
				setBlock(level, wallMaterial, roomBox.minx+x, foundationHeight+y, roomBox.minz+z)
				setBlock(level, wallMaterial, roomBox.minx+x, foundationHeight+y, roomBox.maxz-z-1)
		x = posx
		for z in xrange(0,depth):
			for y in xrange(0,height):
				setBlock(level, wallMaterial, roomBox.minx+x, foundationHeight+y, roomBox.minz+z)
				setBlock(level, wallMaterial, roomBox.maxx-x-1, foundationHeight+y, roomBox.minz+z)
		# Windows
		
				
		index += 1
	
	# 2. Attempt to punch holes for doors and windows at strategic locations.
	
	
	# 3. Central cylinder and roof?
	
	FuncEnd(level,buildingBox,options,method) # Log end
	
def PalladioBuilding(box,options):
	method = "PalladioBuilding"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	
	ARCHWIDTH = 6
	AIR = (0,0)
	GRASSBLOCK = (2,0)
	WALLBLOCK = getBlockFromOptions(options,"Wall:")
	SLABBLOCK = getBlockFromOptions(options,"Slab:")
	ROOFBLOCK = getBlockFromOptions(options,"Roof:")
	ROOFSLABBLOCK = getBlockFromOptions(options,"Roof Slab:")
	b=range(4096); b.remove(0)
	
	# A building is a collection of rooms behind a selection of facades, on a base and topped by a roof
	# 1. facade x1
	# 2. rotate into position (maybe have two symmetries later with two facades)
	# 3. build out the interior levels and rooms based on ratios
	# 4. extrapolate the base
	# 5. add exterior stairs
	# 6. do the roof - consider domed central area.
	
	# Some constants for this building:
	foundationHeight = randint(8,16)
	groundFloorHeight = randint(8,24)
	upperLevelHeight = randint(5,8)
	frontBackFacadeDepth = randint(1,4) * ARCHWIDTH
	leftRightFacadeDepth = randint(1,4) * ARCHWIDTH # Check bounds
	roofDepth = randint(8,16)
	print groundFloorHeight
	print upperLevelHeight

	# Main facade sections
	f = abs(foundationHeight)
	dw = abs(leftRightFacadeDepth)
	dd = abs(frontBackFacadeDepth)
	w = abs(width-2*dw-2*f)
	d = abs(depth-2*dd-2*f)
	hh = abs(height-f-roofDepth)
	
	print 'box %s f %s, dw %s, dd %s, w %s, d %s, hh %s' % (box, f,dw,dd,w,d,hh)
	
	frontFacadeBox = BoundingBox((0,0,0),(w, hh, dd)) 
	frontFacadeSchematic = complex_facade(frontFacadeBox, WALLBLOCK, SLABBLOCK, ROOFBLOCK, ROOFSLABBLOCK, groundFloorHeight, upperLevelHeight)
	level.copyBlocksFrom(frontFacadeSchematic, frontFacadeBox, (box.minx+dw+f,box.miny,box.maxz-dd-2-f),b)
	
	frontFacadeSchematic.rotateLeft()
	frontFacadeSchematic.rotateLeft()
	level.copyBlocksFrom(frontFacadeSchematic, frontFacadeBox, (box.minx+dw+f,box.miny,box.minz+2+f),b)	

	rightFacadeBox = BoundingBox((0,0,0),(d, hh, dw)) 
	rightFacadeSchematic = complex_facade(rightFacadeBox, WALLBLOCK, SLABBLOCK, ROOFBLOCK, ROOFSLABBLOCK, groundFloorHeight, upperLevelHeight)
	rightFacadeSchematic.rotateLeft()
	r90BBox = BoundingBox((0,0,0),(dw,hh,d))
	level.copyBlocksFrom(rightFacadeSchematic, r90BBox, (box.minx+width-dw-2-f,box.miny,box.minz+dd+f),b)
	
	rightFacadeSchematic.rotateLeft()
	rightFacadeSchematic.rotateLeft()
	level.copyBlocksFrom(rightFacadeSchematic, r90BBox, (box.minx+f+2,box.miny,box.minz+f+dd),b)

	roofBox = BoundingBox((0,0,0),(w, roofDepth, d))
	roofSchematic = complex_buildingRoof(roofBox, WALLBLOCK, SLABBLOCK, ROOFBLOCK, ROOFSLABBLOCK) # Create the roof
	level.copyBlocksFrom(roofSchematic, roofBox, (box.minx+dw+f,box.miny+hh,box.minz+dd+f),b) # Add the roof
	
	# Create the lower foundation.
	foundationSchematic = MCSchematic((width,height,foundationHeight+depth))
	for x in xrange(0,width):
		for z in xrange(0,depth):
			# Check the source model for a block, if found, there's a foundation here
			for y in xrange(0,height):
				if getBlock(level,x,y,z) != AIR:
					for fy in xrange(0, foundationHeight):
						setBlock(foundationSchematic, WALLBLOCK, x, fy, z)
					break
	foundationSchematic.copyBlocksFrom(level, box, (0,foundationHeight,0))

	# Create the stairs
	# Search for platforms
	z = int(depth/2)
	y = 0
	x = 0
	keepGoing = True
	while keepGoing == True:
		if getBlock(foundationSchematic,x,y,z) != AIR: # Found a block, must be the platform at the top of the stairs.
			iz = 0
			scanKeepGoing = True
			while scanKeepGoing == True: # Scan for the edge of the platform
				if getBlock(foundationSchematic,x,y,centreDepth+iz) == AIR:
					print 'zz %s %s %s' % (x,y,iz)
					# Draw the stairs
					for jx in xrange(1,x-1):
						for jz in xrange(0,iz):
							if jz == iz-1 or jz == iz-2:
								for jy in xrange(0,foundationHeight):
									setBlock(foundationSchematic, WALLBLOCK, jx+1, jy, centreDepth+jz)
							else:
								setBlock(foundationSchematic, WALLBLOCK, jx+1, jx-2, centreDepth+jz)
					scanKeepGoing = False
				iz += 1
				if iz > int(depth/2): scanKeepGoing = False
			scanKeepGoing = True
			while scanKeepGoing == True: # Scan for the edge of the platform
				if getBlock(foundationSchematic,x,y,centreDepth-iz) == AIR:
					print 'zz %s %s %s' % (x,y,iz)
					# Draw the stairs
					for jx in xrange(1,x-1):
						for jz in xrange(0,iz):
							if jz == iz-1 or jz == iz-2:
								for jy in xrange(0,foundationHeight):
									setBlock(foundationSchematic, WALLBLOCK, jx+1, jy, centreDepth-jz)
							else:
								setBlock(foundationSchematic, WALLBLOCK, jx+1, jx-2, centreDepth-jz)
					scanKeepGoing = False
				iz += 1
				if iz > int(depth/2): scanKeepGoing = False
			keepGoing = False
		x += 1
		if x > int(width/2): keeptGoing = false

	z = int(depth/2)
	y = 0
	x = 0
	keepGoing = True
	while keepGoing == True:
		if getBlock(foundationSchematic,width-x-1,y,z) != AIR: # Found a block, must be the platform at the top of the stairs.
			iz = 0
			scanKeepGoing = True
			while scanKeepGoing == True: # Scan for the edge of the platform
				if getBlock(foundationSchematic,width-x-1,y,centreDepth+iz) == AIR:
					print 'zz %s %s %s' % (x,y,iz)
					# Draw the stairs
					for jx in xrange(1,x-1):
						for jz in xrange(0,iz):
							if jz == iz-1 or jz == iz-2:
								for jy in xrange(0,foundationHeight):
									setBlock(foundationSchematic, WALLBLOCK, width-(jx+2), jy, centreDepth+jz)
							else:
								setBlock(foundationSchematic, WALLBLOCK, width-(jx+2), jx-2, centreDepth+jz)
					scanKeepGoing = False
				iz += 1
				if iz > int(depth/2): scanKeepGoing = False
			scanKeepGoing = True
			while scanKeepGoing == True: # Scan for the edge of the platform
				if getBlock(foundationSchematic,width-x-1,y,centreDepth-iz) == AIR:
					print 'zz %s %s %s' % (x,y,iz)
					# Draw the stairs
					for jx in xrange(1,x-1):
						for jz in xrange(0,iz):
							if jz == iz-1 or jz == iz-2:
								for jy in xrange(0,foundationHeight):
									setBlock(foundationSchematic, WALLBLOCK, width-(jx+2), jy, centreDepth-jz)
							else:
								setBlock(foundationSchematic, WALLBLOCK, width-(jx+2), jx-2, centreDepth-jz)
					scanKeepGoing = False
				iz += 1
				if iz > int(depth/2): scanKeepGoing = False
			keepGoing = False
		x += 1
		if x > int(width/2): keeptGoing = false		

	z = 0
	y = 0
	x = int(width/2)
	keepGoing = True
	while keepGoing == True:
		if getBlock(foundationSchematic,x,y,z) != AIR: # Found a block, must be the platform at the top of the stairs.
			ix = 0
			scanKeepGoing = True
			while scanKeepGoing == True: # Scan for the edge of the platform
				if getBlock(foundationSchematic,centreWidth+ix,y,z) == AIR:
					# Draw the stairs
					for jz in xrange(1,z-1):
						for jx in xrange(0,ix):
							if jx == ix-1 or jx == ix-2:
								for jy in xrange(0,foundationHeight):
									setBlock(foundationSchematic, WALLBLOCK, centreWidth+jx, jy, jz+1)
							else:
								setBlock(foundationSchematic, WALLBLOCK, centreWidth+jx, jz-2, jz+1)
					scanKeepGoing = False
				ix += 1
				if ix > int(width/2): scanKeepGoing = False
			scanKeepGoing = True
			while scanKeepGoing == True: # Scan for the edge of the platform
				if getBlock(foundationSchematic,centreWidth-ix,y,z) == AIR:
					# Draw the stairs
					for jz in xrange(1,z-1):
						for jx in xrange(0,ix):
							if jx == ix-1 or jx == ix-2:
								for jy in xrange(0,foundationHeight):
									setBlock(foundationSchematic, WALLBLOCK, centreWidth-jx, jy, jz+1)
							else:
								setBlock(foundationSchematic, WALLBLOCK, centreWidth-jx, jz-2, jz+1)
					scanKeepGoing = False
				ix += 1
				if ix > int(width/2): scanKeepGoing = False
			keepGoing = False
		z += 1
		if z > int(depth/2): keeptGoing = false		

	z = 0
	y = 0
	x = int(width/2)
	keepGoing = True
	while keepGoing == True:
		if getBlock(foundationSchematic,x,y,depth-z-1) != AIR: # Found a block, must be the platform at the top of the stairs.
			ix = 0
			scanKeepGoing = True
			while scanKeepGoing == True: # Scan for the edge of the platform
				if getBlock(foundationSchematic,centreWidth+ix,y,depth-z-1) == AIR:
					# Draw the stairs
					for jz in xrange(1,z-1):
						for jx in xrange(0,ix):
							if jx == ix-1 or jx == ix-2:
								for jy in xrange(0,foundationHeight):
									setBlock(foundationSchematic, WALLBLOCK, centreWidth+jx, jy, depth-(jz+2))
							else:
								setBlock(foundationSchematic, WALLBLOCK, centreWidth+jx, jz-2, depth-(jz+2))
					scanKeepGoing = False
				ix += 1
				if ix > int(width/2): scanKeepGoing = False
			scanKeepGoing = True
			while scanKeepGoing == True: # Scan for the edge of the platform
				if getBlock(foundationSchematic,centreWidth-ix,y,z) == AIR:
					# Draw the stairs
					for jz in xrange(1,z-1):
						for jx in xrange(0,ix):
							if jx == ix-1 or jx == ix-2:
								for jy in xrange(0,foundationHeight):
									setBlock(foundationSchematic, WALLBLOCK, centreWidth-jx, jy, depth-(jz+2))
							else:
								setBlock(foundationSchematic, WALLBLOCK, centreWidth-jx, jz-2, depth-(jz+2))
					scanKeepGoing = False
				ix += 1
				if ix > int(width/2): scanKeepGoing = False
			keepGoing = False
		z += 1
		if z > int(depth/2): keeptGoing = false	
		
	# Create the doors

	# Create the Gardens
	
	treeW = f+dw
	treeD = f+dd
	treeOpts = { 'Edge block:': alphaMaterials.Leaves,
					 'Operation': method, 
					 'Light block:': alphaMaterials.Wood, 
					 'Fill block:': alphaMaterials.Wood}

	# 1
	if randint(0,99) > 30:
		treeH = randint(int(hh/2),hh+f)
		treeBox = BoundingBox((box.minx,box.miny,box.minz),(treeW,treeH,treeD))
		draw3DTree(foundationSchematic, treeBox, treeOpts)
	# 2
	if randint(0,99) > 30:
		treeH = randint(int(hh/2),hh+f)
		treeBox = BoundingBox((box.minx-f-dw,box.miny,box.minz),(treeW,treeH,treeD))
		draw3DTree(foundationSchematic, treeBox, treeOpts)
	# 3
	if randint(0,99) > 30:
		treeH = randint(int(hh/2),hh+f)
		treeBox = BoundingBox((box.maxx-f-dw,box.miny,box.maxz+-f-dd),(treeW,treeH,treeD))
		draw3DTree(foundationSchematic, treeBox, treeOpts)
	# 4
	if randint(0,99) > 99:
		treeH = randint(int(hh/2),hh+f)
		treeBox = BoundingBox((box.minx,box.miny,box.maxz-f-dd),(treeW,treeH,treeD))
		draw3DTree(foundationSchematic, treeBox, treeOpts)
	else:
		treeH = randint(int(hh/2),hh+f)
		lakeBox = BoundingBox((0,0,0),(treeW,treeH,treeD))
		lakeSchematic = MCSchematic((treeW,treeH,treeD))
		Lake(lakeSchematic, lakeBox, "")
		foundationSchematic.copyBlocksFrom(lakeSchematic, lakeBox, (box.minx,box.miny,box.maxz-f-dd),b)
	
##	f = abs(foundationHeight)
##	dw = abs(leftRightFacadeDepth)
##	dd = abs(frontBackFacadeDepth)
##	w = abs(width-2*dw-2*f)
##	d = abs(depth-2*dd-2*f)
##	hh = abs(height-f-roofDepth)

	
	roomBox = BoundingBox((f+dw,foundationHeight,f+dd),(w,height-roofDepth-foundationHeight,d))
	PalladioBuildingInterior(foundationSchematic, BoundingBox((width,foundationHeight+height,depth)), roomBox, options, WALLBLOCK, groundFloorHeight, upperLevelHeight, foundationHeight, roofDepth )
	
	y=0
	for x in xrange(0,width):
		for z in xrange(0,depth):
			if getBlock(foundationSchematic,x,y,z) == AIR:
				setBlock(foundationSchematic,GRASSBLOCK,x,y,z)

	FuncEnd(level,box,"",method)
	return foundationSchematic

def complex_buildingRoof(box, wallMaterial, slabMaterial, roofMaterial, roofSlabMaterial):
	method = "complex_buildingRoof"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	
	for x in xrange(0,int(width/2)+1):
		for z in xrange(0,int(depth/2)+1):
			y = x
			if z < y: y = z
			(blockID,blockData) = roofSlabMaterial
			if y%2 == 1: blockData += 8 # Upper slab
			y = int(y/2)
			if y >= height-1: y = height-1
			setBlock(level, (blockID,blockData), x, y, z)
			setBlock(level, (blockID,blockData), width-x-1, y, z)
			setBlock(level, (blockID,blockData), x, y, depth-z-1)
			setBlock(level, (blockID,blockData), width-x-1, y, depth-z-1)
		
	FuncEnd(level,box,"",method)
	return level	
		
def complex_facade(box, wallMaterial, slabMaterial, roofMaterial, roofSlabMaterial, groundFloorHeight, upperLevelHeight):
	method = "complex_facade"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	
	# A faced is a collection of primitive shapes within and extending from a wall.
	# It includes:
	# Archways / pillars ||
	# Doors []
	# Windows 
	# Roof segments /\
	# Misc. other bits and pieces.
	
	# The input box is the size of the facade, including any protruding attached structures
	ARCHWIDTH = 6
	# First the basic wall
	wallDepth = 3 # 0=Inside, 1=outside, 2=external detail layer
	wallBox = BoundingBox((0,0,0),(width, height, wallDepth))
	wallSchematic = primitive_wall(wallBox, wallMaterial, slabMaterial, groundFloorHeight, upperLevelHeight)
	level.copyBlocksFrom(wallSchematic, wallBox, (box.minx,box.miny,box.minz))
	
	# Now the protruding patio
	patioDepth = depth - wallDepth
	patioWidth = int(floor(randint(int(width/3),width)/ARCHWIDTH))*ARCHWIDTH
	patioBox = BoundingBox((0,0,0),(patioWidth, height, patioDepth))
	patioSchematic = complex_patio(patioBox, wallMaterial, slabMaterial, roofMaterial, roofSlabMaterial, groundFloorHeight)
	b=range(4096); b.remove(0)
	level.copyBlocksFrom(patioSchematic, patioBox, (box.minx+int(ceil((width-patioWidth)/2)),box.miny,box.minz+wallDepth-1),b) # Copy in the patio
	
	FuncEnd(level,box,"",method)
	return level
	
def complex_patio(box, wallMaterial, slabMaterial, roofMaterial, roofSlabMaterial, groundFloorHeight):
	method = "complex_patio"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	
	archesBox = BoundingBox((0,0,0),(width,groundFloorHeight,depth))
	archesSchematic = complex_arches(archesBox, wallMaterial, slabMaterial, ceil(groundFloorHeight / 8 * 7))
	b=range(4096); b.remove(0)
	level.copyBlocksFrom(archesSchematic, archesBox, (box.minx,box.miny,box.minz),b) # Copy in the patio
	# Patio roof
	roofBox = BoundingBox((0,0,0),(width,height-groundFloorHeight,depth))
	roofSchematic = complex_roof(roofBox, wallMaterial, slabMaterial, roofMaterial, roofSlabMaterial)
	level.copyBlocksFrom(roofSchematic, roofBox, (box.minx,box.miny+groundFloorHeight,box.minz),b) # Copy in the patio
	
	FuncEnd(level,box,"",method)
	return level

def complex_roof(box, wallMaterial, slabMaterial, roofMaterial, roofSlabMaterial):
	method = "complex_roof"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	
	OFFSET = 0
	# Base
	for x in xrange(0,width):
		for z in xrange(0,depth-OFFSET):
			setBlock(level, wallMaterial, x, 0, z)
	
	(roofSlabID,roofSlabData) = roofSlabMaterial
	# Tiles
	for x in xrange(0,int(ceil(width/2))):
		for z in xrange(0,depth-OFFSET):
			if z < depth-OFFSET-1:
				for y in xrange(0,int(x/2)):
					setBlock(level, wallMaterial, x, y+1, z)
					setBlock(level, wallMaterial, width-x-1, y+1, z)
			elif z == depth-OFFSET-1:
				setBlock(level, wallMaterial, x, int(x/2), z)
				setBlock(level, wallMaterial, width-x-1, int(x/2), z)
			materialData = roofSlabData
			if x%2 == 1: materialData = materialData+8 # Upper slab
			setBlock(level, (roofSlabID,materialData), x, int(x/2)+1, z)
			setBlock(level, (roofSlabID,materialData), width-1-x, int(x/2)+1, z)
#	if width%2 == 1: # Central bit
	x = width/2
	for z in xrange(0,depth-OFFSET):
		if z < depth-OFFSET-1:
			for y in xrange(0,int(x/2)):
				setBlock(level, wallMaterial, x, y+1, z)
				setBlock(level, wallMaterial, width-x-1, y+1, z)
		materialData = roofSlabData
		if x%2 == 1: materialData = materialData+8 # Upper slab
		setBlock(level, (roofSlabID,materialData), x, int(x/2)+1, z)
		setBlock(level, (roofSlabID,materialData), width-1-x, int(x/2)+1, z)
	
	
	FuncEnd(level,box,"",method)
	return level
	
def complex_arches(box, archMaterial, slabMaterial, archHeight):
	method = "complex_arches"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	AIR = (0,0)
	ARCHWIDTH = 6 #randint(6,6)
	MAINARCHWIDTH = randint(ARCHWIDTH,ARCHWIDTH*8)
	ARCHDEPTH = 2
	
	# Work out the number of arches dimensions
	numArchesWidth = abs(int(((width-1)-MAINARCHWIDTH)/ARCHWIDTH))
	halfNumArchesWidth = int(floor(numArchesWidth/2)) # I will make the patio symmetric around the centre
	numArchesDepth = int((depth-2)/ARCHWIDTH)
	MAINARCHWIDTH = abs(width-2*halfNumArchesWidth*ARCHWIDTH) # Correct for rounding errors
	print 'MAINARCHWIDTH: %s HALFNUMARCHESWIDTH: %s' % (MAINARCHWIDTH, halfNumArchesWidth)
	# Build an arch
	archBox = BoundingBox((0,0,0),(ARCHWIDTH,height,ARCHDEPTH))
	archSchematic = primitive_arch(archBox, archHeight, int(ARCHWIDTH/2)-1, archMaterial )

	# Build the main arch
	mainArchBox = BoundingBox((0,0,0),(MAINARCHWIDTH,height,ARCHDEPTH))
	mainArchSchematic = primitive_arch(mainArchBox, archHeight, int(MAINARCHWIDTH/2)-1, archMaterial )
	
	rotArchSchem = rotateXZ90Degrees( archSchematic, archBox )
	rotArchBox = BoundingBox((0,0,0),(ARCHDEPTH,height,ARCHWIDTH))

	# Fill the middle section with Columns
	colBox = BoundingBox((0,0,0),(3,height,3))
	colSchematic = primitive_column(colBox,archMaterial,slabMaterial)
	halfNumCols = int(floor(MAINARCHWIDTH/2/ARCHWIDTH)) #+1
	b=range(4096); b.remove(0)
	
#	if halfNumArchesWidth > 0:
	for i in xrange(0, halfNumCols):
#		print colBox
#		print colSchematic
#		print level
#		print (ARCHWIDTH*(halfNumArchesWidth+i),0,(numArchesDepth)*ARCHWIDTH-1)
#		print ARCHWIDTH
#		print halfNumArchesWidth
#		print i
#		print numArchesDepth
#		print ARCHWIDTH*(halfNumArchesWidth+i)
#		print (numArchesDepth)*ARCHWIDTH-1
		try:
			level.copyBlocksFrom(colSchematic, colBox, (ARCHWIDTH*(halfNumArchesWidth+i),0,(numArchesDepth)*ARCHWIDTH-1),b)
		except:
			print 'Skipped arch: %s %s %s %s', (colSchematic, colBox, (ARCHWIDTH*(halfNumArchesWidth+i),0,(numArchesDepth)*ARCHWIDTH-1))
		try:
			level.copyBlocksFrom(colSchematic, colBox, (width-ARCHWIDTH*(halfNumArchesWidth+i)-3,0,(numArchesDepth)*ARCHWIDTH-1),b)
		except:
			print 'Skipped arch: %s %s %s %s', (colSchematic, colBox, (width-ARCHWIDTH*(halfNumArchesWidth+i)-3,0,(numArchesDepth)*ARCHWIDTH-1))
	
	for i in xrange(0,numArchesDepth):
		# Copy in the Depth-wise arches to the depth of the structure
		try:
			level.copyBlocksFrom(rotArchSchem, rotArchBox, (0,0,i*ARCHWIDTH))
		except:
			print 'Skipped arch: %s %s %s', (rotArchSchem, rotArchBox, (0,0,i*ARCHWIDTH))
		try:
			level.copyBlocksFrom(rotArchSchem, rotArchBox, (width-ARCHDEPTH,0,i*ARCHWIDTH))
		except:
			print 'Skipped arch: %s %s %s', (rotArchSchem, rotArchBox, (width-ARCHDEPTH,0,i*ARCHWIDTH))
			
	for i in xrange(0,halfNumArchesWidth):
		try:
			level.copyBlocksFrom(archSchematic, archBox, (i*ARCHWIDTH,0,(numArchesDepth)*ARCHWIDTH))
		except:
			print 'Skipped arch: %s %s %s', (archSchematic, archBox, (i*ARCHWIDTH,0,(numArchesDepth)*ARCHWIDTH))
		try:
			level.copyBlocksFrom(archSchematic, archBox, (width-(i+1)*ARCHWIDTH,0,(numArchesDepth)*ARCHWIDTH))
		except:
			print 'Skipped arch: %s %s %s', (archSchematic, archBox, (width-(i+1)*ARCHWIDTH,0,(numArchesDepth)*ARCHWIDTH))
#	level.copyBlocksFrom(mainArchSchematic, mainArchBox, (ARCHWIDTH*halfNumArchesWidth,0,depth-ARCHDEPTH))

	
	FuncEnd(level,box,"",method)
	return level
	
def primitive_wall(box, wallMaterial, slabMaterial, groundFloorHeight, upperLevelHeight):
	method = "primitive_wall"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	
	# Fill the solid parts of the wall
	for z in xrange(0,2):
		for x in xrange(0,width):
			for y in xrange(0, height):
				# print '%s %s %s: %s' % (x,y,z, wallMaterial)
				setBlock(level, wallMaterial, x, y, z)

	heightMap = []
#	if groundFloorHeight <= box.maxy:
#		heightMap.append(groundFloorHeight)
	stories = ((box.maxy - groundFloorHeight)/upperLevelHeight)%upperLevelHeight
	for i in xrange(0,stories+1):
		heightMap.append(groundFloorHeight+i*upperLevelHeight)

	# Draw slabs at the floor levels
	z = 2
	for x in xrange(0,width):
		for y in heightMap:
			setBlock(level, slabMaterial, x, y, z)
		
	FuncEnd(level,box,"",method)
	return level

def primitive_column(box, columnMaterial, slabMaterial):
	method = "primitive_column"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	(slabID,slabData) = slabMaterial
	for y in xrange(0,height):
		for z in xrange(0,depth):
			for x in xrange(0,width):
				if y == 0:
					setBlock(level, slabMaterial, x, y, z)
				elif y == height-1:
					setBlock(level, (slabID,slabData+8), x, y, z)
				if x == centreWidth and z == centreDepth:
					setBlock(level, columnMaterial, x, y, z)

	FuncEnd(level,box,"",method)
	return level	
	
def primitive_arch(box, archHeight, archRadius, archMaterial):
	method = "primitive_arch"
	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log start
	# Render an arch of the required dimensions
	# layer = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,1)) # One arch layer, for blitting later
	
	#########
	###   ###
	##  o  ##
	##     ##
	##     ##

	AIR = (0,0)
	fill(level, BoundingBox((0,0,0),(width,height,depth)), archMaterial)
	
	centreY = int(ceil(archHeight-archRadius))
	centreX = int(ceil(width/2))
	for z in xrange(0,depth):
		# Clear out the bottom section below the round part
		for x in xrange(int(-archRadius),int(archRadius)):
			for y in xrange(0,centreY):
				setBlock(level, AIR, centreX+x, y, z)
		# Now let's wrestle with the arch. Cos will be our friend
		halfPi = pi/2
		for y in xrange(centreY, int(ceil(archHeight))):
			radiusHere = archRadius*cos(pi/2*(y-centreY)/archRadius)
#			print radiusHere
			for x in xrange(int(-radiusHere),int(radiusHere)):
				setBlock(level, AIR, centreX+x, y, z)
	
	# Blit all the layers along the depth of the box
#	bbox = BoundingBox((0,0,0),(width,height,1))
#	for z in xrange(0,depth):
#		level.copyBlocksFrom(layer, bbox, (0,0,z))
	FuncEnd(level,box,"",method) # Log end
	return level
	
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

############# GFX PRIMITIVES #############

def setBlockIfEmpty(level, (block, data), x, y, z):
	tempBlock = level.blockAt(x,y,z)
	if tempBlock == 0:
		setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def fill(level, box, material):
	for (x, y, z) in box.positions: #@naor2012 
		setBlock(level, material, x, y, z)

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

def rotateXZ90Degrees( schematic, box ):
	(width, height, depth) = (box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)
	level = MCSchematic((depth, height, width)) # Working object
	
	for y in xrange(0,height):
		for z in xrange(0,depth):
			for x in xrange(0,width):
				theBlock = getBlock(schematic,box.minx+x,box.miny+y,box.minz+z)
				setBlock(level, theBlock, z, y, x)
	
	return level
	

			
############# GFX  #############			
			
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

def draw3DTree(level, box, options):
	method = "draw3DTree"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	material = (fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	ANGLESTEP = pi/180
	TwoPI = 2*pi

	(x0,y0,z0) = (centreWidth,0,centreDepth)
	
	drawLine(level, material,
					(box.minx+x0-1,box.miny+y0,box.minz+z0), 
					(box.minx+x0-1,box.miny+y0+height/3,box.minz+z0))
	drawLine(level, material,
					(box.minx+x0+1,box.miny+y0,box.minz+z0), 
					(box.minx+x0+1,box.miny+y0+height/3,box.minz+z0))
	drawLine(level, material,
					(box.minx+x0,box.miny+y0,box.minz+z0+1), 
					(box.minx+x0,box.miny+y0+height/3,box.minz+z0+1))
	drawLine(level, material,
					(box.minx+x0,box.miny+y0,box.minz+z0-1), 
					(box.minx+x0,box.miny+y0+height/3,box.minz+z0-1))
	drawLine(level, material,
					(box.minx+x0,box.miny+y0,box.minz+z0), 
					(box.minx+x0,box.miny+y0+height/3,box.minz+z0))

	MANGLE = 90*((width+depth)/2)/height
	

	draw3DTreeBranch(level, box, options, height/3, (x0,y0+height/3,z0), randint(0,360)*ANGLESTEP, (90+randint(-MANGLE,MANGLE))*ANGLESTEP, randint(30,60)) 
	
	t = (int)(MANGLE / 4)
	if t < 4:
		t = 4
	for iter in xrange(0,t):
		draw3DTreeBranch(level, box, options, height/3, (x0,y0+randint(height/5,height/3),z0), randint(0,360)*ANGLESTEP, (90+randint(-MANGLE,MANGLE))*ANGLESTEP, randint(MANGLE/3,MANGLE)) 

#	draw3DTreeBranch(level, box, options, height/3, (x0,y0+randint(height/5,height/3),z0), randint(0,360)*ANGLESTEP, (90+randint(-80,80))*ANGLESTEP, randint(30,60)) 
	
def draw3DTreeBranch(level, box, options, depth, (x0,y0,z0), theta, phi, angle):
	ANGLESTEP = pi/180
	TwoPI = 2*pi
	ANGLERANGE = angle
	
	#material = (options["Light block:"].ID, options["Light block:"].blockData)
	material = (options["Fill block:"].ID, options["Fill block:"].blockData)
	
	if depth == 1:
		material = (options["Edge block:"].ID, options["Edge block:"].blockData)

	if depth:
		#print '%s %s %s %s %s' % (x0, theta, cos(theta), phi, depth)
		(x2, y2, z2) = getRelativePolar((x0,y0,z0), (theta, phi, depth))
		
		drawLine(level, material,
						(box.minx+x0,box.miny+y0,box.minz+z0), 
						(box.minx+x2,box.miny+y2,box.minz+z2))

		for iter in xrange(0,randint(3,11)):
			draw3DTreeBranch(level, box, options, depth/2, (x2, y2, z2), theta+randint(-ANGLERANGE,ANGLERANGE)*ANGLESTEP, phi+randint(-ANGLERANGE,ANGLERANGE)*ANGLESTEP,angle)	
			
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	
def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
	
def Lake(level, box, options):
	# Randomly make a lake, surrounded by reeds, farmland, crops, etc.
	method = "Lake"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)
	# Block Palette
	WaterBlock = (alphaMaterials.Water.ID, alphaMaterials.Water.blockData)
	FarmlandBlock = (alphaMaterials.Farmland.ID, 7) # Saturated
	
	maxSize = int(centreWidth)
	if maxSize > 6:
		lakeSizeWidth = randint(6,maxSize)
		edgeWidth = lakeSizeWidth+randint(0,4)
		angle = pi/180*randint(0,359)
		eRX = float((centreWidth-lakeSizeWidth) * cos(angle))
		eRZ = float((centreDepth-lakeSizeWidth) * sin(angle))
		radius = randint(1,int(float(sqrt(eRX*eRX+eRZ*eRZ))))
		# print 'Lake %s %s %s' % (radius,eRZ,eRZ)
		px = centreWidth+float(radius * cos(angle))
		pz = centreDepth+float(radius * sin(angle))
		
		bboxEdge = BoundingBox((box.minx+px-edgeWidth,box.miny,box.minz+pz-edgeWidth),(edgeWidth*2,1,edgeWidth*2))
		drawRandomSplodge(level, bboxEdge, options, FarmlandBlock, -1, False, 0.1*randint(1,5), randint(4,720), randint(2,6))	

		bbox = BoundingBox((box.minx+px-lakeSizeWidth,box.miny,box.minz+pz-lakeSizeWidth),(lakeSizeWidth*2,1,lakeSizeWidth*2))
		drawRandomSplodge(level, bbox, options, WaterBlock, -1, False, 0.1*randint(1,5), randint(4,720), randint(2,6))	

		# Add some character to the grass and dirt sections
		if randint(0,100) <= 90:
			blocksToPlace = [ (alphaMaterials.Crops.ID, randint(3,7)),
								(alphaMaterials.Carrots.ID, randint(3,7)),
								(alphaMaterials.Potatoes.ID, randint(3,7)),
								(alphaMaterials.MelonStem.ID, randint(3,7)),
								(alphaMaterials.PumpkinStem.ID, randint(3,7))
							]
			materialToPlaceOn = [ FarmlandBlock	]
			numberOfTries = width + depth + height
			bbox = BoundingBox((box.minx,box.miny+1,box.minz),(width,1,depth))
			sprinkle(level, bboxEdge, options, blocksToPlace, materialToPlaceOn, numberOfTries)
	
	FuncEnd(level, box, options, method)
	
def drawRandomSplodge(level, box, options, material, innerRadius, edgeOnly, STEPSIZE, ANGLES, PARTITION):
	method = "drawRandomSplodge"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Determine the profile of the Radius around the circumference of the disc
	if ANGLES < 360:
		ANGLES = 360
	
	ANGLE = 2*pi/ANGLES
	numberOfWaves = randint(1,3)
	
#	periods = []
#	for iter in xrange(0,numberOfWaves):
#		scalar = randint(1,5)
#		periods.append(0.4*scalar)
#	theShape = []
#	for iter in xrange(0,360):
#		theShape.append(1.0)
#		for iterX in xrange(0, len(periods)):
#			theShape[iter] = theShape[iter]*sin(ANGLE*iter*periods[iterX])
#
#	print periods
#	print theShape

	if STEPSIZE < 0.1:
		STEPSIZE = 0.2
	if STEPSIZE > 1.0:
		STEPSIZE = 0.2
		
	theShape = []
	for iter in xrange(0,ANGLES):
		theShape.append(1.0)

	randWalker=1.0
	startPos = randint(0,ANGLES-1)
	for iter in xrange(0,ANGLES):
#		theShape.append(1.0)
		r = randint(0,100)
		if r < 30:
			randWalker = randWalker+STEPSIZE
		elif r > 70:
			randWalker = randWalker-STEPSIZE
		if randWalker < 0:
			randWalker = 0
		if randWalker > 10:
			randWalker = 10
		
		if randWalker - ((startPos+ANGLES-iter)%ANGLES) > theShape[startPos]:
			randWalker = randWalker - 1
		theShape[(startPos+iter)%ANGLES] = 0.1*randWalker
			
	for iterX in xrange(-centreWidth,centreWidth):
		for iterZ in xrange(-centreDepth,centreDepth):
			angle = atan2(iterZ,iterX)
			radiusHere = float(sqrt(iterX * iterX + iterZ * iterZ))
			eRX = float(centreWidth * cos(angle))
			eRZ = float(centreDepth * sin(angle))
#			print theShape[int(angle/ANGLE)]
#			print int(angle/ANGLE)
			edgeRadiusHere = float(sqrt(eRX*eRX+eRZ*eRZ))
			edgeRadiusHere = edgeRadiusHere/PARTITION*(PARTITION-1) + edgeRadiusHere/PARTITION*abs(theShape[int(angle/ANGLE)])
			#print '%s %s %s %s %s %s %s' % (angle,rX,rZ,radiusHere,eRX,eRZ,edgeRadiusHere)
			if radiusHere > innerRadius and ((radiusHere < edgeRadiusHere) and edgeOnly == False) or ((abs(radiusHere-(edgeRadiusHere-1))<=1.0) and edgeOnly == True):
				for iterY in xrange(0,height):
						setBlock(level, material, box.minx+centreWidth+iterX,box.miny+iterY,box.minz+centreDepth+iterZ )
			
						
				#drawLine(level, material, (box.minx+centreWidth+iterX,box.miny,box.minz+centreDepth+iterZ), (box.minx+centreWidth+iterX,box.miny+height-1,box.minz+centreDepth+iterZ) )
	print '%s: Ended at %s' % (method, time.ctime())	

def Factorise(number):
	Q = []
	
	for iter in xrange(1,(int)(number+1)):
		p = (int)(number/iter)
		if number - (p * iter) == 0:
			if iter not in Q:
				Q.append(iter)
			if p not in Q:
				Q.append(p)

#	print 'Factors of %s are:' % (number)
#	for iter in Q:
#		print '%s,' % (iter)
	
	return Q
	
def sprinkle(level, box, options, blocksToPlace, materialToPlaceOn, numberOfTries):
	# This places a number of blocks in the box, but only above the types of materials nominated
	AIR = (0,0)
	
	for iter in xrange(0, numberOfTries):
		randX = randint(box.minx,box.maxx)
		randY = randint(box.miny,box.maxy)
		randZ = randint(box.minz,box.maxz)
		
		blockBelow = (level.blockAt(int(randX), randY-1, int(randZ)),level.blockDataAt(int(randX), randY-1, int(randZ)))
		block = (level.blockAt(int(randX), randY, int(randZ)),level.blockDataAt(int(randX), randY, int(randZ)))
		# print 'Sprinkling: %s %s' % (block, blockBelow)
		if block == AIR and blockBelow in materialToPlaceOn:
			setBlock(level, blocksToPlace[randint(0,len(blocksToPlace)-1)], randX, randY, randZ)
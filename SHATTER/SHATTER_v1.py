# This filter is for fracturing your world.
# abrightmoore@yahoo.com.au
# http://brightmoore.net

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
from random import Random # @Codewarrior0

inputs = (
		("SHATTER", "label"),
		("Operation", (
			"Quake",
			"Explode",
			"Compress",
  		    )),
		("Epicentres", 10),
		("Fracture Planes", 20),
		("Quantum", 0.5),
		("Scale", 5),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = options["Operation"]
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = True
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation

	if method == "Explode":
		Explode(level, box, options)
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False # Suppress additional copyback

	elif method == "Quake":
		Quake(level, box, options) 
		#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False # Suppress additional copyback

	elif method == "Compress":
		Compress(level, box, options) 
		#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False # Suppress additional copyback

		
		# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end

def Quake(level, box, options):
	method = "Quake"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)

	# Within the selection box, dislocate 'slabs' of material vertically / horizontally to simulate quake damage
	
	# Step 1 - define a fault line
	# Step 2 - for each side of the line, move + or - x,z,y by some amount
	
	r = Random()
	scratch = MCSchematic((width,height,depth))
	box = BoundingBox((0,0,0),(width,height,depth))

	Q = []
	fractures = options["Fracture Planes"]
	print fractures
	epicentres = options["Epicentres"]
	quantum = options["Quantum"]
	for i in xrange(0,epicentres):
		epiX = centreWidth+randint(-int(centreWidth/2),int(centreWidth/2))
		epiY = centreHeight+randint(-int(centreHeight/2),int(centreHeight/2))
		epiZ = centreDepth+randint(-int(centreDepth/2),int(centreDepth/2))
		for iter in xrange(0,fractures):
			slope = r.random() * pi * 2 # x/z angle of the fault line
			slant = r.random() * pi # vertical pitch of the fault line
			(planeX,planeY,planeZ) = (cos(slope)*sin(slant),cos(slant),sin(slope)*sin(slant))
			denom = (planeX*planeX + planeY*planeY + planeZ*planeZ)
			max = randint(1,options["Scale"])
			(shiftX1,shiftY1,shiftZ1) = (randint(-max,max)*quantum,randint(-max,max)*quantum,randint(-max,max)*quantum)
			(shiftX2,shiftY2,shiftZ2) = (randint(-max,max)*quantum,randint(-max,max)*quantum,randint(-max,max)*quantum)

			Q.append(((planeX,planeY,planeZ,denom,epiX,epiY,epiZ),(shiftX1,shiftY1,shiftZ1),(shiftX2,shiftY2,shiftZ2)))
		
	RenderShatteredLand(level,scratch,Q,width,height,depth)
				
	# Copy result from working set
	#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level.copyBlocksFrom(scratch, box, (0,0,0 ))
	
	FuncEnd(level,box,options,method)	
	
def Explode(level, box, options):
	method = "Explode"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)

	# Within the selection box, dislocate 'slabs' of material vertically / horizontally to simulate quake damage
	
	# Step 1 - define a fault line
	# Step 2 - for each side of the line, move the pieces apart
	
	r = Random()
	scratch = MCSchematic((width,height,depth))
	box = BoundingBox((0,0,0),(width,height,depth))

	Q = []
	fractures = options["Fracture Planes"]
	print fractures
	epicentres = options["Epicentres"]
	quantum = options["Quantum"]
	for i in xrange(0,epicentres):
		epiX = centreWidth+randint(-int(centreWidth/2),int(centreWidth/2))
		epiY = centreHeight+randint(-int(centreHeight/2),int(centreHeight/2))
		epiZ = centreDepth+randint(-int(centreDepth/2),int(centreDepth/2))
		for iter in xrange(0,fractures):
			slope = r.random() * pi * 2 # x/z angle of the fault line
			slant = r.random() * pi # vertical pitch of the fault line
			(planeX,planeY,planeZ) = (cos(slope)*sin(slant),cos(slant),sin(slope)*sin(slant))
			denom = (planeX*planeX + planeY*planeY + planeZ*planeZ)
			max = randint(1,options["Scale"])
			(shiftX1,shiftY1,shiftZ1) = (cos(slope)*sin(slant)*quantum,cos(slant)*quantum,sin(slope)*sin(slant)*quantum)
			(shiftX2,shiftY2,shiftZ2) = (-cos(slope)*sin(slant)*quantum,-cos(slant)*quantum,-sin(slope)*sin(slant)*quantum)

			Q.append(((planeX,planeY,planeZ,denom,epiX,epiY,epiZ),(shiftX1,shiftY1,shiftZ1),(shiftX2,shiftY2,shiftZ2)))
		
	RenderShatteredLand(level,scratch,Q,width,height,depth)
				
	# Copy result from working set
	#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level.copyBlocksFrom(scratch, box, (0,0,0 ))
	
	FuncEnd(level,box,options,method)	

def Compress(level, box, options):
	method = "Compress"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)

	# Within the selection box, dislocate 'slabs' of material vertically / horizontally to simulate quake damage
	
	# Step 1 - define a fault line
	# Step 2 - for each side of the line, move the pieces apart
	
	r = Random()
	scratch = MCSchematic((width,height,depth))
	box = BoundingBox((0,0,0),(width,height,depth))

	Q = []
	fractures = options["Fracture Planes"]
	print fractures
	epicentres = options["Epicentres"]
	quantum = options["Quantum"]
	for i in xrange(0,epicentres):
		epiX = centreWidth+randint(-int(centreWidth/2),int(centreWidth/2))
		epiY = centreHeight+randint(-int(centreHeight/2),int(centreHeight/2))
		epiZ = centreDepth+randint(-int(centreDepth/2),int(centreDepth/2))
		for iter in xrange(0,fractures):
			slope = r.random() * pi * 2 # x/z angle of the fault line
			slant = r.random() * pi # vertical pitch of the fault line
			(planeX,planeY,planeZ) = (cos(slope)*sin(slant),cos(slant),sin(slope)*sin(slant))
			denom = (planeX*planeX + planeY*planeY + planeZ*planeZ)
			max = randint(1,options["Scale"])
			(shiftX1,shiftY1,shiftZ1) = (-cos(slope)*sin(slant)*quantum,-cos(slant)*quantum,-sin(slope)*sin(slant)*quantum)
			(shiftX2,shiftY2,shiftZ2) = (cos(slope)*sin(slant)*quantum,cos(slant)*quantum,sin(slope)*sin(slant)*quantum)

			Q.append(((planeX,planeY,planeZ,denom,epiX,epiY,epiZ),(shiftX1,shiftY1,shiftZ1),(shiftX2,shiftY2,shiftZ2)))
		
	RenderShatteredLand(level,scratch,Q,width,height,depth)
				
	# Copy result from working set
	#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level.copyBlocksFrom(scratch, box, (0,0,0 ))
	
	FuncEnd(level,box,options,method)	
	
def RenderShatteredLand(level,scratch,Q,width,height,depth):
	for iterY in xrange(0,height):
		print iterY
		for iterZ in xrange(0,depth):
			for iterX in xrange(0,width):
				# read from level, write to scratch.
				mat = getBlock(level,iterX,iterY,iterZ)
				if mat != (0,0):
					(deltaX,deltaY,deltaZ) = (0,0,0)
					for iter in xrange(0,len(Q)):
						((planeX,planeY,planeZ,denom,epiX,epiY,epiZ),(shiftX1,shiftY1,shiftZ1),(shiftX2,shiftY2,shiftZ2)) = Q[iter]
				
						dist = 1
						# Where is this point relative to the plane?
						if denom != 0:
							dist = (planeX*(epiX-iterX) + planeY*(epiY-iterY) + planeZ*(epiZ-iterZ)) / (planeX*planeX + planeY*planeY + planeZ*planeZ)
						
						if dist <=0:
							(deltaX,deltaY,deltaZ) = (deltaX+shiftX1,deltaY+shiftY1,deltaZ+shiftZ1)
						else:
							(deltaX,deltaY,deltaZ) = (deltaX+shiftX2,deltaY+shiftY2,deltaZ+shiftZ2)
					setBlock(scratch,mat, iterX+deltaX,iterY+deltaY,iterZ+deltaZ)

	
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))
	
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
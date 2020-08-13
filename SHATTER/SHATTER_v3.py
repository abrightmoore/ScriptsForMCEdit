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

# GLOBAL
CHUNKSIZE = 16

inputs = (
		("SHATTER", "label"),
		("Operation", (
			"Quake",
			"Explode",
			"Compress",
			"Pressure",
			"Expand"
  		    )),
		("Epicentres", 10),
		("Fracture Planes", 20),
		("Quantum", 0.5),
		("Scale", 5),
		("Show Planes?", False),
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

	elif method == "Pressure":
		Pressure(level, box, options) 
		#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False # Suppress additional copyback

	elif method == "Expand":
		Expand(originalLevel, originalBox, options) 
		#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
#		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
#		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False # Suppress additional copyback

		
		# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end

def Expand(level, box, options):
	# I pulled the connected-block scan code from my SELECTOR filter
	method = "Expand"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)
	AIR = (0,0)
	DIAGONAL = True
	GAP = options["Scale"]
	
	# Save - because I am a destructive beast
	SAVED = level.extractSchematic(box) # Best I can do is save the selection and restore it later
	
	# Scan through the selection box. Find all the connected blocks of the same type and create new schematics with only those blocks.

	# Find the largest dimension. We need it for a scratchpad to track progress.
	SIZE = width
	if depth > SIZE:
		SIZE = depth
	if height > SIZE:
		SIZE = height
	trackx = SIZE # Centre of the tracking schematic
	tracky = SIZE
	trackz = SIZE
	
	Components = []
	
	print 'Looking for connected sets of blocks...'
	for iterY in xrange(0,height):
		for iterZ in xrange(0,depth):
			for iterX in xrange(0,width):
				(matBlock,matID) = getBlock(level,box.minx+iterX,box.miny+iterY,box.minz+iterZ)
				if (matBlock,matID) != AIR: # Something to work with, scan the surroundings for connected blocks of the same type, and if found then build out a connected graph of blocks
					print 'Connecting blocks from %s %s %s' % (iterX,iterY,iterZ)
					# Find all of the connected blocks
					WORKING = MCSchematic((2*SIZE,2*SIZE,2*SIZE)) # temp - track progress finding connected blocks.
					minx = width-1 # Track extremities, we'll blit out these blocks later.
					miny = height-1
					minz = depth-1
					maxx = 0
					maxy = 0
					maxz = 0
					
					Q = []
					Q.append( (iterX,iterY,iterZ) )
					numBlocks = 0
					while len(Q) > 0:
						(x, y, z) = Q.pop()
						print 'Checking block %s %s %s for Block %s' % (x,y,z,matBlock)
						tx = trackx+x
						ty = tracky+y
						tz = trackz+z
						((block,ID),NBT) = getBlockWithNBT(level,box.minx+x,box.miny+y,box.minz+z)
						#(block,ID) = getBlock(level,box.minx+x,box.miny+y,box.minz+z)
						# print '...found Block %s' % (block)
						if block == matBlock:
							# print 'Block %s matches %s at %s %s %s' % (block, matBlock, x,y,z)
							if getBlock(WORKING,tx,ty,tz) == AIR:
								numBlocks += 1
								setBlockWithNBT(WORKING, (matBlock,matID), NBT, int(tx), int(ty), int(tz)) # Mark this block as 'traversed'
								#setBlock(WORKING, (matBlock,matID), int(tx), int(ty), int(tz)) # Mark this block as 'traversed'
								setBlock(level, AIR, box.minx+x, box.miny+y, box.minz+z) # erase the source block

								if x < minx:
									minx = x
								if y < miny:
									miny = y
								if z < minz:
									minz = z
								if x > maxx:
									maxx = x
								if y > maxy:
									maxy = y
								if z > maxz:
									maxz = z
								
								Q.append( (x-1, y, z) )
								Q.append( (x+1, y, z) )
								Q.append( (x, y-1, z) )
								Q.append( (x, y+1, z) )
								Q.append( (x, y, z-1) )
								Q.append( (x, y, z+1) )
								if DIAGONAL == True:
									Q.append( (x, y-1, z-1) )
									Q.append( (x-1, y, z-1) )
									Q.append( (x-1, y-1, z) )
									Q.append( (x, y+1, z+1) )
									Q.append( (x+1, y, z+1) )
									Q.append( (x+1, y+1, z) )
									Q.append( (x, y+1, z-1) )
									Q.append( (x+1, y, z-1) )
									Q.append( (x+1, y-1, z) )
									Q.append( (x, y-1, z+1) )
									Q.append( (x-1, y, z+1) )
									Q.append( (x-1, y+1, z) )

									Q.append( (x-1, y-1, z-1) )
									Q.append( (x-1, y-1, z+1) )
									Q.append( (x-1, y+1, z-1) )
									Q.append( (x-1, y+1, z+1) )
									Q.append( (x+1, y-1, z-1) )
									Q.append( (x+1, y-1, z+1) )
									Q.append( (x+1, y+1, z-1) )
									Q.append( (x+1, y+1, z+1) )
							
					# Finished scanning - I now have a set of the connected blocks. Blit it out into a new schematic and store it in a queue
					snipBox = BoundingBox((SIZE+minx,SIZE+miny,SIZE+minz),(SIZE+maxx+1,SIZE+maxy+1,SIZE+maxz+1))
					snipSchematic = WORKING.extractSchematic(snipBox)
					Components.append((snipSchematic, BoundingBox((0,0,0),(maxx-minx+1,maxy-miny+1,maxz-minz+1)), (maxx-minx+1,maxy-miny+1,maxz-minz+1), miny, numBlocks))

	print 'Drawing components I found...'
	# Now I have a set of Components. Where to draw them?
	b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	startX = width
	startY = height
	for (P,bx,(w,h,d), y, blockCount) in Components:
		if blockCount >= options["Epicentres"]: # Only plot objects above this size
			startX += GAP
			startY += GAP
			print 'Component %s %s %s' % (P,bx,w)
			level.copyBlocksFrom(P, bx, (box.minx+startX, box.miny+y, box.minz ),b)
			print 'Copied component to %s %s %s' % (box.minx+startX, box.miny, box.minz )
			startX += w
			startY += h

	level.copyBlocksFrom(SAVED, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ),b)

	
	FuncEnd(level,box,options,method) # Log end

	
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
	if options["Show Planes?"] == True:
		RenderPlanes(level,scratch,Q,width,height,depth)
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
	if options["Show Planes?"] == True:
		RenderPlanes(level,scratch,Q,width,height,depth)				
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
	if options["Show Planes?"] == True:
		RenderPlanes(level,scratch,Q,width,height,depth)				
	# Copy result from working set
	#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level.copyBlocksFrom(scratch, box, (0,0,0 ))
	
	FuncEnd(level,box,options,method)	

def Pressure(level, box, options):
	method = "Pressure"
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
		
	RenderShatteredLandUnderPressure(level,scratch,Q,width,height,depth)
	if options["Show Planes?"] == True:
		RenderPlanes(level,scratch,Q,width,height,depth)				
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
				((matBlock,matID),NBT) = getBlockWithNBT(level,iterX,iterY,iterZ)
				if (matBlock,matID) != (0,0):
					(deltaX,deltaY,deltaZ) = (0,0,0)
					for iter in xrange(0,len(Q)):
						((planeX,planeY,planeZ,denom,epiX,epiY,epiZ),(shiftX1,shiftY1,shiftZ1),(shiftX2,shiftY2,shiftZ2)) = Q[iter]
				
						dist = 1
						# Where is this point relative to the plane?
						if denom != 0:
							dist = (planeX*(epiX-iterX) + planeY*(epiY-iterY) + planeZ*(epiZ-iterZ)) / (planeX*planeX + planeY*planeY + planeZ*planeZ)
						
						if dist <=0:
							(deltaX,deltaY,deltaZ) = (deltaX+shiftX1, deltaY+shiftY1, deltaZ+shiftZ1)
						else:
							(deltaX,deltaY,deltaZ) = (deltaX+shiftX2, deltaY+shiftY2, deltaZ+shiftZ2)
					setBlockWithNBT(scratch,(matBlock,matID), NBT, iterX+deltaX, iterY+deltaY, iterZ+deltaZ)

def RenderShatteredLandUnderPressure(level,scratch,Q,width,height,depth):
	for iterY in xrange(0,height):
		print iterY
		for iterZ in xrange(0,depth):
			for iterX in xrange(0,width):
				# read from level, write to scratch.
				((matBlock,matID),NBT) = getBlockWithNBT(level,iterX,iterY,iterZ)
				if (matBlock,matID) != (0,0):
					(deltaX,deltaY,deltaZ) = (0,0,0)
					for iter in xrange(0,len(Q)):
						((planeX,planeY,planeZ,denom,epiX,epiY,epiZ),(shiftX1,shiftY1,shiftZ1),(shiftX2,shiftY2,shiftZ2)) = Q[iter]
				
						dist = 1
						# Where is this point relative to the plane?
						if denom != 0:
							dist = (planeX*(epiX-iterX) + planeY*(epiY-iterY) + planeZ*(epiZ-iterZ)) / (planeX*planeX + planeY*planeY + planeZ*planeZ)
						if dist <=0:
							(deltaX,deltaY,deltaZ) = (deltaX+shiftX1, deltaY+shiftY1, deltaZ+shiftZ1)
						else:
							(deltaX,deltaY,deltaZ) = (deltaX+shiftX2, deltaY+shiftY2, deltaZ+shiftZ2)
					((destBlock,destID),destNBT) = getBlockWithNBT(scratch,iterX+deltaX,iterY+deltaY,iterZ+deltaZ)
					if matBlock == 1 and destBlock == 1: # rock variant
						if matID == 0 and destID == 0:
							matID = 1
						matID = destID + matID
						if matID > 6: # max data value for rock types
							matID = 0
							matBlock = 49 # Obsidian
					setBlockWithNBT(scratch,(matBlock,matID), NBT, iterX+deltaX, iterY+deltaY, iterZ+deltaZ)
					
def RenderPlanes(level,scratch,Q,width,height,depth):
	for iterY in xrange(0,height):
		print iterY
		for iterZ in xrange(0,depth):
			for iterX in xrange(0,width):
				# read from level, write to scratch.
				mat = getBlock(level,iterX,iterY,iterZ)
				if mat == (0,0):
					(deltaX,deltaY,deltaZ) = (0,0,0)
					for iter in xrange(0,len(Q)):
						((planeX,planeY,planeZ,denom,epiX,epiY,epiZ),(shiftX1,shiftY1,shiftZ1),(shiftX2,shiftY2,shiftZ2)) = Q[iter]
						dist = 1
						# Where is this point relative to the plane?
						if denom != 0:
							dist = (planeX*(epiX-iterX) + planeY*(epiY-iterY) + planeZ*(epiZ-iterZ)) / (planeX*planeX + planeY*planeY + planeZ*planeZ)
						
						if abs(dist) < 1.0:
							(deltaX,deltaY,deltaZ) = (deltaX+shiftX1,deltaY+shiftY1,deltaZ+shiftZ1)
							setBlock(scratch,(20,0), iterX+deltaX,iterY+deltaY,iterZ+deltaZ) # Glass
					
	
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))
	
def getBlockWithNBT(level,x,y,z):
	(block,data) = getBlock(level, x, y, z)
	NBT = ''
	chunk = level.getChunk(int(x)/CHUNKSIZE, int(z)/CHUNKSIZE)
	for t in chunk.TileEntities:
		x1 = t["x"].value
		y1 = t["y"].value
		z1 = t["z"].value
		if int(x) == x1 and int(y) == y1 and int(z) == z1:
			NBT = t
	return ((block,data),NBT)

def setBlockWithNBT(level, (block, data), NBT, x,y,z):
	setBlock(level, (block, data), x, y, z)
	chunk = level.getChunk(int(x)/CHUNKSIZE, int(z)/CHUNKSIZE)
	if NBT != '':
		NBT["x"] = TAG_Int(int(x))
		NBT["y"] = TAG_Int(int(y))
		NBT["z"] = TAG_Int(int(z))
		chunk.TileEntities.append(NBT)
	
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
# This filter is for creating structures
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_
import time # for timing

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from numpy import *
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import *
from random import Random # @Codewarrior0

# GLOBAL
CHUNKSIZE = 16
STONE = (1,0)


inputs = (
		("Noodlor", "label"),
		("Inspired by the work of", "label"),
		("/u/MCNoodlor", "label"),
		("Seed:", 0),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	noodlor(level, box, options)

	FuncEnd(level,box,options,method) # Log end	

def room(level,box,CUBEWIDTH,ix,iy,iz):
	p000 = (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+(iz)*CUBEWIDTH)
	p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH-1)
	fillRegion(level, (159,12), p000, p111) # Brown Stained Clay
	# Walls
	p000 = (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH)
	p111 = (box.minx+(ix)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH-1,box.minz+(iz+1)*CUBEWIDTH-1)
	fillRegion(level, (159,11), p000, p111) # Blue Stained Clay
	p000 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH)
	p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH-1,box.minz+(iz+1)*CUBEWIDTH-1)
	fillRegion(level, (159,11), p000, p111) # Blue Stained Clay
	p000 = (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH)
	p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH-1,box.minz+(iz)*CUBEWIDTH)
	fillRegion(level, (159,11), p000, p111) # Blue Stained Clay
	p000 = (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH-1)
	p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH-1,box.minz+(iz+1)*CUBEWIDTH-1)
	fillRegion(level, (159,11), p000, p111) # Blue Stained Clay

def tower(level, box, CUBEWIDTH_, ix, iy, iz):
	CUBEWIDTH = CUBEWIDTH_
	
	# Base flange
	p000 = (box.minx+(ix)*CUBEWIDTH-1,box.miny,box.minz+iz*CUBEWIDTH-1)
	p111 = (box.minx+(ix+1)*CUBEWIDTH,box.miny,box.minz+(iz+1)*CUBEWIDTH)
	edgeRegion(level, (98,0), p000, p111) # Stone Bricks

	# Edge of tower to ground
	p000 = (box.minx+ix*CUBEWIDTH,box.miny,box.minz+iz*CUBEWIDTH)
	p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH-1,box.minz+(iz+1)*CUBEWIDTH-1)
	edgeRegion(level, (98,0), p000, p111) # Stone Bricks
	# Roof of tower
	p000 = (box.minx+ix*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+iz*CUBEWIDTH)
	p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH-1)
	fillRegion(level, (98,0), p000, p111) # Stone Bricks

	# Supports
	p000 = (box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+iz*CUBEWIDTH)
	p111 = (box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH-1)
	fillRegionSkip(level, (109,5), p000, p111,2) # Stone stairs upright west
	# Supports
	p000 = (box.minx+(ix)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH,box.minz+iz*CUBEWIDTH)
	p111 = (box.minx+(ix)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH-1)
	fillRegionSkip(level, (109,4), p000, p111,2) # Stone stairs upright east
	# Supports
	p000 = (box.minx+(ix)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz)*CUBEWIDTH-1)
	p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz)*CUBEWIDTH-1)
	fillRegionSkip(level, (109,6), p000, p111,2) # Stone stairs upright south
	# Supports
	p000 = (box.minx+(ix)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH)
	p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH)
	fillRegionSkip(level, (109,7), p000, p111,2) # Stone stairs upright north

	# Roof
	p000 = (box.minx+ix*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH+1,box.minz+iz*CUBEWIDTH)
	p111 = (box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH+1,box.minz+(iz+1)*CUBEWIDTH)
	fillRegion(level, (159,12), p000, p111) # Brown Stained Clay
	# Roof edge
	p000 = (box.minx+ix*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH+1,box.minz+iz*CUBEWIDTH-1)
	p111 = (box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH+1,box.minz+(iz+1)*CUBEWIDTH)
	edgeRegion(level, (98,0), p000, p111) # Stone Bricks
	
	# Crenelations
	p000 = (box.minx+(ix)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH+2,box.minz+iz*CUBEWIDTH-1)
	p111 = (box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH+2,box.minz+(iz+1)*CUBEWIDTH)
	edgeRegion(level, (98,0), p000, p111) # Stone Bricks
	p000 = (box.minx+(ix)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH+3,box.minz+iz*CUBEWIDTH-1)
	p111 = (box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH+3,box.minz+(iz+1)*CUBEWIDTH)
	edgeRegion(level, (44,0), p000, p111) # Stone slab
	(x1,y1,z1) = p000
	(x2,y2,z2) = p111
	count = 0
	for z in xrange(z1,z2+1):
		count = count +1
		if (count == 3 or count == (z2-z1-1)) or (count > 3 and count < (z2-z1-1) and (count-3)%4 == 0):
			setBlock(level,(0,0),x1,y1,z) # Air
			setBlock(level,(44,5),x1,y1-1,z) # Stone brick slab
			setBlock(level,(0,0),x2,y1,z) # Air
			setBlock(level,(44,5),x2,y1-1,z) # Stone brick slab
	count = 0
	for x in xrange(x1,x2+1):
		count = count +1
		if (count == 3 or count == (x2-x1-1)) or (count > 3 and count < (x2-x1-1) and (count-3)%4 == 0):
			setBlock(level,(0,0),x,y1,z1) # Air
			setBlock(level,(44,5),x,y1-1,z1) # Stone brick slab
			setBlock(level,(0,0),x,y1,z2) # Air
			setBlock(level,(44,5),x,y1-1,z2) # Stone brick slab

	
def noodlor(level, box, options):
	method = "noodlor"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	CUBEWIDTH = 11
	CUBEMID = CUBEWIDTH-(int(CUBEWIDTH)/2)
	# Make a blocky array in the selection box
	cwidth = int(width/CUBEWIDTH)
	cdepth = int(depth/CUBEWIDTH)
	cheight = int(height/CUBEWIDTH)
	print cwidth,cdepth,cheight
	
	# Mechanism to repeat a build by number
	rand = Random(options["Seed:"])
	if options["Seed:"] == 0:
		rand = Random()
	
	# Materials
	EDGEMAT = 1
	WALLMAT = 2
	FLOORMAT = 3
	
	# Enumerations
	VOID = 0
	TOWER = 1
	
	map = zeros((cwidth,cheight,cdepth))
	
	ang=pi/2/cheight
	
	# Create a random structure
	iy = cheight-1 # Start one layer below top to allow crenelations to be added later
	#for iy in xrange(0,cheight):
	while iy > 0:
		iy = iy -1
		for iz in xrange(0,cdepth):
			for ix in xrange(0,cwidth):
				# FUTURE - I may only want to create a component at odd grid axis
				
				# if there is something above, something should be below...
				# Future - consider arches
				distx = abs(int(cwidth/2)-ix)
				distz = abs(int(cdepth/2)-iz)
				dist = int(sqrt(distx**2+distz**2))
				if ix%2 == 1 and iz%2 == 1 and rand.randint(1,100) < cos(iy*ang)*20*dist/((distx+distz)/2): # Prefer low structures
					map[ix,iy,iz] = TOWER # Something is here
				
				if iy < cheight-1: # bounds checking - don't step outside the array
					if map[ix,iy+1,iz] > 0:
						map[ix,iy,iz] = TOWER # Tower section
	
	# Now we have a plan... render it
	
	# Placeholder
	for iy in xrange(0,cheight-1):
		for iz in xrange(0,cdepth):
			for ix in xrange(0,cwidth):
				if map[ix,iy,iz] == TOWER:
					print (ix,iy,iz)
					# Floor
					room(level,box,CUBEWIDTH,ix,iy,iz)
				
	for iz in xrange(0,cdepth):
		for ix in xrange(0,cwidth):
			iy = cheight
			while iy > 0:
				iy = iy - 1
				if map[ix,iy,iz] == TOWER:
					tower(level, box, CUBEWIDTH, ix,iy,iz)
					
					
					iy = 0 # exit
					



					
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy)*CUBEWIDTH,box.minz+(iz)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix)*CUBEWIDTH,box.miny+(iy)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+(ix+1)*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH),(box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH) )
	
	FuncEnd(level,box,options,method) # Log end	

def edgeRegion(level, material, (x1,y1,z1), (x2,y2,z2)):
	fillRegion(level, material, (x1,y1,z1), (x2,y1,z1))
	fillRegion(level, material, (x1,y1,z1), (x1,y2,z1))
	fillRegion(level, material, (x1,y1,z1), (x1,y1,z2))
	fillRegion(level, material, (x1,y2,z2), (x2,y2,z2))
	fillRegion(level, material, (x2,y1,z2), (x2,y2,z2))
	fillRegion(level, material, (x2,y2,z1), (x2,y2,z2))
	fillRegion(level, material, (x1,y2,z1), (x2,y2,z1))
	fillRegion(level, material, (x1,y2,z1), (x1,y2,z2))
	fillRegion(level, material, (x2,y1,z1), (x2,y2,z1))
	fillRegion(level, material, (x1,y1,z2), (x1,y2,z2))
	fillRegion(level, material, (x2,y1,z1), (x2,y1,z2))
	fillRegion(level, material, (x1,y1,z2), (x2,y1,z2))
	
def fillRegion(level, material, (x1,y1,z1), (x2,y2,z2)):
	if (x1,y1,z1) == (x2,y2,z2):
		setBlock(level, material, x1,y1,z1)
	elif (x1,y1) == (x2,y2):
		for z in xrange(z1,z2+1):
			setBlock(level, material, x1, y1, z)
	elif (z1,y1) == (z2,y2):
		for x in xrange(x1,x2+1):
			setBlock(level, material, x, y1, z1)
	elif (z1,x1) == (z2,x2):
		for y in xrange(y1,y2+1):
			setBlock(level, material, x1, y, z1)
	elif x1 == x2:
		for y in xrange(y1,y2+1):
			for z in xrange(z1,z2+1):
				setBlock(level, material, x1, y, z)
	elif y1 == y2:
		for x in xrange(x1,x2+1):
			for z in xrange(z1,z2+1):
				setBlock(level, material, x, y1, z)
	elif z1 == z2:
		for x in xrange(x1,x2+1):
			for y in xrange(y1,y2+1):
				setBlock(level, material, x, y, z1)
	else: # 
		for y in xrange(y1,y2+1):
			for z in xrange(z1,z2+1):
				for x in xrange(x1,x2+1):
					setBlock(level, material, x, y, z)

def fillRegionSkip(level, material, (x1,y1,z1), (x2,y2,z2), skip):
	if (x1,y1,z1) == (x2,y2,z2):
		setBlock(level, material, x1,y1,z1)
	elif (x1,y1) == (x2,y2):
		for z in xrange(z1,z2+1):
			if (z-z1+1)%skip != 0:
				setBlock(level, material, x1, y1, z)
	elif (z1,y1) == (z2,y2):
		for x in xrange(x1,x2+1):
			if (x-x1+1)%skip != 0:
				setBlock(level, material, x, y1, z1)
	elif (z1,x1) == (z2,x2):
		for y in xrange(y1,y2+1):
			if (y-y1+1)%skip != 0:
				setBlock(level, material, x1, y, z1)
	elif x1 == x2:
		for y in xrange(y1,y2+1):
			for z in xrange(z1,z2+1):
				if (z-z1+1)%skip != 0 and (y-y1+1)%skip != 0:
					setBlock(level, material, x1, y, z)
	elif y1 == y2:
		for x in xrange(x1,x2+1):
			for z in xrange(z1,z2+1):
				if (z-z1+1)%skip != 0 and (x-x1+1)%skip != 0:
					setBlock(level, material, x, y1, z)
	elif z1 == z2:
		for x in xrange(x1,x2+1):
			for y in xrange(y1,y2+1):
				if (x-x1+1)%skip != 0 and (y-y1+1)%skip != 0:
					setBlock(level, material, x, y, z1)
	else: # 
		for y in xrange(y1,y2+1):
			for z in xrange(z1,z2+1):
				for x in xrange(x1,x2+1):
					if (z-z1+1)%skip != 0 and (y-y1+1)%skip != 0 and (x-x1+1)%skip != 0:
						setBlock(level, material, x, y, z)
					
def makeBlob(level, x, y, z, ore, radius, replaceMaterial):
	# Make an irregular blob of ore centred at the position
	if radius == 1:
		if getBlock(level,x,y,z) == replaceMaterial:
			setBlock(level, ore, x,y,z)
	else:
		if randint(1,100) < 10: # Spherish
			r2 = radius*radius
			for dy in xrange(-radius,+radius):
				for dz in xrange(-radius,+radius):
					for dx in xrange(-radius,+radius):
						dist = dy**2+dz**2+dx**2
						if dist < r2 or (dist == r2 and randint(1,100) <= 40):
							if getBlock(level,dx+x,dy+y,dz+z) == replaceMaterial:
								setBlock(level, ore, dx+x,dy+y,dz+z)
		else: # brownian squiggle
			radius = radius**2 # Steps
			keepGoing = True
			P = []
			P.append((x,y,z))
			while keepGoing:
				(px,py,pz) = P[randint(0,len(P)-1)]
				dx = randint(-1,1)
				dy = randint(-1,1)
				dz = randint(-1,1)
				P.append((px+dx,py+dy,pz+dz))
				radius = radius-1
				if radius < 1:
					keepGoing = False
			for (px,py,pz) in P:
				if getBlock(level,px,py,pz) == replaceMaterial:
					setBlock(level, ore, px,py,pz)
			

	
	
####################################### LIBS
	
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
	
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
# Ye Olde GFX Libraries
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLine1(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	for px, py, pz in bresenham.bresenham((x,y,z),(x1,y1,z1)):
		setBlock(scratchpad,(blockID, blockData),px,py,pz)
	setBlock(scratchpad,(blockID, blockData),x1,y1,z1)
	
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
			rx = 0
			createArmorStand(level, (int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), "ls", 1, 0, 1, 1, 1, 0, 0, 0, rx, 0,0,0,1,"","","","","","stone",2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
			iter = iter+0.5 # slightly oversample because I lack faith.

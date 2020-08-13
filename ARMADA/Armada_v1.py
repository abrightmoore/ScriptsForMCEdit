# This filter is for generating sailing ships.
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0
import inspect # @Texelelf
from PIL import Image
import png

# GLOBAL
CHUNKSIZE = 16
MAXANGLES = 360
a = 2*pi/MAXANGLES
AIR = (0,0)
LAVA = (11,0)

coloursList = "15 7 8 0 6 2 10 11 3 9 13 5 4 1 14 12".split() # I like this sequence
#coloursList = "15 15 15 15 15 11 11 11 0".split()
colours = map(int, coloursList)
palette = []
palette.append( [ (1,0),(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (80,0) ] )
palette.append( [ (95,3),(22,0), (24,2), (19,0), (18,0), (3,0), (1,0), (80,0) ]	)
RAND2 = Random(42)

# Choose a colour pallette
print 'Pallette Selection'
gap = RAND2.randint(1,4)
for i in range(32):
	newCols = []
	baseIndex = RAND2.randint(0,len(colours))

	for j in range(8):
		newCols.append( (159, (int)(colours[(baseIndex+j*gap)%len(colours)]) ) )
	palette.append(newCols)
print 'Pallette Selection complete'

inputs = (
		("ARMADA", "label"),
		("Exotic?", False),
		("Cross Section?", False),
		("Skeleton?", False),
		("Smooth:", 4),
		("Seed:", 0),
		("Random Materials?", False),
		("Cache:",True),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def armada(level,box,options):
	method = "Armada"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	print "Seed:"
	PARAM = int(options["Seed:"])
	if PARAM == 0:
		PARAM = randint(0,99999999999)
	print PARAM
	RAND = Random(PARAM)
	
	WOOD_PAL = [(17,0),(17,1),(17,2),(17,3),(162,0),(162,1),(159,0),(159,1),(159,2),(159,3),(159,4),(159,5),(159,6),(159,7),(159,8),(159,9),(159,10),(159,11),(159,12),(159,13),(159,14),(159,15)]
	WOOD = (17,0)
	if RAND.randint(1,100) > 20 and options["Random Materials?"] == True:
		WOOD = WOOD_PAL[RAND.randint(0,len(WOOD_PAL)-1)]
	WOODEW_PAL = [(17,4),(17,5),(17,6),(17,7),(162,4),(162,5)]
	WOODEW = (17,5)
	if RAND.randint(1,100) > 20 and options["Random Materials?"] == True:
		WOODEW = WOODEW_PAL[RAND.randint(0,len(WOODEW_PAL)-1)]
	WOODNS_PAL = [(17,8),(17,9),(17,10),(17,11),(162,8),(162,9)]
	WOODNS = (17,9)
	if RAND.randint(1,100) > 20 and options["Random Materials?"] == True:
		WOODNS = WOODNS_PAL[RAND.randint(0,len(WOODNS_PAL)-1)]
	OAKPLANKS_PAL = [(5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]
	OAKPLANKS = (5,0)
	if RAND.randint(1,100) > 20 and options["Random Materials?"] == True:
		OAKPLANKS = OAKPLANKS_PAL[RAND.randint(0,len(OAKPLANKS_PAL)-1)]
	FENCE_PAL = [(85,0),(113,0),(188,0),(189,0),(190,0),(191,0),(192,0),(101,0)]
	FENCE = (85,0)
	if RAND.randint(1,100) > 20 and options["Random Materials?"] == True:
		FENCE = FENCE_PAL[RAND.randint(0,len(FENCE_PAL)-1)]
	GLASS_PAL = [(20, 0),(95,0),(95,1),(95,2),(95,3),(95,4),(95,5),(95,6),(95,7),(95,8),(95,9),(95,10),(95,11),(95,12),(95,13),(95,14),(95,15),(102,0),(160,0),(160,1),(160,2),(160,3),(160,4),(160,5),(160,6),(160,7),(160,8),(160,9),(160,10),(160,11),(160,12),(160,13),(160,14),(160,15),(101,0)]
	GLASS = (20, 0)
	if RAND.randint(1,100) > 20 and options["Random Materials?"] == True:
		GLASS = GLASS_PAL[RAND.randint(0,len(GLASS_PAL)-1)]

	if options["Skeleton?"] == True:
		OAKPLANKS = AIR
		FENCE = AIR
		GLASS = AIR
	SMOOTHAMOUNT = options["Smooth:"]
	# Step 1 will be the shape of the hull, the centre first.
	# We'll build along the depth of the selection box.
	# The width can be the width of the selection box.
	# The deck height is arbitrary but room for the sails and the mast is required.
	
	LENGTH = depth
	LENGTHQUANTUM = depth/8
	WIDTH = width
	WIDTHQUANTUM = width/6
	HEIGHT = height
	HEIGHTQUANTUM = height/5
	DECKHEIGHT = (HEIGHTQUANTUM*2-1)
	DECKROOMVERT = RAND.randint(3,6)
	DECKROOMHORIZ = RAND.randint(4,16)
	
	# "####-
	P = [] # Consider altering this based on the seed
	POOPHEIGHT = RAND.randint(0,int(HEIGHTQUANTUM*2))
	AFT = (centreWidth, HEIGHTQUANTUM*2.1+POOPHEIGHT, 0) # LENGTHQUANTUM/2.1)
	P.append(AFT)
	P.append(AFT)
	P.append((centreWidth, DECKHEIGHT+1+POOPHEIGHT/2, LENGTHQUANTUM))
	P.append((centreWidth, 0, LENGTHQUANTUM))
	P.append((centreWidth, 0, LENGTH-LENGTHQUANTUM*2))
	FORE = (centreWidth, HEIGHTQUANTUM*2.1, LENGTH-LENGTHQUANTUM)
	if options["Exotic?"] == False or RAND.randint(1,100) > 50:
		P.append((centreWidth, DECKHEIGHT+1, LENGTH-LENGTHQUANTUM*1.9))
	elif options["Exotic?"] == False or RAND.randint(1,100) > 50:
		P.append((centreWidth, RAND.randint(0,DECKHEIGHT+1), LENGTH-LENGTHQUANTUM*1.9))
	else: # Double back for a MIG-style intake at the front
		P.append((centreWidth, DECKHEIGHT+1, LENGTH-LENGTHQUANTUM))
		FORE = (centreWidth, HEIGHTQUANTUM*2.1, LENGTH-LENGTHQUANTUM*1.9)
	P.append(FORE)
	P.append(FORE)
	drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,P)
	
	Q = [] 
	Q.append(AFT)
	Q.append(AFT)
	HULLINSET = RAND.randint(0,int(centreWidth)/2)
	if RAND.randint(1,100) > 80:
		Q.append((HULLINSET,DECKHEIGHT+RAND.randint(int(POOPHEIGHT/3),POOPHEIGHT),LENGTHQUANTUM/16))
	Q.append((HULLINSET,DECKHEIGHT+1,LENGTHQUANTUM*2))
	Q.append((HULLINSET/2,DECKHEIGHT+1,LENGTHQUANTUM*5))
	Q.append(FORE)
	Q.append(FORE)
	drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,Q)
	
	HULLSHAPEY = RAND.randint(1,6)
	HULLSHAPEX = RAND.randint(2,6)
	if options["Exotic?"] == False:
		HULLSHAPEY = 2
		HULLSHAPEX = 2
		
	# Move along the length of the ship and for each layer draw the hull curve
	for z in xrange(0,depth):
		if z%10 == 0:
			print z
		# find the centreline block
		y = 0
		x = 0
		keepGoing = True
		block1 = AIR
		while keepGoing == True:
			block1 = getBlock(level,box.minx+x,box.miny+y,box.minz+z)
			if block1 != AIR:
				keepGoing = False
			else:
				x = x + 1
				if x > centreWidth:
					y = y + 1
					x = 0
					if y >= height:
						keepGoing = False
		P0 = (x,y,z)
		if block1 != AIR: # Found a point
			y = height-1
			x = 0
			keepGoing = True
			while keepGoing == True:
				block2 = getBlock(level,box.minx+x,box.miny+y,box.minz+z)
				if block2 != AIR:
					keepGoing = False
				else:
					x = x + 1
					if x > centreWidth:
						y = y - 1
						x = 0
						if y < 0:
							keepGoing = False
			P1 = (x,y,z)
			if block2 != AIR: # Found the second point
				R = []
				R.append(P0)
				R.append(P0)
				(x0,y0,z0) = P0
				dist = (x+x0)/HULLSHAPEX
				if dist <= HULLINSET:
					R.append((dist-HULLINSET, abs(y+y0)/HULLSHAPEY,z))
				else:
					R.append((dist, abs(y+y0)/HULLSHAPEY,z))
				R.append(P1)
				R.append(P1)
				if z%DECKROOMHORIZ == 0:
					L = drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,R)
					for p in L:
						for (xe,ye,ze) in p:
							if ye < DECKHEIGHT:
								for x in xrange(xe,int(centreWidth)):
									if ye <= DECKROOMVERT+2:
										setBlock(level,WOOD,x,ye,ze)
									elif x%DECKROOMVERT == 0:
										setBlock(level,WOOD,x,ye,ze)
							elif ye == DECKHEIGHT:
								drawLine(level,WOODNS,(xe,ye,ze),(centreWidth,ye,ze))
					R = []
					(x2,y2,z2) = P0					
					R.append((x2,y2,z2))
					R.append((x2,y2,z2))
					dist = (x+x0)/HULLSHAPEX
					if dist <= HULLINSET:
						R.append((dist-HULLINSET, abs(y+y0)/HULLSHAPEY,z))
					else:
						R.append((dist, abs(y+y0)/HULLSHAPEY,z))
					(x3,y3,z3) = P1
					R.append((x3+1,y3,z3))
					R.append((x3+1,y3,z3))
					drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,R)
				else:
					drawLinesSmooth(level,box,OAKPLANKS,SMOOTHAMOUNT,R)


	# Draw the masts
	(x0,y0,z0) = AFT
	(x1,y1,z1) = FORE
	mastgap = (z1-z0)/4
	MASTSLANT = RAND.randint(1,int(mastgap))
	MASTS = RAND.randint(1,3)

	# Find the base of the ship at each mast base
	M1 = (x0,0,z0+mastgap)
	y = 0
	while y < height:
		if getBlock(level,box.minx+x0,box.miny+y,box.minz+z0+mastgap) != AIR:
			M1 = (x0,y,z0+mastgap)
		y = y+1
	
	M2 = (x0,0,z0+2*mastgap)
	y = 0
	while y < height:
		if getBlock(level,box.minx+x0,box.miny+y,box.minz+z0+2*mastgap) != AIR:
			M2 = (x0,y,z0+2*mastgap)
		y = y+1
	M3 = (x0,0,z0+3*mastgap)
	y = 0
	while y < height:
		if getBlock(level,box.minx+x0,box.miny+y,box.minz+z0+3*mastgap) != AIR:
			M3 = (x0,y,z0+3*mastgap)
		y = y+1
	(x,y,z) = M1
	if MASTS > 2:
		drawLine(level,WOOD,(x-1,y,z),(x,height-1,z-mastgap/MASTSLANT))
		drawLine(level,WOOD,(x,y,z+1),(x,height-1,z-mastgap/MASTSLANT))
		drawLine(level,WOOD,(x,y,z-1),(x,height-1,z-mastgap/MASTSLANT))
	(x,y,z) = M2
	drawLine(level,WOOD,(x-1,y,z),(x,height-1,z-mastgap/MASTSLANT))
	drawLine(level,WOOD,(x,y,z+1),(x,height-1,z-mastgap/MASTSLANT))
	drawLine(level,WOOD,(x,y,z-1),(x,height-1,z-mastgap/MASTSLANT))
	(x,y,z) = M3
	if MASTS > 1:
		drawLine(level,WOOD,(x-1,y,z),(x,height-1,z-mastgap/MASTSLANT))
		drawLine(level,WOOD,(x,y,z+1),(x,height-1,z-mastgap/MASTSLANT))
		drawLine(level,WOOD,(x,y,z-1),(x,height-1,z-mastgap/MASTSLANT))

	yardist = int((height-1-DECKHEIGHT)/9)
	# Draw the spars
	y = height-1
	while y > DECKHEIGHT:
		if y == (height-1-yardist) or y == (height-1-3*yardist) or y == (height-1-6*yardist):
			for z in xrange(int(LENGTHQUANTUM/2),depth):
				if getBlock(level, box.minx+centreWidth, box.miny+y, box.minz+z+1) != AIR and getBlock(level, box.minx+centreWidth, box.miny+y, box.minz+z) == AIR:
					drawLine(level, WOODEW,(box.minx+centreWidth, box.miny+y, box.minz+z), (box.minx+((centreWidth/2)/((height-y)/yardist)), box.miny+y, box.minz+z))
		if y == (height-1-8*yardist):
			for z in xrange(0,depth):
				if getBlock(level, box.minx+centreWidth, box.miny+y, box.minz+z+1) != AIR and getBlock(level, box.minx+centreWidth, box.miny+y, box.minz+z) == AIR:
					drawLine(level, WOODNS,(box.minx+centreWidth, box.miny+y, box.minz+z), (box.minx+centreWidth, box.miny+y, box.minz+z-mastgap/2))
		y=y-1
	
	# Spar at the front of the ship
	if RAND.randint(1,100) > 20:
		SPARSET = RAND.randint(0,HEIGHTQUANTUM)
		S = []
		(x,y,z) = M3
		S.append((x-1,y,z))
		S.append((x-1,y,z))
		S.append(FORE)
		F = (centreWidth,DECKHEIGHT+SPARSET,depth-1)
		S.append(F)
		S.append(F)
		drawLines(level,box,WOODNS,S)
		S = []
		(x,y,z) = M3
		S.append((x,y,z+1))
		S.append((x,y,z+1))
		(ex,ey,ez) = FORE
		S.append((ex,ey-1,ez))
		S.append(F)
		S.append(F)
		R = drawLines(level,box,WOODNS,S)
		(x,y,z) = M3
		S.append((x,y,z+1))
		S.append((x,y,z+1))
		(ex,ey,ez) = FORE
		S.append((ex,ey-2,ez))
		S.append(F)
		S.append(F)
		R = drawLines(level,box,WOODNS,S)

		for p in R:
			for (x,y,z) in p:
				if z%int(LENGTHQUANTUM/2) == 0 and z > depth-LENGTHQUANTUM and z < depth-LENGTHQUANTUM/2:
					drawLine(level,WOODEW,(centreWidth,y,z),(centreWidth/2,y,z))
	
	
	# Draw the decks, top down
	y = height-1
	keepGoing = True
	while keepGoing == True:
		if y%10 == 0:
			print y
		if (y-DECKHEIGHT)%DECKROOMVERT == 0:
			for z in xrange(0,depth):
				x = 0
				while x <= centreWidth:
					block = getBlock(level,box.minx+x,box.miny+y,box.minz+z)
					if block != AIR:
						setBlockForced(level,WOOD,box.minx+x,box.miny+y,box.minz+z)
						for x1 in xrange(x,int(centreWidth)+1):
							setBlock(level,OAKPLANKS,box.minx+x1,box.miny+y,box.minz+z)
						x = centreWidth+1
					x = x+1
		y = y-1
		if y <= 0:
			keepGoing = False
	
	# Hold
	HOLDSIZE = RAND.randint(2,int(centreWidth/3))
	for i in xrange(1,5):
		HOLDDPOS = RAND.randint(int(centreDepth/3),depth-int(centreDepth/2))
		if HOLDSIZE >= 2:
			for y in xrange(DECKROOMVERT+2, height):
				for z in xrange(int(HOLDDPOS-HOLDSIZE),int(HOLDDPOS+HOLDSIZE)):
					for x in xrange(int(centreWidth-HOLDSIZE),int(centreWidth)+1):
						block = getBlock(level, box.minx+x,box.miny+y,box.minz+z)
						if block == OAKPLANKS and block != AIR:
							if z == int(HOLDDPOS-HOLDSIZE) or z == int(HOLDDPOS+HOLDSIZE-1):
								setBlockForced(level,WOODEW,box.minx+x,box.miny+y,box.minz+z)
								if y == DECKHEIGHT:
									setBlockForced(level,WOODEW,box.minx+x,box.miny+y+1,box.minz+z)
							elif x == int(centreWidth-HOLDSIZE) or x == int(centreWidth+HOLDSIZE-1):
								setBlockForced(level,WOODNS,box.minx+x,box.miny+y,box.minz+z)
								if y == DECKHEIGHT:
									setBlockForced(level,WOODNS,box.minx+x,box.miny+y+1,box.minz+z)
							else:
								setBlockForced(level,AIR,box.minx+x,box.miny+y,box.minz+z)
						
	# Railings
	if RAND.randint(1,100) > 10:
		for y in xrange(0,height):
			for z in xrange(0,depth):
				x = 0
				while x < centreWidth:
					if getBlock(level, box.minx+x,box.miny+y,box.minz+z) == WOOD and getBlock(level, box.minx+x,box.miny+y+1,box.minz+z) == AIR and getBlock(level, box.minx+x+1,box.miny+y+1,box.minz+z) == AIR:
						if z%DECKROOMHORIZ*4 != 0:
							setBlock(level, FENCE, box.minx+x,box.miny+y+1,box.minz+z)
							x = centreWidth
					x = x+1
			
	# Portholes
	PORTHOLEDIST = RAND.randint(2,DECKROOMHORIZ)
	if PORTHOLEDIST > 1:
		y = DECKHEIGHT-DECKROOMVERT+2
		for z in xrange(0,depth):
			if z%PORTHOLEDIST == 0:
				x = 0
				while x < centreWidth:
					block = getBlock(level, box.minx+x,box.miny+y,box.minz+z)
					if block == OAKPLANKS and block != AIR:
						setBlockForced(level,AIR,box.minx+x,box.miny+y,box.minz+z)
						if getBlock(level, box.minx+x,box.miny+y-1,box.minz+z) != AIR:
							setBlockForced(level,WOOD,box.minx+x,box.miny+y-1,box.minz+z)
						# x = centreWidth
					x = x + 1

	# Add in aft windows
	P = []
	z = 0
	while z < LENGTHQUANTUM:
		y = 0
		while y < height:
			found = False
			for x in xrange(0,int(centreWidth+1)):
				if (x,y) not in P:
					block = getBlock(level, box.minx+x,box.miny+y,box.minz+z)
					if block != AIR:
						found = True
						P.append((x,y))
					elif found == True:
						setBlock(level, GLASS, box.minx+x,box.miny+y,box.minz+z)
						P.append((x,y))
			y = y+1
		z = z+1
					
					
	# Copy the other side of the ship over
	if options["Cross Section?"] == False:
		print 'Copying half ship to other side...'
		for y in xrange(0,height):
			if y%10 == 0:
				print y
			for z in xrange(0,depth):
				if width%1 == 1: # odd
					for x in xrange(0,int(centreWidth)):
						setBlock(level, getBlock(level, box.minx+x, box.miny+y, box.minz+z), box.maxx-1-x, box.miny+y, box.minz+z)
				else:
					for x in xrange(0,int(centreWidth)+1): # even
						setBlock(level, getBlock(level, box.minx+x, box.miny+y, box.minz+z), box.maxx-1-x, box.miny+y, box.minz+z)
	
	# Store the seed on the ship
	(x,y,z) = AFT
	createSign(level, box.minx+x, box.miny+y+1, box.minz+z, str(PARAM))
	block = getBlock(level, box.minx+x,box.miny+y,box.minz+z+1) # cleanup
	if block == GLASS: # an error
		setBlockForced(level, AIR, box.minx+x,box.miny+y+1,box.minz+z+1)
						
	FuncEnd(level,box,options,method)

def drawLinesSmooth(level,box,material,SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = drawLines(level,box,material,P)
	return Q
	
def drawLines(level,box,material,P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( drawLine(level,material,(box.minx+x0,box.miny+y0,box.minz+z0),(box.minx+x,box.miny+y,box.minz+z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q
	
def perform(level,box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	levelCopy = level
	boxCopy = box

	if options["Cache:"] == True:
		levelCopy = level.extractSchematic(box) # Working set
		boxCopy = BoundingBox((0,0,0),(width,height,depth))
	
	armada(levelCopy,boxCopy,options)

	if options["Cache:"] == True:
		level.copyBlocksFrom(levelCopy, boxCopy, (box.minx, box.miny, box.minz ))
	
	level.markDirtyBox(box)
	FuncEnd(level,box,options,method) # Log end	

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

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
# Ye Olde GFX Libraries
def createSign(level, x, y, z, text): #abrightmoore - convenience method. Due to Jigarbov - this is not a Sign.
	ALIASKEY = "SHIP NUMBER"
	COMMANDBLOCK = 137
	CHUNKSIZE = 16
	STANDING_SIGN = 63
	
	setBlock(level, (STANDING_SIGN,8), x, y, z)
	setBlock(level, (1,0), x, y-1, z)
	control = TAG_Compound()
	control["id"] = TAG_String("Sign")
	control["Text1"] = TAG_String(ALIASKEY)
	control["Text2"] = TAG_String(text)
	control["Text3"] = TAG_String("Generated by")
	control["Text4"] = TAG_String("@abrightmoore")	
	
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	chunka.TileEntities.append(control)
	chunka.dirty = True

def chaikinSmoothAlgorithm(P): # http://www.idav.ucdavis.edu/education/CAGDNotes/Chaikins-Algorithm/Chaikins-Algorithm.html
	F1 = 0.25
	F2 = 0.75
	Q = []
	(x0,y0,z0) = (-1,-1,-1)
	count = 0
	for (x1,y1,z1) in P:
		if count > 0: # We have a previous point
			(dx,dy,dz) = (x1-x0,y1-y0,z1-z0)
#			Q.append( (x0*F2+x1*F1,0,z0*F2+z1*F1) )
#			Q.append( (x0*F1+x1*F2,0,z0*F1+z1*F2) )

			Q.append( (x0*F2+x1*F1,y0*F2+y1*F1,z0*F2+z1*F1) )
			Q.append( (x0*F1+x1*F2,y0*F1+y1*F2,z0*F1+z1*F2) )

#			Q.append( (x0+dx*F1+*F2,y0*F1+y1*F2,z0*F1+z1*F2) )
#			Q.append( (x0*F2+x1*F1,y0*F2+y1*F1,z0*F2+z1*F1) )
		else:
			count = count+1
		(x0,y0,z0) = (x1,y1,z1)

	return Q

def drawTriangle(level, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
	if materialFill != (0,0):
		# for each step along the 'base' draw a line from the apex
		dx = p3x - p2x
		dy = p3y - p2y
		dz = p3z - p2z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)
		
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
			
			iter = iter+0.5 # slightly oversample because I lack faith.
			drawLine(level, materialFill, (px, py, pz), (p1x, p1y, p1z) )
	
	
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def drawTriangleEdge(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge):
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def plotLine(level,material,p1,p2):

	(x1,y1,z1) = p1
	(x2,y2,z2) = p2
	
	dx = x2-x1
	dy = y2-y1
	dz = z2-z1
	
	steps = abs(dx)
	if abs(dy) > abs(dx):
		steps = abs(dy)
	if abs(dz) > abs(dy):
		steps = abs(dz)
	if steps == 0:
		setBlock(level,material,x1,y1,z1)
	else:
		ddx = float(dx)/float(steps)
		ddy = float(dy)/float(steps)
		ddz = float(dz)/float(steps)
		pdx = float(0)
		pdy = float(0)
		pdz = float(0)
		
		for i in xrange(0,int(steps)):
			setBlock(level,material,x1+pdx,y1+pdy,z1+pdz)
			pdx = pdx + ddx
			pdy = pdy + ddy
			pdz = pdz + ddz
	
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	return drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

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
	P = []
	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(xd,yd,zd) = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)))
			setBlock(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points drawn

def drawLineConstrainedRandom(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), frequency ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)


	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)

	iter = 0
	while iter <= distance:
		if randint(0,99) < frequency:
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
		iter = iter+0.5 # slightly oversample because I lack faith.
	
def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

def setBlock(level, (block, data), x, y, z):
	if getBlock(level, x,y,z) == AIR:
		level.setBlockAt(int(x), int(y), int(z), block)
		level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockForced(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
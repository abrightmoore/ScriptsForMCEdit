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
		("Seed:", 0),
		("Space?", False),
		("Random Materials?", False),
		("Exotic?", False),
		("Rigging?", True),
		("Sails?", True),
		("Skeleton?", False),
		("Cross Section?", False),
		("Barrier Fill?", False),
		("Balloons?", False),
		("Stage:",11),
		("Smooth:", 4),
		("Noise?", False),
		("Noise Material:", alphaMaterials.Fence),
#		("Cache:",True),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def paint(level,box,materials):
	print "Paint"
	width = box.maxx-box.minx
	height = box.maxy-box.miny
	depth = box.maxz-box.minz
	
	print "Masking"
	mask = zeros((width,1,depth))
	for i in xrange(0,len(materials)):
		sz = randint(2,6)
		col = randint(0,len(materials)-1)
		for x in xrange(box.minx,box.maxx):
			for y in xrange(0,1):
				for z in xrange(box.minz,box.maxz):
					if randint(1,100) > 90:
						for ix in xrange(0,randint(1,3)):
							for iy in xrange(0,1):
								for iz in xrange(0,sz):
									if randint(1,100) >2: # Drop an occasional block
										mask[(x+ix)%width,0,(z+iz)%depth] = col
									
	# Apply the colours
	print "Painting"
	for x in xrange(box.minx,box.maxx):
		for y in xrange(box.miny,box.maxy):
			for z in xrange(box.minz,box.maxz):
				b = getBlock(level, x,y,z)
				#print b
				if b != (0,0): # Not air
					#print mask[(x)%width,0,(z)%depth],maskData[(x)%width,0,(z)%depth]
					setBlockForced(level,materials[int(mask[(x)%width,0,(z)%depth])],int(x),int(y),int(z))

def flatten(anArray):
	result = []
	for a in anArray:
		for b in a:
			result.append(b)
	return result

def pod(level,material,radius,length,(x,y,z)):
	# Draw a tapering cylinder along the z axis centred at the point with the characteristics passed
	halfLength = int(length/2)
	
	for iz in xrange(z-halfLength,z+halfLength):
		# draw a vertical circle here
		for ix in xrange(x-radius,x+radius):
			for iy in xrange(y-radius,y+radius):
				dx = ix - x
				dy = iy - y
				d = int(sqrt(dx**2+dy**2))
				if d == radius-1:
					setBlock(level,material,ix,iy,iz)
	
def spaceShip1(level0,box0,options):
	method = "spaceShip1"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level0,box0,options,method) # Log start

	# Box cache support
	level = level0.extractSchematic(box0) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))	

	# Use RAND for consistent generation of artifacts
	print "Seed:"
	PARAM = int(options["Seed:"])
	if PARAM == 0:
		PARAM = randint(0,99999999999)
	print PARAM
	RAND = Random(PARAM)
	###################################################

	# Palette
	BARRIER = (166,0)
	WOOD_PAL = [(17,0),(17,1),(17,2),(17,3),(162,0),(162,1),(159,0),(159,1),(159,2),(159,3),(159,4),(159,5),(159,6),(159,7),(159,8),(159,9),(159,10),(159,11),(159,12),(159,13),(159,14),(159,15)]
	WOOD = (42,0)
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
	WHITEWOOL = (35,0)
	##########################################################
	
	SMOOTHAMOUNT = options["Smooth:"] # Configurable parameter to resolve jaggedy-ness.
	
	# BEAM of the ship
	MIDPOINT = [ (centreWidth, centreHeight, centreDepth) ]
	QUANTUM = int(depth/10)
	SEGMENTS = RAND.randint(1,int(depth/QUANTUM)+1)
	SEGMENTLENGTH = int(depth/SEGMENTS)
	BEAMP = [] # Backbone of the 'ship'
	for i in xrange(0,SEGMENTS+1):
		dY = int(centreHeight/QUANTUM)
		curP = (centreWidth,centreHeight+RAND.randint(-dY,dY),i*SEGMENTLENGTH)
		
#		if i == SEGMENTS and RAND.randint(1,100) > 0:
#			BEAMP.append( (centreWidth,centreHeight+RAND.randint(-dY,dY),depth-1) )
#		else:
		BEAMP.append( curP )
#		if i == 0 or i == SEGMENTS: # Double-add the start and end points
#			BEAMP.append( curP )
	
	drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,BEAMP) # Draw the beam of the ship
	
	# Carve out a hull along the length of the beam
	# Each segment point on the BEAM is a rib of the ship
	HULLPS = []
	
	count = 0
	oldP = (0,centreHeight,centreDepth)
	lastDim = (0,0,0,0)
	for p in BEAMP:
		(x,y,z) = p
		topW = RAND.randint(0,int(centreWidth/2))
		botW = RAND.randint(0,int(centreWidth/2))
		topH = RAND.randint(0,int(centreHeight/2))
		botH = RAND.randint(0,int(centreHeight/2))
		p00 = (x-botW,y-botH,z)
		p01 = (x-topW,y+topH,z)
		p10 = (x+botW,y-botH,z)
		p11 = (x+topW,y+topH,z)
		if count == SEGMENTS and RAND.randint(1,100) > 20:
			p00 = (x,y,z)
			p01 = (x,y,z)
			p10 = (x,y,z)
			p11 = (x,y,z)
			
		if count > 0: # and count < SEGMENTS+1:
			(q00,q01,q10,q11) = lastShape
			#drawLine(level,WOOD,p00,p01) # Rib
			#drawLine(level,WOOD,p01,p11) # Rib
			#drawLine(level,WOOD,p11,p10) # Rib
			#drawLine(level,WOOD,p10,p00) # Rib
			#drawLine(level,WOOD,q00,p00) # Spar
			#drawLine(level,WOOD,q01,p01) # Spar
			#drawLine(level,WOOD,q10,p10) # Spar
			#drawLine(level,WOOD,q11,p11) # Spar
		if count == 0 and RAND.randint(1,100) > 50: # Rockets!
			print 'Pods'
			length = int(SEGMENTLENGTH/2)
			(x,y,z) = p00
			pod(level,WOOD,int(SEGMENTLENGTH/6),int(SEGMENTLENGTH),(int(x),int(y),int(z+length)))
			(x,y,z) = p01
			pod(level,WOOD,int(SEGMENTLENGTH/6),int(SEGMENTLENGTH),(int(x),int(y),int(z+length)))
			(x,y,z) = p10
			pod(level,WOOD,int(SEGMENTLENGTH/6),int(SEGMENTLENGTH),(int(x),int(y),int(z+length)))
			(x,y,z) = p11
			pod(level,WOOD,int(SEGMENTLENGTH/6),int(SEGMENTLENGTH),(int(x),int(y),int(z+length)))
			
		count = count+1
		oldP = p
		lastShape = (p00,p01,p10,p11)
		HULLPS.append( lastShape )
	
	RIBLOCKS = [] # All the blocks in all the ribs
	for ps in HULLPS: # Draw rib
		(p00,p01,p10,p11) = ps
		ribP = []
		ribP.append(p00)
		ribP.append(p01)
		ribP.append(p11)
		ribP.append(p10)
		ribP.append(p00)
		ribP.append(p01)
		RIBLOCKS.append(drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,ribP))
	
	prevRB = []
	for rb in RIBLOCKS:
		rb = flatten(rb)
		if prevRB != []:
			thisRibLen = len(rb)
			thatRibLen = len(prevRB)
			if thisRibLen >= thatRibLen:
				stepSize = float(thatRibLen)/float(thisRibLen)
				for i in xrange(0,thisRibLen):
					# Draw a line from the i_th element of this rib to the corresponding element of that rib
					p = rb[i]
					offset = stepSize*i
					q = prevRB[int(offset)]
					drawLine(level,WOOD,p,q)
			else:
				stepSize = float(thisRibLen)/float(thatRibLen)
				for i in xrange(0,thatRibLen):
					offset = stepSize*i
					p = rb[int(offset)]
					q = prevRB[i]
					drawLine(level,WOOD,p,q)
				
		prevRB = rb

	#Wings
	NUMWINGS = RAND.randint(1,5)
	for wings in xrange(0,NUMWINGS):
		if SEGMENTS > 2:
			z0 = RAND.randint(0,int(SEGMENTS/2)-1)*SEGMENTLENGTH
			z2 = RAND.randint(int(SEGMENTS/2),SEGMENTS)*SEGMENTLENGTH
			x0 = 0 #RAND.randint(0,int(centreWidth/8))
			y0 = RAND.randint(0,height)   #int(centreHeight/8))
			z1 = RAND.randint(z0,z2-((z2-z0)/3))
			p0 = (centreWidth,centreHeight,z0)
			p1 = (x0,y0,z1)
			p2 = (centreWidth,centreHeight,z2)
			P = []
			P.append(p0)
			P.append(p0)
			P.append(p1)
			P.append(p2)
			P.append(p2)
			W1 = drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,P)

			p1 = (width-x0,y0,z1) #(width-1-x0,y0,z1)
			P = []
			P.append(p0)
			P.append(p0)
			P.append(p1)
			P.append(p2)
			P.append(p2)
			W2 = drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,P)

			W1 = flatten(W1)
			for (x,y,z) in W1:
				drawLine(level,WOOD,(x,y,z),(centreWidth,centreHeight,z))
			W2 = flatten(W2)
			for (x,y,z) in W2:
				drawLine(level,WOOD,(x,y,z),(centreWidth,centreHeight,z))
			
			WINGHEIGHT = RAND.randint(2,8)
			for (x,y,z) in W1:
				P = []
				P.append((centreWidth,centreHeight+WINGHEIGHT,z))
				P.append((centreWidth,centreHeight+WINGHEIGHT,z))
				P.append((x,y,z))
				#(x,y,z) = p
				#P.append((x,y+WINGHEIGHT,z))
				P.append((centreWidth,centreHeight-WINGHEIGHT,z))
				P.append((centreWidth,centreHeight-WINGHEIGHT,z))
				drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,P)
			for (x,y,z) in W2:
				P = []
				P.append((centreWidth,centreHeight+WINGHEIGHT,z))
				P.append((centreWidth,centreHeight+WINGHEIGHT,z))
				P.append((x,y,z))
				#(x,y,z) = p
				#P.append((x,y+WINGHEIGHT,z))
				P.append((centreWidth,centreHeight-WINGHEIGHT,z))
				P.append((centreWidth,centreHeight-WINGHEIGHT,z))
				drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,P)
		
	paint(level,box,palette[RAND.randint(0,len(palette)-1)])
	
	# Control deck
	dz = RAND.randint(1,3)
	for y in xrange(int(centreHeight)-1,int(centreHeight)+RAND.randint(1,3)):
		for iz in xrange((SEGMENTS-dz)*SEGMENTLENGTH,((SEGMENTS)*SEGMENTLENGTH)):
			for ix in xrange(0,width):
				b = getBlock(level,ix,y,iz)
				if b != (0,0):
					setBlockForced(level,(95,15),ix,y,iz)
				
	# Store the seed on the ship
	(x,y,z) = BEAMP[0]
	createSign(level, box.minx+x, box.miny+y+1, box.minz+z, str(PARAM))
	# setBlockForced(level, WOOD, box.minx+x,box.miny+y,box.minz+z)
	
	level0.copyBlocksFrom(level, box, (box0.minx, box0.miny, box0.minz )) 	# Box cache support
	
	FuncEnd(level,box,options,method)	

def cosineInterpolate(a, b, x): # http://www.minecraftforum.net/forums/off-topic/computer-science-and-technology/482027-generating-perlin-noise?page=40000
	ft = pi * x
	f = ((1.0 - cos(ft)) * 0.5)
	ret = float(a * (1.0 - f) + b * f)
	return ret

def cnoise(x,y,z):
	# Return the value of interpolated noise at this location
	return float(Random(x+(y<<4)+(z<<8)).random())

def noise(x,y,z):
	ss = 8
	bs = 3
	cx = x >> bs
	cy = y >> bs
	cz = z >> bs

	rdx = float((float(x%ss))/ss)
	rdy = float((float(y%ss))/ss)
	rdz = float((float(z%ss))/ss)
#	print rdx,rdy,rdz
	
	# current noise cell
	P = zeros((2,2,2))
	for iy in xrange(0,2):
		for iz in xrange(0,2):
			for ix in xrange(0,2):
				P[ix,iy,iz] = float(cnoise(cx+ix,cy+iy,cz+iz))
	
	# print P

	dvx1 = cosineInterpolate(P[0,0,0],P[1,0,0],rdx)
	dvx2 = cosineInterpolate(P[0,1,0],P[1,1,0],rdx)
	dvx3 = cosineInterpolate(P[0,0,1],P[1,0,1],rdx)
	dvx4 = cosineInterpolate(P[0,1,1],P[1,1,1],rdx)

	dvz1 = cosineInterpolate(dvx1,dvx3,rdz)
	dvz2 = cosineInterpolate(dvx2,dvx4,rdz)

	n = cosineInterpolate(dvz1,dvz2,rdy)
	
	return n
	
def armada(level0,box0,options):
	method = "Armada"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level0,box0,options,method) # Log start

	level = level0.extractSchematic(box0) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	
	print "Seed:"
	PARAM = int(options["Seed:"])
	if PARAM == 0:
		PARAM = randint(0,99999999999)
	print PARAM
	RAND = Random(PARAM)
	
#	balloons(level,box,options,RAND)
#	return
	
	BARRIER = (166,0)
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
	WHITEWOOL = (35,0)
		
		
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
	DECKHEIGHT = int(HEIGHTQUANTUM*(RAND.randint(1,8)*0.25)-1) # (RAND.randint(1,8)*0.25)
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
	HULLBLOCKS = drawLinesSmooth(level,box,WOOD,SMOOTHAMOUNT,Q)
	
	HULLSHAPEY = RAND.randint(1,6)
	HULLSHAPEX = RAND.randint(2,6)
	if options["Exotic?"] == False:
		HULLSHAPEY = 2
		HULLSHAPEX = 2

	if options["Stage:"] > 1:
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

	if options["Stage:"] > 2:
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

	if options["Stage:"] > 3:
		# Hold
		HOLDSIZE = RAND.randint(2,int(centreWidth/3))
		for i in xrange(1,5):
			HOLDDPOS = RAND.randint(int(centreDepth/2),depth-int(centreDepth*2/3))
			if HOLDSIZE >= 2:
				for y in xrange(DECKROOMVERT*2+2, height):
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

	if options["Stage:"] > 4:
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

	if options["Stage:"] > 5:
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

	if options["Stage:"] > 6:
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

	if options["Stage:"] > 7:
		# Draw the masts and rigging
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
			drawLineForced(level,WOOD,(x-1,y,z),(x,height-1,z-mastgap/MASTSLANT))
			drawLineForced(level,WOOD,(x,y,z+1),(x,height-1,z-mastgap/MASTSLANT))
			drawLineForced(level,WOOD,(x,y,z-1),(x,height-1,z-mastgap/MASTSLANT))
		(x,y,z) = M2
		drawLineForced(level,WOOD,(x-1,y,z),(x,height-1,z-mastgap/MASTSLANT))
		drawLineForced(level,WOOD,(x,y,z+1),(x,height-1,z-mastgap/MASTSLANT))
		drawLineForced(level,WOOD,(x,y,z-1),(x,height-1,z-mastgap/MASTSLANT))
		(x,y,z) = M3
		if MASTS > 1:
			drawLineForced(level,WOOD,(x-1,y,z),(x,height-1,z-mastgap/MASTSLANT))
			drawLineForced(level,WOOD,(x,y,z+1),(x,height-1,z-mastgap/MASTSLANT))
			drawLineForced(level,WOOD,(x,y,z-1),(x,height-1,z-mastgap/MASTSLANT))

		yardist = int((height-1-DECKHEIGHT)/9)
		# Draw the spars
		SPARLIST = []
		y = height-1
		while y > DECKHEIGHT:
			if y == (height-1-yardist) or y == (height-1-3*yardist) or y == (height-1-5*yardist):
				z = depth
				while z >= int(LENGTHQUANTUM/2):
					if getBlock(level, box.minx+centreWidth, box.miny+y, box.minz+z-1) != AIR and getBlock(level, box.minx+centreWidth, box.miny+y, box.minz+z) == AIR:
						# Rigging
						#  Find the edge of the hull a little way forward and back of the mast
						if options["Rigging?"] == True and y == (height-1-5*yardist): # Lowest yard only
							(startx,starty,startz) = (0,0,0)
							(endx,endy,endz) = (0,0,0)
							for HB in HULLBLOCKS:
								for (rigx,rigy,rigz) in HB:
									if rigz == z-int(LENGTHQUANTUM/2):
										(startx,starty,startz) = (rigx,rigy,rigz)
									if rigz == z+int(LENGTHQUANTUM/2):
										(endx,endy,endz) = (rigx,rigy,rigz)
							if (startx,starty,startz) != (0,0,0) and (endx,endy,endz) != (0,0,0):
								drawTriangle(level, (box.minx+centreWidth,box.miny+y,box.minz+z+1), (box.minx+startx+HULLINSET,box.miny+starty,box.minz+startz), (box.minx+endx+HULLINSET,box.miny+endy,box.minz+endz), FENCE, FENCE)
	#							for iz in xrange(startz, endz):
	#								ix = 0 # The rigging (ratline?) has to be straight to look nice. Needs wood under it if the hull curves.
	#								found = False
	#								while ix < centreWidth and found == False: 
	#									block = getBlock(level, box.minx+startx+HULLINSET+ix,box.miny+starty-1,box.minz+iz)
	#									if block == AIR:
	#										found = False
	#										setBlock(level,OAKPLANKS,box.minx+startx+HULLINSET+ix,box.miny+starty-1,box.minz+iz)
	#									else:
	#										found = True
	#									ix = ix+1
								for ix in xrange(-2,1): # platform around the mast
									for iz in xrange(-4,1):
										setBlock(level,OAKPLANKS,box.minx+centreWidth+ix, box.miny+y+2, box.minz+z+iz)
						px1 = (box.minx+centreWidth, box.miny+y, box.minz+z)
						px2 = (box.minx+((centreWidth/2)/((height-y)/yardist)), box.miny+y, box.minz+z)
						SPARLIST.append(px1)
						SPARLIST.append(px2)
						drawLineForced(level, WOODEW,px1,px2)
						if options["Rigging?"] == True and options["Sails?"] == False:
							drawLineForced(level, WHITEWOOL,(box.minx+centreWidth, box.miny+y, box.minz+z+1), (box.minx+((centreWidth/2)/((height-y)/yardist)), box.miny+y, box.minz+z+1))
							drawLineForced(level, WHITEWOOL,(box.minx+centreWidth, box.miny+y-1, box.minz+z+1), (box.minx+((centreWidth/2)/((height-y)/yardist)), box.miny+y-1, box.minz+z+1))
							drawLineForced(level, WHITEWOOL,(box.minx+centreWidth-1, box.miny+y, box.minz+z+2), (box.minx+((centreWidth/2)/((height-y)/yardist))+1, box.miny+y, box.minz+z+2))
							drawLineForced(level, WHITEWOOL,(box.minx+centreWidth-1, box.miny+y-1, box.minz+z+2), (box.minx+((centreWidth/2)/((height-y)/yardist))+1, box.miny+y-1, box.minz+z+2))
					z = z-1					
			if y == (height-1-8*yardist):
				for z in xrange(0,depth):
					if getBlock(level, box.minx+centreWidth, box.miny+y, box.minz+z+1) != AIR and getBlock(level, box.minx+centreWidth, box.miny+y, box.minz+z) == AIR:
						drawLineForced(level, WOODNS,(box.minx+centreWidth, box.miny+y, box.minz+z), (box.minx+centreWidth, box.miny+y, box.minz+z-mastgap/2))
			y=y-1

	if options["Stage:"] > 8:
		# Spar at the front of the ship
		if RAND.randint(1,100) > 20:
			SPARSET = RAND.randint(int(HEIGHTQUANTUM/3),HEIGHTQUANTUM)
			S = []
			(x,y,z) = M3
			S.append((x-1,y,z))
			S.append((x-1,y,z))
			S.append(FORE)
			(fx,fy,fz) = FORE
			F = (centreWidth,fy+SPARSET,depth-1)
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

	if options["Stage:"] > 9:
		# Sails - relies on the location of the yard / spars in the SPARLIST. SPARSLIST counts across the top, middle, then base of the mast yards/spars
		if options["Sails?"] == True:
			i = 0
			drop = RAND.randint(0,2)
			billow = RAND.randint(2,6)
			while i < len(SPARLIST) and len(SPARLIST) %2 == 0:
				(p1x,p1y,p1z) = SPARLIST[i]
				(p2x,p2y,p2z) = SPARLIST[i+1]
				
				SHEET = []
				SHEET.append((p2x,p2y,p2z+1))
				SHEET.append((p2x,p2y,p2z+1))
				SHEET.append(((p1x+p2x)/2,p2y-RAND.randint(1,2),p2z+billow))
				SHEET.append((p1x,p1y-drop,p1z+billow+1))
				SHEET.append((p1x,p1y-drop,p1z+billow+1))
				SHEET1BLOCKS = drawLinesSmoothForced(level,box,WHITEWOOL,SMOOTHAMOUNT,SHEET)
				for S in SHEET1BLOCKS:
					for (sx,sy,sz) in S:
						SHEETLINE = []
						SHEETLINE.append((sx,sy,sz))
						SHEETLINE.append((sx,sy,sz))
						SHEETLINE.append((sx,sy-yardist,sz+2))
						SHEETLINE.append((sx,sy-yardist*15/6,sz))
						SHEETLINE.append((sx,sy-yardist*15/6,sz))
						drawLinesSmoothForced(level,box,WHITEWOOL,SMOOTHAMOUNT,SHEETLINE)
				i = i+2
				
	if options["Stage:"] > 10:
		# Draw the keel
		drawTriangle(level, (centreWidth, DECKHEIGHT, LENGTHQUANTUM/2), (centreWidth, DECKHEIGHT, LENGTHQUANTUM), (centreWidth, 0, LENGTHQUANTUM/3), WOOD, WOOD)
		drawTriangle(level, (centreWidth, 0,LENGTHQUANTUM/3), (centreWidth, 0, LENGTHQUANTUM), (centreWidth, DECKHEIGHT, LENGTHQUANTUM), WOOD, WOOD)

				
	# fill the base with barrier blocks. This helps you place the ship in water
	if options["Barrier Fill?"] == True:
		# Place barrier blocks where the air should be below deck
		y = DECKHEIGHT-1
		keepGoing = True
		while keepGoing == True:
			if y%10 == 0:
				print y
			for z in xrange(0,depth):
				x = 0
				while x <= centreWidth:
					block = getBlock(level,box.minx+x,box.miny+y,box.minz+z)
					if block != AIR:
						for x1 in xrange(x,int(centreWidth)+1):
							block = getBlock(level,box.minx+x1,box.miny+y,box.minz+z)
							if block == AIR:
								setBlock(level,BARRIER,box.minx+x1,box.miny+y,box.minz+z)
						x = centreWidth+1
					x = x+1
			y = y-1
			if y <= 0:
				keepGoing = False		
	
	
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
	block = getBlock(level, box.minx+x,box.miny+y+1,box.minz+z+1) # cleanup
	if block == GLASS: # an error
		setBlockForced(level, AIR, box.minx+x,box.miny+y+1,box.minz+z+1)

	level0.copyBlocksFrom(level, box, (box0.minx, box0.miny, box0.minz ))
		
	FuncEnd(level,box,options,method)

def perform(level,box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	shipBox = box
	NOISEMATERIAL = getBlockFromOptions(options, "Noise Material:")
	if options["Space?"] == False:
		if options["Balloons?"] == True:
			shipBox = BoundingBox((box.minx+int(3*width/8),box.miny,box.minz),(int(centreWidth*5/8),int(centreHeight),depth)) # Smaller box for the ship
		
		
		armada(level,shipBox,options)

		if options["Balloons?"] == True:
			RAND = getRandFromSeed(options)
			boxBalloon = BoundingBox((box.minx,box.miny+int(height/4),box.minz),(width,height-int(height/4),depth-int(depth/10)))
			balloons(level,boxBalloon,options,RAND)
			RAND = getRandFromSeed(options)
			boxBalloon = BoundingBox((box.minx,box.miny+int(height/4),box.minz),(width,height-int(height/4),centreDepth))
			balloons(level,boxBalloon,options,RAND)
			RAND = getRandFromSeed(options)
			boxBalloon = BoundingBox((box.minx,box.miny+int(height/4),box.minz+centreDepth),(width,height-int(height/4),centreDepth-1))
			balloons(level,boxBalloon,options,RAND)

			RAND = getRandFromSeed(options)
			
			# Sketch some cables up to the balloons
			FENCE = (85,0)
			a = pi/18
			drawLine(level,FENCE,(box.minx+centreWidth,box.miny,box.minz+centreDepth-int(depth/20)),(box.minx+centreWidth,box.miny+centreHeight,box.minz+centreDepth-int(depth/20)))
			for i in xrange(0,36):
				if RAND.randint(1,100) > 50:
					drawLine(level,FENCE,(box.minx+centreWidth,box.miny+int(centreHeight/3),box.minz+centreDepth-int(depth/20)),(box.minx+centreWidth-int(centreWidth/3)*cos(i*a),box.miny+centreHeight,box.minz+centreDepth-int(depth/20)-int(centreWidth/3)*sin(i*a)))
	else:
		spaceShip1(level,shipBox,options)
					
	RAND = getRandFromSeed(options)
	threshold = 0.25+RAND.random()/3
	print "Noise limit: "+str(threshold)
	
	if options["Noise?"] == True:
		for y in xrange(box.miny,box.maxy):
			for x in xrange(box.minx,box.maxx):
				for z in xrange(box.minz,box.maxz):
					n = noise(x-box.minx,y-box.miny,z-box.minz)
					if n < threshold:
						(b,d) = getBlock(level,x,y,z)
						if b == 5: # PLANKS
							setBlockForced(level,NOISEMATERIAL,x,y,z)
		
	level.markDirtyBox(box)
	FuncEnd(level,box,options,method) # Log end	

def balloons(level,box,options,RAND):
	method = "Balloons"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	# Pack spheres into the box randomly, adjacent but without overlapping
	P = [] # A collection of sphere positions, with radius
	keepGoing = True
	count = 0
	
	P = []
	P.append((int(centreWidth), int(centreHeight), int(centreDepth),int((centreWidth+centreHeight+centreDepth)/CHUNKSIZE*2),RAND.randint(0,15))) # add centre sphere
	(x0,y0,z0,r0,c0) = P[0] # 1st sphere. Build from here
	
	keepGoing = True
	iters = 0
	while keepGoing == True:
		iters = iters +1
		if iters > 10000:
			keepGoing = False
		c = RAND.randint(0,15)
		r = RAND.randint(int(CHUNKSIZE/8),int(CHUNKSIZE/2))
		theta = RAND.random()*2*pi
		phi = RAND.random()*pi-pi/2
		# bring the sphere in from a distance until it touches the others
		dist = r+r0
		(x, y, z) = (x0+dist*cos(theta)*cos(phi), y0+dist*sin(phi), z0+dist*sin(theta)*cos(phi))
		#drawLine(level,(1,0),(x0,y0,z0),(x,y,z))
		# find a place for this sphere adjacent to the current spheres. Adjust as needed
		collision = 0
		if not (x+r < width and x-r >= 0 and y+r < height and y-r >= 0 and z+r < depth and z-r >= 0): # bounds checking - does this sphere actually fit?
			collision = collision +1
		for (px,py,pz,pr,pc) in P: # check for collisions
			d = sqrt((px-x)**2+(py-y)**2+(pz-z)**2)
			if d < pr+r: # The two spheres overlap
				collision = collision +1
		if collision == 0: # no collisions, ok to add back
			P.append((x,y,z,r,c))
	
	# Render!
	drawSpheres(level,box,options,P,RAND)
	
	FuncEnd(level,box,options,method)

def balloonsRandom(level,box,options,RAND):
	method = "Balloons"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	# Pack spheres into the box randomly, adjacent but without overlapping
	P = [] # A collection of sphere positions, with radius
	keepGoing = True
	count = 0
	
	P = []
	for i in xrange(5,50):
		print i
		(x,y,z) = (RAND.randint(0,width-1),RAND.randint(0,height-1),RAND.randint(0,depth-1))
		c = RAND.randint(0,15)
		r = 1
		exists = False
		for (px,py,pz,pr,pc) in P:
			if x == px and y == py and z == pz:
				exists = True
		if exists == False:
			P.append((box.minx+x,box.miny+y,box.minz+z,r,c)) # add a random point that isn't already in the box
			
			
	keepGoing = True
	stalled = False
	iters = 0
	while keepGoing == True:

		count = 0
		for i in xrange(0,len(P)):
			(x,y,z,r,c) = P.pop()
			r = r+1 # grow the sphere
			collision = 0
			if not (x+r < width and x-r >= 0 and y+r < depth and y-r >= 0 and z+r < depth and z-r >= 0): # bounds checking - does this sphere actually fit?
				collision = collision +1
			for (px,py,pz,pr,pc) in P:
				d = sqrt((px-x)**2+(py-y)**2+(pz-z)**2)
				if d < pr+r-1: # The two spheres overlap
					collision = collision +1
				
			if collision == 0: # no collisions, ok to add back
				P.insert(0,(x,y,z,r,c))
				count = count+1
			else:
				P.insert(0,(x,y,z,r-1,c))
		if count == 0: # No growth in the spheres
			keepGoing = False
		iters = iters+1
		if iters > 1000:
			keepGoing = False

#	(x,y,z) = (int(centreWidth), int(centreHeight), int(centreDepth))
#	r = RAND.randint(2,(width+height+depth)/(2*5))
#	c = RAND.randint(0,15)
#	P.append((box.minx+x,box.miny+y,box.minz+z,r,c))
#	while keepGoing == True:
#		(x,y,z) = (RAND.randint(0,width-1),RAND.randint(0,height-1),RAND.randint(0,depth-1))
#		c = RAND.randint(0,15)
#		r = RAND.randint(2,(width+height+depth)/(2*3))
#		if x+r < width and x-r >= 0 and y+r < depth and y-r >= 0 and z+r < depth and z-r >= 0: # bounds checking - does this sphere actually fit?
#			if len(P) > 0:
#				for ((px,py,pz,pr,pc)) in P: # check for overlap
#					d = sqrt((px-x)**2+(py-y)**2+(pz-z)**2)
#					if d > pr+r: # The two spheres do not overlap
#						P.append((box.minx+x,box.miny+y,box.minz+z,r,c))
#			else:
#				P.append((box.minx+x,box.miny+y,box.minz+z,r,c))
#		if count > 100 and RAND.randint(1,100) < 5: # 5% chance to stop packing spheres
#			keepGoing = False
#		count = count+1
#		if count > 1000:
#			keepGoing = False # cap iterations
	# Render!
	drawSpheres(level,box,options,P)
	
	FuncEnd(level,box,options,method)
	
def drawSpheres(level,box,options,P,RAND):
	method = "drawSpheres"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	FENCE = (85,0)
	
	RAND = getRandFromSeed(options)
	if RAND.randint(1,100) > 70:
		FENCE = AIR
	material = 95
	if RAND.randint(1,100) > 50:
		material = 35
	
	for ((px,py,pz,pr,pc)) in P:
		print (px,py,pz,pr,pc)
		type = RAND.randint(1,10) # What pattern to apply
		for y in xrange(int(-pr),int(pr)):
			for z in xrange(int(-pr),int(pr)):
				for x in xrange(int(-pr),int(+pr)):
					d = sqrt((x)**2+(y)**2+(z)**2)
					if int(d) == int(pr-1) and int(d) <= int(pr):
						if type == 1:
							setBlockForced(level,(material,((y+z+x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 2 :
							setBlockForced(level,(material,((y-z-x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 3 :
							setBlockForced(level,(material,((y-z+x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 4 :
							setBlockForced(level,(material,((y+z-x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 5 :
							setBlockForced(level,(material,((-y-z+x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 6 :
							setBlockForced(level,(material,((-y+z-x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 7 :
							setBlockForced(level,(material,((-y+z+x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 8 :
							setBlockForced(level,(material,((y*z*x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 9 :
							setBlockForced(level,(material,((y*(z+x))*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						else:
							setBlockForced(level,(material,pc),box.minx+px+x,box.miny+py+y,box.minz+pz+z)
						if x%4 == 0 or y%4 == 0 or z%4 == 0:
							setBlock(level,FENCE,box.minx+px+x-1,box.miny+py+y,box.minz+pz+z)
							setBlock(level,FENCE,box.minx+px+x+1,box.miny+py+y,box.minz+pz+z)
							setBlock(level,FENCE,box.minx+px+x,box.miny+py+y-1,box.minz+pz+z)
							setBlock(level,FENCE,box.minx+px+x,box.miny+py+y+1,box.minz+pz+z)
							setBlock(level,FENCE,box.minx+px+x,box.miny+py+y,box.minz+pz+z-1)
							setBlock(level,FENCE,box.minx+px+x,box.miny+py+y,box.minz+pz+z+1)

				
		# Draw a mesh of fences around the sphere to act like ropes

					
	FuncEnd(level,box,options,method)
	
####################################### LIBS
def getRandFromSeed(options):
	PARAM = int(options["Seed:"])
	if PARAM == 0:
		PARAM = randint(0,99999999999)
	print 'Seed: '+str(PARAM)
	return Random(PARAM)

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

def drawLinesSmooth(level,box,material,SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = drawLines(level,box,material,P)
	return Q

def drawLinesSmoothForced(level,box,material,SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = drawLinesForced(level,box,material,P)
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

def drawLinesForced(level,box,material,P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( drawLineForced(level,material,(box.minx+x0,box.miny+y0,box.minz+z0),(box.minx+x,box.miny+y,box.minz+z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q	
	
def drawLineForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	return drawLineConstrainedForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )
	
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

def drawLineConstrainedForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
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
			setBlockForced(scratchpad,(blockID,blockData),xd,yd,zd)
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
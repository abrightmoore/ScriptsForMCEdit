# This filter is for generating Mandelas from the selection box.
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import randint
from random import Random # @Codewarrior0
from numpy import *
from os import listdir
from os.path import isfile, join
import glob
from mcplatform import *
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity, alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials # @Texelelf
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
import inspect # @Texelelf
# from PIL import Image
import png

inputs = (
		("MANDALA", "label"),
		("Seed:", 0),
		("Smooth:", 4),
		("Create Sign?", True),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

MATS = []
for o in xrange(1,6):
	MATS.append(o)
for o in xrange(7,20):
	MATS.append(o)
MATS.append(29)
MATS.append(35)
for o in xrange(41,50):
	MATS.append(o)
for o in xrange(56,59):
	MATS.append(o)
for o in xrange(60,62):
	MATS.append(o)
MATS.append(73)
for o in xrange(79,83):
	MATS.append(o)
for o in xrange(84,90):
	MATS.append(o)
MATS.append(91)
MATS.append(92)
for o in xrange(95,104):
	MATS.append(o)
MATS.append(110)
MATS.append(112)
MATS.append(113)
#for o in xrange(200,256):
#	MATS.append(o)


def getRandomMaterial(RAND): # Simply randomly creates a material
	return (MATS[RAND.randint(0,len(MATS)-1)],0)
	
	
	
	#return (RAND.randint(1,255),0) # This can be improved!

def mandala(level,box,options,RAND):
	method = "Mandala"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start



	# Find the max size of the disc
	rBox = int(floor(centreWidth)) # Radius of the pattern
	if centreDepth < rBox:
		rBox = int(floor(centreDepth))
	print "Pattern max radius is "+str(rBox)
	
	TWOPI = pi*2
	MAXPAT = RAND.randint(4,4+int(floor(rBox/2))) # Max scale of each individual pattern
	
	#for y in xrange(box.miny,box.maxy):
		# Create some circles.
	numCircles = RAND.randint(int(floor(rBox/8)),int(floor(rBox/2))) # Arbitrary
	C = []
	for i in xrange(0,numCircles):
		print i
		r = RAND.randint(1,rBox-1) # The radius of the circle here
		C.append(r)
		# Draw the circle here
		circumference = TWOPI*r
		angleDelta = TWOPI/circumference # Is this just 1/r?
		for y in xrange(box.miny,box.maxy):
			prevPt = (0,y,0)
			material = getRandomMaterial(RAND)
			for s in xrange(0,int(ceil(circumference))): # Check final path?
				(x,z) = (box.minx+centreWidth+r*cos(s*angleDelta),box.minz+centreDepth+r*sin(s*angleDelta))
				if s > 0:
					drawLine(level,material,prevPt,(x,y,z))
				prevPt = (x,y,z)
			
		# loop here
		newStepSize = RAND.randint(int(floor(MAXPAT/4)),MAXPAT*4)
		patternAngleDelta = angleDelta*newStepSize # Magic number, tweak
		if patternAngleDelta > pi/2:
			patternAngleDelta = pi/2
		(d1,t1) = (r,-patternAngleDelta)
		maxR = r+1+MAXPAT-1
		if maxR >= rBox:
			maxR = rBox-1
		minR = r+int(floor(MAXPAT/3))*2
		if minR >= rBox:
			minR = rBox-1
		if minR > maxR:
			t = maxR
			maxR = minR
			minR = t
		
		(d2,t2) = (RAND.randint(minR,maxR),0) #(MAXPAT,0) #(RAND.randint(r+1,r+1+MAXPAT-1),0)
		(d3,t3) = (r,patternAngleDelta)

		material = getRandomMaterial(RAND)
		for s in xrange(0,int(ceil(circumference/(newStepSize)))):
			angleOffset = patternAngleDelta*s
			P = []
			P.append((d1,t1+angleOffset))
			P.append((d2,t2+angleOffset))
			P.append((d3,t3+angleOffset))
			Q = []
			for t in xrange(0,len(P)):
				(d,a) = P[t]
				y = box.miny
				if t%3 == 1:
					y = box.miny+centreHeight
				elif t%3 == 2:
					y = box.maxy-1
				(x0,y0,z0) = (box.minx+centreWidth+d*cos(a),y,box.minz+centreDepth+d*sin(a))
				Q.append((x0,y0,z0))
				if t == 0 or t == len(P)-1:
					Q.append((x0,y0,z0))
			drawLinesSmooth(level,box,material,options["Smooth:"],Q)
			
	
	
	# 1. Draw a pattern
	


	
	# 2. Redraw the pattern a number of times around the circle
	
	
	FuncEnd(level,box,options,method) # Log end	
	
def perform(level,box,options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	level0 = level.extractSchematic(box) # Copy the area of interest into a working area, mostly for 'speed'
	box0 = BoundingBox((0,0,0),(width,height,depth))
	
	(RAND,PARAM) = getRandFromSeed(options) # Extract both a Random and the text equivalent of its seed
	print "Seed: "+str(PARAM)
	
	mandala(level0,box0,options,RAND)

	if options["Create Sign?"] == True:
		createSign(level0, box0.minx+centreWidth, box0.miny, box0.minz+centreDepth, str(PARAM)) # Record the seed that produced this object in a sign at the middle of the base.

	level.copyBlocksFrom(level0, box0, (box.minx, box.miny, box.minz ))	# Copy the working area back into the world
	level.markDirtyBox(box)
	FuncEnd(level,box,options,method) # Log end	
	
####################################### LIBS
def getRandFromSeed(options):
	PARAM = int(options["Seed:"])
	if PARAM == 0:
		PARAM = randint(0,99999999999)
	print 'Seed: '+str(PARAM)
	return (Random(PARAM),PARAM)

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

def flatten(anArray):
	result = []
	for a in anArray:
		for b in a:
			result.append(b)
	return result
	
# Ye Olde GFX Libraries
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

def drawSphere(level,material,r,x,y,z,overwrite):
	r = int(r)
	RSQUARED = r*r
	for iterX in xrange(-r,r):
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			for iterY in xrange(-r,r):
				if XSQUARED + ZSQUARED + iterY*iterY <= RSQUARED:
					plotPoint(level, material, XOFFSET, y+iterY, ZOFFSET, overwrite)

def createSign(level, x, y, z, text): #abrightmoore - convenience method. Due to Jigarbov - this is not a Sign.
	ALIASKEY = "SEED NUMBER"
	COMMANDBLOCK = 137
	CHUNKSIZE = 16
	STANDING_SIGN = 63
	
	setBlockForced(level, (STANDING_SIGN,8), x, y, z)
	setBlockForced(level, (1,0), x, y-1, z)
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

def calcLine((x,y,z), (x1,y1,z1) ):
	return calcLineConstrained((x,y,z), (x1,y1,z1), 0 )
			
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	return drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def calcLinesSmooth(SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = calcLines(P)
	return flatten(Q)

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

def calcLines(P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( calcLine((x0,y0,z0),(x,y,z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
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

def calcLineConstrained((x,y,z), (x1,y1,z1), maxLength ):
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
			# setBlock(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points calc'd

	
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
	if getBlock(level, x,y,z) == (0,0): # AIR
		level.setBlockAt(int(x), int(y), int(z), block)
		level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockForced(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
def plotPoint(level, (block, data), x, y, z, overwrite):
	if overwrite == True:
		setBlockForced(level, (block, data), x, y, z)
	else:
		setBlock(level, (block, data), x, y, z)

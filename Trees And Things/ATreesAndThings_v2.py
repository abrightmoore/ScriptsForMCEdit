# Trees and things
# abrightmoore@yahoo.com.au

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, floor
from random import *
from os import listdir
from os.path import isfile, join
import glob
from mcplatform import *
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity, alphaMaterials, MCSchematic, MCLevel, BoundingBox
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0

# from AJBHelper import *

inputs = (
		("TREES AND THINGS", "label"),
		("Operation",(
			"Palm",
			"Palms",
  		    )),
		("Leaf Block:", alphaMaterials.BlockofQuartz),
		("Trunk Block:", alphaMaterials.Stone),
		("Fruit Block:", alphaMaterials.GlassPane),
		("Seed:", 0),
		("Smoothness:", 4),
		("GROUP PARAMETERS", "label"),
		("Ground Block:", alphaMaterials.Grass),
		("Max Height:", 20),
		("Max Width:", 16),
		("Spacing:", 16),
		("Num Attempts:", 100),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(originalLevel, originalBox, options):
	treeType = options["Operation"]
	seed = options["Seed:"]
	if seed == 0:
		seed = randint(1,999999999999)
	R = Random(seed)
	matLeaf = getBlockFromOptions(options, "Leaf Block:")
	matTrunk = getBlockFromOptions(options, "Trunk Block:")
	matFruit = getBlockFromOptions(options, "Fruit Block:")
	matGround = getBlockFromOptions(options, "Ground Block:")
	smoothamount = options["Smoothness:"]
	maxHeight = options["Max Height:"]
	maxWidth = options["Max Width:"]
	numAttempts = options["Num Attempts:"]
	spacing = options["Spacing:"]
	
	SUCCESS = True
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(originalBox.width,originalBox.height,originalBox.length))

	if treeType == "Palm":
		palm(level,box,R,smoothamount,matLeaf,matTrunk,matFruit)
	elif treeType == "Palms":
		palms(level,box,R,smoothamount,matLeaf,matTrunk,matFruit,matGround,maxHeight,maxWidth,numAttempts,spacing)
	
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096)
		b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

def palms(level,box,R,smoothamount,matLeaf,matTrunk,matFruit,matGround,maxHeight,maxWidth,numAttempts,spacing):
	method = "palms"
	print str(time.ctime())+" Starting "+method
	cx = (box.maxx+box.minx)>>1
	cy = (box.maxy+box.miny)>>1
	cz = (box.maxz+box.minz)>>1
	
	P = [(cx,cz)]
	iters = 0
	keepGoing = True
	while keepGoing == True:
		x,z = P.pop()
		print x,z
		if x > box.maxx-maxWidth:
			x = box.minx+maxWidth+(x-(box.maxx-maxWidth))
		if x < box.minx+maxWidth:
			x = box.maxx-maxWidth-(box.minx+maxWidth-x)
		if z > box.maxz-maxWidth:
			z = box.minz+maxWidth+(z-(box.maxz-maxWidth))
		if z < box.minz+maxWidth:
			z = box.maxz-maxWidth-(box.minz+maxWidth-z)
		
		y = box.maxy-1
		while y >= box.miny:
			block = getBlock(level,x,y,z)
			if block == matGround:
				theHeight = maxHeight
				if theHeight > box.maxy-y:
					theHeight = box.maxy-y
				#theBox = BoundingBox((x-(maxWidth>>1),y,z-(maxWidth>>1)),(maxWidth,theHeight,maxWidth))
				theBox = BoundingBox((0,0,0),(maxWidth,theHeight,maxWidth))
				theLevel = MCSchematic((maxWidth,theHeight,maxWidth))
				palm(theLevel,theBox,R,smoothamount,matLeaf,matTrunk,matFruit)
				b=range(4096)
				b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
				level.copyBlocksFrom(theLevel, theBox, ((x-(maxWidth>>1),y,z-(maxWidth>>1))),b)
				
				
				y = box.miny
			y = y-1
			dir = R.random()*pi*2.0
			P.append((x+spacing*cos(dir),z+spacing*sin(dir)))

		iters = iters + 1
		if iters > numAttempts: #(box.maxx-box.minx)+(box.maxy-box.miny):
			keepGoing = False

	
	print str(time.ctime())+" Ended "+method	
	
def palm(level,box,R,smoothamount,matLeaf,matTrunk,matFruit):
	method = "palm"
	print str(time.ctime())+" Starting "+method
	w = box.maxx-box.minx
	d = box.maxz-box.minz
	h = box.maxy-box.miny
	cw = w>>1
	cd = d>>1
	ch = h>>1
	cx = box.minx+cw
	cy = box.miny+ch
	cz = box.minz+cd
	print cx,cy,cz,w,h,d,cw,ch,cd
	P = []
	(px,py,pz) = (cx,box.miny,cz) # Trunk base
	P.append((px,py,pz))
	P.append(P[0]) # Two of the same point at the start anchors the line
	P.append((px+R.randint(-cw,cw),cy,pz+R.randint(-cd,cd))) # Mid line
	dx = R.randint(-cw>>1,cw>>1)
	dz = R.randint(-cd>>1,cd>>1)
	heightdelta = R.randint(1,ch>>1)
	P.append((px+dx,box.maxy-heightdelta,pz+dz))
	P.append(P[len(P)-1]) # Anchor the end point
	
	TRUNKPOINTS = makePathUnique(flatten(drawLinesSmooth(level,box,matTrunk,smoothamount,P)))
#	for (x,y,z) in TRUNKPOINTS:
#		setBlock(level,matTrunk,x,y,z)

	# Canopy
	numFronds = R.randint(3,7)
	angap = pi*2.0/numFronds
	startang = R.random()*pi
	maxradius = cw
	frondHeightDelta = ch>>1
	if cd < maxradius:
		maxradius = cd
	frondHeight = R.randint(ch+(ch>>3),h-frondHeightDelta)
	for i in xrange(0,numFronds):
		r = R.randint(maxradius>>1,maxradius)
		dx = r*cos(angap*i+startang)
		dz = r*sin(angap*i+startang)
		print dx,dz
		P = []
		(px,py,pz) = TRUNKPOINTS[len(TRUNKPOINTS)-1]
		P.append((px,py,pz))
		P.append(P[0])
		P.append((px+dx/2,box.maxy-1,pz+dz/2))
		P.append((px+dx,box.miny+frondHeight+R.randint(-frondHeightDelta,frondHeightDelta),pz+dz))
		P.append(P[len(P)-1])
		FRONDPOINTS = makePathUnique(flatten(drawLinesSmooth(level,box,matLeaf,smoothamount,P)))
		print FRONDPOINTS
	
	#Fruits
	keepGoing = True
	pos = len(TRUNKPOINTS)-1
	while keepGoing == True:
		if R.random() < 2.0*(float(pos)/float(len(TRUNKPOINTS))):
			(px,py,pz) = TRUNKPOINTS[pos]
			dx = R.randint(-1,1)
			dz = R.randint(-1,1)
			if not (dx == 0 and dz == 0) and (dx == 0 or dz == 0):
				setBlock(level,matFruit,px+dx,py,pz+dz)
		pos = pos - R.randint(0,3)
		if pos < len(TRUNKPOINTS)-(len(TRUNKPOINTS)>>2):
			keepGoing = False
	
	print str(time.ctime())+" Ended "+method	


	
	
	
	
	
	
	
def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def flatten(anArray):
	result = []
	for a in anArray:
		for b in a:
			result.append(b)
	return result

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
	if getBlock(level, x,y,z) == (0,0):
		level.setBlockAt(int(x), int(y), int(z), block)
		level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockForced(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
def calcLinesSmooth(SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = calcLines(P)
	return flatten(Q)
	
def calcLine((x,y,z), (x1,y1,z1) ):
	return calcLineConstrained((x,y,z), (x1,y1,z1), 0 )
	
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

def makePathUnique(P):
	Q = []
	(prevX,prevY,prevZ) = (int(-1),int(-1),int(-1)) # Dummy
	for (x,y,z) in P:
		if (int(x),int(y),int(z)) != (int(prevX),int(prevY),int(prevZ)):
			Q.append((x,y,z))
			(prevX,prevY,prevZ) = (int(x),int(y),int(z))
#		else: # Debug
#			print "Duplicate discarded: "+str(x)+",	"+str(y)+", "+str(z)
	return Q
	
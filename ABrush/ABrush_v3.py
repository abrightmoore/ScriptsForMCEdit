# This filter is for generating voxel objects using a Brush and Path framework.
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

inputs = [
		(
			("ABRUSH", "label"),
			("ACTION", "title"),
			("Operation:", 
				(
					"Apply Brush",
					"Apply Model Brush",
					"Copy Selection to Memory",
					"ATree",
					"Coaster",
					"Gear",
					"Gears",
					"Flower",
				)
			),
			("Brush Name:", ( "lineBRUSH", "lineDashedBRUSH","trackBRUSH","tileSelectionBRUSH","pathSelectionBRUSH","treeRootTrunkBranchBRUSH", )),
			("abrightmoore@yahoo.com.au", "label"),
			("http://brightmoore.net", "label"),

		),
		(
			("OPTIONS", "title"),
			("Seed:", 0),
			("Radius:",-1),
			("Infer Path?", False),
			("Smooth:", 4),
			("Overwrite:", False),
			("Create Sign:", True),
			("abrightmoore@yahoo.com.au", "label"),
			("http://brightmoore.net", "label"),
		),
		(
			("BLOCKS", "title"),
			("Material:", alphaMaterials.Ice),
			("Material 1:", alphaMaterials.Wood),
			("Material 2:", alphaMaterials.BirchWood),
			("Material 3:", alphaMaterials.PinkWool),
			("Material 4:", alphaMaterials.MagentaWool),
			("Material 5:", alphaMaterials.Glowstone),
			("abrightmoore@yahoo.com.au", "label"),
			("http://brightmoore.net", "label"),
		),
]

def leafPatternSpars(RAND):
	# a leaf/petal shape is scalopped based on the seed, and mirrored around the axis.

	NUMSPARS = RAND.randint(1,6) 
	GAP = 1.0/NUMSPARS
	SHAPEX = []
	for i in xrange(0,NUMSPARS): # Control spars - point locations along the length of the leaf defining the curves
		SHAPEX.append((i*GAP,RAND.random())) # Distance from the centre
	return SHAPEX

def leafShape(level,box,options,RAND):
	# Get the shape of a leaf
	method = "leafShape"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	# LeafPattern = leafPatternRandom(level,box,options,RAND)
	LeafPattern = leafPatternSpars(RAND) # This is an edge definition.
	# Now we have a frame harness for the horizontal curve of the leaf
	P = []
	P.append((0,RAND.randint(0,height-1),0))
	P.append(P[0])
	for (z,x) in LeafPattern:
		# brush(level,box,options,RAND,P,"lineBRUSH")
		P.append((-x*centreWidth/2,RAND.randint(0,height-1),z*(centreDepth-1)))
	P.append((0,RAND.randint(0,height-1),centreDepth-1))
	P.append(P[len(P)-1])
	EDGE = calcLinesSmooth(options["Smooth:"],P)
	return EDGE

def flowerStamen(level,box,options,RAND):
	method = "flowerStamen"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	materials = []
	materials.append(getBlockFromOptions(options,"Material:"))
	materials.append(getBlockFromOptions(options,"Material 1:"))
	materials.append(getBlockFromOptions(options,"Material 2:"))
	materials.append(getBlockFromOptions(options,"Material 3:"))	
	materials.append(getBlockFromOptions(options,"Material 4:"))
	materials.append(getBlockFromOptions(options,"Material 5:"))	
	
	stalkMat = materials[RAND.randint(0,len(materials)-1)]
	tipMat = materials[RAND.randint(0,len(materials)-1)]
	count = 10
	while tipMat == stalkMat and count > 0:
		tipMat = materials[RAND.randint(0,len(materials)-1)]
		count = count-1

	tipSize = RAND.randint(0,2)		
	stalkHeight = RAND.randint(0,centreHeight-tipSize)

	wiggle = RAND.randint(2,5)
	
	for i in xrange(0,RAND.randint(0,8)):
		d = RAND.random() * 0.4
		a = RAND.random() * pi/2
		px = d*cos(a)
		pz = d*sin(a)
		y = height
		while y > 0:
			b = getBlock(level,box.minx+centreWidth+px,y,box.minz+centreDepth+pz)
			if b != (0,0): # AIR
				P = []
				P.append((box.minx+centreWidth+px,y,box.minz+centreDepth+pz))
				P.append(P[0])
				P.append((box.minx+centreWidth+px+RAND.randint(-wiggle,wiggle),y+stalkHeight,box.minz+centreDepth+pz+RAND.randint(-wiggle,wiggle)))
				P.append((box.minx+centreWidth+px+RAND.randint(-wiggle,wiggle),y+RAND.randint(int(stalkHeight/2),stalkHeight),box.minz+centreDepth+pz+RAND.randint(-wiggle,wiggle)))
				P.append(P[len(P)-1])
				drawLinesSmooth(level,box,stalkMat,options["Smooth:"],P)
				(tx,ty,tz) = P[len(P)-1]
				if tipSize > 0:
					drawSphere(level,tipMat,tipSize,box.minx+tx,box.miny+ty,box.minz+tz,False)
				y = 0
			y = y -1
	
def flowerColour(level,box,options,RAND):
	method = "flowerColour"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	materials = []
	materials.append(getBlockFromOptions(options,"Material:"))
	materials.append(getBlockFromOptions(options,"Material 1:"))
	materials.append(getBlockFromOptions(options,"Material 2:"))
	materials.append(getBlockFromOptions(options,"Material 3:"))	
	materials.append(getBlockFromOptions(options,"Material 4:"))
	materials.append(getBlockFromOptions(options,"Material 5:"))
	
	c = []
#	c.append((0.1,materials[0]))
#	c.append((0.2,materials[1]))
#	c.append((0.3,materials[2]))
#	c.append((0.5,materials[3]))


	for i in xrange(0,RAND.randint(1,len(materials)-1)): # Choose a random palette
		c.append((RAND.random(),RAND.random(),materials[RAND.randint(0,len(materials)-1)]))
	
	for x in xrange(0,width):
		for z in xrange(0,depth):
			for y in xrange(0,height):
				b = getBlock(level,box.minx+x,box.miny+y,box.minz+z)
				if b != (0,0): # AIR
					(dx,dy,dz) = (x-centreWidth,y,z-centreDepth)
					d = sqrt(dx*dx+dz*dz+y*y)
					for (chance,dist,colmat) in c:
						if d > dist*centreDepth and RAND.random() > chance:
							setBlockForced(level,colmat,box.minx+x,box.miny+y,box.minz+z)
						
	
	
def flower(level,box,options,RAND):
	method = "flower"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	materials = []
	materials.append(getBlockFromOptions(options,"Material:"))
	materials.append(getBlockFromOptions(options,"Material 1:"))
	materials.append(getBlockFromOptions(options,"Material 2:"))
	materials.append(getBlockFromOptions(options,"Material 3:"))	
	materials.append(getBlockFromOptions(options,"Material 4:"))
	materials.append(getBlockFromOptions(options,"Material 5:"))
	
	leafBox = BoundingBox((box.minx,box.miny,box.minz),(width,centreHeight,depth)) # halfheight
	LEAF = leafShape(level,leafBox,options,RAND)
	mat = materials[RAND.randint(0,len(materials)-1)]
	
	NUMLEAVES = RAND.randint(3,11)
	angle = pi*2.0/float(NUMLEAVES)
	for i in xrange(0,NUMLEAVES):
		h = RAND.randint(0,height-1)
		for (x,y,z) in LEAF:
			P = []
			(px,py,pz) = (x,y,z)
			d = sqrt(px*px+pz*pz)
			a = atan2(pz,px)
			(px,pz) = (d*cos(a+angle*i), d*sin(a+angle*i))
			P.append((box.minx+centreWidth+px,box.miny+y,box.minz+centreDepth+pz))
			P.append(P[0])
			(px,py,pz) = (0,y,z)
			d = sqrt(px*px+pz*pz)
			a = atan2(pz,px)
			(px,pz) = (d*cos(a+angle*i), d*sin(a+angle*i))
			P.append((box.minx+centreWidth+px,box.miny+h,box.minz+centreDepth+pz))
			(px,py,pz) = (-x,y,z)
			d = sqrt(px*px+pz*pz)
			a = atan2(pz,px)
			(px,pz) = (d*cos(a+angle*i), d*sin(a+angle*i))
			P.append((box.minx+centreWidth+px,box.miny+y,box.minz+centreDepth+pz))
			P.append(P[len(P)-1])
			drawLinesSmooth(level,box,mat,options["Smooth:"],P)
			h = h + RAND.randint(-1,1)
			if h > centreHeight:
				h = centreHeight
			if h < 0:
				h = 0	
	flowerColour(level,leafBox,options,RAND)
	flowerStamen(level,box,options,RAND)

def gear(level,box,options,RAND):
	# A gear is a circular disc/flywheel with teeth and cut-outs inside.
	# This gear will be a thin cylinder, with an edge.
	
	# Make the cylinder sized to the smaller of the axis
	
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	
	r = int(width/2)
	if depth < r:
		r = int(depth/2)

	teethSize = RAND.randint(4,5+int(r/8))
	r = r-teethSize
	numTeeth = RAND.randint(6,7+r)
	toothAngle = pi/numTeeth
	edgeBevel2 = RAND.randint(2,3+int(r/16))
	edgeBevel1 = r-edgeBevel2
	if edgeBevel1 < edgeBevel2:
		t = edgeBevel1
		edgeBevel1 = edgeBevel2
		edgeBevel2 = edgeBevel1
	
	# Cut aways
	cutNum = RAND.randint(1,5)
	#cutNum = 5 # debug
	cutSize = 8
	if cutNum > 1:
		cutSize = RAND.randint(2,int(r/(cutNum*2)))
	# Draw a cylinder 1/3 the height through the centre of the box

	triangleCuts = True
	if RAND.randint(1,100) > 50: # Triangles
		triangleCuts = False # debug
	
	secondBevel = True
	if RAND.randint(1,100) > 50:
		secondBevel = False

	springs = True
	if RAND.randint(1,100) > 50: # Triangles
		springs = False # debug

	insideOut = False
	if RAND.randint(1,100) > 90: # Teeth inside
		insideOut = True 

	materials = []
	materials.append(getBlockFromOptions(options,"Material:"))
	materials.append(getBlockFromOptions(options,"Material 1:"))
	materials.append(getBlockFromOptions(options,"Material 2:"))
	materials.append(getBlockFromOptions(options,"Material 3:"))
	materials.append(getBlockFromOptions(options,"Material 4:"))
	materials.append(getBlockFromOptions(options,"Material 5:"))
		
	matIndex1 = RAND.randint(0,len(materials)-1)
	matIndex2 = RAND.randint(0,len(materials)-1)
	matIndex3 = RAND.randint(0,len(materials)-1)
		
	maxLayer = RAND.randint(1,3)
	for y in xrange(box.miny,box.maxy):
		py = y-box.miny
		layer = int(py/(int(py/4+1)))%4
		mat = materials[matIndex1]
		if y == box.miny or y == box.maxy-1:
			mat = materials[matIndex2]
		if y == box.miny+1 or y == box.maxy-2:
			mat = materials[matIndex3]

		for x in xrange(box.minx,box.maxx):
			px = x-box.minx-int(width/2)
			for z in xrange(box.minz,box.maxz):

				pz = z-box.minz-int(depth/2)
				
				theta = atan2(pz,px)				
				d = sqrt(px**2+pz**2)
				if insideOut == False and ((d >= edgeBevel1 and d <= r) or (d <= edgeBevel2) or (d < edgeBevel1 and layer > 0 and layer < maxLayer)):
					plotPoint(level, mat, x, y, z, options["Overwrite:"])
				elif insideOut == True and ((d < r and d >= r-teethSize) and int(floor(theta/toothAngle)) % 2 == 0):
					plotPoint(level, mat, x, y, z, options["Overwrite:"])
				elif insideOut == True and (d > r and d <= r+teethSize):
					plotPoint(level, mat, x, y, z, options["Overwrite:"])
				elif insideOut == False and ((d > r and d <= r+teethSize and int(floor(theta/toothAngle)) % 2 == 0) or (secondBevel == True and (int(d) == edgeBevel1-2) or (int(d) == edgeBevel2+2))):
					plotPoint(level, mat, x, y, z, options["Overwrite:"])

		
	# circular cut outs
	if insideOut == False and cutNum > 1:
		for i in xrange(0,cutNum):
			cutAngle = pi*2/cutNum*i
			ox = cos(cutAngle)*int((r)/4)
			oz = sin(cutAngle)*int((r)/4)

			for y in xrange(box.miny,box.maxy):
				for x in xrange(int(ox-cutSize),int(ox+cutSize)):
					for z in xrange(int(oz-cutSize),int(oz+cutSize)):
						dx = x-ox
						dz = z-oz
						if sqrt(dx**2+dz**2) <= cutSize:
							plotPoint(level, (0,0), box.minx+int(width/2)+ox+x, y, box.minz+int(depth/2)+oz+z, True) # Air

	# triangular cut outs
	if insideOut == False and cutNum > 1 and triangleCuts == True:
		cutAngle = pi*2/(cutNum*2)
		for y in xrange(box.miny,box.maxy):
			py = y-box.miny
			for x in xrange(box.minx,box.maxx):
				px = x-box.minx-int(width/2)
				for z in xrange(box.minz,box.maxz):
					pz = z-box.minz-int(depth/2)
					theta = atan2(pz,px)				
					d = sqrt(px**2+pz**2)
					if ((d < edgeBevel1-3 and d > edgeBevel2+3)):
						for i in xrange(0,cutNum*2):
							if i % 2 == 1:
								# print i
								if abs(theta) > i*cutAngle-cutAngle/2 and abs(theta) < (i+1)*cutAngle-cutAngle/2:
									plotPoint(level, (0,0), x, y, z, True) # Air
	
		# Spirally squiggles
	if insideOut == False and springs == True and cutNum > 0:
		(d1,t1) = (RAND.randint(edgeBevel2,edgeBevel1),pi*2*RAND.random())
		(d3,t3) = (RAND.randint(edgeBevel2,edgeBevel1),pi*2*RAND.random())
		(d2,t2) = (edgeBevel1,pi*2*RAND.random())

		for y in xrange(0,box.maxy-box.miny-1):
			mat = materials[matIndex1]
			if y == 0 or y == box.maxy-box.miny-1:
				mat = materials[matIndex2]
			if y == 1 or y == box.maxy-box.miny-2:
				mat = materials[matIndex3]
			(x0,y0,z0) = (int(width/2),y,int(depth/2))
			cutAngle = pi*2/(cutNum*2)
			for i in xrange(0,cutNum*2):
				P = []
				P.append((x0,y0,z0))
				P.append((x0,y0,z0))
				(x1,y1,z1) = (x0+d1*cos(t1+i*cutAngle),y0,z0+d1*sin(t1+i*cutAngle))
				P.append((x1,y1,z1))
				(x3,y3,z3) = (x0+d3*cos(t3+i*cutAngle),y0,z0+d3*sin(t3+i*cutAngle))
				P.append((x3,y3,z3))
				(x2,y2,z2) = (x0+d2*cos(t2+i*cutAngle),y0,z0+d2*sin(t2+i*cutAngle))
				P.append((x2,y2,z2))
				P.append((x2,y2,z2))
				# brush(level,box,options,RAND,P,"lineBRUSH")
				drawLinesSmooth(level,box,mat,options["Smooth:"],P)

def gearsSpammy(level,box,options,RAND):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny

	# Randomly place gears through the space until stop.
	
	count = RAND.randint(5,5+width+depth)
	for i in xrange(0,count):
		print i,count

		try:
			mx = RAND.randint(0,width-height-1)
			mz = RAND.randint(0,depth-height-1)
			dy = RAND.randint(4,4+int(height/2))
			my = RAND.randint(0,height-dy-1)
			dx = RAND.randint(32,height)
			dz = dx

			gearBox = BoundingBox((mx,my,mz),(dx,dy,dz))
			
			gear(level,gearBox,options,RAND)
		except ValueError:
			print "Unable to generate gear, ignoring..."

def gears(level,box,options,RAND):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny

	# Randomly place gears through the space until stop.
	
	count = RAND.randint(5,5+width+depth)
	count = 1000
	for i in xrange(0,count):
		print i,count

		try:
			maxW = 64
			mx = RAND.randint(0,width-maxW-1)
			mz = RAND.randint(0,depth-maxW-1)
			dy = RAND.randint(4,8)
			my = RAND.randint(0,height-dy-1)
			dx = RAND.randint(12,maxW)
			dz = dx

			gearBox = BoundingBox((mx,my,mz),(dx,dy,dz))
			
			gear(level,gearBox,options,RAND)
		except ValueError:
			print "Unable to generate gear, ignoring..."
			
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

def pathSelectionBRUSH(level,box,options,materials,overwrite,RAND,radius,path,arclength,refSchem):
	method = "pathSelectionBRUSH"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	(MX,MY,MZ) = (refSchem.Width,refSchem.Height,refSchem.Length)
	refBox = BoundingBox((MX,MY,MZ))
	print (MX,MY,MZ)
	print refSchem
	print refBox
	
	# Given a path and a 'tile', render each layer of the tile along the path direction
	counter = 0
	(prevX,prevY,prevZ) = (-1,-1,-1)
	for (x,y,z) in path:
		#if counter > 0:
			# To Do: work out which direction we are traveling. This gives the orientation of the tile
		ty = counter % MY
		for tx in xrange(0,MX):
			for tz in xrange(0,MZ):
				plotPoint(level,getBlock(refSchem,tx,ty,tz),x+tx,y,z+tz,overwrite)
		counter = counter +1
		(prevX,prevY,prevZ) = (x,y,z)
		
def tileSelectionBRUSH(level,box,options,materials,overwrite,RAND,radius,path,arclength,refSchem):
	method = "tileSelectionBRUSH"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	(MX,MY,MZ) = (refSchem.Width,refSchem.Height,refSchem.Length)
	refBox = BoundingBox((MX,MY,MZ))
	print (MX,MY,MZ)
	print refSchem
	print refBox
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			

	
	# Given a selection area and a 'tile', copy it into the area 'clone' style
	(px,py,pz) = (box.minx,box.miny,box.minz)
	while py < box.maxy:
		while pz < box.maxz:
			while px < box.maxx:
				for x in xrange(0,MX):
					for y in xrange(0,MY):
						for z in xrange(0,MZ):
							plotPoint(level,getBlock(refSchem,x,y,z),px+x,py+y,pz+z,False)
			
#				print px,py,pz
#				level.copyBlocksFrom(refSchem, refBox, (px, py, pz ))
				
				# plotPoint(level,materials[0],px,py,pz,False)
				px = px+MX
			px = box.minx
			pz = pz+MZ
		pz = box.minz
		py = py+MY
	# level.markDirtyBox(box)

def lineDashedBRUSH(level,box,options,materials,overwrite,RAND,radius,path,arclength):
	method = "lineDashedBRUSH"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	counter = 0
	for (x,y,z) in path:
		if counter % 8 == 0 or counter % 8 == 1 or counter % 8 == 2 or counter % 8 == 5:
			plotPoint(level,materials[0],box.minx+x,box.miny+y,box.minz+z,overwrite)
		counter = counter+1

def trackResolveDiagonals(path):
	counter = 0
	# print path
	# Resolve diagonals
	resultPath = []
	(prevprevx,prevprevy,prevprevz) = (-1,-1,-1)
	(prevx,prevy,prevz) = (-1,-1,-1)
	for (x,y,z) in path:
		if (x,z) != (prevx,prevz): # Ignore vertical transitions
			#resultPath.append((x,y,z))
			if counter >= 1:
			
				# permutations for track
				dirx = x-prevx
				dirz = z-prevz
				diry = y-prevy
				
				# Check if there are any disconnects in the path requiring a patch!
				# Look forward first
				resultPath.append((prevx,prevy,prevz))
#				if diry == 0: # There is no elevation
				if dirz > 0 and dirx < 0: # Diagonal SW
					resultPath.append((prevx-1,prevy,prevz))
				elif dirz > 0 and dirx > 0: # Diagonal SE
					resultPath.append((prevx,prevy,prevz+1))
				elif dirz < 0 and dirx < 0: # Diagonal NW
					resultPath.append((prevx,prevy,prevz-1))
				elif dirz < 0 and dirx > 0: # Diagonal NE
					resultPath.append((prevx,prevy,prevz-1))
			(prevx,prevy,prevz) = (x,y,z)	
#			print (prevx,prevy,prevz),(x,y,z)
			counter = counter+1						
	return resultPath

def trackResolveInclines(path):
	if len(path) > 4:
		# Resolve sudden inclines
		resultPath = []
		resultPath.append(path[0])
		prev = path[0]
		i = 0
		while i < len(path)-3:
			# Look ahead
			(x0,y0,z0) = prev
			(x1,y1,z1) = path[i+1]
			(x2,y2,z2) = path[i+2]
			(x3,y3,z3) = path[i+3]
#			(x4,y4,z4) = path[i+4]
			# Resolve case where 2 is not at the same level as 1 by making 2 == 1 for y
			# 3
			# 21
			#  0
			found = False
#			if (((x0 != x1) and (x1 == x2 == x3)) or (z0 != z1) and (z1 == z2 == z3)) and (y2 > y3):
#				# push p1
#				resultPath.append((x1,y1,z1))
#				# push p2
#				resultPath.append((x2,y3,z2))
#				prev = (x2,y3,z2)
#				i = i + 2
#				found = True

			if (((x0 == x1) and (x1 != x2) and (x2 == x3)) or ((z0 == z1) and (z1 != z2) and (z2 == z3))) and (y2 > y1): # Then move y2 to be y1. ZigZag
				# push p1
				resultPath.append((x1,y1,z1))
				# push p2
				resultPath.append((x2,y1,z2))
				prev = (x2,y1,z2)
				i = i + 2
				found = True
			elif (((x0 == x1) and (x1 != x2) and (x2 == x3)) or ((z0 == z1) and (z1 != z2) and (z2 == z3))) and (y2 < y1): # Then move y1 to be y2. Zig zag
				# push p1
				resultPath.append((x1,y1,z1))
				# push p2
				resultPath.append((x2,y1,z2))
				prev = (x2,y1,z2)
				i = i + 2
				found = True
			
#			elif (((x1 == x2 == x3) and (x0 != x1)) or ((z1 == z2 == z3) and (z0 != z1))) and (y1 > y2):
				# L shape. Raise y2
#				resultPath.append((x1,y1,z1))
#				resultPath.append((x2,y1,z2))
#				prev = (x2,y1,z2)
#				i = i + 2
#				found = True
			elif (((x1 == x2 == x3) and (x0 != x1)) or ((z1 == z2 == z3) and (z0 != z1))) and (y1 < y2):
				# L shape. Drop y2
				resultPath.append((x1,y1,z1))
				resultPath.append((x2,y1,z2))
				prev = (x2,y1,z2)
				i = i + 2
				found = True

			elif (((x1 == x2 == x3) and (x0 != x1)) or ((z1 == z2 == z3) and (z0 != z1))) and (y2 > y3):
				# L shape. Drop y2
				resultPath.append((x1,y1,z1))
				resultPath.append((x2,y3,z2))
				prev = (x2,y1,z2)
				i = i + 2
				found = True
				
#			elif (((x0 == x1 == x2) and (x2 != x3)) or ((z0 == z1 == z2) and (z2 != z3))) and (y0 > y1):
#				resultPath.append((x1,y0,z1))
#				prev = (x1,y0,z1)
#				i = i + 1
#				found = True
#			elif (((x0 == x1 == x2) and (x2 != x3)) or ((z0 == z1 == z2) and (z2 != z3))) and (y1 > y2):
#				resultPath.append((x1,y2,z1))
#				prev = (x1,y0,z1)
#				i = i + 1
#				found = True
				
#			elif ((x0 == x1 == x2) or (z0 == z1 == z2)) and (y2 < y0):
#				resultPath.append((x1,y2,z1))
#				prev = (x1,y2,z1)
#				i = i + 1
#				found = True
				
			if found == False:
				resultPath.append((x1,y1,z1))
				prev = (x1,y1,z1)
				i = i + 1
			
#			if ((x0 == x1) and (x2 == x3) and (x1 != x2)) or ((z0 == z1) and (z2 == z3) and (z1 != z2)):
#				if (y0 != y1):
#					y1 = y0
#				if (y1 != y2):
#					y2 = y1
#				resultPath.append((x1,y1,z1))
#				resultPath.append((x2,y2,z2))
#				prev = (x2,y2,z2)
#				i = i + 2
#			else:
#				resultPath.append((x1,y1,z1))
#				prev = (x1,y1,z1)
#				i = i + 1
				
			
#			if (((x0 == x1) and (x1 != x2)) or ((z0 == z1) and (z1 != z2))) and (y1 != y2):
#				y1 = y2

#			if ((x0 == x1) or (z0 == z1)) and (y0 != y1):
#				y1 = y0
				
#			if ((x0 == x1 == x2) or (z0 == z1 == z2)):
#				if y0 != y1:
#					y1 = y0
#				if y0 == y1 and y2 == y3 and y1 != y2 and ((x2 != x3) or (z2 != z3)):
#					y1 = y2
#				if y1 == y2 and y2 == y3 and y0 != y1:
#					y1 = y0
#				if y1 != y2:
#					y1 = y2

#			if (((x0 != x1) and (x1 == x2 == x3)) or ((z0 != z1) and (z1 == z2 == z3))) and (y1 != y2):
#				y2 = y1
#				resultPath.append((x1,y1,z1))
#				i = i +1
#				(x1,y1,z1) = (x2,y2,z2)
					
		resultPath.append(path[len(path)-2])
		resultPath.append(path[len(path)-1])
		return resultPath
	else:
		return path
	
def trackLay(level,box,materials,overwrite,path):
	RAIL = 66
	PRAIL = 27
	REDSTONE_BLOCK = (152,0)
	counter = 0
	(prevprevx,prevprevy,prevprevz) = (-1,-1,-1)
	(prevx,prevy,prevz) = (-1,-1,-1)
	for (x,y,z) in path:
		#plotPoint(level,materials[1],box.minx+prevx,box.miny-1+prevy,box.minz+prevz,overwrite)
		if (x,z) != (prevx,prevz): # Ignore vertical transitions
			if counter >= 2:

				# permutations for track
				dirx = x-prevx
				dirz = z-prevz
				diry = y-prevy
				prevdirx = prevx-prevprevx
				prevdirz = prevz-prevprevz
				prevdiry = prevy-prevprevy
								
				# Lay down the track!
#				print prevdirx,prevdiry,prevdirz,dirx,diry,dirz
				
				trackData = 0 # default north/south
				
				if abs(prevdirx) > 0 and abs(dirx) > 0 and (diry == 0 or diry < 0) and prevdirz == 0 and dirz == 0:
					trackData = 1
					
	# Incline			
				if (prevdiry < 0 and prevdirx < 0) or (diry > 0 and dirx > 0):
					trackData = 2 # Ascending East
				if (prevdiry < 0 and prevdirx > 0) or (diry > 0 and dirx < 0):
					trackData = 3 # Ascending West
				if (prevdiry < 0 and dirz > 0) or (diry > 0 and dirz < 0):
					trackData = 4 # Ascending North
				if (prevdiry < 0 and dirz < 0) or (diry > 0 and dirz > 0):
					trackData = 5 # Ascending South

	# Curves				
				if (prevdirz < 0 and dirx > 0) or (prevdirx < 0 and dirz > 0): # SE
					trackData = 6
				if (prevdirz < 0 and dirx < 0) or (prevdirx > 0 and dirz > 0): # SW
					trackData = 7
				if (prevdirz > 0 and dirx < 0) or (prevdirx > 0 and dirz < 0): # NW
					trackData = 8
				if (prevdirz > 0 and dirx > 0) or (prevdirx < 0 and dirz < 0): # NE
					trackData = 9
					
					
				if trackData >= 0 and trackData <= 5:
					plotPoint(level,REDSTONE_BLOCK,box.minx+prevx,box.miny+prevy,box.minz+prevz,overwrite)
					plotPoint(level,(PRAIL,trackData+8),box.minx+prevx,box.miny+prevy+1,box.minz+prevz,overwrite) # Put track above the path
				else:
					plotPoint(level,materials[0],box.minx+prevx,box.miny+prevy,box.minz+prevz,overwrite)
					plotPoint(level,(RAIL,trackData),box.minx+prevx,box.miny+prevy+1,box.minz+prevz,overwrite) # Put track above the path

#				createSign(level, box.minx+prevx, box.miny+prevy-5, box.minz+prevz, str(prevdirx)+","+str(prevdiry)+","+str(prevdirz)+" "+str(dirx)+","+str(diry)+","+str(dirz))
#				createSign(level, box.minx+prevx, box.miny+prevy-7, box.minz+prevz, str(prevprevx)+","+str(prevprevy)+","+str(prevprevz)+" "+str(prevx)+","+str(prevy)+","+str(prevz)+" "+str(x)+","+str(y)+","+str(z))

			(prevprevx,prevprevy,prevprevz) = (prevx,prevy,prevz)
			(prevx,prevy,prevz) = (x,y,z)			
			counter = counter+1
	
def trackBRUSH(level,box,options,materials,overwrite,RAND,radius,path,arclength): # Track is Rail
	method = "trackBRUSH" # Creates minecart track along the path.
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
				
	path = trackResolveDiagonals(path)
	path = makePathUnique(path)
	for i in xrange(0,40):
		path = trackResolveInclines(path)
		path = makePathUnique(path)

	trackLay(level,box,materials,overwrite,path)
	trackSupports(level,box,materials,False,path)
	
def trackSupports(level,box,materials,overwrite,path):
	for (x,y,z) in path:
		for i in xrange(0,y):
			plotPoint(level,materials[1],box.minx+x,box.miny+i,box.minz+z,overwrite)
			plotPoint(level,materials[1],box.minx+x-1,box.miny+i,box.minz+z-1,overwrite)
			plotPoint(level,materials[1],box.minx+x-1,box.miny+i,box.minz+z+1,overwrite)
			plotPoint(level,materials[1],box.minx+x+1,box.miny+i,box.minz+z-1,overwrite)
			plotPoint(level,materials[1],box.minx+x+1,box.miny+i,box.minz+z+1,overwrite)
			if i < y/2:
				plotPoint(level,materials[1],box.minx+x-2,box.miny+i,box.minz+z-2,overwrite)
				plotPoint(level,materials[1],box.minx+x-2,box.miny+i,box.minz+z+2,overwrite)
				plotPoint(level,materials[1],box.minx+x+2,box.miny+i,box.minz+z-2,overwrite)
				plotPoint(level,materials[1],box.minx+x+2,box.miny+i,box.minz+z+2,overwrite)				
		plotPoint(level,materials[2],box.minx+x-1,box.miny+y,box.minz+z-1,overwrite)
		plotPoint(level,materials[2],box.minx+x-1,box.miny+y,box.minz+z+1,overwrite)
		plotPoint(level,materials[2],box.minx+x+1,box.miny+y,box.minz+z-1,overwrite)
		plotPoint(level,materials[2],box.minx+x+1,box.miny+y,box.minz+z+1,overwrite)
			
def lineBRUSH(level,box,options,materials,overwrite,RAND,radius,path,arclength):
	method = "lineBRUSH"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	counter = 0
	for (x,y,z) in path:
		plotPoint(level,materials[0],box.minx+x,box.miny+y,box.minz+z,overwrite)
		counter = counter+1
		r = abs(sin(float(counter*arclength))*radius)
		drawSphere(level,materials[0],r,box.minx+x,box.miny+y,box.minz+z,overwrite)
	
def treeRootTrunkBranchBRUSH(level,box,options,materials,overwrite,RAND,radius,path,arclength):
	method = "treeRootTrunkBranch"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	#Render it
	counter = 0
	for (x,y,z) in path:
		plotPoint(level,materials[0],box.minx+x,box.miny+y,box.minz+z,overwrite) # SAP at the core	
		# Trunk section
		counter = counter+1
		r = abs(sin(float(counter*arclength))*radius)
		mat = materials[1]
		if RAND.randint(1,100) > 80:
			mat	= materials[2]
		drawSphere(level,mat,r,box.minx+x,box.miny+y,box.minz+z,overwrite)

def inferPathFromBlocks(level,box):
	P = []
	for y in xrange(box.miny,box.maxy):
		for z in xrange(box.minz,box.maxz):
			for x in xrange(box.minx,box.maxx):
				(blockID,blockData) = getBlock(level,x,y,z)
				if (blockID,blockData) != (0,0): # AIR
					P.append((blockID,x,y,z))
#	print P
	P = sorted(P, key=lambda blockPoint: blockPoint[0])
#	print "After:"
#	print P
	path = []
	for (i,x,y,z) in P:
		path.append((x,y,z))
	return path
		
def brush(level,box,options,RAND,path,theBrush):
	# For a given path, apply the brush and any brush options
	possibles = globals().copy() # http://stackoverflow.com/questions/7936572/python-call-a-function-from-string-name
	possibles.update(locals())
	method = possibles.get(theBrush)
	if not method:
		raise Exception("Method %s not implemented" % theBrush)
	
	# If a path is to be inferred, scan the selection box, find all non-air blocks, and order them based on their blockID
	radius = options["Radius:"]
	if radius < 1:
		radius = RAND.randint(1,int((box.maxy-box.miny)/10)) # Default if not defined properly
	
	if options["Infer Path?"] == True or len(path) == 0:
		path = inferPathFromBlocks(level,box)
		
	# The points in the path may define an interpolated line. If -1, just work with the points. If 0, straight lines. If > 0 Chaiken's smoothing algorithm.
	if options["Smooth:"] > -1:
		path = calcLinesSmooth(options["Smooth:"],path) # Calculate a set of smooth points given the defined path

	# Remove adjacent duplicate points (integer values) which can be artifacts of the previous path smoothing procedure. Speeds up and simplifies the plot.
	path = makePathUnique(path) # Discard duplicate points, if any.
	
	arclength = 0
	if len(path) > 0:
		arclength = pi/len(path) # Used to work out how far along the path we are	
	materials = []
	materials.append(getBlockFromOptions(options,"Material:"))
	materials.append(getBlockFromOptions(options,"Material 1:"))
	materials.append(getBlockFromOptions(options,"Material 2:"))
	materials.append(getBlockFromOptions(options,"Material 3:"))	
	materials.append(getBlockFromOptions(options,"Material 4:"))
	materials.append(getBlockFromOptions(options,"Material 5:"))
	
	return method(level,box,options,materials,options["Overwrite:"],RAND,radius,path,arclength)

def modelBrush(level,box,options,RAND,path,theBrush,refSchem):
	# For a given path, apply the brush and any brush options
	possibles = globals().copy() # http://stackoverflow.com/questions/7936572/python-call-a-function-from-string-name
	possibles.update(locals())
	method = possibles.get(theBrush)
	if not method:
		raise Exception("Method %s not implemented" % theBrush)
	
	# If a path is to be inferred, scan the selection box, find all non-air blocks, and order them based on their blockID
	radius = options["Radius:"]
	if radius < 1:
		radius = RAND.randint(1,int((box.maxy-box.miny)/10)) # Default if not defined properly
	
	if options["Infer Path?"] == True or len(path) == 0:
		path = inferPathFromBlocks(level,box)
		
	# The points in the path may define an interpolated line. If -1, just work with the points. If 0, straight lines. If > 0 Chaiken's smoothing algorithm.
	if options["Smooth:"] > -1:
		path = calcLinesSmooth(options["Smooth:"],path) # Calculate a set of smooth points given the defined path

	# Remove adjacent duplicate points (integer values) which can be artifacts of the previous path smoothing procedure. Speeds up and simplifies the plot.
	path = makePathUnique(path) # Discard duplicate points, if any.
	
	arclength = 0
	if len(path) > 0:
		arclength = pi/len(path) # Used to work out how far along the path we are	
	materials = []
	materials.append(getBlockFromOptions(options,"Material:"))
	materials.append(getBlockFromOptions(options,"Material 1:"))
	materials.append(getBlockFromOptions(options,"Material 2:"))
	materials.append(getBlockFromOptions(options,"Material 3:"))	
	materials.append(getBlockFromOptions(options,"Material 4:"))
	materials.append(getBlockFromOptions(options,"Material 5:"))
	
	return method(level,box,options,materials,options["Overwrite:"],RAND,radius,path,arclength,refSchem)
	
def coaster1(level,box,options,RAND): # The first test coaster. Rename to coaster to test
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	D = 3
	P0 = (0,0,0)
	P1 = (0,RAND.randint(0,height-5),depth-1)
	P2 = (width-1,RAND.randint(0,height-5),depth-1)
	P3 = (width-1,RAND.randint(0,height-5),0)
	P4 = (0,RAND.randint(0,height-5),0)

	for i in xrange(0,8):
		P = []
		(x,y,z) = P0
		P.append((x+i*D,y,z))
		(x,y,z) = P1
		P.append((x+i*D,y,z-i*D))
		(x,y,z) = P2
		P.append((x-i*D,y,z-i*D))
		(x,y,z) = P3
		P.append((x-i*D,y,z+i*D))
		(x,y,z) = P4
		P.append((x-i*D,y,z))
		brush(level,box,options,RAND,P,"trackBRUSH")

def coaster2(level,box,options,RAND):
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	D = 4
	P0 = (centreWidth,centreHeight,centreDepth)
	P1 = (0,centreHeight,depth-1)
	P2 = (width-1,centreHeight,depth-1)
	P3 = (width-1,centreHeight,0)
	P4 = (0,centreHeight,0)
	
	lanes = int((centreWidth+centreHeight)/2/D)
	for i in xrange(0,lanes):
		print i
		P = []
		(x,y,z) = P0
		P.append((x+i*D,y-int(centreHeight/2),z+i*D))
		P.append((x+i*D,y-int(centreHeight/2),z+i*D))

		(x,y,z) = P1
		P.append((x+i*D,y,z-i*D))
		(x,y,z) = P2
		P.append((x-i*D,y,z-i*D))

		(x,y,z) = P0
		P.append((x-i*D,y+int(centreHeight/2),z-i*D))
		(x,y,z) = P0
		P.append((x-i*D,y+int(centreHeight/2),z-i*D))

		(x,y,z) = P3
		P.append((x-i*D,y,z+i*D))
		(x,y,z) = P4
		P.append((x+i*D,y,z+i*D))

		(x,y,z) = P0
		P.append((x+i*D,y-int(centreHeight/2),z+i*D))
		P.append((x+i*D,y-int(centreHeight/2),z+i*D))

		brush(level,box,options,RAND,P,"trackBRUSH")
	
def coaster3(level,box,options,RAND):
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	D = 3
	P0 = (centreWidth,centreHeight,centreDepth)
	P1 = (0,RAND.randint(0,height-5),depth-1)
	P2 = (width-1,RAND.randint(0,height-5),depth-1)
	P3 = (width-1,RAND.randint(0,height-5),0)
	P4 = (0,RAND.randint(0,height-5),0)
	
	lanes = int((centreWidth+centreHeight)/2/D)
	for i in xrange(0,lanes):
		print i
		P = []
		(x,y,z) = P0
		P.append((x+i*D,y-int(centreHeight)+2*i,z))
		P.append((x+i*D,y-int(centreHeight)+2*i,z))

		(x,y,z) = P1
		P.append((x+i*D,y,z-i*D))
		(x,y,z) = P2
		P.append((x-i*D,y,z-i*D))

		(x,y,z) = P0
		P.append((x+i*D,y+int(centreHeight)-2*i,z))
		P.append((x+i*D,y+int(centreHeight)-2*i,z))

		(x,y,z) = P4
		P.append((x-i*D,y,z))
		(x,y,z) = P3
		P.append((x-i*D,y,z+i*D))

		(x,y,z) = P0
		P.append((x+i*D,y-int(centreHeight)+2*i,z))
		P.append((x+i*D,y-int(centreHeight)+2*i,z))

		(x,y,z) = P1
		P.append((x+i*D,y,z-i*D))
		(x,y,z) = P2
		P.append((x-i*D,y,z-i*D))

		(x,y,z) = P0
		P.append((x+i*D,y+int(centreHeight)-2*i,z))
		P.append((x+i*D,y+int(centreHeight)-2*i,z))
		
		brush(level,box,options,RAND,P,"trackBRUSH")	
	
def coaster4(level,box,options,RAND): # Loop
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	D = 3
	P0 = (centreWidth,centreHeight,centreDepth)
	P1 = (0,centreHeight-int(centreHeight/4),depth-1)
	P2 = (width-1,centreHeight,depth-1)
	P3 = (width-1,centreHeight+int(centreHeight/4),0)
	P4 = (0,centreHeight,0)
	
	lanes = int((centreWidth+centreHeight)/2/D)
#	if lanes > 10:
#		lanes = 10 # Realms limit
	for i in xrange(0,lanes):
		print i
		P = []
		(x,y,z) = P1
		P.append((x+i*D,y,z-i*D))
		(x,y,z) = P2
		P.append((x-i*D,y,z-i*D))
		(x,y,z) = P3
		P.append((x-i*D,y,z+i*D))
		(x,y,z) = P4
		P.append((x+i*D,y,z+i*D))
		(x,y,z) = P1
		P.append((x+i*D,y,z-i*D))
		(x,y,z) = P2
		P.append((x-i*D,y,z-i*D))

		brush(level,box,options,RAND,P,"trackBRUSH")	

def coaster5(level,box,options,RAND): # Loop
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	D = 3
	P0 = (centreWidth,centreHeight,centreDepth)
	P1 = (0,centreHeight-int(centreHeight/4),depth-1)
	P2 = (width-1,centreHeight,depth-1)
	P3 = (width-1,centreHeight+int(centreHeight/4),0)
	P4 = (0,centreHeight,0)
	
	lanes = int((centreWidth+centreHeight)/2/D)
#	if lanes > 10:
#		lanes = 10 # Realms limit
	P = []
	P.append(((RAND.randint(0,width-1)),(RAND.randint(0,height-1)),(RAND.randint(0,depth-1))))
	P.append(P[0])
	for i in xrange(7,RAND.randint(8,20)):
		P.append(((RAND.randint(0,width-1)),(RAND.randint(0,height-1)),(RAND.randint(0,depth-1))))
	P.append(P[0])
	P.append(P[0])
	
	brush(level,box,options,RAND,P,"trackBRUSH")

def coaster6(level,box,options,RAND): # Loop - random smoosh. Localised
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	D = 3
	P0 = (centreWidth,centreHeight,centreDepth)
	P1 = (0,centreHeight-int(centreHeight/4),depth-1)
	P2 = (width-1,centreHeight,depth-1)
	P3 = (width-1,centreHeight+int(centreHeight/4),0)
	P4 = (0,centreHeight,0)
	
	lanes = int((centreWidth+centreHeight)/2/D)
#	if lanes > 10:
#		lanes = 10 # Realms limit
	P = []
	P.append(((RAND.randint(0,width-1)),(RAND.randint(0,height-1)),(RAND.randint(0,depth-1))))
	P.append(P[0])
	(x,y,z) = P[0]
	for i in xrange(0,RAND.randint(width+1,width+depth)):
		print i
		(x1,y1,z1) = (x+RAND.randint(-32,32),y+RAND.randint(-32,32),z+RAND.randint(-32,32))
		if x1 > width - 1:
			x1 = width-17
		if x1 < 0:
			x1 = 16
		if y1 > height-2:
			y1 = centreHeight
		if y1 < 0:
			y1 = 16
		if z1 > depth-1:
			z1 = depth-17
		if z1 < 0:
			z1 = 16
		P.append((x1,y1,z1))
	P.append(P[0])
	P.append(P[0])
	
	brush(level,box,options,RAND,P,"trackBRUSH")

def coaster7(level,box,options,RAND): # Loop
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	D = 3
	P0 = (centreWidth,centreHeight,centreDepth)
	P1 = (0,centreHeight-int(centreHeight/4),depth-1)
	P2 = (width-1,centreHeight,depth-1)
	P3 = (width-1,centreHeight+int(centreHeight/4),0)
	P4 = (0,centreHeight,0)
	
	P = []
	P.append(P0)
	P.append(P0)

	P.append((centreWidth,0,0))
	P.append((0,0,0))
	P.append((0,0,depth-1))
	P.append((width-1,centreHeight,depth-1))
	P.append((width-1,centreHeight,centreDepth))
	P.append((width-1,height-2,0))
	P.append((centreWidth,0,0))
	P.append((centreWidth,0,centreDepth))
	P.append((width-1,0,centreDepth))
	P.append((width-1,0,depth-1))

	P.append(P0)
	P.append(P0)

	brush(level,box,options,RAND,P,"trackBRUSH")	

def coaster8(level,box,options,RAND): # Loop
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	P = []
	
	dirH = 0
	dirV = 0

	P.append((centreWidth,centreHeight,centreDepth))
	P.append(P[0])
	(x,y,z) = P[0]
	for i in xrange(0,RAND.randint(width+1,width+depth)):
		print i
		(x1,y1,z1) = (x,y,z)
		if dirH == 0:
			z1 = z1+RAND.randint(1,3)*8
		elif dirH == 1:
			x1 = x1+RAND.randint(1,3)*8
			z1 = z1+RAND.randint(1,3)*8
		elif dirH == 2:
			x1 = x1+RAND.randint(1,3)*8
		elif dirH == 3:
			x1 = x1+RAND.randint(1,3)*8
			z1 = z1-RAND.randint(1,3)*8
		elif dirH == 4:
			z1 = z1-RAND.randint(1,3)*8
		elif dirH == 5:
			x1 = x1-RAND.randint(1,3)*8
			z1 = z1-RAND.randint(1,3)*8
		elif dirH == 6:
			x1 = x1-RAND.randint(1,3)*8
		elif dirH == 7:
			x1 = x1-RAND.randint(1,3)*8
			z1 = z1+RAND.randint(1,3)*8

		if dirV == 0:
			y1 = y1-RAND.randint(1,3)*8
			dirV = 1
		elif dirV == 2:
			y1 = y1+RAND.randint(1,3)*8
			dirV = 1
			
		if x1 > width - 1:
			x1 = width-17
			dirH = (dirH + RAND.randint(-1,1))%8
		if x1 < 0:
			x1 = 16
			dirH = (dirH + RAND.randint(-1,1))%8
		if y1 > height-2:
			y1 = centreHeight
			dirV = (dirV+RAND.randint(-1,1))%3
		if y1 < 0:
			y1 = 16
			dirV = (dirV+RAND.randint(-1,1))%3
		if z1 > depth-1:
			z1 = depth-17
			dirH = (dirH + RAND.randint(-1,1))%8
		if z1 < 0:
			z1 = 16
			dirH = (dirH + RAND.randint(-1,1))%8
		P.append((x1,y1,z1))
		
		dirH = (dirH + RAND.randint(-1,1))%8
		
		if RAND.randint(1,100) > 80:
			dirV = (dirV+RAND.randint(-1,1))%3
		(x,y,z) = (x1,y1,z1)
		
	P.append(P[0])
	P.append(P[0])
	
	brush(level,box,options,RAND,P,"trackBRUSH")

def coaster(level,box,options,RAND): # Loop
	method = "Coaster"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	P = []
	
	dirH = 0
	dirV = 0

	P.append((centreWidth,centreHeight,centreDepth))
	P.append(P[0])
	(x,y,z) = P[0]
	for i in xrange(0,RAND.randint(width+1,width+depth)):
		print i
		(x1,y1,z1) = (x,y,z)
		if dirH == 0:
			z1 = z1+RAND.randint(1,3)*8
		elif dirH == 1:
			x1 = x1+RAND.randint(1,3)*8
			z1 = z1+RAND.randint(1,3)*8
		elif dirH == 2:
			x1 = x1+RAND.randint(1,3)*8
		elif dirH == 3:
			x1 = x1+RAND.randint(1,3)*8
			z1 = z1-RAND.randint(1,3)*8
		elif dirH == 4:
			z1 = z1-RAND.randint(1,3)*8
		elif dirH == 5:
			x1 = x1-RAND.randint(1,3)*8
			z1 = z1-RAND.randint(1,3)*8
		elif dirH == 6:
			x1 = x1-RAND.randint(1,3)*8
		elif dirH == 7:
			x1 = x1-RAND.randint(1,3)*8
			z1 = z1+RAND.randint(1,3)*8

		if dirV == 0:
			y1 = y1-RAND.randint(1,3)*8
			dirV = 1
		elif dirV == 2:
			y1 = y1+RAND.randint(1,3)*8
			dirV = 1

		
		dirH = (dirH + RAND.randint(-1,1))%8
		
		if RAND.randint(1,100) > 80:
			dirV = (dirV+RAND.randint(-1,1))%3

		if x1 > width - 1:
			x1 = width-17
			dirH = (dirH + RAND.randint(-1,1))%8
		if x1 < 0:
			x1 = 16
			dirH = (dirH + RAND.randint(-1,1))%8
		if y1 > height-2:
			y1 = height-3
			dirV = (dirV+RAND.randint(-1,1))%3
		if y1 < 0:
			y1 = 0
			dirV = (dirV+RAND.randint(0,1))%3
		if z1 > depth-1:
			z1 = depth-17
			dirH = (dirH + RAND.randint(-1,1))%8
		if z1 < 0:
			z1 = 16
			dirH = (dirH + RAND.randint(-1,1))%8
		
		# Adjust the next point to fit within the bounds of what Minecraft can draw.
		diffH = abs(abs(x1-x)-abs(z1-z))
		diffV = y1-y
		if abs(diffV) >= (diffH-1)/3*2: # Too high
			if diffV > 0:
				y1 = y+int(diffH/3*2)-2
			elif diffV < 0:
				y1 = y-int(diffH/3*2)+2
			else: # 0
				y1 = y
		# End adjust next point.		
		
		(x,y,z) = (x1,y1,z1)		
		P.append((x1,y1,z1))
				
	P.append(P[0])
	P.append(P[0])
	
	brush(level,box,options,RAND,P,"trackBRUSH")
	
def atree(level,box,options,RAND):
	method = "ATree"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	MAT_LEAF = getBlockFromOptions(options,"Material 3:")
	MAT_LEAF2 = getBlockFromOptions(options,"Material 4:")
	MAT_FRUIT = getBlockFromOptions(options,"Material 5:")
	SMOOTHAMT = options["Smooth:"]
	
	maxR = RAND.randint(1,int(height/10))
	FOLIAGEHEIGHT = RAND.randint(int(floor(centreHeight/4)),height-2*maxR)
	FOLIAGECHANCE = RAND.randint(5,50)
		
	cw = centreWidth  # Convenience
	ch = centreHeight # Convenience
	cz = centreDepth  # Convenience

	cw2 = cw-4+RAND.randint(0,8)
	cz2 = cz-4+RAND.randint(0,8)
	
	# A twisty trunk
	print "Trunk..."
	refRadius = int(floor((cw+cz)/2))
	ENDS = []

	centreTrunk = (cw-refRadius/16+RAND.randint(0,refRadius/8),RAND.randint(int(floor(centreHeight/4)),int(floor(centreHeight+centreHeight/4))),cz-refRadius/16+RAND.randint(0,refRadius/8))
	
	SQUIG = []
	for j in xrange(0,RAND.randint(1,3)):
		SQUIG.append((cw-refRadius/16+RAND.randint(0,refRadius/8),RAND.randint(int(floor(centreHeight/4))*j,int(floor(centreHeight/4))*j+int(floor(centreHeight/3))*j),cz-refRadius/16+RAND.randint(0,refRadius/8)))
	
	for i in xrange(0,4+int(height/16)): # A number of tendrils
		P = []
		start = (cw,0,cz)
		if RAND.randint(1,100) > 10:
			start = (cw-int(floor(refRadius/2))+RAND.randint(0,refRadius),0,cz-int(floor(refRadius/2))+RAND.randint(0,refRadius))
		P.append(start) # Root start
		P.append(start) # Root start
		if RAND.randint(1,100) > 10: # Squiggle root
			P.append((cw-int(floor(refRadius/2))+RAND.randint(0,refRadius),0,cz-int(floor(refRadius/2))+RAND.randint(0,refRadius)))
		for j in SQUIG:
			P.append(j)
#		P.append((cw2,centreHeight,cz2)) # Centre mark of trunk
#		if RAND.randint(1,100) > 95:
#			P.append((cw2,centreHeight+RAND.randint(0,centreHeight),cz2)) # Centre mark of trunk
#		else:
		P.append(centreTrunk) # Centre mark of trunk
		P.append((cw2,height-int(floor(height/8)),cz2)) # Top of trunk
		end = (cw-refRadius+RAND.randint(0,2*refRadius),height-RAND.randint(1,int(centreHeight/2)),cz-refRadius+RAND.randint(0,2*refRadius))
		P.append(end) # Branch end
		P.append(end) # Branch end
		ENDS.append(end) # Record this location
#		mat = MAT_TRUNK
#		if RAND.randint(1,100) > 80:
#			mat	= MAT_TRUNK2
#		C = drawLinesSmooth(level,box,mat,SMOOTHAMT,P) # Calculate the shape of the face
#		C = flatten(C)
		brush(level,box,options,RAND,P,options["Brush Name:"])		
		
	print "Foliage"
	for y in xrange(height-maxR*4,height): # More foliage on top
		for x in xrange(0,width):
			for z in xrange(0,depth):
				if getBlock(level,x,y,z) != (0,0) and RAND.randint(1,100) <= FOLIAGECHANCE:
					mat = MAT_LEAF
					if RAND.randint(1,100) > 80:
						mat = MAT_LEAF2
					setBlockForced(level,mat,x,y,z)
	
	print "Fruit"
	for (x,y,z) in ENDS:
		depth = RAND.randint(maxR,centreHeight)
		for i in xrange(1,depth):
			setBlock(level,(85,0),x,y-i,z) # Fence
		setBlockForced(level,MAT_FRUIT,x,y-depth,z)
	

	# Store the seed on the tree
#	(x,y,z) = (cw,0,cz)
#	createSign(level, box.minx+x, box.miny+y+1, box.minz+z, str(PARAM))


	FuncEnd(level,box,options,method)

def perform(level,box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	global THESTOREDSHAPE

	
	# 0. Create a working area
	#
	# 1. Create a path, which is a collection of points
	# 2. Create a brush
	# 3. Render the path using the brush
	# 4. Repeat from 1 until complete
	# 5. When complete, copy the working area into the world level

	# 0.
	level0 = level.extractSchematic(box) # Copy the area of interest into a working area, mostly for 'speed'
	box0 = BoundingBox((0,0,0),(width,height,depth))
#	level0 = level
#	box0 = box
	
	(RAND,PARAM) = getRandFromSeed(options) # Extract both a Random and the text equivalent of its seed
	print "Seed: "+str(PARAM)
	# 1. to 4. Replace this with your object procedure
	
	if options["Operation:"] == "Copy Selection to Memory":
		THESTOREDSHAPE = level.extractSchematic(box)
		# refBox = BoundingBox((refSchem.Width,refSchem.Height,refSchem.Length))
	elif options["Operation:"] == "ATree": # An example of using the framework programmatically
		atree(level0,box0,options,RAND)
	elif options["Operation:"] == "Coaster": # An example of using the framework programmatically
		coaster(level0,box0,options,RAND)
	elif options["Operation:"] == "Gear": # An example of using the framework programmatically
		gear(level0,box0,options,RAND)
	elif options["Operation:"] == "Gears": # An example of using the framework programmatically
		gears(level0,box0,options,RAND)
	elif options["Operation:"] == "Flower":
		flower(level0,box0,options,RAND)

	elif options["Operation:"] == "Apply Model Brush":
		modelBrush(level0,box0,options,RAND,[],options["Brush Name:"],THESTOREDSHAPE)
	else:
		brush(level0,box0,options,RAND,[],options["Brush Name:"])

	if options["Create Sign:"] == True:
		createSign(level0, box0.minx+centreWidth, box0.miny+1, box0.minz+centreDepth, str(PARAM)) # Record the seed that produced this object in a sign at the middle of the base.

	# 5.
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

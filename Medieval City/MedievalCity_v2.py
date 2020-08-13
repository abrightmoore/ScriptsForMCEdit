# This filter is to create a Medieval style city
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
from random import Random # @Codewarrior0

inputs = (
		("MEDIEVAL CITY", "label"),
		("Quick render?", True),
		("Seed:", 42),
		("Fill Material:", alphaMaterials.BlockofQuartz),
		("Edge Material:", alphaMaterials.BlockofQuartz),
		("Floor Material:", alphaMaterials.BlockofQuartz),
		("Roof Material:", alphaMaterials.BlockofQuartz),
		("Glass Material:", alphaMaterials.BlockofQuartz),
		("Max Iterations:", 10000),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def MedievalHouse2(level,box,options):
	# Spam some boxes.
	method = "MedievalHouse1"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	
	rangle = randint(0,359) # Orientation of the building
	boxes = []
	keepGoing = True
	posx = box.minx+centreWidth
	posz = box.minz+centreDepth
	posy = box.miny
	counter = 0
	while keepGoing == True:
		counter += 1
		print counter
		curHeight = 4+randint(0,6)
		thisWidth = randint(10,16)
		thisDepth = randint(int(thisWidth/1.5),int(thisWidth*1.5))
		newBox = BoundingBox((posx-thisWidth/2,posy,posz-thisDepth/2),(thisWidth,curHeight,thisDepth))
		print newBox
		MedievalRoom1(level, newBox, options, rangle,False)
		boxes.append(newBox)
		posx = posx + randint(-thisWidth,thisWidth)
		posz = posz + randint(-thisDepth,thisDepth)
		if randint(0,100) < 90: # go up!
			abox = boxes.pop(randint(0,len(boxes)-1))
			aboxw = abox.maxx-abox.minx
			aboxd = abox.maxz-abox.minz
			newBox = BoundingBox((abox.minx+randint(1,4),abox.maxy,abox.minz+randint(1,4)),(abox.maxx-abox.minx-randint(1,8),curHeight,abox.maxz-abox.minz-randint(1,8)))
			MedievalRoom1(level, newBox, options, rangle,True)
			boxes.append(abox)
		if randint(0,100) < 5:
			keepGoing = False

def MedievalHouse1(level,box,options):
	# Spam some boxes.
	method = "MedievalHouse1"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	
	rangle = randint(0,359) # Orientation of the building
	boxes = []
	keepGoing = True
	posx = box.minx+centreWidth
	posz = box.minz+centreDepth
	posy = box.miny
	counter = 0
	while keepGoing == True:
		counter += 1
		print counter
		curHeight = 4+randint(0,4)
		thisWidth = randint(8,16)
		thisDepth = randint(int(thisWidth/1.5),int(thisWidth*1.5))
		newBox = BoundingBox((posx-thisWidth/2,posy,posz-thisDepth/2),(thisWidth,curHeight,thisDepth))
		print newBox
		MedievalRoom1(level, newBox, options, rangle,True)
		boxes.append(newBox)
		posx = posx + randint(-thisWidth,thisWidth)
		posz = posz + randint(-thisDepth,thisDepth)
		if randint(0,100) < 50: # go up!
			abox = boxes.pop(randint(0,len(boxes)-1))
			aboxw = abox.maxx-abox.minx
			aboxd = abox.maxz-abox.minz
			newBox = BoundingBox((abox.minx+randint(1,4),abox.maxy,abox.minz+randint(1,4)),(abox.maxx-abox.minx-randint(1,8),curHeight,abox.maxz-abox.minz-randint(1,8)))
			MedievalRoom1(level, newBox, options, rangle,True)
			boxes.append(abox)
		if randint(0,100) < 5:
			keepGoing = False
		
	
	

def MedievalRoom1(level, box, options, rangle, roof):
	method = "MedievalRoom1"
#	level = MCSchematic((box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz)) # Working object
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,"",method) # Log 
	fillMaterial = getBlockFromOptions(options,"Fill Material:")
	edgeMaterial = getBlockFromOptions(options,"Edge Material:")
	floorMaterial = getBlockFromOptions(options,"Floor Material:")
	roofMaterial = getBlockFromOptions(options,"Roof Material:")
	
	ANGLE = pi/180
	w = centreWidth-1
	h = height-1
	d = centreDepth-1
	
	# Extremities of the cube
	o = (box.minx+centreWidth,box.miny,box.minz+centreDepth)
	p = [		(-w,0,-d),			# 0
				(w,0,-d),	# 1
				(w,0,d),	# 2
				(-w,0,d),	# 3
				(-w,h,-d),	# 4
				(w,h,-d),	# 5
				(w,h,d),	# 6
				(-w,h,d)		# 7
			  ]

	# Rotate!
#	rangle = randint(0,359) # Degrees!
	theta = rangle * ANGLE
	T = [	(cos(theta),0,sin(theta)),
			(0,1.0,0),
			(cos(theta+pi/2),0,sin(theta+pi/2)) ] # Simple transformation around Y
	tp = transformPoints( p, o, T) # Transformed Points
	
#	(min,max) = getMinMax(tp)
#	rBox = BoundingBox(min,max) 
#	level = MCSchematic((rBox.maxx-rBox.minx,rBox.maxy-rBox.miny,rBox.maxz-rBox.minz))

	drawRectangle(level, box, options,
					tp[0],
					tp[1],
					tp[2],
					tp[3],
					floorMaterial)
	drawRectangle(level, box, options,
					tp[4],
					tp[5],
					tp[6],
					tp[7],
					floorMaterial)
	drawTrussWall(level, box, options, [tp[0],tp[1],tp[5],tp[4]] , fillMaterial, edgeMaterial)
	drawTrussWall(level, box, options, [tp[0],tp[3],tp[7],tp[4]] , fillMaterial, edgeMaterial)
	drawTrussWall(level, box, options, [tp[3],tp[2],tp[6],tp[7]] , fillMaterial, edgeMaterial)
	drawTrussWall(level, box, options, [tp[1],tp[2],tp[6],tp[5]] , fillMaterial, edgeMaterial)

	if roof == True:
		# Roof!
		h *= 3
		d *= 1.5
		w *= 1.5
		o = (box.minx+centreWidth,box.maxy,box.minz+centreDepth)
		p = [		(0,h,0),			 	#0
					(w/10,h/3*2,d/10),			#1
					(w/10,h/3*2,-d/10),			#2
					(-w/10,h/3*2,-d/10),			#3
					(-w/10,h/3*2,d/10),			#4
					(w/3,h/4,d/3),	#5
					(w/3,h/4,-d/3),	#6
					(-w/3,h/4,-d/3),#7
					(-w/3,h/4,d/3),	#8
					(w,0,d),				#9
					(w,0,-d),				#10
					(-w,0,-d),				#11	
					(-w,0,d),				#12
				  ]

		# Rotate!
	#	rangle = randint(0,359) # Degrees!
		T = [	(cos(theta),0,sin(theta)),
				(0,1.0,0),
				(cos(theta+pi/2),0,sin(theta+pi/2)) ] # Simple transformation around Y
		tp = transformPoints( p, o, T) # Transformed Points

		drawRectangle(level, box, options,
						tp[9],
						tp[10],
						tp[11],
						tp[12],
						floorMaterial)
		
		drawTrussWall(level, box, options, [tp[0],tp[1],tp[2],tp[0]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[0],tp[2],tp[3],tp[0]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[0],tp[3],tp[4],tp[0]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[0],tp[4],tp[1],tp[0]] , roofMaterial, edgeMaterial)
		
		drawTrussWall(level, box, options, [tp[1],tp[2],tp[6],tp[5]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[2],tp[3],tp[7],tp[6]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[3],tp[4],tp[8],tp[7]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[4],tp[1],tp[5],tp[8]] , roofMaterial, edgeMaterial)

		drawTrussWall(level, box, options, [tp[5],tp[6],tp[10],tp[9]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[6],tp[7],tp[11],tp[10]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[7],tp[8],tp[12],tp[11]] , roofMaterial, edgeMaterial)
		drawTrussWall(level, box, options, [tp[8],tp[5],tp[9],tp[12]] , roofMaterial, edgeMaterial)
	
def drawTrussWall(level, box, options, points, fillMaterial, edgeMaterial):
	# Walls
	drawRectangle(level, box, options,
					points[0],
					points[1],
					points[2],
					points[3],
					fillMaterial)
	# Edge around wall
	drawLine(level, edgeMaterial, points[0],points[1])
	drawLine(level, edgeMaterial, points[1],points[2])
	drawLine(level, edgeMaterial, points[2],points[3])
	drawLine(level, edgeMaterial, points[3],points[0])
	# Braces
	drawLine(level, edgeMaterial, points[0],points[2])
	drawLine(level, edgeMaterial, points[1],points[3])
	
def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "PERFORM MEDIEVALCITY"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
#	level = originalLevel.extractSchematic(originalBox) # Working set
#	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	
	MedievalHouse2(originalLevel, originalBox, options)
	# Conditionally copy back the working area into the world
#	if SUCCESS == True: # Copy from work area back into the world
#		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
#		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
#		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,originalBox,options,method) # Log end
	
############# METHOD HELPERS #############
def areaOfPolygon(points): # http://www.mathopenref.com/coordpolygonarea2.html
	area = 0
	xl = 0
	zl = 0
	for index in xrange(0,len(points)-2):
		(x1,y1) = points[index]
		(x,y) = points[(index+1)%len(points)]
		area = area + (x1+x) * (y1+y)
	area = area /2
	return area
	
def getMinMax( points ):
	AHUGENUM = 99999
	ATINYNUM = -99999
	xmin = AHUGENUM
	ymin = AHUGENUM
	zmin = AHUGENUM
	xmax = ATINYNUM
	ymax = ATINYNUM
	zmax = ATINYNUM
	
	for (x,y,z) in points:
			if x < xmin: xmin = x
			if x > xmax: xmax = x
			if y < ymin: ymin = y
			if y > ymax: ymax = y
			if z < zmin: zmin = z
			if z > zmax: zmax = z

	return ((xmin,ymin,zmin),(xmax,ymax,zmax))
			
def drawShape(level, box, options, THESHAPE, TRANSFORM, origin):
	for (type, material, points) in THESHAPE:
		if type == "Line":
			p = transformPoint( points[0], (0,0,0), TRANSFORM )
			q = transformPoint( points[1], (0,0,0), TRANSFORM )
			drawLineWithOffset(level, material, origin, p, q )
		elif type == "Triangle":
			p = transformPoint( points[0], (0,0,0), TRANSFORM )
			q = transformPoint( points[1], (0,0,0), TRANSFORM )
			r = transformPoint( points[2], (0,0,0), TRANSFORM )
			drawTriangleWithOffset(level, box, options, origin, p, q, r, material, material)
		elif type == "Triangledge":
			p = transformPoint( points[0], (0,0,0), TRANSFORM )
			q = transformPoint( points[1], (0,0,0), TRANSFORM )
			r = transformPoint( points[2], (0,0,0), TRANSFORM )
			drawLineWithOffset(level, material, origin, p, q )
			drawLineWithOffset(level, material, origin, q, r )
			drawLineWithOffset(level, material, origin, r, p )
		elif type == "Linesegment":
			for index in xrange(0,len(points)-1):
				p = transformPoint( points[index], (0,0,0), TRANSFORM )			
				q = transformPoint( points[index+1], (0,0,0), TRANSFORM )
				drawLineWithOffset(level, material, origin, p, q )
		elif type == "3DFillRect": # Ignored in build.
			#print points
			(px, py, pz) = transformPoint( points[0], (0,0,0), TRANSFORM )
			(qx, qy, qz) = transformPoint( points[1], (0,0,0), TRANSFORM )
			(ox, oy, oz) = origin
			for iterX in xrange(int(px),int(qx)): # Speed up - us PYMCLEVEL methods to do a build fill.
				print iterX
				for iterY in xrange(int(py),int(qy)):
					for iterZ in xrange(int(pz),int(qz)):
						#print px, py, pz
						setBlock(level, material, int(ox+iterX), int(oy+iterY), int(oz+iterZ))
		else:
			print 'Unknown shape type: %s' % type

def drawLineWithOffset( level, material, (ox, oy, oz), (px, py, pz), (qx, qy, qz) ): # Shim for ease of use
	drawLine(level, material,(int(ox+px),int(oy+py),int(oz+pz)), (int(ox+qx),int(oy+qy),int(oz+qz)))

def drawTriangleWithOffset(level, box, options, (ox, oy, oz), (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
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
			drawLine(level, materialFill, (ox+px, oy+py, oz+pz), (ox+p1x, oy+p1y, oz+p1z) )
	
	
	drawLine(level, materialEdge, (ox+p1x, oy+p1y, oz+p1z), (ox+p2x, oy+p2y, oz+p2z) )
	drawLine(level, materialEdge, (ox+p1x, oy+p1y, oz+p1z), (ox+p3x, oy+p3y, oz+p3z) )
	drawLine(level, materialEdge, (ox+p2x, oy+p2y, oz+p2z), (ox+p3x, oy+p3y, oz+p3z) )

def transformPoints( points, o, TRANSFORM ):
	transformedPoints = []
	for point in points:
		transformedPoints.append(transformPoint(point,o,TRANSFORM) )
	return transformedPoints
	
def transformPoint( (px, py, pz), (ox, oy, oz), TRANSFORM ):
	# Given the point p in the frame of reference given by Origin o and axis vectors x, y, z, work out where it is in the world
	method = 'Transform Point'
	#print '%s: Started at %s' % (method, time.ctime())
	(xx, xy, xz) = TRANSFORM[0]
	(yx, yy, yz) = TRANSFORM[1]
	(zx, zy, zz) = TRANSFORM[2]
	# What are the distances along each vector for point P in that space defined by those vectors x, y, z?
	(vxx, vxy, vxz) = (px * xx, px * xy, px * xz)
	(vyx, vyy, vyz) = (py * yx, py * yy, py * yz)
	(vzx, vzy, vzz) = (pz * zx, pz * zy, pz * zz)
	# What is the resultant point in 'ordinary cartesian space'
	(rx, ry, rz) = (vxx + vyx + vzx, vxy + vyy + vzy, vxz + vyz + vzz)
	# Now take into account the origin, O, of the space
	(rx, ry, rz) = (rx + ox, ry + oy, rz +oz)

	#print '%s: Ended at %s' % (method, time.ctime())

	return (rx, ry, rz)
			
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

def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
	
############# GFX PRIMITIVES #############

def setBlockIfEmpty(level, (block, data), x, y, z):
	tempBlock = level.blockAt(x,y,z)
	if tempBlock == 0:
		setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

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

############# GFX  #############			
			
def distance( (x1,y1,z1), (x2,y2,z2) ):
	p = x1 * x2 + z1 * z2
	return sqrt( p + y1 * y2 )

def drawRectangle(level,box,options,p1,p2,p3,p4,material):
	drawTriangle(level, box, options, p1, p2, p3,material, material)
	drawTriangle(level, box, options, p1, p4, p3,material, material)
	
def drawTriangle(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
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
		
def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	#print 'ANALYSE %s %s %s' % (width, height, depth)

	minX = width
	minY = height
	minZ = depth
	maxX = 0
	maxY = 0
	maxZ = 0
	found = False
	
	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depth):
				if level.blockAt(iterX, iterY, iterZ) != 0:
					#print 'ANALYSING %s %s %s' % (iterX, iterY, iterZ)
					if iterX > maxX:
						maxX = iterX
					if iterY > maxY:
						maxY = iterY
					if iterZ > maxZ:
						maxZ = iterZ
				
					if iterX < minX:
						minX = iterX
					if iterY < minY:
						minY = iterY
					if iterZ < minZ:
						minZ = iterZ
						
					found = True

	#print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	#print '%s: Ended at %s' % (method, time.ctime())
	
	if found == False:
		return BoundingBox((0, 0, 0), (width, height, depth))	
	else:
		return BoundingBox((minX, 0, minZ), (maxX+1, maxY+1, maxZ+1))

def checkBoundingBoxIntersect(A, B):
	#print 'Checking BB A/B intersection '
	#printBoundingBox(A)
	#printBoundingBox(B)
	# Check for A completely to the left of B. https://github.com/mcedit/pymclevel/blob/master/box.py
	# http://www.toymaker.info/Games/html/3d_collisions.html
	if A.maxx < B.minx:
	    return False
	# Check for A to the right of B
	if A.minx > B.maxx:
	    return False
	# Check for A in front of B
	if A.maxz < B.minz:
	    return False
	# Check for A behind B
	if A.minz > B.maxz:
	    return False
	# Check for A above B
	if A.miny > B.maxy:
	    return False
	# Check for A below B
	if A.maxy < B.miny:
	   return False
	   
	# Collision has occurred
	#print 'Collision occurred'
	return True
	

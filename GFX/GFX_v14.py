# This filter is for drawing blocky thingies. See http://mathworld.wolfram.com/QuadraticSurface.html
# abrightmoore@yahoo.com.au
# http://brightmoore.net

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob

# For Reference (see @Texelelf and @CodeWarrior0 examples)
# 	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Mirror the blocks - in memory working read only copy
# 	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
#	setBlock(schematic, (BLOCKID, BLOCKDATA), (int)(centreWidth+xx), (int)(centreHeight+yy), (int)(centreDepth+zz))

# YOUR CODE GOES HERE \/ \/ \/ \/ \/ \/ \/ \/ \/

inputs = (
		("GFX", "label"),
		("Operation", (
			"City",
			"City Grid",
			"Circular City",
			"Angled Building",
			"Ruined Building",
			"Park",
			"Disc",
			"Death Star 2",
			"Death Star Bands",
			"Sculpt",
  		    "Toffee",
			"Fractree",
			"3DTree",
			"Forest",
			"Test Intersecting Spheres",
			"Solve Quadratic for Destruc7i0n",
  		    )),
		("Edge block:", alphaMaterials.BlockofQuartz),
		("Fill block:", alphaMaterials.Stone),
		("Light block:", alphaMaterials.GlassPane), # Randomly assigned
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	method = options["Operation"]
	if method == "Toffee":
		Toffee(level, box, options)
	elif method == "Death Star 2":
		DeathStar2(level, box, options)
	elif method == "Death Star Bands":
		DeathStarBands(level, box, options,(box.maxx-box.minx)/2)
	elif method == "Sculpt":
		Sculpt(level, box, options)
	elif method == "Test Intersecting Spheres":
		drawSphereIntersection(level,(box.minx, box.miny, box.minz), (box.maxx-box.minx)/3*4, (1,0), (box.maxx, box.maxy, box.maxz), (box.maxx-box.minx)/3*4)
	elif method == "Solve Quadratic for Destruc7i0n":
		print [[x, y] for x in xrange(-10,11) for y in xrange(-10, 11) if x + y == -10 and x <= y and x * y == 21]
	elif method == "Ruined Building":
		RuinedBuilding(level, box, options)
	elif method == "Angled Building":
		BuildingAngledShim(level, box, options)
	elif method == "City":
		City(level, box, options)
	elif method == "City Grid":
		CityGrid(level, box, options)
	elif method == "Circular City":
		CircularCity(level, box, options)
	elif method == "Fractree":
		Fractree(level, box, options)
	elif method == "Park":
		Park(level, box, options)
	elif method == "Disc":
		drawDisc(level, box, options)
	elif method == "3DTree":
		draw3DTree(level, box, options)
	elif method == "Forest":
		Forest(level, box, options)
		
	level.markDirtyBox(box)

def Forest(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Work out how 'big' to build. Loosely explained, this affects the number of floors in each module
	MINSIZE = 4 # Residential is if the maximum dimension of the selection box is less than 12 times this number (i.e. 48 when drafting this code)
	buildType = height
	if width > buildType:
		buildType = width
	if depth > buildType:
		buildType = depth
	if buildType > MINSIZE * 12:
		MINSIZE = MINSIZE * 2 # Commercial
	
	# Places random buildings radially within the selection box
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	O = (box.minx+centreWidth, box.miny, box.minz+centreDepth) # Origin

	# buildings = (width + height + depth) / 3
	buildings = height
	buildings = randint(buildings/2,buildings*MINSIZE)+1
	
	for iter in xrange(1,buildings):
		print 'Constructing forest %s of %s' % (iter,buildings)
		r = randint(0,centreWidth/8*7)
		theta = randint(0,360)*angleSize
		phi = 0 * angleSize #randint (0,360)*angleSize
		(x1,y1,z1) = getRelativePolar(O, (theta, phi, r))  # p2 is now the position of a new building!
		
		# Work out how big this building needs to be based on where it is in relation to the centre of the box (with occasional variation)
		
		w = width /MINSIZE
		if w < MINSIZE:
			w = MINSIZE +1
		w = randint(MINSIZE,w)
		w = w/2
		
		coef = (float)(r/(centreWidth/8.0*7.0)) # Scale the buildings further out downwards
		if randint(1,20) < 2:
			h = height
		else:
			h = (int)((float)(height * (float)(1.0-coef)))
		
		if h < MINSIZE:
			h = MINSIZE +1
		h = randint(MINSIZE,h)
		d = depth /MINSIZE
		if d < MINSIZE:
			d = MINSIZE +1		
		d = randint(MINSIZE,d)
		d = d/2
		if w < MINSIZE:
			w = MINSIZE
		if w > MINSIZE*2:
			if randint(1,10) < 2:
				w = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
			else:
				w = MINSIZE*2
		if h < MINSIZE:
			h = MINSIZE
		if d < MINSIZE:
			d = MINSIZE
		if d > MINSIZE*2:
			if randint(1,10) < 2:
				d = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
			else:
				d = MINSIZE*2
		
		print '%s %s %s, %s %s %s' % (x1, y1, z1, w, h, d)
		
		(tx1, ty1, tz1) = (x1-w, y1, z1-d)
		(tx2, ty2, tz2) = (abs(w*2), abs(h), abs(d*2))
		
		print '%s %s %s, %s %s %s' % (tx1, ty1, tz1, tx2, ty2, tz2)
		
		newBox = BoundingBox((tx1, ty1, tz1), (tx2, ty2, tz2))
#		(width1, height1, depth1) = getBoxSize(newBox)
#		print '%s %s %s' % (width1, height1, depth1)
		draw3DTree(level,newBox,options)
	
	print '%s: Ended at %s' % (method, time.ctime())


	
def draw3DTree(level, box, options):
	method = options["Operation"]
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
		print '%s %s %s %s %s' % (x0, theta, cos(theta), phi, depth)
		(x2, y2, z2) = getRelativePolar((x0,y0,z0), (theta, phi, depth))
		
		drawLine(level, material,
						(box.minx+x0,box.miny+y0,box.minz+z0), 
						(box.minx+x2,box.miny+y2,box.minz+z2))

		for iter in xrange(0,randint(3,11)):
			draw3DTreeBranch(level, box, options, depth/2, (x2, y2, z2), theta+randint(-ANGLERANGE,ANGLERANGE)*ANGLESTEP, phi+randint(-ANGLERANGE,ANGLERANGE)*ANGLESTEP,angle)	

def drawDisc(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Draws concentric circles out to the border in the nominated materials
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	ANGLESTEP = pi/180
	TwoPI = 2*pi

	SideLength = centreWidth


	Orientation = randint(0,45)
	
	offsetX = 0
	offsetZ = 0
	
	angle = TwoPI/360
	
	numSides = SideLength

	y = 0
	radius = (int)(SideLength)

	for y in xrange(0, height):
		for r in xrange(1,radius):
			MATERIAL = (fillMaterialBlock, fillMaterialData)
			x = r * cos(Orientation*angle)
			z = r * sin(Orientation*angle)
					
			for sides in xrange(0,numSides+3):
				x1 = r * cos((Orientation+360/numSides*sides)*angle)
				z1 = r * sin((Orientation+360/numSides*sides)*angle)
				drawLine(level, MATERIAL, (box.minx+centreWidth+x+offsetX,box.miny+y,box.minz+offsetZ+centreDepth+z), (box.minx+centreWidth+x1+offsetX,box.miny+y,box.minz+centreDepth+z1+offsetZ) )
				x = x1
				z = z1

	print '%s: Ended at %s' % (method, time.ctime())
	drawTorus(level, box, options, centreWidth/2, centreWidth-2, (edgeMaterialBlock, edgeMaterialData) )
	
def drawTorus(level, box, options, startR, endR, material):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Draws concentric circles out to the border in the nominated materials

	ANGLESTEP = pi/180
	TwoPI = 2*pi

	SideLength = centreWidth


	Orientation = randint(0,45)
	
	offsetX = 0
	offsetZ = 0
	
	angle = TwoPI/360
	
	numSides = SideLength

	y = 0
	radius = (int)(SideLength)

	for y in xrange(0, height):
		for r in xrange(startR,endR):
			MATERIAL = material
			x = r * cos(Orientation*angle)
			z = r * sin(Orientation*angle)
					
			for sides in xrange(0,numSides+3):
				x1 = r * cos((Orientation+360/numSides*sides)*angle)
				z1 = r * sin((Orientation+360/numSides*sides)*angle)
				drawLine(level, MATERIAL, (box.minx+centreWidth+x+offsetX,box.miny+y,box.minz+offsetZ+centreDepth+z), (box.minx+centreWidth+x1+offsetX,box.miny+y,box.minz+centreDepth+z1+offsetZ) )
				x = x1
				z = z1

	print '%s: Ended at %s' % (method, time.ctime())
	
def Fractree(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	drawTree(level, box, options, (fillMaterialBlock, fillMaterialData), centreWidth, 0, centreDepth, 90, height/5)
	
def drawTree(level, box, options, material, x1, y1, z1, angle, depth):
    if depth:
		x2 = x1 + int(math.cos(math.radians(angle)) * depth * 1.0)
		y2 = y1 + int(math.sin(math.radians(angle)) * depth * 1.0)
		z2 = z1
		
		drawLine(level, material,
						(box.minx+x1,box.miny+y1,box.minz+z1), 
						(box.minx++x2,box.miny+y2,box.minz+z2))

		drawTree(level, box, options, material, x2, y2, z2, angle - 20, depth - 1)
		drawTree(level, box, options, material, x2, y2, z2, angle + 20, depth - 1)	

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

def CircularCity(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	
	# Draw a circular city 
	# 1. Locate the centre of the selection box. This is the hub
	# 2. Draw a plot (park, complex, building, etc. there. Add the bounding box to a queue
	# 3. Around the park, draw a circular road
	# 4. At a random location on the road, draw a road of a random length going away from the hub to another hub that does not intersect with any known box. Make a bounding box there, add it to a queue.
	# 5. Repeat 4 until consecutive placement failures occur.
	
	
	
def CityGrid(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Work out how 'big' to build. Loosely explained, this affects the number of floors in each module
	MINSIZE = 4 # Residential is if the maximum dimension of the selection box is less than 12 times this number
	buildType = height
	if width > buildType:
		buildType = width
	if depth > buildType:
		buildType = depth
	if buildType > MINSIZE * 12:
		MINSIZE = MINSIZE * 2 # Commercial
	
	# Places random buildings in an 8x8 grid from the selection box with a quarter of the box gab between each row.
#	angleSize = pi/180
#	TwoPI = 2*pi
#	angleSize = pi/180
#	O = (box.minx+centreWidth, box.miny, box.minz+centreDepth) # Origin

	# buildings = (width + height + depth) / 3
#	buildings = height/MINSIZE
#	if width/MINSIZE < buildings:
#		buildings = width/MINSIZE
#	if depth/MINSIZE < buildings:
#		buildings = depth/MINSIZE
#	if buildings < 2:
#		buildings = 2
#	buildings = randint(buildings/2,buildings*MINSIZE)+1

	buildings = 8
	buildings2 = buildings * buildings
	gapX = width
	gapZ = depth
	
	counter = 1
	for iterX in xrange(0,buildings):
		for iterY in xrange(0,buildings):
			counter = counter + 1
			print 'Constructing buildings - step %s of %s %s' % (counter,buildings2,buildings)
#		r = randint(0,centreWidth/8*7)
#		theta = randint(0,360)*angleSize
#		phi = 0 * angleSize #randint (0,360)*angleSize
#		(x1,y1,z1) = getRelativePolar(O, (theta, phi, r))  # p2 is now the position of a new building!
		
		# Work out how big this building needs to be based on where it is in relation to the centre of the box (with occasional variation)
			w = width
			if w < MINSIZE:
				w = MINSIZE +1
			w = randint(MINSIZE,w)
			w = w/2
			
#		coef = (float)(r/(centreWidth/8.0*7.0)) # Scale the buildings further out downwards
#		if randint(1,20) < 2:
			h = height
#		else:
#			h = (int)((float)(height * (float)(1.0-coef)))
		
			if h < MINSIZE:
				h = MINSIZE +1
			h = randint(MINSIZE,h)
			d = depth
			if d < MINSIZE:
				d = MINSIZE +1		
			d = randint(MINSIZE,d)
			d = d/2
			if h < MINSIZE:
				h = MINSIZE
			if d < MINSIZE:
				d = MINSIZE
			if d > MINSIZE*2:
				if randint(1,10) < 2:
					d = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
				else:
					d = MINSIZE*2
			
			y1 = 0
			(tx1, ty1, tz1) = (iterX*(buildings+gapX), y1, iterY*(buildings+gapZ))			
			(tx2, ty2, tz2) = (width, h, depth)
		
			print '%s %s %s, %s %s %s' % (tx1, ty1, tz1, tx2, ty2, tz2)
		
			newBox = BoundingBox((box.minx+tx1, box.miny+ty1, box.minz+tz1), (tx2, ty2, tz2))
#		(width1, height1, depth1) = getBoxSize(newBox)
#		print '%s %s %s' % (width1, height1, depth1)
			RuinedBuilding(level,newBox,options)

	
	print '%s: Ended at %s' % (method, time.ctime())
	
def City(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Work out how 'big' to build. Loosely explained, this affects the number of floors in each module
	MINSIZE = 4 # Residential is if the maximum dimension of the selection box is less than 12 times this number (i.e. 48 when drafting this code)
	buildType = height
	if width > buildType:
		buildType = width
	if depth > buildType:
		buildType = depth
	if buildType > MINSIZE * 12:
		MINSIZE = MINSIZE * 2 # Commercial
	
	# Places random buildings radially within the selection box
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	O = (box.minx+centreWidth, box.miny, box.minz+centreDepth) # Origin

	# buildings = (width + height + depth) / 3
	buildings = height/MINSIZE
	if width/MINSIZE < buildings:
		buildings = width/MINSIZE
	if depth/MINSIZE < buildings:
		buildings = depth/MINSIZE
	if buildings < 2:
		buildings = 2
	buildings = randint(buildings/2,buildings*MINSIZE)+1
	
	for iter in xrange(1,buildings):
		print 'Constructing building %s of %s' % (iter,buildings)
		r = randint(0,centreWidth/8*7)
		theta = randint(0,360)*angleSize
		phi = 0 * angleSize #randint (0,360)*angleSize
		(x1,y1,z1) = getRelativePolar(O, (theta, phi, r))  # p2 is now the position of a new building!
		
		# Work out how big this building needs to be based on where it is in relation to the centre of the box (with occasional variation)
		
		w = width /MINSIZE
		if w < MINSIZE:
			w = MINSIZE +1
		w = randint(MINSIZE,w)
		w = w/2
		
		coef = (float)(r/(centreWidth/8.0*7.0)) # Scale the buildings further out downwards
		if randint(1,20) < 2:
			h = height
		else:
			h = (int)((float)(height * (float)(1.0-coef)))
		
		if h < MINSIZE:
			h = MINSIZE +1
		h = randint(MINSIZE,h)
		d = depth /MINSIZE
		if d < MINSIZE:
			d = MINSIZE +1		
		d = randint(MINSIZE,d)
		d = d/2
		if w < MINSIZE:
			w = MINSIZE
		if w > MINSIZE*2:
			if randint(1,10) < 2:
				w = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
			else:
				w = MINSIZE*2
		if h < MINSIZE:
			h = MINSIZE
		if d < MINSIZE:
			d = MINSIZE
		if d > MINSIZE*2:
			if randint(1,10) < 2:
				d = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
			else:
				d = MINSIZE*2
		
		print '%s %s %s, %s %s %s' % (x1, y1, z1, w, h, d)
		
		(tx1, ty1, tz1) = (x1-w, y1, z1-d)
		(tx2, ty2, tz2) = (abs(w*2), abs(h), abs(d*2))
		
		print '%s %s %s, %s %s %s' % (tx1, ty1, tz1, tx2, ty2, tz2)
		
		newBox = BoundingBox((tx1, ty1, tz1), (tx2, ty2, tz2))
#		(width1, height1, depth1) = getBoxSize(newBox)
#		print '%s %s %s' % (width1, height1, depth1)
		if MINSIZE > 4 and randint(0,100) < 10:
			BuildingAngledShim(level,newBox,options)
		else:
			RuinedBuilding(level,newBox,options)

	
	print '%s: Ended at %s' % (method, time.ctime())

def BuildingAngledShim(level, box, options): # After the ENT filter
	BuildingAngled(level, box, options, randint(0,45), randint(3,11))
	
def BuildingAngled(level, box, options, Orientation, numSides): # After the ENT filter
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	if randint(1,100) < 30:
		t1 = (fillMaterialBlock, fillMaterialData)
		(fillMaterialBlock, fillMaterialData) = (edgeMaterialBlock, edgeMaterialData)
		(edgeMaterialBlock, edgeMaterialData) = t1
	
	ANGLESTEP = pi/180
	TwoPI = 2*pi
	
	SideLength = centreWidth
	RINGS = randint(1,SideLength/4+1)

	if Orientation == -1: # Randomise
		Orientation = randint(0,45)
	
	offsetX = 0
	offsetZ = 0
	
	angle = TwoPI/360
	
	if numSides < 3:
		numSides = 3+randint(0,15)
	
	banding = False
	bandType = 1
	bandingSize1 = 0
	bandingSize2 = 0
	if randint(1,20) < 10:
		banding = True
		bandingSize1 = randint(2,8)
		bandingSize2 = randint(1,bandingSize1)
	if randint(1,20) < 5:
		bandType = 2
	
	for y in xrange(0, height):
		print '%s: %s of %s' % (method, y, height)
		radius = (int)(SideLength)
		
		for r in xrange(1,radius):
			MATERIAL = (fillMaterialBlock, fillMaterialData)
			ringR = (int)(SideLength/RINGS)
			if ringR == 0:
				ringR == 2
			if r == radius-1:
				MATERIAL = (lightMaterialBlock, lightMaterialData)
				if banding == True:
					t = y%(bandingSize1+bandingSize2)
					if t < bandingSize1:
						MATERIAL = (edgeMaterialBlock, edgeMaterialData)
						
			elif r%ringR == 0: # Interior walls
				MATERIAL = (edgeMaterialBlock, edgeMaterialData)
			if (MATERIAL == (fillMaterialBlock, fillMaterialData) and y%4 == 0) or (MATERIAL == (lightMaterialBlock, lightMaterialData)) or (MATERIAL == (edgeMaterialBlock, edgeMaterialData)):
				x = r * cos(Orientation*angle)
				z = r * sin(Orientation*angle)
				
				for sides in xrange(0,numSides+1):
					x1 = r * cos((Orientation+360/numSides*sides)*angle)
					z1 = r * sin((Orientation+360/numSides*sides)*angle)
					drawLine(level, MATERIAL, (box.minx+centreWidth+x+offsetX,box.miny+y,box.minz+offsetZ+centreDepth+z), (box.minx+centreWidth+x1+offsetX,box.miny+y,box.minz+centreDepth+z1+offsetZ) )
					x = x1
					z = z1
		
		if SideLength < 1:
			break
	
	print '%s: Ended at %s' % (method, time.ctime())
	
def RuinedBuilding(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	W = Factorise(width-1)
	H = Factorise(height-1)
	D = Factorise(depth-1)
	
	w = W.pop(randint(0,len(W)-1))
	h = H.pop(randint(0,len(H)-1))
	d = D.pop(randint(0,len(D)-1))

	drawGlass = False
	if randint(1,20) > 1:
		drawGlass = True
	
	banding = False
	bandType = 1
	bandingSize1 = 0
	bandingSize2 = 0
	if randint(1,20) < 10:
		banding = True
		bandingSize1 = randint(2,8)
		bandingSize2 = randint(1,bandingSize1)
	if randint(1,20) < 5:
		bandType = 2
	
	#Floors
	print '%s: Floors' % (method)
	for iterY in xrange(0,height-1):
		if iterY == 0 or (iterY % 4 == 0 and randint(1,10) > 1):
			for iterX in xrange(1,width-1):
				for iterZ in xrange(1,depth-1):
					setBlock(level, (fillMaterialBlock, fillMaterialData), box.minx+iterX, box.miny+iterY, box.minz+iterZ)
	
	roomSize = randint(6,12)		
	#Uprights
	print '%s: Uprights' % (method)
	for iterX in xrange(0,width):
		for iterZ in xrange(0,depth):
			if drawGlass == True and (iterX == 0 or iterX == width-1 or iterZ == 0 or iterZ == depth-1): # Walls
				if banding == False:
					drawLine(level, (lightMaterialBlock, lightMaterialData),
							(box.minx+iterX,box.miny,box.minz+iterZ), 
							(box.minx+iterX,box.miny+height-1,box.minz+iterZ))
				else:
					iterY = 0
					while iterY < height:
						if bandType == 1:
							drawLine(level, (edgeMaterialBlock, edgeMaterialData),
								(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
								(box.minx+iterX,box.miny+iterY+bandingSize1,box.minz+iterZ))
						else:
							if iterY < height-1:
								if iterY+bandingSize1 >= height-1:
									drawLine(level, (fillMaterialBlock, fillMaterialData),
										(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
										(box.minx+iterX,box.miny+height-1,box.minz+iterZ))
								else:
									drawLine(level, (fillMaterialBlock, fillMaterialData),
										(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
										(box.minx+iterX,box.miny+iterY+bandingSize1,box.minz+iterZ))
										
						iterY = iterY + bandingSize1
						
						if iterY < height-1:
							if iterY+bandingSize2 >= height-1:
								drawLine(level, (lightMaterialBlock, lightMaterialData),
									(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
									(box.minx+iterX,box.miny+height-1,box.minz+iterZ))
							else:
								drawLine(level, (lightMaterialBlock, lightMaterialData),
									(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
									(box.minx+iterX,box.miny+iterY+bandingSize2,box.minz+iterZ))
						iterY = iterY + bandingSize2

			if (iterZ % d == 0 and iterX % w == 0) or (iterZ % roomSize == 0 and iterX % roomSize == 0):
				drawLine(level, (edgeMaterialBlock, edgeMaterialData),
							(box.minx+iterX,box.miny,box.minz+iterZ), 
							(box.minx+iterX,box.miny+height-1,box.minz+iterZ))
	
	#Bounding
	print '%s: Bounding' % (method)
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+0,box.minz+0), 
			(box.minx+width-1,box.miny+0,box.minz+0))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+0,box.minz+depth-1), 
			(box.minx+width-1,box.miny+0,box.minz+depth-1))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+0,box.minz+0), 
			(box.minx+0,box.miny+0,box.minz+depth-1))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+width-1,box.miny+0,box.minz+0), 
			(box.minx+width-1,box.miny+0,box.minz+depth-1))

	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+height-1,box.minz+0), 
			(box.minx+width-1,box.miny+height-1,box.minz+0))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+height-1,box.minz+depth-1), 
			(box.minx+width-1,box.miny+height-1,box.minz+depth-1))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+height-1,box.minz+0), 
			(box.minx+0,box.miny+height-1,box.minz+depth-1))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+width-1,box.miny+height-1,box.minz+0), 
			(box.minx+width-1,box.miny+height-1,box.minz+depth-1))

	# Damage
#	print '%s: Damage' % (method)
#	purgeDepth = centreHeight
#
#	for iterX in xrange(0,width):
#		purgeDepth = purgeDepth + randint(-h,h)
#		if purgeDepth < 0:
#			purgeDepth = 0
#		if purgeDepth > height-1:
#			purgeDepth = height-1
#		for iterY in xrange(0,purgeDepth):
#			drawLine(level, AIR,
#				(box.minx+iterX,box.maxy-1,box.minz), 
#				(box.minx+iterX,box.maxy-1-iterY,box.minz+depth-1))
#
#	purgeDepth = centreHeight
#	
#	for iterZ in xrange(0,depth):
#		purgeDepth = purgeDepth + randint(-h,h)
#		if purgeDepth < 0:
#			purgeDepth = 0
#		if purgeDepth > height-1:
#			purgeDepth = height-1
#		for iterY in xrange(0,purgeDepth):
#			drawLine(level, AIR,
#				(box.minx,box.maxy-1,box.minz+iterZ), 
#				(box.minx+width-1,box.maxy-1-iterY,box.minz+iterZ))

							
	
	print '%s: Ended at %s' % (method, time.ctime())

def Toffee(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	for i in xrange(0, randint(1,16)):
		drawRandomTriangle(level, box, options, (edgeMaterialBlock, i%16), (fillMaterialBlock, i%16))
	print '%s: Ended at %s' % (method, time.ctime())
		
def DeathStar2(level, box, options):
	# draw a spherical object reminiscent of a certain non-moon
	# for each 'layer' draw a random line from the edge of the sphere at this point to random depth
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
		
	r = centreWidth
	r=r-2
	rr = r*r
	
	tr = r/16
	while tr < r:
		DeathStarBands(level, box, options, tr)
		if r/16 > 2:
			tr = tr + randint(2,r/16)
		else:
			tr = tr + 2

	
	print '%s: Internal pipes %s' % (method, time.ctime())
	for iterY in xrange(0,height):
		print '%s: Layer %s of %s' % (method, iterY, height-1)
		dy = centreHeight - iterY
		dydy = dy * dy
		for iterX in xrange(0, width):
			dx = centreWidth - iterX
			dxdx = dx * dx
			for iterZ in xrange(0, depth):
				dz = centreDepth - iterZ
				dzdz = dz * dz
				posn = abs(dxdx + dydy + dzdz - rr)
				if posn >= 0 and posn < 121: # this block is on the sphere surface
					if dz > 0 and (iterY%5 == 0 or iterZ%5 == 0):
						randomDepth = randint(0,2*dz) # percent depth to render with 
						drawLine(level, (fillMaterialBlock, fillMaterialData), (box.minx+iterX, box.miny+iterY, box.minz+iterZ),
											      (box.minx+iterX, box.miny+iterY, box.minz+iterZ+randomDepth) )
					chanceOfSurface = (float)((1.0-(float)((float)(1.3*iterZ)/(float)(depth)))*100.0)
					# print '%s: Chance %s' % (method, chanceOfSurface)
					if chanceOfSurface > (float)(randint(1,80)):
						if 2 > (float)(randint(1,100)):
							setBlock(level, (lightMaterialBlock, lightMaterialData), box.minx+iterX, box.miny+iterY, box.minz+iterZ)
						else:
							setBlock(level, (edgeMaterialBlock, edgeMaterialData), box.minx+iterX, box.miny+iterY, box.minz+iterZ)

	r = r + 2
	# Bands
	print '%s: Bands %s' % (method, time.ctime())
	DeathStarBands(level, box, options, r)
	
	# Back
	print '%s: Open back %s' % (method, time.ctime())
	#DeathStarRemoveBackChunks(level, box, options, r, (int)(r/2))
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/4))
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/8))
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/10))
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/16))

	# Open Panelling
	print '%s: Open panelling %s' % (method, time.ctime())
	DeathStarPanels(level, box, options, r, AIR)

	# Random walk
	print '%s: Channels %s' % (method, time.ctime())
	for s in xrange(5, randint(1,r)):
		theta = randint(0,360)*angleSize
		phi = randint (0,360)*angleSize
		for t in xrange(10, r):
			u = randint(5,10)*angleSize
			phiU = phi+u
			phiT = phi
			while phiT < phiU:
				p2 = getRelativePolar(p1, (theta, phiT, r))
				p3 = getRelativePolar(p1, (theta, phiT+angleSize, r))
				drawLine(level, AIR, p3, p2)
				p2 = getRelativePolar(p1, (theta, phiT, r-1))
				p3 = getRelativePolar(p1, (theta, phiT+angleSize, r-1))
				drawLine(level, AIR, p3, p2)
				p2 = getRelativePolar(p1, (theta, phiT, r-2))
				p3 = getRelativePolar(p1, (theta, phiT+angleSize, r-2))
				drawLine(level, AIR, p3, p2)
				phiT = phiT+angleSize
			phi = phi+randint(-1,1)*angleSize
			theta = theta+randint(-1,1)*angleSize

	r=r-3

	# LASER
	print '%s: LASER %s' % (method, time.ctime())
	theta = -pi/2
	phi = pi/6

	size = r/2
	radius = r+(size*3/4)
	(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
	drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (0,0))
	drawSphereIntersection(level, ((int)(x), (int)(y), (int)(z)), (int)(size+2), (fillMaterialBlock, fillMaterialData), (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth), (int)(r+1))

	# Interior chambers
	drawSphere(level, ((int)(box.minx+centreWidth), (int)(box.miny+centreHeight), (int)(box.minz+centreDepth)), (int)(r/8), (edgeMaterialBlock, edgeMaterialData))
	drawSphere(level, ((int)(box.minx+centreWidth), (int)(box.miny+centreHeight), (int)(box.minz+centreDepth)), (int)(r/8-2), (0,0))

#	size = r/2
#	radius = r+(size*3/4)
#	t = randint(5,10)
#	for numholes in xrange(0, t):
#		theta = angleSize * randint(0,180)
#		phi = angleSize * randint(-90,90)
#		(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
#		drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (0,0))
		
#	theta = 0
#	phi = 0
#	(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
#	drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (2,0))

#	theta = 90 * angleSize
#	phi = 0
#	(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
#	drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (3,0))

#	theta = 0
#	phi = 90 * angleSize
#	(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
#	drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (4,0))


	
	print '%s: Ended at %s' % (method, time.ctime())

def DeathStarPanels(level, box, options, r, material):
	# draw a spherical object reminiscent of a certain non-moon
	# for each 'layer' draw a random line from the edge of the sphere at this point to random depth
	method = options["Operation"]
	print '%s DeathStarPanels: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)

	# Bands
	t = randint(r,2*r)
	for i in xrange(0,t):
		print '%s: Vertical band %s of %s' % (method, i, t)
		vertAngle1 = angleSize * randint(-90,83)
		vertAngle2 = vertAngle1 + angleSize * randint(3,7)
		horizAngle = angleSize * randint(0,180)
		if vertAngle1 > vertAngle2:
			temp = vertAngle1
			vertAngle1 = vertAngle2
			vertAngle2 = temp
		vertAngle = vertAngle1
		while vertAngle <= vertAngle2:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			vertAngle = vertAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 5 > (float)(randint(1,100)):
				drawLine(level, material, p3, p2)
			else:
				drawLine(level, material, p3, p2)

	t = randint(r,4*r)
	for i in xrange(0,t):
		print '%s: Horizontal band %s of %s' % (method, i, t)
		horizAngle1 = angleSize * randint(0,173)
		horizAngle2 = horizAngle1 + angleSize * randint(3,7)
		vertAngle = angleSize * randint(-90,90)
		if horizAngle1 > horizAngle2:
			temp = horizAngle1
			horizAngle1 = horizAngle2
			horizAngle2 = temp
		horizAngle = horizAngle1
		while horizAngle <= horizAngle2:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 66 > (float)(randint(1,100)):
				drawLine(level, material, p3, p2)
			else:
				drawLine(level, material, p3, p2)

	print '%s: Ended at %s' % (method, time.ctime())
			
	
def DeathStarRemoveBackChunks(level, box, options, r, CHUNKSIZE):
	# draw a spherical object reminiscent of a certain non-moon
	# remove cubic chunks from the back to a certain depth
	method = options["Operation"]
	print '%s DeathStarRemoveBackChunks: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
	
	if CHUNKSIZE < 4:
		CHUNKSIZE = 4
	band = (int)(r/16)
		
	iterY = 0
	while iterY < height:
		print '%s: Removing back chunks %s of %s' % (method, iterY, height)
		iterX = 0

		while iterX < width:
			t = randint(0, (int)(r/CHUNKSIZE))
			print '%s: Removing back chunks - row %s of %s' % (method, iterX, width)
			iterZ = 0
			while iterZ < t:
				print '%s: Removing back chunks - column %s of %s' % (method, iterZ, t)
				for x in xrange(0,CHUNKSIZE):
					for y in xrange(0,CHUNKSIZE):
						for z in range(0,CHUNKSIZE):
							if (iterY+y) < (centreHeight-band) or (iterY+y) > (centreHeight+band): # Preserve most of the equator
								setBlock(level, (0,0), box.minx+iterX+x, box.miny+iterY+y, box.maxz-iterZ*CHUNKSIZE-z)
							elif randint(0,10) < 3: # but destroy bits of the equator too
								setBlock(level, (0,0), box.minx+iterX+x, box.miny+iterY+y, box.maxz-iterZ*CHUNKSIZE-z)
								#drawLine(level, (0,0), (box.minx+iterX, box.miny+iterY, box.maxz-1), (box.minx+iterX, box.miny+iterY, box.maxz-1-t))
					iterZ = iterZ + 1
				iterX = iterX + CHUNKSIZE
		iterY = iterY + CHUNKSIZE

				
def DeathStarRemoveBackOneLine(level, box, options, r):
	# draw a spherical object reminiscent of a certain non-moon
	# for each 'layer' draw a random line from the edge of the sphere at this point to random depth
	method = options["Operation"]
	print '%s DeathStarRemoveBackOneLine: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)

	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			t = randint(0, r)
			drawLine(level, (0,0), (box.minx+iterX, box.miny+iterY, box.maxz-1), (box.minx+iterX, box.miny+iterY, box.maxz-1-t))
	
	
def DeathStarBands(level, box, options, r):
	# draw a spherical object reminiscent of a certain non-moon
	# for each 'layer' draw a random line from the edge of the sphere at this point to random depth
	method = options["Operation"]
	print '%s DeathStarBands: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)


	# Bands
	t = randint(r,2*r)
	for i in xrange(0,t):
		print '%s: Vertical band %s of %s' % (method, i, t)
		vertAngle1 = angleSize * randint(0,360)
		vertAngle2 = vertAngle1 + angleSize * randint(16,360)
		horizAngle = angleSize * randint(0,360)
		if vertAngle1 > vertAngle2:
			temp = vertAngle1
			vertAngle1 = vertAngle2
			vertAngle2 = temp
		vertAngle = vertAngle1
		while vertAngle <= vertAngle2:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			vertAngle = vertAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 5 > (float)(randint(1,100)):
				drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			else:
				drawLine(level, (fillMaterialBlock, fillMaterialData), p3, p2)

	t = randint(r,4*r)
	for i in xrange(0,t):
		print '%s: Horizontal band %s of %s' % (method, i, t)
		horizAngle1 = angleSize * randint(0,360)
		horizAngle2 = horizAngle1 + angleSize * randint(45,360)
		vertAngle = angleSize * randint(0,360)
		if horizAngle1 > horizAngle2:
			temp = horizAngle1
			horizAngle1 = horizAngle2
			horizAngle2 = temp
		horizAngle = horizAngle1
		while horizAngle <= horizAngle2:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 10 > (float)(randint(1,100)):
				drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			else:
				drawLine(level, (edgeMaterialBlock, edgeMaterialData), p3, p2)

		
	vertAngle = 0
	vertAngles = [angleSize,-angleSize,2*angleSize,-3*angleSize] #,3*angleSize,-3*angleSize]
	for vertAngle in vertAngles:
		horizAngle = 0
		while horizAngle < TwoPI:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 5 > (float)(randint(1,100)):
				drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			else:
				drawLine(level, (edgeMaterialBlock, edgeMaterialData), p3, p2)

	vertAngle = 0
	vertAngles = [0,-angleSize*2] # Central bands
	for vertAngle in vertAngles:
		horizAngle = 0
		while horizAngle < TwoPI:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			p2a = getRelativePolar(p1, ( horizAngle, vertAngle, r-1))
			p2b = getRelativePolar(p1, ( horizAngle, vertAngle, r-2))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			p3a = getRelativePolar(p1, ( horizAngle, vertAngle, r-1))
			p3b = getRelativePolar(p1, ( horizAngle, vertAngle, r-2))
			#if 66 > (float)(randint(1,100)):
			#	drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			#else:
			#	drawLine(level, (edgeMaterialBlock, edgeMaterialData), p3, p2)
			drawLine(level, (0,0), p3, p2)
			drawLine(level, (0,0), p3a, p2a)
			drawLine(level, (0,0), p3b, p2b)

	print '%s: Ended at %s' % (method, time.ctime())

def Sculpt(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
#TBD
	print '%s: Ended at %s' % (method, time.ctime())
				
# END YOUR CODE BIT /\ /\ /\ /\ /\ /\ /\ /\ /\ /\

# Support libraries


# GFX Tests

def drawRandomTriangle(level, box, options, edgeMaterial, fillMaterial):
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	
	drawTriangle(level, box, options, 
					(box.minx+(int)(randint(0,width-1)), box.miny+(int)(randint(0,height-1)), box.minz+(int)(randint(0,depth-1))),
					(box.minx+(int)(randint(0,width-1)), box.miny+(int)(randint(0,height-1)), box.minz+(int)(randint(0,depth-1))),
					(box.minx+(int)(randint(0,width-1)), box.miny+(int)(randint(0,height-1)), box.minz+(int)(randint(0,depth-1))),
					edgeMaterial,
					fillMaterial
				)
	
# GFX primitives

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

def drawPoint(level, (block, data), x, y, z):
	setBlock(level, (block, data), x, y, z)
	
# Ye Olde GFX Libraries
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

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

def drawPolygon(level, box, options, sides, radius, Orientation, (offsetX, offsetY, offsetZ), material):
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	ANGLESTEP = pi/180
	TwoPI = 2*pi
	angle = TwoPI/360
	r = radius
	
	x = r * cos(Orientation*angle)
	z = r * sin(Orientation*angle)
				
	for sides in xrange(0,numSides+1):
		x1 = r * cos((Orientation+360/numSides*sides)*angle)
		z1 = r * sin((Orientation+360/numSides*sides)*angle)
		drawLine(level, material, (x+offsetX,offsetY,offsetZ+z), (x1+offsetX,offsetY,z1+offsetZ) )
		x = x1
		z = z1
			
def Cube(level, block, (x1,y1,z1),(x2,y2,z2)):
	# Draws a wireframe cube
	method = "CUBE"
	print '%s: Started at %s' % (method, time.ctime())

	# Render all the vertices
	
	drawLine(level, block, (x1, y1, z1), (x2, y1, z1) )
	drawLine(level, block, (x1, y1, z1), (x1, y2, z1) )
	drawLine(level, block, (x1, y1, z1), (x1, y1, z2) )
	drawLine(level, block, (x2, y2, z1), (x2, y2, z2) )
	drawLine(level, block, (x2, y2, z1), (x1, y2, z1) )
	drawLine(level, block, (x2, y2, z1), (x2, y1, z1) )
	drawLine(level, block, (x1, y2, z2), (x1, y2, z1) )
	drawLine(level, block, (x1, y2, z2), (x1, y1, z2) )
	drawLine(level, block, (x1, y2, z2), (x2, y2, z2) )
	drawLine(level, block, (x2, y1, z2), (x1, y1, z2) )
	drawLine(level, block, (x2, y1, z2), (x2, y2, z2) )
	drawLine(level, block, (x2, y1, z2), (x2, y1, z1) )
	
	print '%s: Ended at %s' % (method, time.ctime())	

def drawSphere(level,(x,y,z), r, material):
	RSQUARED = r*r
	for iterX in xrange(-r,r):
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			for iterY in xrange(-r,r):
				if XSQUARED + ZSQUARED + iterY*iterY <= RSQUARED:
					setBlock(level, material, XOFFSET, y+iterY, ZOFFSET)

def drawSphereIntersection(level,(x,y,z), r, material, (x2,y2,z2), r2):
	RSQUARED = r*r
	R2SQUARED = r2*r2
	for iterX in xrange(-r,r): # for each point in the sphere
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		X2OFFSET = XOFFSET-x2
		X2SQUARED = X2OFFSET * X2OFFSET
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			Z2OFFSET = ZOFFSET-z2
			Z2SQUARED = Z2OFFSET * Z2OFFSET
			for iterY in xrange(-r,r):
				YSQUARED = iterY * iterY
				YOFFSET = y+iterY
				Y2OFFSET = YOFFSET-y2
				Y2SQUARED = Y2OFFSET * Y2OFFSET
				if abs(XSQUARED + ZSQUARED + YSQUARED - RSQUARED) < 100: # point is on the sphere surface to be drawn
					if X2SQUARED + Z2SQUARED + Y2SQUARED <= R2SQUARED: # point is within the intersecting sphere
						setBlock(level, material, XOFFSET, YOFFSET, ZOFFSET)
#				if XSQUARED + ZSQUARED + YSQUARED < RSQUARED: # point is on the sphere surface to be drawn
#					if X2SQUARED + Z2SQUARED + Y2SQUARED <= R2SQUARED: # point is within the intersecting sphere
#						setBlock(level, (0,0), XOFFSET, YOFFSET, ZOFFSET)

						
def drawSphereSprinkles(level, (x,y,z), r, materialBase, materialOption, chance):
	RSQUARED = r*r
	for iterX in xrange(-r,r):
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			for iterY in xrange(-r,r):
				if XSQUARED + ZSQUARED + iterY*iterY <= RSQUARED:
					if randint(0,100) < chance:
						setBlock(level, materialBase, XOFFSET, y+iterY, ZOFFSET)
					else:
						setBlock(level, materialOption, XOFFSET, y+iterY, ZOFFSET)

def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
						
# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt(x,y,z)
    if tempBlock == 0:
	setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
    	level.setBlockDataAt(x, y, z, data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, y):
    	setBlockIfEmpty(level, (block, data), x, iterY, z)

def findSurface(x, y, z, level, box, options):
	# Find a candidate surface
	iterY = 250
	miny = y
	foundy = y
	while iterY > miny:
		block = level.blockAt(x,iterY,z)
		if block != 0: # not AIR
			foundy = iterY
			iterY = miny # end search, block found was a legitimate candidate for the surface				
		iterY = iterY -1
	return foundy

# Boxes
		
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
				
def	copyBlocksFromDBG(level,schematic, A, cursorPosn):
	(x1,y1,z1,x2,y2,z2) = (A.minx,A.miny,A.minz,A.maxx,A.maxy,A.maxz)
	(width, height, depth) = getBoxSize(schematic.bounds)

	if x2 > width or y2 > height or z2 > depth:
		return False
	else:
		level.copyBlocksFrom(schematic, A, cursorPosn)
	return True

def printBoundingBox(A):
	print 'BoundingBox %s %s %s %s %s %s' % (A.minx,A.miny,A.minz,A.maxx,A.maxy,A.maxz)
	
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
	
def makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS):
	if COORDS == True:
		cX = cX - spawnerX
		cY = cY - spawnerY
		cZ = cZ - spawnerZ 
		theCommand = "/"+PREFIX+" ~"+str(cX)+" ~"+str(cY)+" ~"+str(cZ)+" "+str(SUFFIX)
	else:
		theCommand = "/"+PREFIX+" "+str(cX)+" "+str(cY)+" "+str(cZ)+" "+str(SUFFIX)

	chunk.TileEntities.append( 	createCommandBlockData(spawnerX, 
									spawnerY, 
									spawnerZ, 
									theCommand
								))
								
def createCommandBlockData(x, y, z, theCommand):
	e = TileEntity.Create("Control")
	e["Command"] = TAG_String(theCommand)
	TileEntity.setpos(e, (x, y, z))
	return e
	
def makePNGTicles(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "PNGTicles"
	print '%s: Started at %s' % (method, time.ctime())
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16
	PACKEDCHUNKSIZE = options["Generator Width"]
	if PACKEDCHUNKSIZE == 0:
		PACKEDCHUNKSIZE = CHUNKSIZE
	LAYERGAP = options["Layer Separation"]+1
	ORIENTATION = options["Orientation"]
	COORDS = options["Relative coordinates?"]	
	TRANSPARENCY_T = options["Transparency Threshold"]
	baseX = options["Generator X"]
	baseY = options["Generator Y"]
	baseZ = options["Generator Z"]
	Dx = options["Draw X"]
	Dy = options["Draw Y"]
	Dz = options["Draw Z"]
	OFFSET = options["Offset"]+1
	PREFIX = options["Prefix"]
	SUFFIX = options["Suffix"]
	SCALE = options["Scale"]
	METHOD = options["Method"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2


	packedSpawnerCount = 0
	CHUNKSIZE = 16
	PACKEDCHUNKSIZE = options["Generator Width"]
	if PACKEDCHUNKSIZE == 0:
		PACKEDCHUNKSIZE = CHUNKSIZE
	LAYERGAP = options["Layer Separation"]+1
	
	if METHOD == "Draw Line": # Create command blocks that creat particles alone a 3D line
		print '%s: Processing a Line' % (method)
		x = options["Line Start X"]
		y = options["Line Start Y"]
		z = options["Line Start Z"]
		x1 = options["Line End X"]
		y1 = options["Line End Y"]
		z1 = options["Line End Z"]
		dx = x1 - x
		dy = y1 - y
		dz = z1 - z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)

		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
			spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
			spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
			setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
			setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
			chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
						
			cX = (x+iter*cos(theta)*cos(phi))
			cY = (y+iter*sin(phi))
			cZ = (z+iter*sin(theta)*cos(phi))
		
			makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS)
			iter = iter+SCALE
			packedSpawnerCount = packedSpawnerCount+1
			chunk.dirty = True

	if METHOD == "Render PNG": # Draw picture
		print '%s: Processing a picture' % (method)
		filename = options["Path and Filename"]
		filename = filename.strip()
		if filename == "":
			filename = askOpenFile("Select an image...", False)
		f = open(filename, "rb")
		data = f.read()
		f.close()

		reader = png.Reader(bytes=data) # @Sethbling
		(width, height, pixels, metadata) = reader.asRGBA8() # @Sethbling
		pixels = list(pixels) # @Sethbling
		
		for iterY in xrange(0, height):
			print '%s: Processing row %s of %s' % (method, iterY, height)
			for iterX in xrange(0, width):
					colour = getPixel(pixels, iterX, iterY) # after @Sethbling	
					if opaque(colour, TRANSPARENCY_T): # @Sethbling
						(theBlock, theBlockData) = closestMaterial(colour) # @Sethbling
						(r,g,b,a) = colour
		
						spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
						spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
						spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
						setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
						chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
						cX = Dx+iterX*SCALE
						cY = Dy+(height-1-iterY)*SCALE # Fix inverted image
						cZ = Dz+0
						if ORIENTATION == "Z-Y":
							cX = Dx+0
							cY = Dy+(height-1-iterY)*SCALE # Fix inverted image
							cZ = Dz+iterX*SCALE
						elif ORIENTATION == "X-Z":
							cX = Dx+iterX*SCALE
							cY = Dy+0
							cZ = Dz+(height-1-iterY)*SCALE
						
						makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS)
						packedSpawnerCount = packedSpawnerCount+1
						chunk.dirty = True

	if METHOD == "Block Model": # Create command blocks that creat particles alone a 3D line
		MATERIALID = options["Material"].ID
		print '%s: Examining the selection box for material %s' % (method, MATERIALID)
	
		# Scan through the selection box and make a command block particle for each block of the right type
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				for iterX in xrange(0, width):
					tempBlock = level.blockAt(box.minx + iterX, box.miny + iterY, box.minz + iterZ)
					if tempBlock == MATERIALID: # We are in business! Man the hatches! Batten the mainsail! Create a particle command block
						# Manage the stack of spawners
						spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
						spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
						spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
						setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
						setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
						chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)

						cX = (Dx+iterX*SCALE)
						cY = (Dy+iterY*SCALE)
						cZ = (Dz+iterZ*SCALE)						

						makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS)
						packedSpawnerCount = packedSpawnerCount+1
						chunk.dirty = True
						
	print '%s: Ended at %s' % (method, time.ctime())

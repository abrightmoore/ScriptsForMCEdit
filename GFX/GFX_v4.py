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
  		    "Death Star 2",
			"Death Star Bands",
			"Sculpt",
  		    "Toffee",
			"Test Intersecting Spheres",
  		    )),
		("Edge block:", alphaMaterials.BlockofIron),
		("Fill block:", alphaMaterials.Stone),
		("Light block:", alphaMaterials.Stone),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

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
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/2))
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
	vertAngles = [0,-angleSize*2]
	for vertAngle in vertAngles:
		horizAngle = 0
		while horizAngle < TwoPI:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 66 > (float)(randint(1,100)):
				drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			else:
				drawLine(level, (edgeMaterialBlock, edgeMaterialData), p3, p2)

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
	level.markDirtyBox(box)

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
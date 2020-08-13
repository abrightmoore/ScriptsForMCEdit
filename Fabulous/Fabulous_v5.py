# This filter replaces all non-air blocks within the selection with a rainbow sequence of wool
# This is a ridiculous filter. Enjoy!
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)
# v4 has a material type selector

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

inputs = (
		("FABULOUS", "label"),
		("Method", ("Horizontal","Vertical","Spherical","Diagonal","Sinusoidal","Chequers","Box")),
		("Material", alphaMaterials.WhiteWool),	
		("Wool colours:", ("string","value=14 1 4 5 11 3 10 3 11 5 4 1")),
		("Ignore block IDs:", ("string","value=0 6 7 8 9 10 11 12 13 27 28 30 31 32 37 38 39 40 50 51 52 55 59 63 64 65 66 68 69 70 71 72 78 83 93 94 96 104 105 106 115 116 118 119 127 131 132 140 141 142 143 145 147 148 149 150 151 154 157") ),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt((int)(x),(int)(y),(int)(z))
    if tempBlock == 0:
	setBlock(level, (block, data), (int)(x),(int)(y),(int)(z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, (int)(y)):
    	setBlockIfEmpty(level, (block, data), (int)(x),(int)(iterY),(int)(z))
    	

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def fix(angle):
	while angle > pi:
		angle = angle - 2 * pi
	while angle < -pi:
		angle = angle + 2 * pi
	return angle

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


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Fabulous(level, box, options)		
	level.markDirtyBox(box)

def Fabulous(levelOrig, box, options): 
	
	method = "Fabulous"
	print '%s: Started at %s' % (method, time.ctime())	
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	orientation = options["Method"]
	ignore = options["Ignore block IDs:"].split()
	ignoreList = map(int, ignore)
	colours = options["Wool colours:"].split()
	coloursList = map(int, colours)
	MATERIALID = options["Material"].ID # Choose wool, stained glass, clay, etc.

	level = levelOrig.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth)))
	
	
	if orientation == "Horizontal": # Horizontal
		colourCounter = 0
		for iterY in xrange(0, height):
			print '%s: step %s of %s' % (method, iterY+1, height)
			for iterX in xrange(0, width):
				for iterZ in xrange(0, depth):
					tempBlock = level.blockAt(iterX, iterY, iterZ)
					if tempBlock != 0 and not (tempBlock in ignoreList):
						setBlock(level, (MATERIALID, coloursList[colourCounter]), iterX,  iterY, iterZ)
			colourCounter = colourCounter + 1
			if colourCounter >= len(colours):
				colourCounter = 0
	elif orientation == "Vertical":
		colourCounter = 0
		for iterX in xrange(0, width):
			print '%s: step %s of %s' % (method, iterX+1, width)
			for iterY in xrange(0, height):
				for iterZ in xrange(0, depth):
					tempBlock = level.blockAt(iterX, iterY, iterZ)
					if tempBlock != 0 and not (tempBlock in ignoreList):
						setBlock(level, (MATERIALID, coloursList[colourCounter]), iterX, iterY, iterZ)
			colourCounter = colourCounter + 1
			if colourCounter >= len(colours):
				colourCounter = 0
	elif orientation == "Spherical":
		for iterX in xrange(0, width):
			print '%s: step %s of %s' % (method, iterX+1, width)
			for iterY in xrange(0, height):
				for iterZ in xrange(0, depth):
					tempBlock = level.blockAt(iterX, iterY, iterZ)
					if tempBlock != 0 and not (tempBlock in ignoreList):
						dx = centreWidth - iterX
						dy = centreHeight - iterY
						dz = centreDepth - iterZ
						r = (int)(sqrt(dx * dx + dz * dz + dy * dy))
						setBlock(level, (MATERIALID, coloursList[r%len(colours)]), iterX, iterY, iterZ)
	elif orientation == "Diagonal":
		for iterX in xrange(0, width):
			print '%s: step %s of %s' % (method, iterX+1, width)
			for iterY in xrange(0, height):
				for iterZ in xrange(0, depth):
					tempBlock = level.blockAt(iterX, iterY, iterZ)
					if tempBlock != 0 and not (tempBlock in ignoreList):
						dx = centreWidth - iterX
						dy = centreHeight - iterY
						dz = centreDepth - iterZ
						r = (int)(dx+dy-dz)
						setBlock(level, (MATERIALID, coloursList[r%len(colours)]), iterX, iterY, iterZ)
	elif orientation == "Sinusoidal":
		for iterX in xrange(0, width):
			print '%s: step %s of %s' % (method, iterX+1, width)
			for iterY in xrange(0, height):
				for iterZ in xrange(0, depth):
					tempBlock = level.blockAt(iterX, iterY, iterZ)
					if tempBlock != 0 and not (tempBlock in ignoreList):
						dx = centreWidth - iterX
						dy = centreHeight - iterY
						dz = centreDepth - iterZ
						r = (int)(len(colours)*atan2(dx,dy)*atan2(dy,dz))
						setBlock(level, (MATERIALID, coloursList[r%len(colours)]), iterX, iterY, iterZ)

	elif orientation == "Chequers":
		for iterX in xrange(0, width):
			print '%s: step %s of %s' % (method, iterX+1, width)
			for iterY in xrange(0, height):
				for iterZ in xrange(0, depth):
					tempBlock = level.blockAt(iterX, iterY, iterZ)
					if tempBlock != 0 and not (tempBlock in ignoreList):
						dx = abs((centreWidth - iterX) % len(colours))
						dy = abs((centreHeight - iterY) % len(colours))
						dz = abs((centreDepth - iterZ) % len(colours))
						r = dx
						if dz > dx:
							r = dz
						elif dy > dx:
							r = dy
						setBlock(level, (MATERIALID, coloursList[r%len(colours)]), iterX, iterY, iterZ)
							
	elif orientation == "Box":
		for iterX in xrange(0, width):
			print '%s: step %s of %s' % (method, iterX+1, width)
			for iterY in xrange(0, height):
				for iterZ in xrange(0, depth):
					#tempBlock = level.blockAt(box.minx + iterX, box.miny + iterY, box.minz + iterZ)
					#if tempBlock != 0 and not (tempBlock in ignoreList):
					dx = abs((centreWidth - iterX) % len(colours))
					dy = abs((centreHeight - iterY) % len(colours))
					dz = abs((centreDepth - iterZ) % len(colours))
					if dx == 0 or dy == 0 or dz == 0:
						r = 0
						setBlock(level, (MATERIALID, coloursList[r%len(colours)]), iterX, iterY, iterZ)
	
	b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	levelOrig.copyBlocksFrom(level, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ),b)
						
	print '%s: Ended at %s' % (method, time.ctime())

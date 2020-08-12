import time # for timing
from math import *
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import *
from os.path import isfile, join
import glob
from mcplatform import *

inputs = (
	  ("SPRINKLE", "label"),
	  ("Divide into how many squares you want?", 30),
	  ("Minimal distance between squares:", 4),
	  ("CRATERS", "label"),
	  ("Use down surface?", False),
	  ("Radius begin:", 10),
	  ("Radius end:", 30),
	  ("Material for Craters:", alphaMaterials.BlockofIron),
)


def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)

def perform(level, box, options):		
	Sprinkle(level, box, options)
	level.markDirtyBox(box)

def Sprinkle(level, box, options):

	method = "Sprinkle"
	TimeStart = time.ctime()
	print '%s: Started at %s' % (method, TimeStart)

	zonesNum = options["Divide into how many squares you want?"]
	(width, height, depth) = getBoxSize(box)
	miniBoxWidth = width/zonesNum
	miniBoxDepth = depth/zonesNum
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	MINDISTANCE = options["Minimal distance between squares:"]
	SetBlocksCoordinate = []

	for zoneXNum in range(0, zonesNum):
		for zoneZNum in range(0, zonesNum):
			xStart = zoneXNum * miniBoxWidth
			zStart = zoneZNum * miniBoxDepth
			(randX, randZ) = (randint(MINDISTANCE, miniBoxWidth - MINDISTANCE - 1), randint(MINDISTANCE, miniBoxDepth - MINDISTANCE - 1))
			temp = [box.minx + xStart + randX, box.miny, box.minz + zStart + randZ]
			SetBlocksCoordinate.append(temp)			

	TimeEnd = time.ctime()						
	print '%s: Ended at %s' % (method, TimeEnd)

	Drape(level, height,SetBlocksCoordinate, options)

def Drape(level, height, SetBlocksCoordinate, options):

	method = "DRAPE"
	AIR = (0,0)

	TimeStart = time.ctime()
	print '%s: Start at %s' % (method, TimeStart)

	for i in range(0,len(SetBlocksCoordinate)):
		iterX = SetBlocksCoordinate[i][0]
		iterY = SetBlocksCoordinate[i][1]
		iterZ = SetBlocksCoordinate[i][2]
		tempBlock = (level.blockAt(iterX,iterY,iterZ), level.blockDataAt(iterX,iterY,iterZ))
		for j in xrange(iterY-1,-1,-1):
			if tempBlock != AIR: # found a block. Must be the top!
				break
			else:
				iterY-=1
				tempBlock = (level.blockAt(iterX,iterY,iterZ), level.blockDataAt(iterX,iterY,iterZ))
		SetBlocksCoordinate[i][1] = iterY

	TimeEnd = time.ctime()
	print '%s: Complete at %s' % (method, TimeEnd)
	blockCraterSwapper(level, SetBlocksCoordinate, options)


def blockCraterSwapper(level, SetBlocksCoordinate, options):
	method = "blockCraterSwapper"
	TimeStart = time.ctime()
	print '%s: Start at %s' %(method, TimeStart)

	for i in xrange(0,len(SetBlocksCoordinate)):
		X = SetBlocksCoordinate[i][0]
		Y = SetBlocksCoordinate[i][1]
		Z = SetBlocksCoordinate[i][2]
		thatsCrarer(level, X, Y, Z,(randint(options["Radius begin:"],options["Radius end:"])), options)
		print 'Crater %s with %s ' %(i+1,len(SetBlocksCoordinate))
	
	TimeEnd = time.ctime()
	print '%s: Complete at %s' % (method, TimeEnd)

def thatsCrarer(level, ox, oy, oz, radius, options):

	UseSurface = options["Use down surface?"]
	material = (options["Material for Craters:"].ID, options["Material for Craters:"].blockData)
	radiusAir = 5*radius/6

	drawSphere(level, (ox, oy-radius/2, oz), radius, material, False)
	drawSphere(level, (ox, oy+radiusAir/5, oz), radiusAir, (0, 0), UseSurface)

def drawSphere(level,(x,y,z), r, material, UseSurface):
	RSQUARED = r*r

	if UseSurface:
		for iterY in xrange(-r,r):
			if iterY<(-2*r/5-1):
				continue

			YSQUARED = iterY*iterY
			YOFFSET = y+iterY

			for iterZ in xrange(-r,r):
				ZSQUARED = iterZ*iterZ
				ZOFFSET = z+iterZ

				for iterX in xrange(-r,r):
					if YSQUARED + ZSQUARED + iterX*iterX <= RSQUARED:
						setBlock(level, material, x+iterX, YOFFSET, ZOFFSET)

	else:
		for iterY in xrange(-r,r):
			YSQUARED = iterY*iterY
			YOFFSET = y+iterY

			for iterZ in xrange(-r,r):
				ZSQUARED = iterZ*iterZ
				ZOFFSET = z+iterZ

				for iterX in xrange(-r,r):
					if YSQUARED + ZSQUARED + iterX*iterX <= RSQUARED:
						setBlock(level, material, x+iterX, YOFFSET, ZOFFSET)
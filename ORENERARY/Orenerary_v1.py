# This filter is for creating ArmorStand entities above each command block found in the selection region, per @CocoaMix86
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_
import time # for timing

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from numpy import *
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import *
from random import Random # @Codewarrior0

# GLOBAL
CHUNKSIZE = 16
STONE = (1,0)


inputs = (
		("Orenerary", "label"),

		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	orenerary(level, box, options)

	FuncEnd(level,box,options,method) # Log end	

def orenerary(level, box, options):
	ORETABLE2 = [
				("copper",1470,0,0.0114398813560256,1,255,3), # 0.0114398813560256
				("granite",1903,0,0.00755583489081116,1,255,3),
				("salt ore ",2498,0,0.00231829884829339,1,255,3),
				("aluminum ore",2726,5,0.000923460302233396,1,255,3),
				("limestone",1942,0,0.0110815236268007,1,255,3),
				("certus quartz",1360,0,0.00335477966512849,1,255,3),
				("amber",1498,7,0.000622991129267903,1,255,3),
				("earth infused stone",1498,4,0.00071120226261557,1,255,3),
				("osmium ore",2911,0,0.00315354801717912,1,255,3),
				("marble",1953,0,0.0122365381540718,1,255,3),
				("andesite",1859,0,0.00659378221773816,1,255,3),
				("diorite",1875,0,0.0102545442516664,1,255,3),
				("salt block",2923,0,0.000493431027163516,1,255,3),
				("dark ore",2279,0,0.00092621690015051,1,255,3),
				("tritanium",3378,0,0.00241753637330952,1,255,3),
				("air infused stone",1498,1,0.000206744843783596,1,255,3),
				("chance cube",1844,0,0.0000799413395963238,1,255,1),
				("water infused stone",1498,3,0.000275659791711461,1,255,3),
				("charged certus quartz",1361,0,0.000766334220957863,1,255,3),
				("order infused stone",1498,5,0.000154369483358418,1,255,3),
				("fire infused stone",1498,2,0.000170909070861106,1,255,3),
				("entropy infused stone",1498,6,0.000126803504187272,1,255,3),
				("cinnabar",1498,0,0.000931730095984739,1,255,3),
				("ruby",3188,0,0.000421759481318536,1,255,3),
				("minicio",3262,0,0.00289718441088746,1,255,3),
				("zinc",3186,0,0.00147753648357343,1,255,3),
				("amethyst",3190,0,0.000380410512561817,1,255,3),
				("sapphire",3189,0,0.000350087935473556,1,255,3),
				("apatite",2833,0,0.000777360612626321,1,255,3),
				("copper oreberry bush",2724,0,0.000148856287524189,1,255,1),
				("amethyst",219,0,0.000457595254241026,1,32,3),
				("yellorite",1482,0,0.000614721335516559,1,32,3),
				("limonite",226,0,0.00459249212991295,1,32,3),
				("dilithium",3377,0,0.00123495586686735,1,32,3),
				("aluminum oreberry",2725,0,0.0000992375250161261,1,32,1),
				("runium",647,0,0.00194064493364869,1,32,3),
				("teslatite",3183,0,0.00119085030019351,1,32,3),
				("Draconium",2086,0,0.0000192961854198023,1,16,1),
				("jade",224,0,0.0000771847416792092,1,16,1),
				("rosite",227,0,0.000104750720850355,1,16,1),
				("sapphire",228,0,0.0000634017520936361,1,16,1),
				("tungsten",3187,0,0.0000248093812540315,1,16,1),
				]
	method = "Orenerary"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	#freqQuantum = 0.000001
	# Move through each chunk in the map and, based on the probability established for ores appearing, attempt to spawn them in.
	for p in box.chunkPositions:
		print "Processing Chunk "+str(p)
		(cx,cz) = p		
		for (name,blockID,blockData,frequency,minY,maxY,radius) in ORETABLE2:
			f = frequency*1000000
			# print (name,blockID,blockData,frequency,minY,maxY,radius)
			if float(randint(0,999999)) <= f: # this ore may be in this chunk
				r = radius
				if r > 1:
					r = randint(1,radius)
				(px,pz) = (cx*CHUNKSIZE+randint(0,15),cz*CHUNKSIZE+randint(0,15))
				py = randint(minY,maxY)
				makeBlob(level,px,py,pz,(blockID,blockData),r,STONE)
	
	FuncEnd(level,box,options,method) # Log end	

def makeBlob(level, x, y, z, ore, radius, replaceMaterial):
	# Make an irregular blob of ore centred at the position
	if radius == 1:
		if getBlock(level,x,y,z) == replaceMaterial:
			setBlock(level, ore, x,y,z)
	else:
		if randint(1,100) < 10: # Spherish
			r2 = radius*radius
			for dy in xrange(-radius,+radius):
				for dz in xrange(-radius,+radius):
					for dx in xrange(-radius,+radius):
						dist = dy**2+dz**2+dx**2
						if dist < r2 or (dist == r2 and randint(1,100) <= 40):
							if getBlock(level,dx+x,dy+y,dz+z) == replaceMaterial:
								setBlock(level, ore, dx+x,dy+y,dz+z)
		else: # brownian squiggle
			radius = radius**2 # Steps
			keepGoing = True
			P = []
			P.append((x,y,z))
			while keepGoing:
				(px,py,pz) = P[randint(0,len(P)-1)]
				dx = randint(-1,1)
				dy = randint(-1,1)
				dz = randint(-1,1)
				P.append((px+dx,py+dy,pz+dz))
				radius = radius-1
				if radius < 1:
					keepGoing = False
			for (px,py,pz) in P:
				if getBlock(level,px,py,pz) == replaceMaterial:
					setBlock(level, ore, px,py,pz)
			

	
	
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

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
# Ye Olde GFX Libraries
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

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

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			rx = 0
			createArmorStand(level, (int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), "ls", 1, 0, 1, 1, 1, 0, 0, 0, rx, 0,0,0,1,"","","","","","stone",2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
			iter = iter+0.5 # slightly oversample because I lack faith.

# @abrightmoore
# Rebuilding Exeter - 1700s living in a prosperous English town
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
from random import * # @Codewarrior0

inputs = (
			("EXETER", "label"),
			("Operation", (
				"Showcase",
				"Random",
				"City",
				"Inferred"
				)
			),

			("Point 1 X:", 0),
			("Point 1 Z:", 0),
			("Point 2 X:", 1),
			("Point 2 Z:", 1),
			("Y:", 0),
			("City block size:",64),
			("Asset path:", ("string","value=")),
			("abrightmoore@yahoo.com.au", "label"),
			("http://brightmoore.net", "label")
)

def perform(level, box, options):
	
	# Given two points and a selection of house assets, spray them along the length of the line, with the direction of 'skew' determined by the slope of the line.
	
	(X1,Z1) = (options["Point 1 X:"],options["Point 1 Z:"])
	(X2,Z2) = (options["Point 2 X:"],options["Point 2 Z:"])
	Y = options["Y:"]
	ASSETPATH = options["Asset path:"]
	

	rise = (Z2-Z1)
	run = (X2-X1)
	length = sqrt(rise**2+run**2)
	
	assets = readAssets(ASSETPATH)
	if options["Operation"] == "Showcase":
		placeAllAssets(level, assets, X1, Y, Z1, rise, run, length)
	elif options["Operation"] == "Random":
		placeRandomAssets(level, assets, X1, Y, Z1, rise, run, length)
	elif options["Operation"] == "City": # Create a grid laid out city in the selection box
		BLOCKSIZE = options["City block size:"]
		ROADWIDTH = 2
		ROWS = int(floor((box.maxz-box.minz)/BLOCKSIZE))
		COLS = int(floor((box.maxx-box.minx)/BLOCKSIZE))
		# grid = zeros((ROWS,COLS))
		
		for x in xrange(0,ROWS-1):
			for z in xrange(0,COLS-1):
				print x,z
				px1 = x*BLOCKSIZE+ROADWIDTH+randint(-1,1)+box.minx
				pz1 = z*BLOCKSIZE+ROADWIDTH+randint(-1,1)+box.minz
				px2 = (x+1)*BLOCKSIZE-ROADWIDTH+randint(-1,1)+box.minx
				pz2 = z*BLOCKSIZE+ROADWIDTH+randint(-1,1)+box.minz
				px3 = (x+1)*BLOCKSIZE-ROADWIDTH+randint(-1,1)+box.minx
				pz3 = (z+1)*BLOCKSIZE-ROADWIDTH+randint(-1,1)+box.minz
				px4 = x*BLOCKSIZE+ROADWIDTH+randint(-1,1)+box.minx
				pz4 = (z+1)*BLOCKSIZE-ROADWIDTH+randint(-1,1)+box.minz
				
				rise = (pz2-pz1)
				run = (px2-px1)
				length = sqrt(rise**2+run**2)				
				placeRandomAssets(level, assets, px1, Y, pz1, rise, run, length)
				rise = (pz3-pz2)
				run = (px3-px2)
				length = sqrt(rise**2+run**2)				
				placeRandomAssets(level, assets, px2, Y, pz2, rise, run, length)
				rise = (pz4-pz3)
				run = (px4-px3)
				length = sqrt(rise**2+run**2)				
				placeRandomAssets(level, assets, px3, Y, pz3, rise, run, length)
				rise = (pz1-pz4)
				run = (px1-px4)
				length = sqrt(rise**2+run**2)				
				placeRandomAssets(level, assets, px4, Y, pz4, rise, run, length)
	elif options["Operation"] == "Inferred": # Draw the block based on order of block IDs found in the selection
		P = inferPathFromBlocks(level,box)
		for i in xrange(0,len(P)):
			print i,len(P)
			(X1,Y1,Z1) = P[i]
			(X2,Y2,Z2) = P[(i+1)%(len(P))]
			rise = (Z2-Z1)
			run = (X2-X1)
			length = sqrt(rise**2+run**2)

			placeRandomAssets(level, assets, X1, Y, Z1, rise, run, length)
	
	
	# Read in all the assets and cache them
	

def placeAllAssets(level, assets, startx, starty, startz, rise, run, maxdist):
	dist = 0
	angle = atan2(rise,run)
	count = 0
	for asset in assets:
		count = count+1
		print "Rendering asset "+str(count)

		(w,h,d) = (asset.Width,asset.Height,asset.Length)
		
		# Place the asset against the line traced by the start pos and rise / run
		for x in xrange(0,w<<1):
			for z in xrange(0,d<<1):
				for y in xrange(0,h):
					px = startx + (dist+x*0.5)*cos(angle)+z*0.5*cos(angle+pi/2)
					py = starty + y
					pz = startz + (dist+x*0.5)*sin(angle)+z*0.5*sin(angle+pi/2)
					material = getBlock(asset,x>>1,y,z>>1)
					setBlock(level,material,px,py,pz)
					
		dist = dist + w + 1
		if dist > maxdist:
			break

def placeRandomAssets(level, assets, startx, starty, startz, rise, run, maxdist):
	dist = 0
	angle = atan2(rise,run)
	count = 0
	
	asset = assets[randint(0, len(assets)-1)]
	while dist < maxdist:
		if random() > 0.5: # Choose another
			asset = assets[randint(0, len(assets)-1)]
		count = count+1
		print "Rendering asset "+str(count)

		(w,h,d) = (asset.Width,asset.Height,asset.Length)
		# Place the asset against the line traced by the start pos and rise / run
		
		orientation = randint(0,1)

		if orientation == 0:
			if dist+w < maxdist:
				for x in xrange(0,w<<1):
					for z in xrange(0,d<<1):
						for y in xrange(0,h):
							px = startx + (dist+x*0.5)*cos(angle)+z*0.5*cos(angle+pi/2)
							py = starty + y
							pz = startz + (dist+x*0.5)*sin(angle)+z*0.5*sin(angle+pi/2)
							material = getBlock(asset,x>>1,y,z>>1)
							setBlock(level,material,px,py,pz)
							
			dist = dist + w-randint(0,3)
		else:
			if dist+d < maxdist:

				for x in xrange(0,w<<1):
					for z in xrange(0,d<<1):
						for y in xrange(0,h):
							px = startx + (dist+z*0.5)*cos(angle)+x*0.5*cos(angle+pi/2)
							py = starty + y
							pz = startz + (dist+z*0.5)*sin(angle)+x*0.5*sin(angle+pi/2)
							material = getBlock(asset,x>>1,y,z>>1)
							setBlock(level,material,px,py,pz)
						
			dist = dist + d-randint(0,3)
		
		if dist >= maxdist:
			break
			
def readAssets(path):
	print 'Scanning available schematics...'
	SchematicFileNames = glob.glob(path+"/*.schematic")
	for fileName in SchematicFileNames:
		print fileName
	print 'Found %s schematic files' % (len(SchematicFileNames))
	# End cached file names
	CACHE = []
	for fn in SchematicFileNames:
		print 'Loading schematic from file - %s' % (fn)
		sourceSchematic = MCSchematic(filename=fn)
		# (x,y,z) = sourceSchematic.size
		CACHE.append(sourceSchematic)	
	return CACHE
	
################## PRIMITIVES ########################

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

def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

def setBlock(level, (block, data), x, y, z):
	if getBlock(level, x,y,z) == (0,0): # AIR
		level.setBlockAt(int(x), int(y), int(z), block)
		level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockForced(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

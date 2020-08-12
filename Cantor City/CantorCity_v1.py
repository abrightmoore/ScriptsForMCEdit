# @TheWorldFoundry
# Based on http://procworld.blogspot.com/search/label/City

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
#from numpy import *
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials

inputs = (
		("CANTOR CITY", "label"),
		("Material:", alphaMaterials.Stone),
		("Floor Height:", 3),
		("Min Dimension:", 4),
		("Ratio:", 3.0),
		("Chance:", 0.9),
		("Seed:", 0),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
		)
		
def perform(level, box, options):
	(RAND,SEED) = getRandFromSeed(options)
	cantorCity(level, box, options, RAND,0)
	level.markDirtyBox(box)
	
def cantorCity(level, box, options, RAND, iter):
	print iter,box
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height= box.maxy-box.miny
	# Draw the current layer

	if height > 0:
		material = getBlockFromOptions(options, "Material:")
		
		floorHeight = options["Floor Height:"]
		if floorHeight < 1:
			floorHeight = RAND.randint(1,16)
			if iter > floorHeight and RAND.random() > 0.1:
				floorHeight = iter-floorHeight
		for y in xrange(box.miny,box.miny+floorHeight):
			for z in xrange(box.minz, box.maxz):
				for x in xrange(box.minx, box.maxx):
					setBlock(level,material,x,y,z) # Draw draw draw!
		
		# Now spawn the NEXT layer up in each corner
		if True:
			if height > 1:
				RATIO = options["Ratio:"]
				if RATIO < 1.0:
					RATIO = 1.0+random() # Random splits!
				widthThird = int(width/RATIO)
				depthThird = int(depth/RATIO)
				MINDIM = options["Min Dimension:"]
				if widthThird >= MINDIM and depthThird >= MINDIM: # We stop when either dimension trends to 0
					CHANCE = options["Chance:"]
					y = y+1
					if y < box.maxy:
						# Conditionally create a new box and build the next layer
						NewBox1 = BoundingBox((box.minx,y,box.minz),(widthThird,box.maxy-y,depthThird))
						NewBox2 = BoundingBox((box.maxx-widthThird,y,box.minz),(widthThird,box.maxy-y,depthThird))
						NewBox3 = BoundingBox((box.maxx-widthThird,y,box.maxz-depthThird),(widthThird,box.maxy-y,depthThird))
						NewBox4 = BoundingBox((box.minx,y,box.maxz-depthThird),(widthThird,box.maxy-y,depthThird))
						if RAND.random() < CHANCE: cantorCity(level,NewBox1,options, RAND,iter+1)
						if RAND.random() < CHANCE: cantorCity(level,NewBox2,options, RAND,iter+1)
						if RAND.random() < CHANCE: cantorCity(level,NewBox3,options, RAND,iter+1)
						if RAND.random() < CHANCE: cantorCity(level,NewBox4,options, RAND,iter+1)
	
	

AIR = (0,0)
	
def setBlock(level, (block, data), x, y, z):
	if getBlock(level, x,y,z) == AIR:
		level.setBlockAt(int(x), int(y), int(z), block)
		level.setBlockDataAt(int(x), int(y), int(z), data)		

def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))
		
def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def getRandFromSeed(options):
	PARAM = int(options["Seed:"])
	if PARAM == 0:
		PARAM = randint(0,99999999999)
	print 'Seed: '+str(PARAM)
	return (Random(PARAM),PARAM)
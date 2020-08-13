# This filter is for playing around with height maps.
# abrightmoore@yahoo.com.au
# http://brightmoore.net

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0
import inspect # @Texelelf
from PIL import Image
import png

# GLOBAL
CHUNKSIZE = 16

inputs = (
		("HEIGHTMAP", "label"),
		("Operation", (
			"Save","Load"
  		    )),
		("Ignore block IDs:", ("string","value=0 6 7 8 9 10 11 12 13 27 28 30 31 32 37 38 39 40 50 51 52 55 59 63 64 65 66 68 69 70 71 72 78 83 93 94 96 104 105 106 115 116 118 119 127 131 132 140 141 142 143 145 147 148 149 150 151 154 157") ),
		("File name:", ("string","value=Heightmap.png")),
		("Material", alphaMaterials.Stone),
		("Max height:", 255),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = options["Operation"]
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = True
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation

	if method == "Save":
		HMSave(originalLevel, originalBox, options) 
		SUCCESS = False # Suppress additional copyback
	if method == "Load":
		HMLoad(level, box, options) 
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False # Suppress additional copyback

		# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end

def HMLoad(level,box,options):
	method = "HMLoad"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)

	material = (options["Material"].ID, options["Material"].blockData)
	
	maxHeight = options["Max height:"]
	quantumHeight = maxHeight / height
	img = Image.open(options["File name:"])
	w = img.size[0]
	d = img.size[1]
	pixels = img.load()
	wStep = float(float(w)/width)
	dStep = float(float(d)/depth)
	print wStep
	print dStep
	for iterX in xrange(0,width):
		print '%s of %s' % (iterX, width)
		for iterZ in xrange(0,depth):
			x1 = float(iterX*wStep)
			z1 = float(iterZ*dStep)
			(r,g,b) = pixels[int(x1), int(z1)]
			if maxHeight > 255:
				h = (b+0xff*g+0xffff*r)/quantumHeight
			else:
				h = float(r/quantumHeight)
			# print h
			for iterY in xrange(0, int(h)):
				setBlock(level, material,box.minx+int(iterX),box.miny+int(iterY),box.minz+int(iterZ))
	FuncEnd(level,box,options,method) # Log end		
	
def HMSave(level,box,options):
	method = "HMSave"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)
	
	ignore = options["Ignore block IDs:"].split()
	ignoreList = map(int, ignore)
	
	maxHeight = options["Max height:"]
	quantumHeight = maxHeight / height
	print 'Preparing image, step size is %s' % (quantumHeight)
	img = Image.new('RGB', (width, depth))
	
	pixels = img.load()
	print img.size
	for iterZ in xrange(0,depth):

		print '%s of %s' % (iterZ, depth)
		for iterX in xrange(0,width):
			iterY = height-1
			h = 0 # assert height is 0, try to prove otherwise
			while iterY > 0:
				# Walk to find the top of the terrain
				theBlock = level.blockAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				#if theBlock != 0:
				if not (theBlock in ignoreList): # current block is not air or ignored
					h = iterY*quantumHeight
					iterY = 0 # break the loop
				iterY -= 1
			if maxHeight > 255:
				pixels[iterX,iterZ] = (int(h/65535),int(h/256)%65535,h%256)
			else:
				pixels[iterX,iterZ] = (int(h),int(h),int(h))
	img.save(options["File name:"])
	
	FuncEnd(level,box,options,method) # Log end			

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

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
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
			"Save","Load","ExportPNG XY","ExportPNG ZY","ExportPNG XZ","Projection"
  		    )),
		("Ignore block IDs:", ("string","value=0 6 7 8 9 10 11 12 13 27 28 30 31 32 37 38 39 40 50 51 52 55 59 63 64 65 66 68 69 70 71 72 78 83 93 94 96 104 105 106 115 116 118 119 127 131 132 140 141 142 143 145 147 148 149 150 151 154 157") ),
		("File name:", ("string","value=HM")),
		("adrian@theworldfoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

blockColMap = [
			((35,0), (244,244,244,255), "White"), # White
			((35,1), (217,128,69,255), "Orange"),
			((35,2), (176,69,186,255), "Magenta"),
			((35,3), (101,132,198,255), "Light Blue"),
			((35,4), (205,192,48,255), "Yellow"),
			((35,5), (71,191,62,255), "Lime"),
			((35,6), (215,156,171,255), "Pink"), # Pink
			((35,7), (72,72,72,255), "Grey"), # Grey
			((35,8), (170,176,176,255), "Light Grey"), # Light Grey
			((35,9), (53,126,156,255), "Cyan"), # Cyan
			((35,10), (122,57,176,255), "Purple"), # Purple
			((35,11), (53,63,162,255), "Blue"), # Blue
			((35,12), (91,57,36,255), "Brown"), # Brown
			((35,13), (57,77,30,255), "Green"), # Green
			((35,14), (172,61,55,255), "Red"), # Red
			((35,15), (36,22,32,255), "Black"), # Black
		]


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
		LayerSave(level,box,options)
		SUCCESS = False # Suppress additional copyback
	if method == "Load":
		LayerLoad(originalLevel,originalBox,options) 
		#originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
		#originalLevel.markDirtyBox(originalBox)
		SUCCESS = False # Suppress additional copyback
	if method == "ExportPNG XY": # https://www.youtube.com/watch?v=qpk5aIbXIBI @theCommonPeople
		ExportPNGXY(originalLevel,originalBox,options)
		SUCCESS == False
	if method == "ExportPNG ZY": # https://www.youtube.com/watch?v=qpk5aIbXIBI @theCommonPeople
		ExportPNGZY(originalLevel,originalBox,options)
		SUCCESS == False
	if method == "ExportPNG XZ": # https://www.youtube.com/watch?v=qpk5aIbXIBI @theCommonPeople
		ExportPNGXZ(originalLevel,originalBox,options)
		SUCCESS == False
	if method == "Projection":
		Projection(level,box,options)
		SUCCESS == False
		
		# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end

def Projection(level,box,options):
	method = "Projection"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)

	img = Image.new('RGBA', (width, depth))
	pixels = img.load()
	w = img.size[0]
	d = img.size[1]
	

	for x in xrange(0,img.size[0]):
		
		for z in xrange(0,img.size[1]):
			print "Processing ",x,z
			count = 1
			while box.maxy-count >= box.miny:
				count += 1
				y = box.maxy-count
				theBlock = level.blockAt(x+box.minx, y, z+box.minz)
				if theBlock != 0:
					pixels[x,z] = (int(y),(int(y)),int(y),0xff)
					count = 255
	img.save(options["File name:"]+".png",compress_level=0)
	FuncEnd(level,box,options,method) # Log end
	
def Factorise(number):
	Q = []
	
	for iter in xrange(1,(int)(number+1)):
		p = (int)(number/iter)
		if number - (p * iter) == 0:
			if iter not in Q:
				Q.append(iter)
			if p not in Q:
				Q.append(p)
	return Q

def LayerLoad(level,box,options):
	method = "LayerLoad"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)

	img = Image.open(options["File name:"]+".png")
	pixels = img.load()
	w = img.size[0]
	d = img.size[1]
	(w1,h1,d1,a) = pixels[0,0]
	
	for iterX in xrange(0,w):
		for iterZ in xrange(1,d):
			(b1, data, b3, alpha) = pixels[iterX,iterZ]
			#(b1, b2, b3, data) = pixels[iterX,iterZ]
			
			cx = int( iterX / w1 )
			cz = int( iterZ / d1 )
			
			#theData = int(data)
			layer = cx+cz*int(w/w1)
			setBlock(level, (b1,data), box.minx+int(iterX-cx*w1),box.miny+int(layer),box.minz+int(iterZ-cz*d1-1))
	
	
	FuncEnd(level,box,options,method) # Log end
	
def LayerSave(level,box,options):
	method = "LayerSave"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)

	ignore = options["Ignore block IDs:"].split()
	ignoreList = map(int, ignore)	

	Q = Factorise(height)
	# Choose the "best" pair of factorials
	P = []
	max = height
	r1 = 1
	c1 = height
	for q in Q:
		r = height/q
		diff = abs(q-r)
		if diff < max:
			max = diff
			r1 = q
			c1 = r

	print r1
	print c1
	
	img = Image.new('RGBA', (width*c1, depth*r1+1))
	print 'Sizes %s %s' % (width*c1, depth*r1+1)
	pixels = img.load()
	# Iterate through each layer, top down, rendering each layer to the image file
	pixels[0,0] = (int(width),int(height),int(depth),0xff) # Plenty of room to re-code > 255 dimension objects
	for y in xrange(0,height):
		print y
		for z in xrange(0,depth):
			for x in xrange(0,width):
				theBlock = level.blockAt(x, y, z)
				if not (theBlock in ignoreList): # current block is not air or ignored
					theBlockData = level.blockDataAt(x, y, z)
					p1 = (int(y)%c1)*width    #width*(y%((c1-1)*width))
					p2 = y/(c1)*depth	#int(y/((c1-1)*width))*depth
					#print 'P1 P2 %s %s' % (p1,p2)

					pixels[x+p1,z+int(p2)+1] = (int(theBlock),(int(theBlockData)),int(theBlock),0xff)
					#pixels[x+p1,z+int(p2)+1] = (int(theBlock),int(theBlock),int(theBlock),255-(int(theBlockData)))
	
	img.save(options["File name:"]+".png",compress_level=9)
	
	FuncEnd(level,box,options,method) # Log end							
	
def ExportPNGXY(level,box,options): # See https://www.youtube.com/watch?v=qpk5aIbXIBI by @theCommonPeople
	method = "ExportPNGXY"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)
	BLK_WOOL = 35
	
	ignore = options["Ignore block IDs:"].split()
	ignoreList = map(int, ignore)	

	# Iterate through each layer in the selection rendering each layer to an image file

	for z in xrange(box.minz,box.minz+depth):
		foundABlock = False
		img = Image.new('RGBA', (width, height))
		#print 'Sizes %s %s' % (width, height)
		fileName = options["File name:"]+"_X"+str(box.minx)+"_Y"+str(box.miny)+"_Z"+str(box.minz+z)+"_"+str(randint(1000000,9999999))+".png"
		print "Considering creating file "+fileName
		pixels = img.load()
		for y in xrange(box.miny,box.miny+height):
			for x in xrange(box.minx,box.minx+width): # ToDo: Check with @theCommonPeople whether width or depth-wise scanning
				# each block maps to a pixel in the destination image
				theBlock = getBlock(level, x, y, z) # Source block
				for ((bid,bda),(r,g,b,a),name) in blockColMap: # Ignore non-mapped blocks. Add more if you like!
					if theBlock == (bid,bda): # Match - change this to a lookup for perf.
						foundABlock = True
						px = x-box.minx
						py = y-box.miny
						pixels[px,height-py-1] = (r,g,b,a) # Map in the target pixel at the right location
		# Now we have created the pattern, write it out to the file
		if foundABlock == True:
			print "Saving file "+fileName
			img.save(fileName,compress_level=9)
		else:
			print "No blocks matched, ignoring layer "+fileName

	FuncEnd(level,box,options,method) # Log end	

def ExportPNGZY(level,box,options): # See https://www.youtube.com/watch?v=qpk5aIbXIBI by @theCommonPeople
	method = "ExportPNGZY"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)
	BLK_WOOL = 35
	
	ignore = options["Ignore block IDs:"].split()
	ignoreList = map(int, ignore)	

	# Iterate through each layer in the selection rendering each layer to an image file

	for x in xrange(box.minx,box.minx+width): 
		foundABlock = False
		img = Image.new('RGBA', (depth, height))
		#print 'Sizes %s %s' % (width, height)
		fileName = options["File name:"]+"_X"+str(box.minx+x)+"_Y"+str(box.miny)+"_Z"+str(box.minz)+"_"+str(randint(1000000,9999999))+".png"
		print "Considering creating file "+fileName
		pixels = img.load()
		for y in xrange(box.miny,box.miny+height):
			# ToDo: Check with @theCommonPeople whether width or depth-wise scanning
			for z in xrange(box.minz,box.minz+depth):
			# each block maps to a pixel in the destination image
				theBlock = getBlock(level, x, y, z) # Source block
				for ((bid,bda),(r,g,b,a),name) in blockColMap: # Ignore non-mapped blocks. Add more if you like!
					if theBlock == (bid,bda): # Match - change this to a lookup for perf.
						foundABlock = True
						pz = z-box.minz
						py = y-box.miny
						#print pz,py
						pixels[pz,height-py-1] = (r,g,b,a) # Map in the target pixel at the right location
		# Now we have created the pattern, write it out to the file
		if foundABlock == True:
			print "Saving file "+fileName
			img.save(fileName,compress_level=9)
		else:
			print "No blocks matched, ignoring layer "+fileName

	FuncEnd(level,box,options,method) # Log end		

def ExportPNGXZ(level,box,options): # See https://www.youtube.com/watch?v=qpk5aIbXIBI by @theCommonPeople
	method = "ExportPNGXZ"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)
	BLK_WOOL = 35
	
	ignore = options["Ignore block IDs:"].split()
	ignoreList = map(int, ignore)	

	# Iterate through each layer in the selection rendering each layer to an image file

	for y in xrange(box.miny,box.miny+height):
		foundABlock = False
		img = Image.new('RGBA', (width, depth))
		#print 'Sizes %s %s' % (width, height)
		fileName = options["File name:"]+"_X"+str(box.minx)+"_Y"+str(box.miny+y)+"_Z"+str(box.minz)+"_"+str(randint(1000000,9999999))+".png"
		print "Considering creating file "+fileName
		pixels = img.load()
		for x in xrange(box.minx,box.minx+width): 
			# ToDo: Check with @theCommonPeople whether width or depth-wise scanning
			for z in xrange(box.minz,box.minz+depth):
			# each block maps to a pixel in the destination image
				theBlock = getBlock(level, x, y, z) # Source block
				for ((bid,bda),(r,g,b,a),name) in blockColMap: # Ignore non-mapped blocks. Add more if you like!
					if theBlock == (bid,bda): # Match - change this to a lookup for perf.
						foundABlock = True
						px = x-box.minx
						pz = z-box.minz
						pixels[px,pz] = (r,g,b,a) # Map in the target pixel at the right location
		# Now we have created the pattern, write it out to the file
		if foundABlock == True:
			print "Saving file "+fileName
			img.save(fileName,compress_level=9)
		else:
			print "No blocks matched, ignoring layer "+fileName
	
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
	
def getBlock(level, x, y, z):
	return (level.blockAt(x, y, z),level.blockDataAt(x, y, z))
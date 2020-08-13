# This filter is for jiggling the blocks in your selection box for @Broadbent45
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

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

# Filter pseudocode:
#

inputs = (
		("JIGGLE", "label"),
		("Delta X:",0),
		("Delta Y:",5),
		("Delta Z:",0),
		("Operation:", (
			"Random",
			"Absolute",
			"Cone",
			"Cone 2",
			"Pyramid",
			"Pyramid 2",
			"Sine Wave",
			"Cosine Wave",
			"Dome",
  		    )),
		("Delete source?", True),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def jiggle(olevel, obox, level, box, options):
	method = "Jiggle"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	# Displace each column in the level into the original level according to the operation
	DX = options["Delta X:"]
	DY = options["Delta Y:"]
	DZ = options["Delta Z:"]
	OP = options["Operation:"]
	DEL = options["Delete source?"]
	
	# fill the original selection box
	if DEL == True:
		olevel.fillBlocks(obox,alphaMaterials.Air)

	abox = BoundingBox((0,0,0),(1,height,1))		
	MAXDIST = sqrt(centreWidth*centreWidth+centreDepth*centreDepth)
	ANGLE = pi/180
	for iterX in xrange(0,width):
		if iterX % 10 == 0:
			print iterX
		for iterZ in xrange(0,depth):
			# Extract a column of blocks from the copy of the original space
			cbox = BoundingBox((iterX,0,iterZ),(1,height,1))

			clevel = level.extractSchematic(cbox) # Working set
			
			dx = DX
			dy = DY
			dz = DZ
			if  OP == "Random":
				if dx > 0:
					dx = randint(0,dx)
				elif dx < 0:
					dx = randint(dx,0)
				if dy > 0:
					dy = randint(0,dy)
				elif dy < 0:
					dy = randint(dy,0)
				if dz > 0:
					dz = randint(0,dz)
				elif dz < 0:
					dz = randint(dz,0)
			elif OP == "Cone 2":
				dx = 0
				dz = 0
				ddx = centreWidth - iterX
				ddz = centreDepth - iterZ
				dist = sqrt(ddx*ddx+ddz*ddz)
				MAXDIST = (centreWidth+centreDepth)/2
				dy = sqrt((MAXDIST-dist)**2)
			elif OP == "Cone":
				dx = 0
				dz = 0
				ddx = centreWidth - iterX
				ddz = centreDepth - iterZ
				dy = DY-int(DY*float(sqrt(ddx*ddx+ddz*ddz)/MAXDIST))
			elif OP == "Sine Wave":
				dx = 0
				dz = 0
				ddx = centreWidth - iterX
				ddz = centreDepth - iterZ
				dist = sqrt(ddx*ddx+ddz*ddz)
				ddy = DY-int(DY*float(dist/MAXDIST))
				wl = DX # Wavelength
				# DY is max amplitude at centre
				dy = ddy*sin(2*pi*dist/wl)
			elif OP == "Cosine Wave":
				dx = 0
				dz = 0
				ddx = centreWidth - iterX
				ddz = centreDepth - iterZ
				dist = sqrt(ddx*ddx+ddz*ddz)
				ddy = DY-int(DY*float(dist/MAXDIST))
				wl = DX # Wavelength
				# DY is max amplitude at centre
				dy = ddy*cos(2*pi*dist/wl)
			elif OP == "Pyramid 2":
				dx = 0
				dz = 0
				ddx = centreWidth - iterX
				ddz = centreDepth - iterZ
				ddp = (abs(ddx)+abs(ddz))/2
				ddMAX = (centreWidth+centreDepth)/2
				dy = DY-int(DY*ddp/ddMAX)
			elif OP == "Pyramid":
				dx = 0
				dz = 0
				ddx = centreWidth - iterX
				ddz = centreDepth - iterZ
				dy = DY-ddx
				if ddx > ddz:
					dy = DY-ddx
				if ddz > ddx:
					dy = DY-ddz
			elif OP == "Dome":
				dx = 0
				dz = 0
				dy = 0
				ddx = centreWidth - iterX
				ddz = centreDepth - iterZ
				ddMAX = (centreWidth+centreDepth)/2
				if sqrt(ddx**2+ddz**2) <= ddMAX:
					dy = int(sqrt(ddMAX**2-ddx**2-ddz**2))

				
			#print cbox
			#print obox
			olevel.copyBlocksFrom(clevel, abox, (obox.minx+iterX+dx, obox.miny+dy, obox.minz+iterZ+dz ))
	
	FuncEnd(level,box,options,method)

def perform(originalLevel,originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation
	jiggle(originalLevel, originalBox, level, box, options)
		
		# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end	
	
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

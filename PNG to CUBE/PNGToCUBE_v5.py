# This filter is a hack of @Sethbling's Player Statue filter. 
# It takes a (small) PNG from a web site and renders it as blocks using @Sethbling's material mapping
# This hack @abrightmoore http://brightmoore.net
# Hacks marked up. All other code by @Sethbling, as below:

# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from httplib import HTTPConnection
import png
import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *


# displayName = "PNG to Cube" # Blech. Difficult to version without onscreen clues folks.

inputs = (
	("Alternate Face Orientation", False),
	("Sides", True),
	("Top", True), # Melon, etc
	("Bottom", True), # workbench, logs
	("Flat Model", False),	# Pumpkin, Flower, Glass pane - bring it in as a single vertical render
	("Diagonal Model", False),	# Flower, Glass pane - bring it in as a single vertical render
	("Relief Map", False),	# Bonus transformation - relief map
	("Relief Material", alphaMaterials.Stone),	# Bonus transformation
	("Relief Max Depth", 32),	# Bonus transformation

)


# @Sethbling
materials = [
	(1,   0,  125, 125, 125),
	(3,   0,  134,  96,  67),
	(5,   0,  156, 127,  78),
	(5,   1,  103,  77,  46),
	(5,   2,  195, 179, 123),
	(5,   3,  154, 110,  77),
	(22,  0,   29,  71, 165),
	(24,  0,  229, 221, 168),
	(25,  0,  100,  67,  50),
	(35,  0,  221, 221, 221),
	(35,  1,  219, 125,  62),
	(35,  2,  179,  80, 188),
	(35,  3,  107, 138, 201),
	(35,  4,  177, 166,  39),
	(35,  5,   65, 174,  56),
	(35,  6,  208, 132, 153),
	(35,  7,   64,  64,  64),
	(35,  8,  154, 161, 161),
	(35,  9,   46, 110, 137),
	(35, 10,  126,  61, 181),
	(35, 11,   46,  56, 141),
	(35, 12,   79,  50,  31),
	(35, 13,   53,  70,  27),
	(35, 14,  150,  52,  48),
	(35, 15,   25,  22,  22),
	(41,  0,  249, 236,  78),
	(42,  0,  219, 219, 219),
	(45,  0,  146,  99,  86),
	(49,  0,   20,  18,  29),
	(57,  0,   97, 219, 213),
	(80,  0,  239, 251, 251),
	(82,  0,  158, 164, 176),
	(87,  0,  111,  54,  52),
	(88,  0,   84,  64,  51),
	(98,  0,  122, 122, 122),
	(103, 0,  141, 145,  36),
	(112, 0,   44,  22,  46),
	(121, 0,  221, 223, 165),
	(133, 0,   81, 217, 117),
	#(152, 0,  171,  27,   9), # 1.5
	#(155, 0,  236, 233, 226), # 1.5
]

# Utility methods - by me

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
			scratchpad.setBlockAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockID)
			scratchpad.setBlockDataAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.


def getPixel(pixels, x, y): # @Sethbling
	idx = x*4
	return (pixels[y][idx], pixels[y][idx+1], pixels[y][idx+2], pixels[y][idx+3])
	
def transparent((r, g, b, a)): # @Sethbling
	return a < 1 #28
	
def closestMaterial((r, g, b, a)): # @Sethbling
	closest = 255*255*3
	best = (35, 0)
	for (mat, dat, mr, mg, mb) in materials:
		(dr, dg, db) = (r-mr, g-mg, b-mb)
		dist = dr*dr+dg*dg+db*db
		if dist < closest:
			closest = dist
			best = (mat, dat)
	return best

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	cubePNG(level, box, options)		
	level.markDirtyBox(box)


def cubePNG(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "CUBEPNG"
	print '%s: Started at %s' % (method, time.ctime())

	filename = askOpenFile("Select a Texture image...", False)
	f = open(filename, "rb")
	data = f.read()
	f.close()

	
	AFO = options["Alternate Face Orientation"]
	SIDES = options["Sides"]
	TOP = options["Top"]
	BOTTOM = options["Bottom"]
	FLAT = options["Flat Model"]
	DIAGONAL = options["Diagonal Model"]
	RELIEF = options["Relief Map"]
	RELIEFMATERIAL = (options["Relief Material"].ID, options["Relief Material"].blockData)
	RELIEFMAXDEPTH = options["Relief Max Depth"]


	reader = png.Reader(bytes=data) # @Sethbling
	(width, height, pixels, metadata) = reader.asRGBA8() # @Sethbling
	pixels = list(pixels) # @Sethbling
	
	for x in xrange(0, width):
		print '%s: %s Progress - %s of %s' % (method, time.ctime(), x, width-1)
		for y in xrange(0, height):
			colour = getPixel(pixels, x, y) # after @Sethbling
			if not transparent(colour): # @Sethbling
				(theBlock, theBlockData) = closestMaterial(colour) # @Sethbling

				if RELIEF == False:
					if DIAGONAL == False:

						# Draw the planes
						if FLAT == True:
								setBlock(level, (theBlock, theBlockData), box.minx+x, box.miny+height-y-1, box.minz) # front face
						else:
							if BOTTOM == True:				
								setBlock(level, (theBlock, theBlockData), box.minx+x, box.miny, box.minz+y) # Bottom

							if SIDES == True:
								setBlock(level, (theBlock, theBlockData), box.minx+x, box.miny+height-y-1, box.minz) # front face
								setBlock(level, (theBlock, theBlockData), box.minx+x, box.miny+height-y-1, box.minz+height-1) # back face
								if AFO == True:
									setBlock(level, (theBlock, theBlockData), box.minx, box.miny+y, box.minz+x) # Left face
									setBlock(level, (theBlock, theBlockData), box.minx+height-1, box.miny+y, box.minz+x) # right face
								else:
									setBlock(level, (theBlock, theBlockData), box.minx, box.miny+height-y-1, box.minz+x) # Left face
									setBlock(level, (theBlock, theBlockData), box.minx+height-1, box.miny+height-y-1, box.minz+x) # right face
							if TOP == True:
								setBlock(level, (theBlock, theBlockData), box.minx+x, box.miny+height-1, box.minz+y) # Top
					else: # diagonal
						setBlock(level, (theBlock, theBlockData), box.minx+x, box.miny+height-y-1, box.minz+x)
						setBlock(level, (theBlock, theBlockData), box.minx+width-x, box.miny+height-y-1, box.minz+x)
				else: # Relief map. Plot blocks corresponding to the intensity of the pixels
					(r,g,b,a) = colour
					intensity = (r+g+b)/3
					intensity = intensity*RELIEFMAXDEPTH/255
					for iter in xrange(0,(int)(intensity)):
						setBlock(level, RELIEFMATERIAL, box.minx+x, box.miny+iter, box.minz+y)

	print '%s: Ended at %s' % (method, time.ctime())			
# This filter renders a height map from a colour map
# It takes a (small) PNG from a web site and renders it as blocks
# This hack @abrightmoore http://brightmoore.net
# Hacks marked up. All other code by @Sethbling, as below:

# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

import png
import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *


inputs = (
	("Material", alphaMaterials.WhiteWool),	
	("Max Depth", 32),	
	("Path and Filename", ("string","value=")),
)


# Map fragment originally by @Sethbling - this needs some work to decouple the colour from the intensity.
materials = [
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
]

# Utility methods - by abrightmoore
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
	landscape(level, box, options)		
	level.markDirtyBox(box)


def landscape(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "LANDSCAPE"
	print '%s: Started at %s' % (method, time.ctime())
	filename = options["Path and Filename"]
	filename = filename.strip()
	if filename == "":
		filename = askOpenFile("Select an image...", False)
	f = open(filename, "rb")
	data = f.read()
	f.close()

	
	MATERIALID = options["Material"].ID # Choose wool, stained glass, clay, etc.
	MAXDEPTH = options["Max Depth"]
	
	reader = png.Reader(bytes=data) # @Sethbling
	(width, height, pixels, metadata) = reader.asRGBA8() # @Sethbling
	pixels = list(pixels) # @Sethbling
	
	for x in xrange(0, width):
		print '%s: %s Progress - %s of %s' % (method, time.ctime(), x, width-1)
		for y in xrange(0, height):
			colour = getPixel(pixels, x, y) # after @Sethbling
			if not transparent(colour): # @Sethbling
				(theBlock, theBlockData) = closestMaterial(colour) # @Sethbling
				(r,g,b,a) = colour
				intensity = (r+g+b)/3
				intensity = intensity*MAXDEPTH/255
				for iter in xrange(0,(int)(intensity)):
					setBlock(level, (MATERIALID,theBlockData), box.minx+x, box.miny+iter, box.minz+y)

	print '%s: Ended at %s' % (method, time.ctime())			
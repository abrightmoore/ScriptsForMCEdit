# This filter creates command blocks which trace out a pattern from a supplied picture
# v3 is for drawing lines of particles based on two cartesian points

from httplib import HTTPConnection
import png
import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *
import time # for timing

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

# These imports by @SethBling (http://youtube.com/SethBling)
from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Float
from pymclevel import TAG_Double
from pymclevel import TAG_String


inputs = (
	("PNGTicles", "label"),
	("Orientation", ("X-Y","Z-Y","X-Z")),
	("Path and Filename", ("string","value=")),
	("Transparency Threshold", 128), # New in v3
	("Relative coordinates?", False),	
	("Generator X", 0),
	("Generator Y", 0),
	("Generator Z", 0),
	("Generator Width", 16),
	("Offset",0),
	("Layer Separation", 0),
	("Draw X", 0.0), 
	("Draw Y", 70.0),
	("Draw Z", 0.0),
	("Prefix", ("string","value=particle reddust")),
	("Suffix", ("string","value=-1 1 -1 1 0")), # /particle reddust ~ ~2 ~ -1 1 -1 1 0 is GREEN!
	("Scale", 0.1),
	("Draw Line?", False),
	("Line Start X", 0.5),
	("Line Start Y", 74.5),
	("Line Start Z", 0.5),
	("Line End X", 15.2),
	("Line End Y", 80.2),
	("Line End Z", -7.3),
	
	("abrightmoore@yahoo.com.au", "label"),
	("http://brightmoore.net", "label"),	
)

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

def getPixel(pixels, x, y): # @Sethbling
	idx = x*4
	return (pixels[y][idx], pixels[y][idx+1], pixels[y][idx+2], pixels[y][idx+3])
	
def transparent((r, g, b, a)):
	return a < 128
	
def opaque((r, g, b, a), threshold):
	return a >= threshold

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
	
def createCommandBlockData(x, y, z, theCommand):
	e = TileEntity.Create("Control")
	e["Command"] = TAG_String(theCommand)
	TileEntity.setpos(e, (x, y, z))
	return e
	
	

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	makePNGTicles(level, box, options)		
	level.markDirtyBox(box)
	
def makePNGTicles(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "PNGTicles"
	print '%s: Started at %s' % (method, time.ctime())
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16
	PACKEDCHUNKSIZE = options["Generator Width"]
	if PACKEDCHUNKSIZE == 0:
		PACKEDCHUNKSIZE = CHUNKSIZE
	LAYERGAP = options["Layer Separation"]+1
	ORIENTATION = options["Orientation"]
	COORDS = options["Relative coordinates?"]	
	TRANSPARENCY_T = options["Transparency Threshold"]
	baseX = options["Generator X"]
	baseY = options["Generator Y"]
	baseZ = options["Generator Z"]
	Dx = options["Draw X"]
	Dy = options["Draw Y"]
	Dz = options["Draw Z"]
	OFFSET = options["Offset"]+1
	PREFIX = options["Prefix"]
	SUFFIX = options["Suffix"]
	SCALE = options["Scale"]
	DRAWLINE = options["Draw Line?"]


	packedSpawnerCount = 0
	CHUNKSIZE = 16
	PACKEDCHUNKSIZE = options["Generator Width"]
	if PACKEDCHUNKSIZE == 0:
		PACKEDCHUNKSIZE = CHUNKSIZE
	LAYERGAP = options["Layer Separation"]+1
	
	if DRAWLINE == True: # Create command blocks that creat particles alone a 3D line
		x = options["Line Start X"]
		y = options["Line Start Y"]
		z = options["Line Start Z"]
		x1 = options["Line End X"]
		y1 = options["Line End Y"]
		z1 = options["Line End Z"]
		dx = x1 - x
		dy = y1 - y
		dz = z1 - z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)

		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
			spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
			spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
			setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
			setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
			chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
						
			cX = (x+iter*cos(theta)*cos(phi))
			cY = (y+iter*sin(phi))
			cZ = (z+iter*sin(theta)*cos(phi))
		
			makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS)
			iter = iter+SCALE
			packedSpawnerCount = packedSpawnerCount+1
			chunk.dirty = True

	if DRAWLINE == False: # Draw picture
		filename = options["Path and Filename"]
		filename = filename.strip()
		if filename == "":
			filename = askOpenFile("Select an image...", False)
		f = open(filename, "rb")
		data = f.read()
		f.close()

		reader = png.Reader(bytes=data) # @Sethbling
		(width, height, pixels, metadata) = reader.asRGBA8() # @Sethbling
		pixels = list(pixels) # @Sethbling
		
		for iterY in xrange(0, height):
			print '%s: Processing row %s of %s' % (method, iterY, height)
			for iterX in xrange(0, width):
					colour = getPixel(pixels, iterX, iterY) # after @Sethbling	
					if opaque(colour, TRANSPARENCY_T): # @Sethbling
						(theBlock, theBlockData) = closestMaterial(colour) # @Sethbling
						(r,g,b,a) = colour
		
						spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
						spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
						spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
						setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
						chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
						cX = Dx+iterX*SCALE
						cY = Dy+(height-1-iterY)*SCALE # Fix inverted image
						cZ = Dz+0
						if ORIENTATION == "Z-Y":
							cX = Dx+0
							cY = Dy+(height-1-iterY)*SCALE # Fix inverted image
							cZ = Dz+iterX*SCALE
						elif ORIENTATION == "X-Z":
							cX = Dx+iterX*SCALE
							cY = Dy+0
							cZ = Dz+(height-1-iterY)*SCALE
						
						makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS)
						packedSpawnerCount = packedSpawnerCount+1
						chunk.dirty = True
	
	print '%s: Ended at %s' % (method, time.ctime())
	
def makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS):
	if COORDS == True:
		cX = cX - spawnerX
		cY = cY - spawnerY
		cZ = cZ - spawnerZ 
		theCommand = "/"+PREFIX+" ~"+str(cX)+" ~"+str(cY)+" ~"+str(cZ)+" "+str(SUFFIX)
	else:
		theCommand = "/"+PREFIX+" "+str(cX)+" "+str(cY)+" "+str(cZ)+" "+str(SUFFIX)

	chunk.TileEntities.append( 	createCommandBlockData(spawnerX, 
									spawnerY, 
									spawnerZ, 
									theCommand
								))

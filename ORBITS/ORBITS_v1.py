# This filter creates command blocks which tp an entity to relative coordinates around another entity
# An outgrowth of an idea from @rsmalec's orbital function
# ... extending the PNGTicles filter methods
# ... at the request of Onnowhere

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
	("ORBITAL", "label"),
	("Entity selector being Orbited", ("string","value=@e[name]")),
	("Entity selector in Orbit", ("string","value=@e[name]")),
	("X-Z Radius", 8.0),
	("X-Z Step Angle", 10.0),
#	("Y Radius", 8.0),
#	("Y Step Angle", 5.0),
	
	("Generates command blocks that cause one entity to orbit another", "label"),
	("I supply the math, you supply the redstone power", "label"),
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
	ORBITAL(level, box, options)		
	level.markDirtyBox(box)
	
def ORBITAL(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "ORBITAL"
	print '%s: Started at %s' % (method, time.ctime())
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16
	(width, height, depth) = getBoxSize(box)
	spawnerX = box.minx
	spawnerY = box.miny
	spawnerZ = box.minz
	ESIO = options["Entity selector in Orbit"]
	ESBO = options["Entity selector being Orbited"]
	XZRADIUS = options["X-Z Radius"]
	XZSTEPANGLE = options["X-Z Step Angle"]
#	YRADIUS = options["Y Radius"]
#	YSTEPANGLE = options["Y Step Angle"]
	
	print '%s: Calculating X-Z orbit command blocks!!!OOOOOO' % (method)
	radius = XZRADIUS
	theta = 0.0
	phi = 0.0
	angle = pi/180 * XZSTEPANGLE
	NUMSTEPS = (int)(360/(abs)(XZSTEPANGLE))
	
	(pX,pY,pZ) = (0,0,0)
	
	for iterSteps in xrange(0,NUMSTEPS):
		print 'Step %s of %s' % (iterSteps,NUMSTEPS)
		chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
		setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
		chunk.TileEntities.append( 	createCommandBlockData(spawnerX,spawnerY,spawnerZ,"tp "+ESIO+" "+ESBO)) # Per CrushedPixel, first tick is to orient ESIO at ESBO
		chunk.dirty = True
		spawnerX = spawnerX+2

		# Calculate new X, Y, Z
		(cX,cY,cZ) = getRelativePolar((0,0,0), (theta, phi, radius))
		chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
		setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
		makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),"tp "+ESIO,"",True,True)
		theta = theta + angle
		chunk.dirty = True
		spawnerX = spawnerX-1
		spawnerY = spawnerY+1
		chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
		setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
		chunk.TileEntities.append( 	createCommandBlockData(spawnerX,spawnerY,spawnerZ,"clone ~ ~-1 ~ ~ ~-1 ~ ~ ~-1 ~1 replace move")) # Move the redstone block along
		chunk.dirty = True
		spawnerZ = spawnerZ+1
		spawnerX = spawnerX-1
		spawnerY = spawnerY-1

	print '%s: Ended at %s' % (method, time.ctime())

def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation
	return (x+xDelta, y+yDelta, z+zDelta)
	
def makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS,LOCAL):
	if LOCAL == True:
		theCommand = "/"+PREFIX+" ~"+str(cX)+" ~"+str(cY)+" ~"+str(cZ)+" "+str(SUFFIX)
	elif COORDS == True:
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

# This filter is for namimng Command Blocks using their co-ordinates as the name.
# This is a debugging step so you can see which processes are firing in the admin log
# abrightmoore@yahoo.com.au
# http://brightmoore.net

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy
 
inputs = (
		("CustomName to Coords", "label"),
		("Block Type", ("string","value=Control")),
		("Prefix", ("string","value=[CB@Pos:")),
		("NBT Tag", ("string","value=CustomName")),
		("Suffix", ("string","value=]")),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	NBTCustomNameSwap(level, box, options)
	level.markDirtyBox(box)

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def createCommandBlockData(x, y, z, theCommand):
	e = TileEntity.Create("Control")
	e["Command"] = TAG_String(theCommand)
	TileEntity.setpos(e, (x, y, z))
	return e

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
	level.setBlockDataAt(x, y, z, data)
	
def NBTCustomNameSwap(level, box, options):
	method = "NBTCustomNameSwap"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16

	BLOCKTYPE = options["Block Type"]
	PREFIX = options["Prefix"]
	NBTTAGROOT = str(options["NBT Tag"])
	SUFFIX = options["Suffix"]

	for (chunk, slices, point) in level.getChunkSlices(box):
		print 'a'
		for te in chunk.TileEntities:
			theCommand = PREFIX

			x = te["x"].value
			y = te["y"].value
			z = te["z"].value
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				print '1 - %s' % (te)
				if te["id"].value == BLOCKTYPE:
					theCommand = theCommand + " "+str(te["x"].value)+" "+str(te["y"].value)+" "+str(te["z"].value)+" "+SUFFIX
					te[NBTTAGROOT] = TAG_String(theCommand) # Swap strings		
					chunk.dirty = True

# Converts dropper contents into command blocks - you supply the pre and post-fix
# Requested by ~Sparks
# Based on work by: ItsJustJumby, CrushedPixel, Wire Segal/NicolPotent
#
# This filter is for creating a Command Block using a chunk of NBT from a Dropper.
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
		("SPARKS' NBT CLIPPER", "label"),
		("Prefix", ("string","value=")), # execute @e[type=ArmorStand,name=GM4_CustomCrafter,score_GM4_CCIsEmpty=0] testforblock minecraft:dropper ~ ~-1 ~
		("NBT Tag Root", ("string","value=Items")),
		("Suffix", ("string","value=")),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	NBTClipper(level, box, options)
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
	
def NBTClipper(level, box, options):
	method = "NBTClipper"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16

	PREFIX = options["Prefix"]
	NBTTAGROOT = options["NBT Tag Root"]
	SUFFIX = options["Suffix"]

	for (chunk, slices, point) in level.getChunkSlices(box):
		print 'a'
		for te in chunk.TileEntities:
			theCommand = PREFIX + " "
			print '1 - %s' % (te)
			x = te["x"].value
			y = te["y"].value
			z = te["z"].value
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if te["id"].value == "Dropper":
					theCommand = theCommand + "{" + NBTTAGROOT + ":["
					index = 0
					print '2 - %s' % (te[NBTTAGROOT].value)
					for entry in te[NBTTAGROOT]: # e.g. Items
#						theCommand = theCommand + str(index) + ":{id:\""
#						theCommand = theCommand + str(entry["id"].value) + "\",Damage:" # Thanks @Wout123456

						theCommand = theCommand + "{id:\""
						theCommand = theCommand + str(entry["id"].value) + "\",Damage:" # Thanks @Wout123456

						theCommand = theCommand + str(entry["Damage"].value) +"s,Count:" # Thanks @Wout123456
						theCommand = theCommand + str(entry["Count"].value) +"b,Slot:" # Thanks @Wout123456
						theCommand = theCommand + str(entry["Slot"].value) + "b,}," # Thanks @Wout123456
						index = index+1
					theCommand = theCommand + "]}" + SUFFIX
					chunk = level.getChunk(x/CHUNKSIZE, z/CHUNKSIZE)
					setBlock(level, COMMANDBLOCK, x, y+1, z)
					chunk.TileEntities.append( createCommandBlockData(x,y+1,z,theCommand) )				
					chunk.dirty = True

# {Items:[0:{id:"minecraft:ice",Damage:0s,Count:1b,Slot:0b,},1:{id:"minecraft:ice",Damage:0s,Count:1b,Slot:1b,},2:{id:"minecraft:ice",Damage:0s,Count:1b,Slot:2b,},3:{id:"minecraft:ice",Damage:0s,Count:1b,Slot:3b,},4:{id:"minecraft:snow",Damage:0s,Count:1b,Slot:4b,},5:{id:"minecraft:ice",Damage:0s,Count:1b,Slot:5b,},6:{id:"minecraft:ice",Damage:0s,Count:1b,Slot:6b,},7:{id:"minecraft:ice",Damage:0s,Count:1b,Slot:7b,},8:{id:"minecraft:ice",Damage:0s,Count:1b,Slot:8b,},]}		

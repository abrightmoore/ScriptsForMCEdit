# This filter is for creating ArmorStand entities above each command block found in the selection region, per @CocoaMix86
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_
import time # for timing

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from numpy import *
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import *
from random import Random # @Codewarrior0
import inspect # @Texelelf
from PIL import Image
import png

# GLOBAL
CHUNKSIZE = 16

# Filter pseudocode:
#

inputs = (
		("ArmourCommand", "label"),
		("For @CocoaMix86", "label"),
		("CustomName", ("string","value=x")),
		("Invisible", 1),
		("CustomNameVisible", 1),
		("Invulnerable", 1),
		("Marker", 1),
		("NoGravity",1),
		("MotionX",0.0),
		("MotionY",0.0),
		("MotionZ",0.0),
		("RotationX",0.0),
		("RotationY",0.0),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	armourCommand(level, box, options)

	FuncEnd(level,box,options,method) # Log end	

def armourCommand(level, box, options):
	# Local variables
	method = "armourCommand"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	CMDBLOCK = [137, 210, 211]
	as_CustomName = options["CustomName"]
	as_Invisible = options["Invisible"]
	as_CustomNameVisible = options["CustomNameVisible"]
	as_Invulnerable = options["Invulnerable"]
	as_Marker = options["Marker"]
	as_NoGravity = options["NoGravity"]
	as_MotionX = options["MotionX"]
	as_MotionY = options["MotionY"]
	as_MotionZ = options["MotionZ"]
	as_RotationX = options["RotationX"]
	as_RotationY = options["RotationY"]
	
	for x in xrange(box.minx,box.maxx):
		for z in xrange(box.minz,box.maxz):
			for y in xrange(box.miny,box.maxy):
				(theBlock, theBlockData) = getBlock(level, x, y, z)
				print theBlock
				if theBlock in CMDBLOCK:
					# Create a new ArmorStand Entity above this block with the nominated string as the NBT
					print 'Making a stand'
					createArmorStand(level, x, y+1, z, as_CustomName, as_Invisible, as_CustomNameVisible, as_Invulnerable, as_Marker, as_NoGravity, as_MotionX, as_MotionY, as_MotionZ, as_RotationX, as_RotationY) # After @Sethbling
	FuncEnd(level,box,options,method) # Log end	

def createArmorStand(level, x, y, z, customName, Invisible, CustomNameVisible, Invulnerable, Marker, NoGravity, MotionX, MotionY, MotionZ, RotationX, RotationY): # After @Sethbling
	print("New ArmorStand named "+customName)
	
	mob = TAG_Compound()
	mob["CustomName"] = TAG_String(customName)
	mob["Invisible"] = TAG_Byte(Invisible)
	mob["CustomNameVisible"] = TAG_Byte(CustomNameVisible)
	mob["Invulnerable"] = TAG_Byte(Invulnerable)
	mob["Marker"] = TAG_Byte(Marker)
	mob["NoGravity"] = TAG_Byte(NoGravity)
	mob["OnGround"] = TAG_Byte(1)
	mob["Air"] = TAG_Short(300)
	mob["DeathTime"] = TAG_Short(0)
	mob["Fire"] = TAG_Short(-1)
	mob["Health"] = TAG_Short(20)
	mob["HurtTime"] = TAG_Short(0)
	mob["Age"] = TAG_Int(0)
	mob["FallDistance"] = TAG_Float(0)
	mob["Motion"] = TAG_List()
	mob["Motion"].append(TAG_Double(MotionX))
	mob["Motion"].append(TAG_Double(MotionY))
	mob["Motion"].append(TAG_Double(MotionZ))
	mob["Pos"] = TAG_List()
	mob["Pos"].append(TAG_Double(x + 0.5))
	mob["Pos"].append(TAG_Double(y))
	mob["Pos"].append(TAG_Double(z + 0.5))
	mob["Rotation"] = TAG_List()
	mob["Rotation"].append(TAG_Float(RotationX))
	mob["Rotation"].append(TAG_Float(RotationY))
	mob["id"] = TAG_String("ArmorStand")
	chunk = level.getChunk(x / CHUNKSIZE, z / CHUNKSIZE)
	chunk.Entities.append(mob)
	chunk.dirty = True

	
	
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
	

# This filter is for creating Invisible Armour Stands that have a Custom Name of the command in a command block
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, cosh
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0

inputs = (
		("CBLOCK LABELS", "label"),
		("X offset", 0),
		("Y offset", 1),
		("Z offset", 0),
		("Pad?", False),
		("Suggested by Brian Lorgon", "label"),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
		)

def perform(level, box, options):
	xoff = options["X offset"]
	yoff = options["Y offset"]
	zoff = options["Z offset"]
	
	Q = []
	maxlen = 0
	for (chunk, slices, point) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
	
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if t["id"].value == "Control":
					command = t["Command"].value
					print("Command At: " +str(x)+"(x)"+" "+str(y)+"(y)"+" "+str(z)+ "(z)" + " " +"is: " + t["Command"].value + "													")
					Q.append((command, x, y, z))
					if len(command) > maxlen:
						maxlen = len(command)
	
	for (c, x, y, z) in Q:
		if options["Pad?"] == True:
			createArmorStand(level, x+xoff,y+yoff,z+zoff, c.ljust(maxlen, ' '))
		else:
			createArmorStand(level, x+xoff,y+yoff,z+zoff, c)

def createArmorStand(level, x, y, z, customName): # After @Sethbling
	print("New ArmorStand named "+customName)
	
	mob = TAG_Compound()
	mob["CustomName"] = TAG_String(customName)
	mob["Invisible"] = TAG_Byte(1)
	mob["CustomNameVisible"] = TAG_Byte(1)
	mob["Invulnerable"] = TAG_Byte(1)
	mob["Marker"] = TAG_Byte(1)
	mob["NoGravity"] = TAG_Byte(1)
	mob["OnGround"] = TAG_Byte(1)
	mob["Air"] = TAG_Short(300)
	mob["DeathTime"] = TAG_Short(0)
	mob["Fire"] = TAG_Short(-1)
	mob["Health"] = TAG_Short(20)
	mob["HurtTime"] = TAG_Short(0)
	mob["Age"] = TAG_Int(0)
	mob["FallDistance"] = TAG_Float(0)
	mob["Motion"] = TAG_List()
	mob["Motion"].append(TAG_Double(0))
	mob["Motion"].append(TAG_Double(0))
	mob["Motion"].append(TAG_Double(0))
	mob["Pos"] = TAG_List()
	mob["Pos"].append(TAG_Double(x + 0.5))
	mob["Pos"].append(TAG_Double(y))
	mob["Pos"].append(TAG_Double(z + 0.5))
	mob["Rotation"] = TAG_List()
	mob["Rotation"].append(TAG_Float(0))
	mob["Rotation"].append(TAG_Float(0))

	
	mob["id"] = TAG_String("ArmorStand")
	chunk = level.getChunk(x / 16, z / 16)
	chunk.Entities.append(mob)
	chunk.dirty = True


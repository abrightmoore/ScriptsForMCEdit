# This filter is requested by @MrIlliteracy. It creates command blocks that test for vert and horiz rotation conditions
# Suggested by a number of people, most recently @lemoesh
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
MAXANGLES = 360
a = 2*pi/MAXANGLES
AIR = (0,0)

inputs = (
	("ROTATRACKER", "label"),
	("Viewer X:", 0.5),
	("Viewer Y:", 66.62),
	("Viewer Z:", 0.5),
	("Radius:", 0.3),
	("Selector Prefix:", ("string","value=execute @a[")),
	("Selector Suffix:", ("string","] ~ ~ ~ summon Shulker ")),
	("Block position Suffix:", ("string"," {Glowing:1b}")),
	("Command Blocks X:", 0),
	("Command Blocks Y:", 65),
	("Command Blocks Z:", 0),	
	("abrightmoore@yahoo.com.au", "label"),
	("http://brightmoore.net", "label"),
)

def rotatracker(level,box,options):
	method = "rotatracker"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	px = options["Viewer X:"] # Where the eyes are
	py = options["Viewer Y:"] # Where the eyes are
	pz = options["Viewer Z:"] # Where the eyes are

	cbx = options["Command Blocks X:"] # Where the cblocks start
	cby = options["Command Blocks Y:"] 
	cbz = options["Command Blocks Z:"] 

	
	c1 = options["Selector Prefix:"]
	c2 = options["Selector Suffix:"]
	c3 = options["Block position Suffix:"]
	
	delta = options["Radius:"] # This is the precision of the detection. Not optimal, but since Minecraft only allows for square selection it will have to do.

	cblockXOffset = 0
	
	# Identify all non-air blocks in the selection area
	for y in xrange(box.miny,box.maxy):
		for z in xrange(box.minz,box.maxz):
			for x in xrange(box.minx,box.maxx):
				if getBlock(level,x,y,z) != AIR:
					print "Found a block at "+str(x)+" "+str(y)+" "+str(z)
					# this is a block which needs a command block created
					# 4 positions around the block position - minh, maxh, minv, maxv: ry/rym. rx/rxm
					bxc = float(x+0.5)
					byc = float(y+0.5)
					bzc = float(z+0.5)
					bmx = bxc-delta
					bmy = byc-delta
					bmz = bzc-delta
					bxm = bxc+delta
					bym = byc+delta
					bzm = bzc+delta
					
					dx = bmx - px
					dy = bmy - py
					dz = bmz - pz
					dh = sqrt(dx**2+dz**2)
					thetamin = makeFriendlyNumber(atan2(dz,dx)*360/(2*pi)-90)
					phimin = -makeFriendlyNumber(atan2(dy,dh)*360/(2*pi))
					dx = bxm - px
					dy = bym - py
					dz = bzm - pz
					dh = sqrt(dx**2+dz**2)
					thetamax = makeFriendlyNumber(atan2(dz,dx)*360/(2*pi)-90)
					phimax = -makeFriendlyNumber(atan2(dy,dh)*360/(2*pi))
					if thetamax < thetamin:
						t = thetamin
						thetamin = thetamax
						thetamax = t
					if phimax < phimin:
						t = phimin
						phimin = phimax
						phimax = t
					
					# /execute @a[rxm=5,rx=20,ry=2,rym=-7] ~ ~ ~ summon Shulker 12 48 11 {Glowing:1b}
					command = c1 + "rxm=" + str(phimin) + ",rx=" + str(phimax) + ",rym=" + str(thetamin) + ",ry=" + str(thetamax) + c2 + str(x)+" "+str(y)+" "+str(z)+c3
					createCmdBlock(level, cbx+cblockXOffset, cby, cbz, command)
					cblockXOffset = cblockXOffset + 1
					
					
					# theta is the horizontal angle to the target block
					# phi is the vertical offset
					
					
					
	# Calculate the required rotation values from the Viewer position to the facing corners of this block.
	
	
	FuncEnd(level,box,options,method)	

def makeFriendlyNumber(num):
	num = num * 100
	num = int(num)
	num = float(num)/100.0
	if num < -180:
		num = num + 360
	if num > 179.9:
		num = num - 360
		
	return num

def perform(level,box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	CACHE = False # options["Cache:"]
	
	levelCopy = level
	boxCopy = box

	if CACHE == True:
		levelCopy = level.extractSchematic(box) # Working set
		boxCopy = BoundingBox((0,0,0),(width,height,depth))
	
	rotatracker(levelCopy,boxCopy,options)

	if CACHE == True:
		level.copyBlocksFrom(levelCopy, boxCopy, (box.minx, box.miny, box.minz ))
	
	level.markDirtyBox(box)
	FuncEnd(level,box,options,method) # Log end	

def createCmdBlock(level, x, y, z, command): #abrightmoore - convenience method.
	# 2016-04-17 added TrackOutput default off
	COMMANDBLOCK = (211,5) # Chain Command Block #137
	CHUNKSIZE = 16
	
	setBlock(level, COMMANDBLOCK, int(x), int(y), int(z))
	
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command)
	control["SuccessCount"] = TAG_Int(0)
	control["TrackOutput"] = TAG_Int(0)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	chunka.TileEntities.append(control)
	chunka.dirty = True

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
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
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)


# This filter is for adjusting the selection area to the size of the object within it
# abrightmoore@yahoo.com.au, based on @Texelelf's method of accessing MCEdit interface features
# http://brightmoore.net and http://www.elemanser.com/filters.html
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
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
import inspect # @Texelelf

# For Reference (see @Texelelf and @CodeWarrior0 examples)
# 	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Mirror the blocks - in memory working read only copy
# 	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
#	setBlock(schematic, (BLOCKID, BLOCKDATA), (int)(centreWidth+xx), (int)(centreHeight+yy), (int)(centreDepth+zz))

# YOUR CODE GOES HERE \/ \/ \/ \/ \/ \/ \/ \/ \/
inputs = (
		("SELECTOR", "label"),
		("abrightmoore@yahoo.com.au with @Texelelf", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	# Traverse all the non-air blocks connected to the selected block at the origin of the box.

	AIR = 0
	STONE = 1
	SIZE = 127
	WORKING = MCSchematic((2*SIZE,2*SIZE,2*SIZE))
	
	trackx = SIZE
	tracky = SIZE
	trackz = SIZE
	minx = box.minx
	miny = box.miny
	minz = box.minz
	maxx = box.maxx-1
	maxy = box.maxy-1
	maxz = box.maxz-1
	
	count = 0
	
	Q = []
	Q.append( (box.minx, box.miny, box.minz) )
	while len(Q) > 0:
		print '%s %s %s  %s %s %s' % (minx,miny,minz,maxx,maxy,maxz)
		(x, y, z) = Q.pop()
		print '%s %s %s Popped' % (x,y,z)
		tx = trackx+x-box.minx
		ty = tracky+y-box.miny
		tz = trackz+z-box.minz
		if level.blockAt(x, y, z) != AIR and WORKING.blockAt(tx,ty,tz) == AIR:
			WORKING.setBlockAt(int(tx), int(ty), int(tz), STONE)
			print '%s %s %s = %s' % (x,y,z,level.blockAt(x, y, z))
			if x < minx:
				minx = x
			if y < miny:
				miny = y
			if z < minz:
				minz = z
			if x > maxx:
				maxx = x
			if y > maxy:
				maxy = y
			if z > maxz:
				maxz = z
			
			Q.append( (x-1, y, z) )
			Q.append( (x+1, y, z) )
			Q.append( (x, y-1, z) )
			Q.append( (x, y+1, z) )
			Q.append( (x, y, z-1) )
			Q.append( (x, y, z+1) )

		count = count+1
		if count%1 == 10000:
			print '%s' % (len(Q))		

	editor = inspect.stack()[1][0].f_locals.get('self', None).editor 	# Texelelf
	newBox = BoundingBox( (minx,miny,minz), (maxx-minx+1,maxy-miny+1,maxz-minz+1))
	editor.selectionTool.setSelection(newBox)							# Texelelf
	editor.mainViewport.cameraPosition = (newBox.size/2)+newBox.origin	# Texelelf
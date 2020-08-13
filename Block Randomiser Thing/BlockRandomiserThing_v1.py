# Mader's block thing. Based on Fractal_v3

# MCSchematic access method @TexelElf
# Texelelf's guidance:
#	from pymclevel import MCSchematic, mclevel
#	deformation = pymclevel.MCSchematic((width, height, length), mats=self.editor.level.materials)
#	deformation.setBlockAt(x,y,z,blockID)
#	deformation.setBlockDataAt(x,y,z,blockData)
#	deformation.Blocks[::4] = 57
#	schematic_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir? or mcplatform.schematicsDir, "Save Schematic As...", "", "Schematic\0*.schematic\0\0", ".schematic")
#	deformation.saveToFile(schematic_file)
# And from Codewarrior0's filterdemo.py:
#	level.copyBlocksFrom(temp, temp.bounds, box.origin)

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

inputs = (
	  ("BLOCK RANDOMISER THING", "label"),
	  ("Chance of air", 50),
	  ("Requested by Mader", "label"),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	BlockRandomiserThing(level, box, options)		

def BlockRandomiserThing1(level, box, options):
	AIR = (0,0)
	method = "BlockRandomiserThing"
	print '%s: Started at %s' % (method, time.ctime())
	# Rearranges the blocks in the selection, randomly, with a chance of leaving some of them out of the result
	(width, height, depth) = getBoxSize(box)
	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth)))
	y = height-1
	while y > 0:
		print '%s: Examining the selection area - step %s of %s' % (method, y, height-1)
		for x in xrange(0,width):
			for z in xrange(0,depth):
				tempBlock = (schematic.blockAt(x, y, z),schematic.blockDataAt(x, y, z))
				tempBlockAbove = (schematic.blockAt(x, y+1, z),schematic.blockDataAt(x, y+1, z))
				if y < height-1:
					if tempBlockAbove == AIR:
						if randint(0,100) < options["Chance of air"]:
							setBlock(schematic,AIR,x,y,z)
				elif randint(0,100) < options["Chance of air"]:
					setBlock(schematic,AIR,x,y,z)
		y = y - 1
	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
	
def BlockRandomiserThing(level, box, options): # Prototype - works upwards
	AIR = (0,0)
	method = "BlockRandomiserThing"
	print '%s: Started at %s' % (method, time.ctime())
	# Rearranges the blocks in the selection, randomly, with a chance of leaving some of them out of the result
	(width, height, depth) = getBoxSize(box)
	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth)))
	for y in xrange(0,height):
		print '%s: Examining the selection area - step %s of %s' % (method, y, height-1)
		for x in xrange(0,width):
			for z in xrange(0,depth):
				tempBlock = (schematic.blockAt(x, y, z),schematic.blockDataAt(x, y, z))
				tempBlockBelow = (schematic.blockAt(x, y-1, z),schematic.blockDataAt(x, y-1, z))
				if y > 0:
					if tempBlockBelow == AIR:
						setBlock(schematic,AIR,x,y,z)
				if randint(0,100) < options["Chance of air"]:
					setBlock(schematic,AIR,x,y,z)
	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
	
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
    	level.setBlockDataAt(x, y, z, data)	
	
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
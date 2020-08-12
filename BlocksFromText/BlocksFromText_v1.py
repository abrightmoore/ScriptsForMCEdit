# @abrightmoore
#
# Specification:
# [CommanderRedstone]
# basically, I want some text in notepad, 
# and when I run the filter, it will put dirt
# in this giant stone canvas thing, with dirt 
# being "1"s and stone being "0"s
# kinda like what seth had
# ...
# the thing is hundreds of layers thick

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import randint
from random import Random # @Codewarrior0
from numpy import *
from os import listdir
from os.path import isfile, join
import glob
from mcplatform import *
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity, alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials # @Texelelf
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
import inspect # @Texelelf
# from PIL import Image
import png

inputs = (
			("BLOCKS FROM TEXT", "label"),
			("Block 0:", alphaMaterials.BlockofQuartz),
			("Block 1:", alphaMaterials.Stone),
			("Block 2:", alphaMaterials.Grass),
			("Block 3:", alphaMaterials.Dirt),
			("Block 4:", alphaMaterials.Cobblestone),
			("Block 5:", alphaMaterials.WoodPlanks),
			("Block 6:", alphaMaterials.Wood),
			("Block 7:", alphaMaterials.Glass),
			("Block 8:", alphaMaterials.Sandstone),
			("Block 9:", alphaMaterials.WhiteWool),			
			("Input file and path:", ("string","value=")),
			("abrightmoore@yahoo.com.au", "label"),
			("http://brightmoore.net", "label")
)

def perform(originalLevel, originalBox, options):
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(originalBox.maxx-originalBox.minx,originalBox.maxy-originalBox.miny,originalBox.maxz-originalBox.minz))

	# Do the work
	blocksFromText(level,box,options)
	
	# Replace original world
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
	originalLevel.markDirtyBox(originalBox)

	
def blocksFromText(level,box,options):
	# Read the input file
	blocks = [getBlockFromOptions(options,"Block 0:"),
			  getBlockFromOptions(options,"Block 1:"),
			  getBlockFromOptions(options,"Block 2:"),
			  getBlockFromOptions(options,"Block 3:"),
			  getBlockFromOptions(options,"Block 4:"),
			  getBlockFromOptions(options,"Block 5:"),
			  getBlockFromOptions(options,"Block 6:"),
			  getBlockFromOptions(options,"Block 7:"),
			  getBlockFromOptions(options,"Block 8:"),
			  getBlockFromOptions(options,"Block 9:")]
	with open(options["Input file and path:"]) as f:
		layer = 0
		row = 0
		for line in f: # Parse each line, conditionally write the blocks out in the selection box from the zeroth position
			col = 0
			print row # Progress counter
			if line == "\n":
				layer = layer+1
				row = 0
			else:
				for c in line:
					if c == " ":
						setBlock(level,(0,0),box.minx+col,box.miny+layer,box.minz+row) # Gap / Air
					elif c != "\n":
						v = int(c)
						setBlock(level,blocks[v%len(blocks)],box.minx+col,box.miny+layer,box.minz+row) 
					col += 1
				row += 1
	
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
		
def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
				
	
	
	

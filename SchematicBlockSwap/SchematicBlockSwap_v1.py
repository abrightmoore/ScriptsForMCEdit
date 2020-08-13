# This filter is for enumerating all block variants of Lentebriesje's tree library: http://www.planetminecraft.com/project/native-trees-of-europe-template-repository-1779952/
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
CHUNKSIZE = 16

# Filter pseudocode:
#
#(1) Find the list of 'source schematics' in your Schematics region sub-directories 
#(2) for each file, read it in. 
#(3) create a copy in memory and for each wood and leaf type create a new model with the blocks substituted. 
#(4) Write the new model to a new schematic file (naming?) 
#(5) repeat until no more source schematics available.
# Consider - creating a library schematic with everything laid out neatly

inputs = (
	  ("Schematic Block Swap", "label"),
	  ("Creates variants of schematics with all possible block types", "label"),
	  ("Schematic Folder:", ("string","value=Custom Tree Repository by Lentebriesje")),
#  	  ("Blocks:", ("string","value=16 14 21 73 56 37 38 31 85 52 30 8 9 3 50 39 40 54") ),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

blockIDListWood = [
# Wood blocks
 (17,12),
 (17,13),
 (17,14),
 (17,15),
 
 (162,12),
 (162,13),
]

blockIDListLeaf = [
# Leaves blocks
 (18,4),
 (18,5),
 (18,6),
 (18,7),
 (18,12),
 (18,13),
 (18,14),
 (18,15),

 (161,4),
 (161,5),
 (161,12),
 (161,13),

 ]
	
def SchematicBlockSwap(level, box, options):
	method = "SchematicBlockSwap"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)	
	
	AIR = (0,0)
	
	DIRPATH = options["Schematic Folder:"]
	print 'Scanning available schematics...'
	SchematicFileNames = glob.glob(DIRPATH+"/*.schematic")
	for fileName in SchematicFileNames:
		print fileName
	print 'Found %s schematic files' % (len(SchematicFileNames))
	# End cached file names
	
	blockIDList = []
	for a in blockIDListWood:
		blockIDList.append(a)
	for a in blockIDListLeaf:
		blockIDList.append(a)	
	
	for fn in SchematicFileNames:
		print 'Loading schematic from file - %s' % (fn)
		sourceSchematic = MCSchematic(filename=fn)
		(x,y,z) = sourceSchematic.size
		theBox = BoundingBox((0,0,0),(x,y,z))
		#level.fillBlocks(box, level.materials[mapToList[i]], [level.materials[x]])

		print 'Marking patterns'
		P = []
		for (b,d) in blockIDList:
			print 'Finding the pattern for block ID '+str(b)+' data '+str(d)
			pattern = MCSchematic((x,y,z)) 
			empty = True
			for iterY in xrange(0,y):
				for iterZ in xrange(0,z):
					for iterX in xrange(0,x):
						(b1,d1) = getBlock(sourceSchematic,iterX,iterY,iterZ)
						if (b1,d1) == (b,d): # if this block is of the required type
							setBlock(pattern, (b1,d1), iterX,iterY,iterZ) # change all the copies of the model to have the 		
							empty = False
			if empty == False:
				P.append((b,d,pattern))
		# Now we have pattern schemas, we need to combine them in interesting ways.
		
		print 'Merging patterns with block type variants - wood'
		Q = []
		for (b1,d1,pattern1) in P:
			for (m,n) in blockIDListWood:
				blendedPattern = sourceSchematic.extractSchematic(theBox)
				for iterY in xrange(0,y):
					#print iterY
					for iterZ in xrange(0,z):
						for iterX in xrange(0,x):
							(e,f) = getBlock(pattern1,iterX,iterY,iterZ)
							if (e,f) != AIR:
								setBlock(blendedPattern, (m,n), iterX,iterY,iterZ)
				Q.append((b1,d1,m,n,blendedPattern))
		# produces a bunch of 
								
		R = []
		print 'Merging patterns with block type variants - leaves'
		for (b1,d1,b2,d2,pattern) in Q:
			print fn+"_Block_"+str(b1)+"_Data_"+str(d1)+"_Block_"+str(b2)+"_Data_"+str(d2)
			for (m,n) in blockIDListLeaf:
				for (o,p) in blockIDListLeaf:
					newPattern = pattern.extractSchematic(theBox)
					changed = False
					for iterY in xrange(0,y):
						#print iterY
						for iterZ in xrange(0,z):
							for iterX in xrange(0,x):
								(e,f) = getBlock(pattern,iterX,iterY,iterZ)
								if (e,f) == (m,n):
									setBlock(newPattern, (o,p), iterX,iterY,iterZ)
									changed = True
					if changed == True:
						R.append((b2,d2,o,p,newPattern))
	
		for (b1,d1,b2,d2,newSchematic) in R:
			# Write out the variant schematic files.
			filename = fn+"_Block_"+str(b1)+"_Data_"+str(d1)+"_Block_"+str(b2)+"_Data_"+str(d2)+".schematic"
			newSchematic.saveToFile(filename)
	
	FuncEnd(level,box,options,method)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	SchematicBlockSwap(level, box, options)		
	level.markDirtyBox(box)
	
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
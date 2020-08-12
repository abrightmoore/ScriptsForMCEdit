# Replace whole blocks with steps and slabs to 'smooth' out a surface.
# @abrightmoore on Twitter
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_


import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0



inputs = (
		("SLAB STEP SMOOTH", "label"),
		("Target Material:", alphaMaterials.BlockofQuartz),
#		("Slab Upper:", alphaMaterials.BlockofQuartz),
#		("Slab Lower:", alphaMaterials.Stone),
		("Step Lower East West:", alphaMaterials.GlassPane), # 0
#		("Step Lower West East:", alphaMaterials.GlassPane), # 1
#		("Step Lower North South:", alphaMaterials.GlassPane), # 3
#		("Step Lower South North:", alphaMaterials.GlassPane), # 2
#		("Step Upper East West:", alphaMaterials.GlassPane), 
#		("Step Upper West East:", alphaMaterials.GlassPane), 
#		("Step Upper North South:", alphaMaterials.GlassPane), 
#		("Step Upper South North:", alphaMaterials.GlassPane), 

		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = True
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))

	stairSmooth(level,box,options)
	
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096)
		b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end
	
def stairSmooth(level,box,options):
	method = "Stair Smooth"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)	
	AIR = (0,0)
	# This method scans through a schematic and where it finds a block that can be replaced with stairs or slabs it will try to do so, 'smoothing' out the shape.
	
	material = getBlockFromOptions(options, "Target Material:") # Block to replace
#	materialSU = getBlockFromOptions(options, "Slab Upper:") 
#	materialSL = getBlockFromOptions(options, "Slab Lower:")
	materialSLEW = (mID,mDV) = getBlockFromOptions(options, "Step Lower East West:") 
	materialSLEW = (mID, 0)
	materialSLWE = (mID, 1) # getBlockFromOptions(options, "Step Lower West East:")
	materialSLNS = (mID, 3) # getBlockFromOptions(options, "Step Lower North South:")
	materialSLSN = (mID, 2) # getBlockFromOptions(options, "Step Lower South North:")
#	materialSUEW = getBlockFromOptions(options, "Step Upper East West:") 
#	materialSUWE = getBlockFromOptions(options, "Step Upper West East:") 
#	materialSUNS = getBlockFromOptions(options, "Step Upper North South:")
#	materialSUSN = getBlockFromOptions(options, "Step Upper South North:")
	
	# Take a reference copy of the selection box which will not change. We can refer back to it...
	refLevel = level.extractSchematic(box) # Working set
	refBox = BoundingBox((0,0,0),(width,height,depth))
	
	# Start at the bottom
	for y in xrange(0,height):
		for z in xrange(0,depth):
			for x in xrange(0,width):
				B0 = getBlock(refLevel,refBox.minx+x,refBox.miny+y,refBox.minz+z)
				if B0 == material: # This is a block of interest as it may be changed based on what's around it
					# Test the region around this block for a configuration that we can use to swap in a stair or slab
					BU = getBlock(refLevel,refBox.minx+x,refBox.miny+y+1,refBox.minz+z)
					BD = getBlock(refLevel,refBox.minx+x,refBox.miny+y-1,refBox.minz+z)
					BE = getBlock(refLevel,refBox.minx+x+1,refBox.miny+y,refBox.minz+z)
					BW = getBlock(refLevel,refBox.minx+x-1,refBox.miny+y,refBox.minz+z)
					BN = getBlock(refLevel,refBox.minx+x,refBox.miny+y,refBox.minz+z+1)
					BS = getBlock(refLevel,refBox.minx+x,refBox.miny+y,refBox.minz+z-1)
					BEU = getBlock(refLevel,refBox.minx+x+1,refBox.miny+y+1,refBox.minz+z)
					BWU = getBlock(refLevel,refBox.minx+x-1,refBox.miny+y+1,refBox.minz+z)
					BNU = getBlock(refLevel,refBox.minx+x,refBox.miny+y+1,refBox.minz+z+1)
					BSU = getBlock(refLevel,refBox.minx+x,refBox.miny+y+1,refBox.minz+z-1)
					BED = getBlock(refLevel,refBox.minx+x+1,refBox.miny+y-1,refBox.minz+z)
					BWD = getBlock(refLevel,refBox.minx+x-1,refBox.miny+y-1,refBox.minz+z)
					BND = getBlock(refLevel,refBox.minx+x,refBox.miny+y-1,refBox.minz+z+1)
					BSD = getBlock(refLevel,refBox.minx+x,refBox.miny+y-1,refBox.minz+z-1)
					BNE = getBlock(refLevel,refBox.minx+x+1,refBox.miny+y,refBox.minz+z+1)
					BNW = getBlock(refLevel,refBox.minx+x-1,refBox.miny+y,refBox.minz+z+1)
					BSE = getBlock(refLevel,refBox.minx+x+1,refBox.miny+y,refBox.minz+z-1)
					BSW = getBlock(refLevel,refBox.minx+x-1,refBox.miny+y,refBox.minz+z-1)

					
					if BU == AIR: # Air above the target block

						if BW == material and BE == AIR and BWU == AIR and BWD == material:
							setBlock(level,materialSLWE,box.minx+x,box.miny+y,box.minz+z)
						if BE == material and BW == AIR and BEU == AIR and BED == material:
							setBlock(level,materialSLEW,box.minx+x,box.miny+y,box.minz+z)
						if BN == material and BS == AIR and BNU == AIR and BND == material:
							setBlock(level,materialSLSN,box.minx+x,box.miny+y,box.minz+z)
						if BS == material and BN == AIR and BSU == AIR and BSD == material:
							setBlock(level,materialSLNS,box.minx+x,box.miny+y,box.minz+z)
					
						if BW == material and BE == AIR and BWU == material:
							setBlock(level,materialSLWE,box.minx+x,box.miny+y,box.minz+z)
						if BE == material and BW == AIR and BEU == material:
							setBlock(level,materialSLEW,box.minx+x,box.miny+y,box.minz+z)
						if BN == material and BS == AIR and BNU == material:
							setBlock(level,materialSLSN,box.minx+x,box.miny+y,box.minz+z)
						if BS == material and BN == AIR and BSU == material:
							setBlock(level,materialSLNS,box.minx+x,box.miny+y,box.minz+z)

						if BE == AIR and BWU == material:
							setBlock(level,materialSLWE,box.minx+x,box.miny+y,box.minz+z)
						if BW == AIR and BEU == material:
							setBlock(level,materialSLEW,box.minx+x,box.miny+y,box.minz+z)
						if BS == AIR and BNU == material:
							setBlock(level,materialSLSN,box.minx+x,box.miny+y,box.minz+z)
						if BN == AIR and BSU == material:
							setBlock(level,materialSLNS,box.minx+x,box.miny+y,box.minz+z)
							
						if BE == AIR and BN == AIR and BS == material and BW == material: # Corner
							setBlock(level,materialSLNS,box.minx+x,box.miny+y,box.minz+z)
#						if BE == material and BN == AIR and BS == AIR and BW == material:
#							setBlock(level,materialSL,box.minx+x,box.miny+y,box.minz+z) # Slab lower
						if BE == material and BN == material and BS == AIR and BW == AIR:
							setBlock(level,materialSLSN,box.minx+x,box.miny+y,box.minz+z) # Corner
#						if BE == AIR and BN == material and BS == material and BW == AIR:
#							setBlock(level,materialSL,box.minx+x,box.miny+y,box.minz+z) # Slab lower
						if BE == material and BN == material and BS == material and BW == material: # Corner
							if BNE == material and BNW == material and BSE == material and BSW == AIR:
								setBlock(level,materialSLSN,box.minx+x,box.miny+y,box.minz+z)
							if BNE == material and BNW == material and BSE == AIR and BSW == material:
								setBlock(level,materialSLSN,box.minx+x,box.miny+y,box.minz+z)
							if BNE == material and BNW == AIR and BSE == material and BSW == material:
								setBlock(level,materialSLNS,box.minx+x,box.miny+y,box.minz+z)
							if BNE == AIR and BNW == material and BSE == material and BSW == material:
								setBlock(level,materialSLNS,box.minx+x,box.miny+y,box.minz+z)

							
							
	FuncEnd(level,box,options,method)

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))
	
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

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
	
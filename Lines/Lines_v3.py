# This filter creates lines between all blocks in a selection area
# v2 adds an option to place rails on the blocks drawn
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)

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
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *

inputs = (
	  ("LINES", "label"),
#	  ("Rails?", False),
	  ("Custom fill?", False),
	  ("Material", alphaMaterials.WhiteWool),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt((int)(x),(int)(y),(int)(z))
    if tempBlock == 0:
	setBlock(level, (block, data), (int)(x),(int)(y),(int)(z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, (int)(y)):
    	setBlockIfEmpty(level, (block, data), (int)(x),(int)(iterY),(int)(z))
    	

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def fix(angle):
	while angle > pi:
		angle = angle - 2 * pi
	while angle < -pi:
		angle = angle + 2 * pi
	return angle

def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			px = x+iter*cos(theta)*cos(phi)
			py = y+iter*sin(phi)
			pz = z+iter*sin(theta)*cos(phi)
			b = scratchpad.blockAt(px, py, pz)
			if b == 0:
				scratchpad.setBlockAt(px, py, pz, blockID)
				scratchpad.setBlockDataAt(px, py, pz, blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Web(level, box, options)		
	level.markDirtyBox(box)

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def Web(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "WEB"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	MATERIAL = (35, 0)
	RAIL = (66, 0)
	# RAILS = options["Rails?"]
	CUSTOMFILL = options["Custom fill?"]
	scratchpad = level.extractSchematic(box)
	# END CONSTANTS
	mat = getBlockFromOptions(options,"Material")
	# 1st pass - scan and build the list of blocks
	Q = []

	for iterX in xrange(0,width):
		for iterY in xrange(0,height):
			for iterZ in xrange(0,depth):
				theBlock = level.blockAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				if theBlock != 0: # current block is not air
					theBlockData = level.blockDataAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					setBlock(scratchpad, (theBlock, theBlockData), iterX, iterY, iterZ)
					print 'Found a block at %s %s %s' % (iterX, iterY, iterZ)
					Q.append( (iterX, iterY, iterZ, (theBlock, theBlockData) ))

	# 2nd pass - build a path from each block to every other block, using the material of the source block

	P = Q
	
	for (x, y, z, (blockID,blockData)) in Q:
		for (x1, y1, z1, (material1)) in P:

			# if randint(0,50) == 1:
			#drawLineConstrained(scratchpad, (blockID, blockData), (x, y, z), (x1, y1, z1), width / 3 )
			if CUSTOMFILL == True:
				(blockID,blockData) = mat
			drawLine(scratchpad, (blockID, blockData), (x, y, z), (x1, y1, z1) )
			#if RAILS == True:
			#	drawLine(scratchpad, RAIL, (x, y+1, z), (x1, y1+1, z1) )

	# Copy schematic into the world
	level.copyBlocksFrom(scratchpad, scratchpad.bounds, box.origin)
	
	print '%s: Ended at %s' % (method, time.ctime())
	

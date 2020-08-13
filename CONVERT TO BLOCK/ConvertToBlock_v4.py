# This filter changes all blocks to a particular block type in a selection area
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
	  ("Convert To Block", "label"),
	  ("Material:", alphaMaterials.Brick), # https://github.com/mcedit/pymclevel/blob/master/materials.py
	  ("Other IDs:", ("string","value=10 11") ),
	  ("Only This?", False),
	  ("Match Data?", False),
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
			scratchpad.setBlockAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockID)
			scratchpad.setBlockDataAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	ConvertToBlock(level, box, options)		
	level.markDirtyBox(box)
	
def ConvertToBlock(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "CONVERTTOBLOCK"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	MATERIALID = options["Material:"].ID 
	MATERIAL = (MATERIALID, options["Material:"].blockData)
	OTHERIDS = options["Other IDs:"].split()
	OTHERIDS = map(int, OTHERIDS)
	ONLYTHIS = options["Only This?"]
	MATCHDATA = options["Match Data?"]
	AIR = (0,0)
	# END CONSTANTS

	for iterX in xrange(0,width):
		print '%s of %s' % (iterX, width)
		for iterY in xrange(0,height):
			for iterZ in xrange(0,depth):
				theBlock = level.blockAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				if theBlock != 0:
					if ONLYTHIS == False: # current block is not air
						setBlock(level, MATERIAL, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					elif MATCHDATA == True:
						theData = level.blockDataAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
						if (theBlock,theData) != MATERIAL:
							setBlock(level, AIR, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					elif MATERIALID != theBlock and theBlock not in OTHERIDS:
						setBlock(level, AIR, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
	
	print '%s: Ended at %s' % (method, time.ctime())
	

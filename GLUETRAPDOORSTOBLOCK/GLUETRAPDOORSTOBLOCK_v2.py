# @TheWorldFoundry
# Filter that 'glues' trapdoors to the adjacent block of the specified type. 
# Requested by @Smurfmashers
# Select a region. Select the trapdoor material type, and the block to align with if there is a 'floating' trapdoor next to it.

import time # for timing
from numpy import zeros
from random import randint,random
from pymclevel import alphaMaterials,MCSchematic,BoundingBox
from math import sqrt,cos,pi,ceil
from os import listdir
from os.path import isfile, join
import glob
from PIL import Image

import PROCGEN_TOOLS
from PROCGEN_TOOLS import getBlock,setBlock,getBlockFromOptions

inputs = (
		("GLUE TRAPDOORS TO BLOCK", "label"),
		("What trapdoor material to glue?", "label"), 
		("Trapdoor material:", alphaMaterials.Glowstone),
		("What block type to glue it on?", "label"),
		("Block to glue on:", alphaMaterials.Trapdoor),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

def logMessage(source,msg):
	print time.ctime(),"[",source,"]",msg

def perform(level, box, options):
	#Find the material
	logMessage("GLUE","Starting...")
	(blockID,blockData) = materialBlock = getBlockFromOptions(options,"Block to glue on:")
	(trapdoorID,trapdoorData) = materialTrapdoor = getBlockFromOptions(options,"Trapdoor material:")
	AIR = 0,0
	
	# Trapdoor orientation values via https://minecraft.gamepedia.com/Trapdoor
	SOUTH = 0
	NORTH = 1
	EAST = 2
	WEST = 3
	OPEN = 4
	TOP = 8
	INVALID = -1
	
	for y in xrange(box.miny,box.maxy):
		for z in xrange(box.minz,box.maxz):
			for x in xrange(box.minx,box.maxx):
				blockHere = getBlock(level,x,y,z)
				if blockHere == materialBlock: # Found a block to glue TO
					# Search around this block for instances of the trapdoor block id
					for ix in xrange(-1,2):
						for iz in xrange(-1,2):
							for iy in xrange(-1,2):
								px = x+ix
								py = y+iy
								pz = z+iz
								if px >= box.minx and px < box.maxx and py >= box.miny and py < box.maxy and pz >= box.minz and pz < box.maxz: # Check we're in-bounds of the selection
									neighbourBlockID = level.blockAt(px,py,pz)
									if neighbourBlockID == trapdoorID: # a match
										logMessage("GLUE","I found a block to glue to at "+str(x)+" "+str(y)+" "+str(z))
										currentData = level.blockDataAt(px,py,pz)
										data = INVALID # Trapdoor on sout 
										# 0: Trapdoor on the south side of a block
										# 1: Trapdoor on the north side of a block
										# 2: Trapdoor on the east side of a block
										# 3: Trapdoor on the west side of a block
										if ix == -1: # Block is to the West, so the trapdoor should be on the east face
											data = EAST | OPEN
										elif ix == 1: # East
											data = WEST | OPEN
										elif iz == -1: # North
											data = SOUTH | OPEN
										elif iz == 1: # South
											data = NORTH | OPEN
										elif iy == -1: # Below
											data = TOP | (currentData & 0x3) # Clear the OPEN bit
										elif iy == 1: # Above
											data = currentData & 0x3 # Mask out the up/down for down, and make it closed bit but leave the position info
											
										if data != INVALID: # If nothing went wrong
											level.setBlockDataAt(int(px),int(py),int(pz),data)

	logMessage("GLUE","Complete.")
									
									
								
					
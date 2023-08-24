# @TheWorldFoundry
# Read all schematics in a folder, load each one and place it in the world starting at the selection box

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import *
from os import listdir
from os.path import isfile, join
import glob

inputs = (
	  ("SchematicImportLoader", "label"),
	  ("Schematic Folder:", ("string","value=")),
 	  ("adrian@TheWorldFoundry.com", "label"),
	  ("http://TheWorldFoundry.com", "label"),
)

def perform(level, box, options):
	schematicImportLoader(level, box, options)
	# level.markDirtyBox(box)

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def makeChunksIfNotPresent(level,pos,size):
	bb = BoundingBox(pos,size)
	# print "chunkPositions",bb.chunkPositions
	for p in bb.chunkPositions:
		(cx,cz) = p
		if not level.containsChunk(cx, cz):
			level.createChunk(cx, cz)
			print "Created chunk ", cx, cz
		else:
			print "Chunk ", cx, cz, " already exists"

def placeASchematic(x,y,z, charSchematic, level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "placeASchematic"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	
	# END CONSTANTS

	# cursorPosn = box.origin
	# import the corresponding MCSchematic to the supplied filename
	cursorPosn = (x, y, z)
	makeChunksIfNotPresent(level, cursorPosn, (charSchematic.Width+1, charSchematic.Height, charSchematic.Length+1))
	blocksIDs = range(level.materials.id_limit)
	level.copyBlocksFrom(charSchematic, BoundingBox((0,0,0),(charSchematic.Width,charSchematic.Height,charSchematic.Length)), cursorPosn, blocksToCopy=blocksIDs)

	print '%s: Ended at %s' % (method, time.ctime())

def schematicImportLoader(level, box, options):
	# CONSTANTS
	method = "schematicImportLoader"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	DIRPATH = options["Schematic Folder:"]
	schematicFiles = glob.glob(DIRPATH+"/*.schematic")
	for fileName in schematicFiles:
		print fileName
	print 'Found %s start schematic files' % (len(schematicFiles))
	
	x,y,z = box.minx, box.miny, box.minz
	for fileName in schematicFiles:
		print x,y,z
		print 'Loading schematic from file - %s' % (fileName)
		print os.getcwd()
		try:
			charSchematic = MCSchematic(filename=fileName)
			
			# Check if chunks exist, make them if not
			placeASchematic(x,y,z, charSchematic, level, box, options)
			dz = charSchematic.Length + 1
			z += dz
		except:
			print "Failed to load and place the schematic ", fileName
		
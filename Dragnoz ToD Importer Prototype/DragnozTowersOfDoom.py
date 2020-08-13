# This filter places the "Dragnoz Towers of Doom" schematic in the current OverWorld
#    at a specific location that is needed for the mechanism to work
# Requested by @Dragnoz
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# MCSchematic access method @TexelElf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import time # for timing

displayName = "DRAGNOZ Towers of Doom Importer"

SCHEMATICFILENAME = "DragnozTowersOfDoom.schematic"
COORDINATES = ( 0, 100, 0)
SHAPE = (128,128,128)

inputs = (
	  ("Dragnoz TOWERS OF DOOM", "label"),
	  ("TO IMPORT THE MECHANISM, PRESS FILTER (BELOW) THEN SAVE THE WORLD", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	DragnozTowersOfDoom(level, box, options)		
	level.markDirtyBox(box)

def DragnozTowersOfDoom(level, box, options):
	print 'Dragnoz Towers of Doom schematic load sequence started...'
	(theSchematic , theBoundingBox) = retrieveSelectedSchematic(SCHEMATICFILENAME)
	print 'Dragnoz Towers of Doom schematic loaded!'
	level.copyBlocksFrom(theSchematic, theBoundingBox, COORDINATES)
	print 'Dragnoz Towers of Doom schematic has been placed in the world. Press SAVE in MCEdit to finish.'
	
def retrieveSelectedSchematic(theFileName): # Load a schematic, analyse it (find the bounds) and return the schematic and bounding box
	# ... todo: Cache schematics so I don't need to analyse on each access
	method = "retrieveSelectedSchematic"
	print 'Loading schematic from file - %s' % (theFileName)
	charSchematic = MCSchematic(shape=SHAPE,filename=theFileName)
	return (charSchematic, analyse(charSchematic))
	
def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	#print 'ANALYSE %s %s %s' % (width, height, depth)

	minX = width
	minY = height
	minZ = depth
	maxX = 0
	maxY = 0
	maxZ = 0
	found = False
	
	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depth):
				if level.blockAt(iterX, iterY, iterZ) != 0:
					#print 'ANALYSING %s %s %s' % (iterX, iterY, iterZ)
					if iterX > maxX:
						maxX = iterX
					if iterY > maxY:
						maxY = iterY
					if iterZ > maxZ:
						maxZ = iterZ
				
					if iterX < minX:
						minX = iterX
					if iterY < minY:
						minY = iterY
					if iterZ < minZ:
						minZ = iterZ
						
					found = True

	#print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	#print '%s: Ended at %s' % (method, time.ctime())
	
	if found == False:
		return BoundingBox((0, 0, 0), (width, height, depth))	
	else:
		return BoundingBox((minX, 0, minZ), (maxX+1, maxY+1, maxZ+1))
		
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
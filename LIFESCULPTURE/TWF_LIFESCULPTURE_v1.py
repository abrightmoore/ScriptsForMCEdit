# @TheWorldFoundry

# Select a region. The life-plane is x/y and the depth holds each tick.
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
		("LIFE SCULPTURE", "label"),
		("Number of ticks", 0),
		("Material:", alphaMaterials.BlockofQuartz),
		("Mode", ( "Randomise", "Load image", "None")),
		("Initial chance:", 0.5),
		("File path", ("string","value=")),
		("Red", 255),
		("Green", 255),
		("Blue", 255),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

def logMessage(source,msg):
	print time.ctime(),"[",source,"]",msg

def initialiseFromImageFile(plane,path,material,(R,G,B)):
	logMessage("loadImageFromFile","Start loading file "+path)
	img = Image.open(path)
	img = img.convert("RGBA")
	imgPix = img.load()
	width = img.size[0]
	height = img.size[1]
	
	# Put the image in the centre of the plane
	
	gapWidth = (plane.Width - width)>>1
	gapHeight = (plane.Height - height)>>1
	print width,height
	for x in xrange(0,width):
		for y in xrange(0,height):
			(r,g,b,a) = imgPix[x,y]
			if r == R and g == G and b == B:
				px = x+gapWidth
				py = y+gapHeight
				if px >= 0 and px < plane.Width and py >= 0 and py < plane.Height: # Bounds check
					setBlock(plane,px,py,0,material)
	logMessage("loadImageFromFile","End")

	
	
def initialise(plane,chance,material):
	# Randomly seed the plane
	print "Initialising..."
	count = 0
	for x in xrange(0,plane.Width):
		for y in xrange(0,plane.Height):
			if random() <= chance:
				setBlock(plane,x,y,0,material)
				count += 1
	print "Initialised",count,"blocks!"

def calculateLifeTick(prevPlane,plane,material):
	DEAD = -1
	ALIVE = 1
	AIR = 0,0
	
	Q = zeros((plane.Width,plane.Height)) # -1 = dead, otherwise the number indicates the number of neighbours

	countAlive = 0
	countDeath = 0
	countBirth = 0
	# Seed the field with the blocks from the MCEdit selection
	for iterY in xrange(0, plane.Height):
		for iterX in xrange(0, plane.Width): # For each cell in the previous plane
			if prevPlane.blockAt(iterX,iterY,0) != 0: # Not air
				Q[iterX,iterY] = ALIVE # alive
			else:
				Q[iterX,iterY] = DEAD
	logMessage("calculateLifeTick","Sweeping plane")
	for iterY in xrange(0, plane.Height):
		for iterX in xrange(0, plane.Width): # For each cell in the previous plane
			neighbourCount = 0
			for ix in xrange(-1,2):
				for iy in xrange(-1,2):
					if ix == 0 and iy == 0:
						t = 0 # Pass
					else: #if ix != 0 or iz != 0: # Don't count the current cell
						if iterX+ix < plane.Width and iterX+ix >= 0 and iterY+iy < plane.Height and iterY+iy >= 0: # Only consider cells in the plane, no loops
							if Q[iterX+ix,iterY+iy] != DEAD:
								neighbourCount = neighbourCount +1
			if Q[iterX,iterY] != DEAD: # It's alive!
				if neighbourCount < 2 or neighbourCount > 3: # Lonely or crowded, die in the next generation
					# setBlock(plane,AIR,iterX,iterY) # DEAD
					#print 'killing %s %s' % (iterX, iterZ)
					countDeath = countDeath +1
				elif neighbourCount == 2 or neighbourCount ==3: # Live another day
					setBlock(plane,iterX,iterY,0,material) # Alive
					# print 'leaving alive %s %s' % (iterX, iterZ)
					countAlive = countAlive +1
			else: # It is dead
				if neighbourCount == 3:
					setBlock(plane,iterX,iterY,0,material) # Alive! Born again.
					# print 'new baby at %s %s' % (iterX, iterZ)
					countBirth = countBirth +1
				else:
					t = 0 # Pass. Q[iterX, iterY, 0] = DEAD # Set it dead on the target field.
	print "This tick: Alive",countAlive,"Born",countBirth,"Died",countDeath
	logMessage("calculateLifeTick","Plane swept")
	
def perform(level,box,options):
	print "ALife generation: Start."

	width = box.maxx - box.minx
	height= box.maxy - box.miny
	depth = box.maxz - box.minz
	material = getBlockFromOptions(options,"Material:")
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	
	
	planes = []
	prevTickPlane = MCSchematic((width, height, depth))
	print options["Mode"]
	if options["Mode"] == "Randomise":
		# Randomise to initialise
		initialise(prevTickPlane,options["Initial chance:"],material)
	elif options["Mode"] == "Load image":
		# Use black pixels to seed the generation
		initialiseFromImageFile(prevTickPlane,options["File path"],material,(options["Red"],options["Green"],options["Blue"]))
	else: # Use what's in the lowest plane of the selection box (i.e. the SOUTH most layer). Not air equals an alive cell.
		prevTickPlane = level.extractSchematic(BoundingBox((box.minx,box.miny,box.minz),(width,height,1)))
	
	numTicksToRun = options["Number of ticks"]
	if numTicksToRun > depth:
		numTicksToRun = depth
	level.copyBlocksFrom(prevTickPlane, BoundingBox((0,0,0),(width,height,1)), (box.minx, box.miny, box.minz ),b) #First layer
	for z in xrange(1,numTicksToRun):
		print "Ticking",z
		TickPlane = MCSchematic((width, height, depth))
		calculateLifeTick(prevTickPlane, TickPlane, material)
		# planes.append(TickPlane) # History
		level.copyBlocksFrom(TickPlane, BoundingBox((0,0,0),(width,height,1)), (box.minx, box.miny, box.minz+z ),b)
		prevTickPlane = TickPlane
	
	if options["Mode"] == "File path": # Save the last plane so it can be the next input if required.
		img.save(options["File path"]+"_end.png")
		
	level.markDirtyBox(box)
	print "ALife generation: Done."
	print "Complete!"


def loadImageFromFile(path,filename):
	logMessage("loadImageFromFile","Start")
	newimg = Image.open(os.path.join(path, filename))
	logMessage("loadImageFromFile","End")
	return newimg
	
def loadRandomImage(path):
	logMessage("loadRandomImage","Start")
	images = glob.glob(os.path.join(path, "*.png"))
	selectedImage = images[randint(0,len(images)-1)]
	print selectedImage
	img = loadImageFromFile("",selectedImage)
	logMessage("loadRandomImage","End")
	return img
	
def saveImageToFile(img,path,filename):
	logMessage("saveImageToFile","Start")
	img.save(os.path.join(path, filename))
	logMessage("saveImageToFile","End")	
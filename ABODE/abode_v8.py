# @TheWorldFoundry
# Settlement challenge 2018


import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0
import inspect # @Texelelf
import png
import pygame

# GLOBAL
CHUNKSIZE = 16
MAXANGLES = 360
a = 2*pi/MAXANGLES
AIR = (0,0)
LAVA = (11,0)

coloursList = "15 7 8 0 6 2 10 11 3 9 13 5 4 1 14 12".split() # I like this sequence
#coloursList = "15 15 15 15 15 11 11 11 0".split()
colours = map(int, coloursList)
palette = []
palette.append( [ (1,0),(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (80,0) ] )
palette.append( [ (95,3),(22,0), (24,2), (19,0), (18,0), (3,0), (1,0), (80,0) ]	)
RAND2 = Random(42)

# Choose a colour pallette
print 'Pallette Selection'
gap = RAND2.randint(1,4)
for i in range(32):
	newCols = []
	baseIndex = RAND2.randint(0,len(colours))

	for j in range(8):
		newCols.append( (159, (int)(colours[(baseIndex+j*gap)%len(colours)]) ) )
	palette.append(newCols)
print 'Pallette Selection complete'


inputs = (
		("ABODE", "label"),
		("Dwellings:", 10),
		("Seed:", 0),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

def perform(level,box,options):
#	print "Generating settlement graph:"

#	townSquare = Square()
#	for i in xrange(0,options["Dwellings:"]):
#		house = makeAbodeA()
#		path = Pathway()
#		path.connect(house)
#		townSquare.connect(path)
#	print "Settlement graph generated:"
#	townSquare.printOut()
	
	# Find a place to lay down the centre of the map
	
	heightMap = getMyHeightMap(level,box,options) # Interrogate the world
	heightMapImg = convertHeightMapToImage(heightMap) # Get the data as intensity values so we can do some processing
	UNIQUEID = str(randint(1000000,9999999))
	pygame.image.save(heightMapImg, "ABODE_"+UNIQUEID+"_HeightMap.png")
	
	# Image processing... edges
	print "Finding areas to avoid:"
	edgyImage = findEdges(heightMapImg)
	pygame.image.save(edgyImage, "ABODE_"+UNIQUEID+"_EdgeMap.png")
	# Candidate regions

#	print "Profiling a range of plot sizes for taste and flavour:"
#	AHM = generateAggregateHeightMaps(heightMap) # Carve up the map into regions of various sizes. This is one strategy to identifytify plots
#	plots = []

	# NEW STRATEGY
	# Select a candidate location from the edge map
	# Build out the dwelling at that location, track it (for joining up with roadways later), and update the edge map showing it's no longer available
	
	# First step - find all the 'zero points' as these are buildout candidates
	(RAND,SEED) = getRandFromSeed(options)
	flatPoints = findLocations(edgyImage,0)
	fillMat = (98,0) # Stone Brick

	for i in xrange(0,options["Dwellings:"]):
		print "Building dwelling number",i+1,"of",options["Dwellings:"]
		selectedLocation = flatPoints[randint(0,len(flatPoints)-1)]
		# Draw a building
		(y,(bID,bData)) = getHeight(heightMap,selectedLocation)
		(z,x) = selectedLocation # This is a relative location from the origin of the image
		x += box.minx # Make it absolute
		z += box.minz # Make it absolute
		#y += box.miny
		plotWidth = RAND.randint(12,32)
		plotHeight = RAND.randint(16,64)
		plotDepth = RAND.randint(12,32)
		print "Let's build a house at",(x,y,z),(plotWidth,plotHeight,plotDepth)
		theBox = BoundingBox((x,y,z),(plotWidth,plotHeight,plotDepth))
		ahouse(level,theBox,options)
		# Remove all points in the building plot from the candidate plots
		for px in xrange(x,x+plotWidth):
			for pz in xrange(z,z+plotDepth):
				if (px,pz) in flatPoints:
					flatPoints.remove((px,pz))
					
				# Fix up any gaps that might exist due to terrain variation. i.e fill to ground.
				dy = y
				keepGoing = True
				while keepGoing and dy >= 0:
					dy -= 1
					(bID,bData) = getBlock(level,px,dy,pz)
					if bID == 0 or bID == 2 or (bID >= 8 and bID <= 11): # Air and grass and water and lava
						setBlock(level,fillMat,px,dy,pz)
					else:
						keepGoing = False # Stop when there's a block that's not replacable.
							
					
					
					
		

def findLocations(img,val):
	'''
		Creates a list of points where the value of the point is the same as specified
	'''
	p = []
	width = img.get_width()
	height = img.get_height()

	pix = pygame.PixelArray(img)
	for x in xrange(0,width):
		for y in xrange(0,height):
			if pix[x,y] == val:
				p.append((x,y))
	img.unlock()
	return p



def findEdges(img):
	width = img.get_width()
	height = img.get_height()
	delta = 16 # This is the number to change to adjust the sensitivity of edge detection. Decrease to increase the possible plot locations to flatter zones.
	deltaHalf = delta >> 1
	imgB = pygame.Surface((width-delta, height-delta),0,8)

	pix = pygame.PixelArray(img)
	pixB = pygame.PixelArray(imgB)
	for x in xrange(deltaHalf,width-deltaHalf):
		for y in xrange(deltaHalf,height-deltaHalf):
			avgDelta = 0
			vr = pix[x,y]
			count = 0
			for dx in xrange(-deltaHalf,deltaHalf+1):
				for dy in xrange(-deltaHalf,deltaHalf+1):
					count += 1
					if not (dx == 0 and dy == 0):
						nr = pix[x+dx,y+dy]
						# print vr,nr
						avgDelta = avgDelta + int(abs(vr-nr))
			avgDelta = avgDelta / count # Divide by 8 through bitshift
			# pixB[x-1,y-1] = avgDelta
			if avgDelta != 0:
				pixB[x-delta,y-delta] = 255

	img.unlock()
	imgB.unlock()
	return imgB	
		
def findEdges2(img): # Not used
	width = img.get_width()
	height = img.get_height()
	imgB = pygame.Surface((width-2, height-2),0,8)

	pix = pygame.PixelArray(img)
	pixB = pygame.PixelArray(imgB)
	for x in xrange(1,width-1):
		for y in xrange(1,height-1):
			avgDelta = 0
			vr = pix[x,y]
			for dx in xrange(-1,2):
				for dy in xrange(-1,2):
					if not (dx == 0 and dy == 0):
						nr = pix[x+dx,y+dy]
						# print vr,nr
						avgDelta = avgDelta + int(abs(vr-nr))
			avgDelta = avgDelta >> 3 # Divide by 8 through bitshift
			# pixB[x-1,y-1] = avgDelta
			if avgDelta != 0:
				pixB[x-1,y-1] = 255
	img.unlock()
	imgB.unlock()
	return imgB	
		
def convertHeightMapToImage(heightMap):
	''' 
		Creates a displayable greyscale image of the height data
	'''
	height = len(heightMap)
	width = len(heightMap[0])
	
	surface = pygame.Surface((width, height),0,8)
	pix = pygame.PixelArray(surface)
	rowIndex = 0
	for row in heightMap:
		colIndex = 0
		for (height, (bID,bData)) in row:
			pix[colIndex,rowIndex] = height
			# surface.set_at((colIndex,rowIndex),height)
			colIndex += 1
		rowIndex += 1
	surface.unlock()
	return surface
		
def getHeight(heightMap,pos):
	(x,z) = pos
	row = heightMap[int(x)]
	height = row[int(z)]
	return height
		
class Plot(object):
	''' Represents a proto-structure. All common code goes here
	'''
	def __init__(self,label):
		self.connections = []
		self.label = label
	
	def connect(self,thing):
		self.connections.append(thing)
	
	def printOut(self):
		self.dump(1)
		
	def dump(self,tier):
		if tier == None:
			tier = 1
		print tier,self.label
		for c in self.connections:
			c.dump(tier+1)
	
	def setLocation(self, level, AHM, location, size, analyseBlocks):
		self.level = level
		self.AHM = AHM
		self.location = location
		self.size = size
		self.analyseBlocks = analyseBlocks
	
class AHouse(Plot):
    def __init__(self):
        super(AHouse,self).__init__("AHouse")

	
class AbodeEntrance(Plot):
    def __init__(self):
        super(AbodeEntrance,self).__init__("AbodeEntrance")

class AbodeLiving(Plot):
    def __init__(self):
        super(AbodeLiving,self).__init__("AbodeLiving")

class AbodeKitchen(Plot):
    def __init__(self):
        super(AbodeKitchen,self).__init__("AbodeKitchen")

class AbodeHall(Plot):
    def __init__(self):
        super(AbodeHall,self).__init__("AbodeHall")

class AbodeBedroom(Plot):
    def __init__(self):
        super(AbodeBedroom,self).__init__("AbodeBedroom")

class Square(Plot):
    def __init__(self):
        super(Square,self).__init__("Square")
		
class Pathway(Plot):
    def __init__(self):
        super(Pathway,self).__init__("Pathway")

def connectEverything(anArray):
	'''
		Pass in an array of Plots and each will have the next Plot connected.
	'''
	for i in xrange(0,len(anArray)-1):
		anArray[i].connect(anArray[i+1])
		
def makeAbodeA():
	'''
		Simple house style consisting of entrance, and then a simple layout with variable rooms
		TODO: Use a seed to randomise
	'''
	newHall = AbodeHall()
	numberOfBedrooms = randint(1,4)
	for i in xrange(0,numberOfBedrooms):
		newHall.connect(AbodeBedroom())
	newAbode = AbodeEntrance()
	
	theHouse = [newAbode,AbodeLiving(),AbodeKitchen(),newHall]
	connectEverything(theHouse) # 
	
	return newAbode

# VOXEL DRAWING PRIMITIVES
def setBlock(level,material,x,y,z):
	(bID,bData) = material
	level.setBlockAt(x,y,z,bID)
	level.setBlockDataAt(x,y,z,bData)

def markerTape(level,box):
	'''
		Draws a wireframe around the selection made of alternating blocks
	'''
	edgeMaterial = (35,15) # Black wool
	fillMaterial = (35,4) # Yellow wool

	for y in xrange(box.miny,box.maxy):
		material = fillMaterial
		if y%2 == 1:
			material = edgeMaterial
		setBlock(level,material,box.minx,y,box.minz)
		setBlock(level,material,box.maxx-1,y,box.minz)
		setBlock(level,material,box.minx,y,box.maxz-1)
		setBlock(level,material,box.maxx-1,y,box.maxz-1)
	
	for x in xrange(box.minx,box.maxx):
		material = fillMaterial
		if x%2 == 1:
			material = edgeMaterial
		setBlock(level,material,x,box.miny,box.minz)
		setBlock(level,material,x,box.maxy-1,box.minz)
		setBlock(level,material,x,box.miny,box.maxz-1)
		setBlock(level,material,x,box.maxy-1,box.maxz-1)
		
	for z in xrange(box.minz,box.maxz):
		material = fillMaterial
		if z%2 == 1:
			material = edgeMaterial
		setBlock(level,material,box.minx,box.miny,z)
		setBlock(level,material,box.maxx-1,box.miny,z)
		setBlock(level,material,box.minx,box.maxy-1,z)
		setBlock(level,material,box.maxx-1,box.maxy-1,z)

# ANALYTICAL METHODS - EXAMINE THE WORLD AND CHARACTERISTICS OF IT

NONSURFACE = [ 0, 17, 18, 31, 37, 38, 78, 175 ] # Block IDs for non-surface blocks. Metadata hints. TBD: Add woods and leaves
DEBUG = False # Turn on for verbose logging to stdout / MCEdit log

def analyse(template):
	results = {}
	for y in xrange(0,template.Height):
		for z in xrange(0,template.Length):
			for x in xrange(0,template.Width):
				(id,data) = getBlock(template,x,y,z)
				if (id,data) in results:
					results[(id,data)] = results[(id,data)]+1
				else:
					results[(id,data)] = 1
	return results

def dumpEntitiesInSelection(level, box,options):
	for (chunk, _, _) in level.getChunkSlices(box):
		print "Entities:"
		for e in chunk.Entities:
			print e
		print "TileEntities:"
		for e in chunk.TileEntities:
			print e

def getMyHeightMap(level, box, options):
	'''
		Iterate through space and explore it
	'''
	print "INFO: Starting to getMyHeightMap()"
	HM = [] # A set of rows
	for z in xrange(box.minz,box.maxz):
		COL = []
		for x in xrange(box.minx,box.maxx):
			(theBlock,theBlockData) = (-1,-1)
			heightHere = -1 # default to 'invalid'/void
			y = box.maxy
			while y >= box.miny: # Examine each 1x1 line, top down
				y -= 1
				theBlock = level.blockAt(x,y,z)
				if theBlock not in NONSURFACE:
					theBlockData = level.blockDataAt(x,y,z)
					heightHere = y
					y = box.miny-1 # or... break
			COL.append((heightHere,(theBlock,theBlockData)))
		HM.append(COL) # Adding the current column of values to the set
	if DEBUG: print "Height Map:\n",HM
	print "INFO: Completed getMyHeightMap()"
	return HM

def generateAggregateHeightMaps(HM):
	'''
	Gathers a set of info about regions together
	'''
	print "INFO: Starting to generateAggregateHeightMaps()"
	DEPTH = len(HM)
	# print HM
	WIDTH = len(HM[0])
	
	AHM = []
	DIM = 4
	keepGoing = True
	while keepGoing:
		if DIM > DEPTH or DIM > WIDTH:
			keepGoing = False
		else:
			CZ = 0
			ROWS = []
			while (CZ+DIM) <= DEPTH:
				COL = []
				CX = 0
				while (CX+DIM) <= WIDTH:
					heightSum = 0
					heightMin = 999999  # Invalid
					heightMax = -999999 # Invalid
					
					analyseBlocks = {} # Analyse Block types
					
					for dz in xrange(0,DIM):
						for dx in xrange(0,DIM):
							HMRow = HM[CZ+dz]
							(heightHere,(bID,bData)) = HMRow[CX+dx]
							if (bID,bData) in analyseBlocks: # Analyse Block types
								analyseBlocks[(bID,bData)] = analyseBlocks[(bID,bData)]+1 # Analyse Block types
							else: # Analyse Block types
								analyseBlocks[(bID,bData)] = 1 # Analyse Block types
							heightSum += heightHere
							if heightHere < heightMin: heightMin = heightHere
							if heightHere > heightMax: heightMax = heightHere
					heightAvg = heightSum/(DIM**2)
					COL.append(((CX,CZ),(heightAvg,heightSum,heightMin,heightMax,heightMax-heightMin),analyseBlocks)) # Sample tuple - including variance
					#print COL
					CX += DIM
				ROWS.append(COL)
				CZ += DIM
			AHM.append((DIM,ROWS))
			DIM += 1 # DIM*2 # Or otherwise double it
	if DEBUG: print "Aggregate Height Maps:\n",AHM
	print "INFO: Completed generateAggregateHeightMaps()"
	return AHM
	
def getPlotSet(AHM,dimension):
	'''
		Extract one of the rows from the aggregate height map so the caller can work with it
	'''
	
	for (dim,rows) in AHM:
		if dimension == dim:
			return rows
	print "WARN: No suitable plot sizes available." # If we get this far we failed to extract a row
	return [] # Failed to find anything of the suitable scale (or larger)

# PLOT HANDLING PRIMITIVES
	
def checkBoundingBoxIntersect(A, B):
	#print 'Checking BB A/B intersection '
	#printBoundingBox(A)
	#printBoundingBox(B)
	# Check for A completely to the left of B. https://github.com/mcedit/pymclevel/blob/master/box.py
	# http://www.toymaker.info/Games/html/3d_collisions.html
	if A.maxx < B.minx:
	    return False
	# Check for A to the right of B
	if A.minx > B.maxx:
	    return False
	# Check for A in front of B
	if A.maxz < B.minz:
	    return False
	# Check for A behind B
	if A.minz > B.maxz:
	    return False
	# Check for A above B
	if A.miny > B.maxy:
	    return False
	# Check for A below B
	if A.maxy < B.miny:
	   return False
	   
	# Collision has occurred
	#print 'Collision occurred'
	return True

def checkForPlotCollisions(A,plots):
	for plot in plots:
		if checkBoundingBoxIntersect(A,BoundingBox(plot.location,plot.size)) == True:
			return True # At least one overlap
	return False # No collision

def selectPlot(level,box,plotType,dimension,dimensionHeight,AHM,plots,HEIGHTDELTA):
	locations = getPlotSet(AHM,dimension)
	#print "LOCATIONS",locations
	if locations != []:
		# Choose a location with appropriate properties
		candidates = []
		for row in locations:
			for loc in row:
				((CX,CZ),(heightAvg,heightSum,heightMin,heightMax,heightDelta),analyseBlocks) = loc
				px = CX+box.minx
				pz = CZ+box.minz
				#print "heightDelta: ",px,",",pz," = ",heightDelta
				if heightDelta <= HEIGHTDELTA: # Not too rough. Any other criteria go here - like check for lava / etc. This is the placement heuristic
					#print px,heightMin,pz,dimension,dimensionHeight,dimension
					if checkForPlotCollisions(BoundingBox((px,heightMin,pz),(dimension,dimensionHeight,dimension)),plots) == False: # Ensure this plot doesn't overlap any already here
						candidates.append(loc)
				
		# Choose a candidate location from the set of valid candidates
		#print "Candidates: ",candidates
		if len(candidates) > 0:
			plot = candidates[randint(0,len(candidates)-1)]
			((CX,CZ),(heightAvg,heightSum,heightMin,heightMax,heightDelta),analyseBlocks) = plot
			px = CX+box.minx
			pz = CZ+box.minz
			return (px,heightMin,pz,analyseBlocks)
			print "Plot",plot
		#else:
		#	print "WARN: Unable to find a plot to place a "+plotType
	else:
		print "WARN: Unable to find a set of plots to evaluate for a "+plotType
	return None

def cosineInterpolate(a, b, x): # http://www.minecraftforum.net/forums/off-topic/computer-science-and-technology/482027-generating-perlin-noise?page=40000
	ft = pi * x
	f = ((1.0 - cos(ft)) * 0.5)
	ret = float(a * (1.0 - f) + b * f)
	return ret

def cnoise(x,y,z):
	# Return the value of interpolated noise at this location
	return float(Random(x+(y<<4)+(z<<8)).random())

def noise(x,y,z):
	ss = 8
	bs = 3
	cx = x >> bs
	cy = y >> bs
	cz = z >> bs

	rdx = float((float(x%ss))/ss)
	rdy = float((float(y%ss))/ss)
	rdz = float((float(z%ss))/ss)
#	print rdx,rdy,rdz
	
	# current noise cell
	P = zeros((2,2,2))
	for iy in xrange(0,2):
		for iz in xrange(0,2):
			for ix in xrange(0,2):
				P[ix,iy,iz] = float(cnoise(cx+ix,cy+iy,cz+iz))
	
	# print P

	dvx1 = cosineInterpolate(P[0,0,0],P[1,0,0],rdx)
	dvx2 = cosineInterpolate(P[0,1,0],P[1,1,0],rdx)
	dvx3 = cosineInterpolate(P[0,0,1],P[1,0,1],rdx)
	dvx4 = cosineInterpolate(P[0,1,1],P[1,1,1],rdx)

	dvz1 = cosineInterpolate(dvx1,dvx3,rdz)
	dvz2 = cosineInterpolate(dvx2,dvx4,rdz)

	n = cosineInterpolate(dvz1,dvz2,rdy)
	
	return n
	
def chooseMaterial(A,R):
	return A[R.randint(0,len(A)-1)]

def interiorFloor(level, box, options, R, type, mFloorMain, mFloorA, mCarpet, mLight):
	# Draw floor
	method = "interiorFloor"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	# A floor is either a continuous block type filling the interior of the bottom layer of the box, or it has a pattern
	# types:
	# -1 - random type
	# 0 - solid
	# 1 - NS beams
	# 2 - EW beams
	# 3 - scattering of additional blocks

	y = box.miny
	if type == -1:
		type = R.randint(0,3) # Max type
	
	beamDist = 1
	if type >= 1 and type <= 2:
		beamDist = R.randint(2,3)
	chance = 0
	if type == 3:
		chance = R.randint(1,30)
	mFloorBeam = chooseMaterial(mFloorA,R)
	
	for z in xrange(box.minz+1,box.maxz-1):
		for x in xrange(box.minx+1,box.maxx-1):
			block = mFloorMain
			if (type == 1 and x%beamDist == 0) or (type == 2 and z%beamDist == 0): # beams
				block = mFloorBeam
			elif type == 3: # random
				if R.randint(1,100) <= chance:
					block = chooseMaterial(mFloorA,R)
			setBlockForced(level, block, x, y, z)
			if (type == 1 and x%beamDist == 0) or (type == 2 and z%beamDist == 0): # roof beams
				setBlockForced(level, block, x, box.maxy-1, z)
	y=box.miny+1
	if R.randint(0,100) > 50: # Carpet
		tm1 = box.minx+1
		tm2 = box.maxx-2
		tm3 = box.minz+1
		tm4 = box.maxz-2
	
		if tm2 > tm1 and tm4 > tm3:
			cx,cz = R.randint(tm1,tm2),R.randint(tm3,tm4)
			cw,cd = R.randint(1,int(centreWidth)),R.randint(1,int(centreDepth))
			if cx-cw >= box.minx+1 and cx+cw <= box.maxx-2 and cz-cd >= box.minz+1 and cz+cd <= box.maxz-2:
				setBlockForced(level,(89,0),cx,box.miny,cz)
				for x in xrange(cx-cw,cx+cw):
					for z in xrange(cz-cd,cz+cd):
						setBlockForced(level, mCarpet, x, y, z)
	
	
	FuncEnd(level,box,options,method)
	
def exteriorWalls(level, box, options, mWall, mBeam, hBeamGap, vBeamGap, chopped):
	# Draw panelled walls on all the faces of the box
	method = "exteriorWalls"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	# This little hack moves the beam positions a little if there is a risk of drawing an entire beam wall. Not perfect, but OK enough
#	if box.minx%hBeamGap == 0:
#		hBeamGap = hBeamGap+1
#	if box.maxx%hBeamGap == 0:
#		hBeamGap = hBeamGap+1
#	if box.minz%hBeamGap == 0:
#		hBeamGap = hBeamGap+1	
#	if box.maxz%hBeamGap == 0:
#		hBeamGap = hBeamGap+1	
	
	
	# This section loops through the box and decides what each block in the box should be based on the beam layout requested
	for y in xrange(box.miny,box.maxy):
		for z in xrange(box.minz,box.maxz):
			for x in xrange(box.minx,box.maxx):
				if x == box.minx or z == box.minz or x == box.maxx-1 or z == box.maxz-1: # Only draw the vertical faces of the box
					# The type of material here is determined by spacial offset from edges
					block = mWall # Assume this is wall, then prove it is not
					if (y == box.miny or y == box.maxy-1) or ((x == box.minx or x == box.maxx-1) and (z == box.minz or z == box.maxz-1)): # True edges
						block = mBeam
					if x%hBeamGap == 0 or z%hBeamGap == 0 or y%vBeamGap == 0:
						block = mBeam
					if chopped == True and ((x == box.minx or x == box.maxx-1) and (z == box.minz or z == box.maxz-1)):
						block = AIR
						
					setBlockForced(level, block, x, y, z)

	FuncEnd(level,box,options,method)

def room(level,box,options, RAND, RANDMAT,mWall,mWallBeam,mFloor,mWindow,mDoor,chopped):
	beamGap = RAND.randint(3,5)
	
	exteriorWalls(level, box, options, mWall, mWallBeam, beamGap, RAND.randint(beamGap,int(beamGap*1.5)),chopped)
#	doors(level,box,options,RAND,mDoor)
	interiorFloor(level, box, options, RAND, -1, mFloor, [(17,RANDMAT.randint(12,15)),(162,RANDMAT.randint(12,13))], (171,RANDMAT.randint(0,15)), (89,0))

def roofNS(level,box,options,RAND,RANDMAT,roofHeight,materialIndex,mWall):
	MAT_ROOF = [ (125,0),(125,2),(125,5) ]	
	mRoof = chooseMaterial(MAT_ROOF,RANDMAT)
	if materialIndex != -1:
		mRoof = MAT_ROOF[materialIndex%len(MAT_ROOF)]

	width = box.maxx-box.minx-1
	centreWidth = width/2
	height = box.maxy-box.miny-1
	depth = box.maxz-box.minz-1

	
	# Curve of the roof
	H = []
	numSegments = RAND.randint(3,8)
	for i in xrange(0,numSegments):
		H.append((RAND.randint(0,2)))
	
	P = []
	P.append((centreWidth,height-H[0],0))
	P.append((centreWidth,height-H[0],0))
	c = 0
	for h in H:
		c = c+1
		if c > 0 and c < len(H)-1:
			P.append((centreWidth,height-h,c*depth/numSegments))
	P.append((centreWidth,height-H[len(H)-1],depth))
	P.append((centreWidth,height-H[len(H)-1],depth))
	#print P
	ROOFLINE = drawLinesSmoothForced(level,box,mRoof,4,P)
	#print ROOFLINE
	
	x1,y1,z1 = -999,-999,-999
	# Render the roof arc
	arc = RAND.randint(0,3)
	for A in ROOFLINE:
		for (x,y,z) in A:
			if x != x1 and y != y1 and z != z1 or 1 != 0:
				# print x,y,z
				P = []
				P.append((0,roofHeight,z-box.minz))
				P.append((0,roofHeight,z-box.minz))
				P.append((centreWidth/2,roofHeight+arc*(height-roofHeight)/4,z-box.minz))
				P.append((x-box.minx,y-box.miny,z-box.minz))
				P.append((x-box.minx,y-box.miny,z-box.minz))
				blocks = drawLinesSmoothForced(level,box,mRoof,4,P)
				c = 0
				for B in blocks:
					for (x2,y2,z2) in B:
						c = c+1
						for iy in xrange(y2+1,box.maxy):
							#print x2,iy,z2
							b = getBlock(level,x2,iy,z2)
							if b not in MAT_ROOF:
								setBlockForced(level,AIR,x2,iy,z2)
						if c == 2:
							for iy in xrange(box.miny+roofHeight,y2):
								setBlock(level,mRoof,x2,iy,z2)

				P = []
				P.append((width,roofHeight,z-box.minz))
				P.append((width,roofHeight,z-box.minz))
				P.append((width-centreWidth/2,roofHeight+arc*(height-roofHeight)/4,z-box.minz))
				P.append((x-box.minx,y-box.miny,z-box.minz))
				P.append((x-box.minx,y-box.miny,z-box.minz))
				blocks = drawLinesSmoothForced(level,box,mRoof,4,P)
				c = 0
				for B in blocks:
					for (x2,y2,z2) in B:
						c = c+1
						for iy in xrange(y2+1,box.maxy):
							#print x2,iy,z2
							b = getBlock(level,x2,iy,z2)
							if b not in MAT_ROOF:
								setBlockForced(level,AIR,x2,iy,z2)
						if c == 2:
							for iy in xrange(box.miny+roofHeight,y2):
								setBlock(level,mRoof,x2,iy,z2)

			x1,y1,z1 = x,y,z # suppress duplicates

def roofEW(level,box,options,RAND,RANDMAT,roofHeight,materialIndex,mWall):
	# MAT_ROOF = [ (5,0), (5,1), (5,2), (5,3), (5,4), (5,5) ]
	MAT_ROOF = [ (125,0),(125,2),(125,5) ]
	mRoof = chooseMaterial(MAT_ROOF,RANDMAT)
	if materialIndex != -1:
		mRoof = MAT_ROOF[materialIndex%len(MAT_ROOF)]

	width = box.maxx-box.minx-1
	centreWidth = width/2
	height = box.maxy-box.miny-1
	depth = box.maxz-box.minz-1
	centreDepth = depth/2

	
	# Curve of the roof
	H = []
	numSegments = RAND.randint(3,8)
	for i in xrange(0,numSegments):
		H.append((RAND.randint(0,2)))
	
	P = []
	P.append((0,height-H[0],centreDepth))
	P.append((0,height-H[0],centreDepth))
	c = 0
	for h in H:
		c = c+1
		if c > 0 and c < len(H)-1:
			P.append((c*width/numSegments,height-h,centreDepth))
	P.append((width,height-H[len(H)-1],centreDepth))
	P.append((width,height-H[len(H)-1],centreDepth))
	#print P
	ROOFLINE = drawLinesSmoothForced(level,box,mRoof,4,P)
	#print ROOFLINE
	
	x1,y1,z1 = -999,-999,-999
	# Render the roof arc
	arc = RAND.randint(0,3)
	for A in ROOFLINE:
		for (x,y,z) in A:
			if x != x1 and y != y1 and z != z1 or 1 != 0:
				# print x,y,z
				P = []
				P.append((x-box.minx,roofHeight,0))
				P.append((x-box.minx,roofHeight,0))
				P.append((x-box.minx,roofHeight+arc*(height-roofHeight)/4,centreDepth/2))
				P.append((x-box.minx,y-box.miny,z-box.minz))
				P.append((x-box.minx,y-box.miny,z-box.minz))
				blocks = drawLinesSmoothForced(level,box,mRoof,4,P)
				c = 0
				for B in blocks:
					for (x2,y2,z2) in B:
						c = c +1
						for iy in xrange(y2+1,box.maxy):
							#print x2,iy,z2
							b = getBlock(level,x2,iy,z2)
							if b not in MAT_ROOF: # or iy > y2+1:
								setBlockForced(level,AIR,x2,iy,z2)
						if c == 2:
							for iy in xrange(box.miny+roofHeight,y2):
								setBlock(level,mRoof,x2,iy,z2)
				P = []
				P.append((x-box.minx,roofHeight,depth))
				P.append((x-box.minx,roofHeight,depth))
				P.append((x-box.minx,roofHeight+arc*(height-roofHeight)/4,depth-centreDepth/2))
				P.append((x-box.minx,y-box.miny,z-box.minz))
				P.append((x-box.minx,y-box.miny,z-box.minz))
				blocks = drawLinesSmoothForced(level,box,mRoof,4,P)
				c = 0
				for B in blocks:
					for (x2,y2,z2) in B:
						c = c +1
						for iy in xrange(y2+1,box.maxy):
							#print x2,iy,z2
							b = getBlock(level,x2,iy,z2)
							if b not in MAT_ROOF:
								setBlockForced(level,AIR,x2,iy,z2)
						if c == 2:
							for iy in xrange(box.miny+roofHeight,y2):
								setBlock(level,mRoof,x2,iy,z2)

			x1,y1,z1 = x,y,z # suppress duplicates

def chimney(level,box,options,RAND,p):
	(x,y,z) = p # Fireplace location
	dist = RAND.randint(0,2)
	setBlockForced(level, (44,5),x,box.maxy-dist-1,z)
	setBlockForced(level, (145,2),x,box.maxy-dist-2,z)
	setBlockForced(level, (98,3),x,box.maxy-dist-3,z)
	setBlockForced(level, (98,0),x,box.maxy-dist-4,z)
	setBlockForced(level, (4,0),x,box.maxy-dist-5,z)
	for iy in xrange(y,box.maxy-dist-5):
		if RAND.randint(1,100) > 50:
			setBlockForced(level, (4,0),x,iy,z)
		else:
			setBlockForced(level, (98,0),x,iy,z)

def doors(level,box,options,RAND,mDoor):
	# create doors 
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	(b,d) = mDoor
#	doorBox = BoundingBox((1,2,1))
#	EWdoorSchem = MCSchematic((1,2,1))
#	setBlock(EWdoorSchem,(b,0),0,0,0)
#	setBlock(EWdoorSchem,(b,8),0,1,0)

#	NSdoorSchem = MCSchematic((1,2,1))
#	setBlock(NSdoorSchem,(b,1),0,0,0)
#	setBlock(NSdoorSchem,(b,9),0,1,0)

	if width >= 3:
		pos = RAND.randint(1,width-2)
		if getBlock(level,box.minx+pos-1, box.miny+1, box.minz) != AIR and getBlock(level,box.minx+pos+1, box.miny+1, box.minz) != AIR:
			setBlockForced(level,(b,1),box.minx+pos, box.miny+1, box.minz)
			setBlockForced(level,(b,9),box.minx+pos, box.miny+2, box.minz)
		pos = RAND.randint(1,width-2)
		if getBlock(level,box.minx+pos-1, box.miny+1, box.minz) != AIR and getBlock(level,box.minx+pos+1, box.miny+1, box.minz) != AIR:
			setBlockForced(level,(b,3),box.minx+pos, box.miny+1, box.maxz-1)
			setBlockForced(level,(b,11),box.minx+pos, box.miny+2, box.maxz-1)
		print box.minx+pos, box.miny+1, box.maxz-1
		#level.copyBlocksFrom(EWdoorSchem, doorBox, (box.minx+pos, box.miny+1, box.maxz-1))
	if depth >= 3:
		pos = RAND.randint(1,depth-2)
		if getBlock(level,box.minx, box.miny+1, box.minz+pos-1) != AIR and getBlock(level,box.minx, box.miny+1, box.minz+pos+1) != AIR:
			setBlockForced(level,(b,0),box.minx, box.miny+1, box.minz+pos)
			setBlockForced(level,(b,8),box.minx, box.miny+2, box.minz+pos)
#		level.copyBlocksFrom(NSdoorSchem, doorBox, (box.minx, box.miny+1, box.minz+pos))
		pos = RAND.randint(1,depth-2)
		if getBlock(level,box.minx, box.miny+1, box.minz+pos-1) != AIR and getBlock(level,box.minx, box.miny+1, box.minz+pos+1) != AIR:
			setBlockForced(level,(b,2),box.maxx-1, box.miny+1, box.minz+pos)
			setBlockForced(level,(b,10),box.maxx-1, box.miny+2, box.minz+pos)
#		level.copyBlocksFrom(NSdoorSchem, doorBox, (box.maxx-1, box.miny+1, box.minz+pos))

def stairs(level,box,options,RAND,RANDMAT):
	MAT_STAIRS = [ (53,0),  (134,0), (135,0)] # (67,0), (108,0), (109, 0), (114,0), (128,0), (164,0)
	(b,d) = chooseMaterial(MAT_STAIRS,RANDMAT)
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	
	dir = RAND.randint(0,3)

	if box.maxx-4 > box.minx+3 and box.maxz-4 > box.minz+3:
		x = box.minx+RAND.randint(box.minx+3,box.maxx-4)
		y = box.miny+1
		z = box.minz+RAND.randint(box.minz+3,box.maxz-4)
		for y in xrange(y,box.maxy):
			setBlockForced(level, (b,dir), x,y,z)
			if dir == 0:
				x = x+1
			if dir == 1:
				x = x-1
			if dir == 2:
				z = z+1
			if dir == 3:
				z = z-1
				
			if x == box.maxx-3:
				dir = 2
				x = x-1
				z = z+1
			if x == box.minx+2:
				dir = 3
				x = x+1
				z = z-1
			if z == box.maxz-3:
				dir = 1
				x = x-1
				z = z-1
			if z == box.minz+2:
				dir = 0
				x = x+1
				z = z+1
				
			for iy in xrange(y+1,y+5):
				setBlockForced(level,AIR,x,iy,z) # Clear out the headspace
			iy = y+1
			keepGoing = True
			if RAND.randint(1,100) > 50:
				keepGoing = False
			while keepGoing == True:
				block = getBlock(level,x,iy,z)
				if block == AIR:
					setBlock(level,(85,0),x,iy,z) # Fence post
				else:
					keepGoing = False
				iy=iy-1
				if iy < box.miny:
					keepGoing = False
			
			for iy in xrange(y+1,y+5):
				setBlockForced(level,AIR,x,iy,z) # Clear out the headspace

def placePorch(level,box,options,RAND,RANDMAT,mDoor):
	MAT_PORCH = [ (126,0),(126,1),(126,2) ] #(44,0),(44,1),(44,2),(44,3),(44,4),(44,5),(44,6),(44,7),(126,0),(126,1),(126,2),(126,3),(126,4),(126,5),(126,6),(182,0)]
	(br,dr) = mDoor
	y = box.miny
	for z in xrange(box.minz,box.maxz):
		for x in xrange(box.minx,box.maxx):
			# Find all the doors
			(b,d) = getBlock(level,x,y+1,z)
			if b == br: # A match - there is a door
				block = getBlock(level,x-1,y,z)
				if block == AIR: # Build a little step up
					setBlock(level,chooseMaterial(MAT_PORCH,RANDMAT),x-1,y,z)
				block = getBlock(level,x+1,y,z)
				if block == AIR: # Build a little step up
					setBlock(level,chooseMaterial(MAT_PORCH,RANDMAT),x+1,y,z)
				block = getBlock(level,x,y,z+1)
				if block == AIR: # Build a little step up
					setBlock(level,chooseMaterial(MAT_PORCH,RANDMAT),x,y,z+1)
				block = getBlock(level,x,y,z-1)
				if block == AIR: # Build a little step up
					setBlock(level,chooseMaterial(MAT_PORCH,RANDMAT),x,y,z-1)

def placeWindows(level,box,options,RAND,RANDMAT,FLOORHEIGHT,mWindow,mWall,mWallBeam,mDoor):
	MAT_PORCH = [ (44,10),(126,8),(126,9),(126,10),(126,13)]
	mPorch = chooseMaterial(MAT_PORCH,RANDMAT)
	# scan from each face of the selection box, using the projection method, and place windows.
	height = box.maxy-box.miny
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	(bd,dd) = mDoor
	NUMFLOORS = int(height/FLOORHEIGHT)
	for i in xrange(0,NUMFLOORS):
		type = RAND.randint(1,2) # Types of Windows - (1) is a glass pane (2) has a window sill projecting out.
		# For each floor, place windows in the structure
		for iter in xrange(0,RAND.randint(1,2)): # Number of window placement attempts
			by = box.miny+2+i*FLOORHEIGHT # Windows height
			# Front face -x
			if int(width/4) > 2:
				pos = randint(2,int(width/4)) # Position of the Window from either end of the 'width' edge
				hsz = RAND.randint(1,2)
				vsz = RAND.randint(1,2)
				z = box.minz
				# find plane
				keepGoing = True
				while keepGoing:
					if getBlock(level, box.minx+pos, box.miny+i*FLOORHEIGHT+2, z) != AIR:
						keepGoing = False
					else:
						z = z+1
					if z >= box.maxz:
						keepGoing = False
				
				if z < box.maxz:
					for x in xrange(box.minx+pos,box.minx+pos+hsz):
						for y in xrange(by,by+vsz):
							if type >= 1 and RAND.randint(1,100) > 30: # embed glass
								(b,d) = getBlock(level,x,y,z)
								if (b,d) != AIR and b != bd and (getBlock(level,x+1,y,z) != AIR or getBlock(level,x-1,y,z) != AIR or getBlock(level,x,y,z+1) != AIR or getBlock(level,x,y,z-1) != AIR): # Not air nor a door
									setBlockForced(level,mWindow,x,y,z)
						# Place something under the window
						if type == 2:
							(bw,dw) = getBlock(level,x,by-1,z-1)
							(b,d) = getBlock(level,x,by,z)
							if (b,d) == mWindow and (bw,dw) == AIR: # Not air nor a door
								setBlockForced(level,mPorch,x,by-1,z-1)
						
					for x in xrange(box.maxx-1-pos-hsz,box.maxx-1-pos):
						for y in xrange(by,by+vsz):
							if type >= 1 and RAND.randint(1,100) > 30: # embed glass
								(b,d) = getBlock(level,x,y,z)
								if (b,d) != AIR and b != bd and (getBlock(level,x+1,y,z) != AIR or getBlock(level,x-1,y,z) != AIR or getBlock(level,x,y,z+1) != AIR or getBlock(level,x,y,z-1) != AIR): # Not air nor a door
									setBlockForced(level,mWindow,x,y,z)
						# Place something under the window
						if type == 2:
							(bw,dw) = getBlock(level,x,by-1,z-1)
							(b,d) = getBlock(level,x,by,z)
							if (b,d) == mWindow and (bw,dw) == AIR: # Not air nor a door
								setBlockForced(level,mPorch,x,by-1,z-1)

				# Back face +x
				pos = randint(2,int(width/4)) # Position of the Window from either end of the 'width' edge
				hsz = RAND.randint(1,2)
				vsz = RAND.randint(1,2)
				z = box.maxz-1
				# find plane
				keepGoing = True
				while keepGoing:
					if getBlock(level, box.minx+pos, box.miny+i*FLOORHEIGHT+2, z) != AIR:
						keepGoing = False
					else:
						z = z-1
					if z < box.minz:
						keepGoing = False
				
				if z >= box.minz:
					for x in xrange(box.minx+pos,box.minx+pos+hsz):
						for y in xrange(by,by+vsz):
							if type >= 1 and RAND.randint(1,100) > 30: # embed glass
								(b,d) = getBlock(level,x,y,z)
								if (b,d) != AIR and b != bd and (getBlock(level,x+1,y,z) != AIR or getBlock(level,x-1,y,z) != AIR or getBlock(level,x,y,z+1) != AIR or getBlock(level,x,y,z-1) != AIR): # Not air nor a door
									setBlockForced(level,mWindow,x,y,z)
						# Place something under the window
						if type == 2:
							(bw,dw) = getBlock(level,x,by-1,z+1)
							(b,d) = getBlock(level,x,by,z)
							if (b,d) == mWindow and (bw,dw) == AIR: # Not air nor a door
								setBlockForced(level,mPorch,x,by-1,z+1)
									
					for x in xrange(box.maxx-1-pos-hsz,box.maxx-1-pos):
						for y in xrange(by,by+vsz):
							if type >= 1 and RAND.randint(1,100) > 30: # embed glass
								(b,d) = getBlock(level,x,y,z)
								if (b,d) != AIR and b != bd and (getBlock(level,x+1,y,z) != AIR or getBlock(level,x-1,y,z) != AIR or getBlock(level,x,y,z+1) != AIR or getBlock(level,x,y,z-1) != AIR): # Not air nor a door
									setBlockForced(level,mWindow,x,y,z)
						# Place something under the window
						if type == 2:
							(bw,dw) = getBlock(level,x,by-1,z+1)
							(b,d) = getBlock(level,x,by,z)
							if (b,d) == mWindow and (bw,dw) == AIR: # Not air nor a door
								setBlockForced(level,mPorch,x,by-1,z+1)

				# Side face +z
				pos = randint(2,int(width/4)) # Position of the Window from either end of the 'width' edge
				hsz = RAND.randint(1,2)
				vsz = RAND.randint(1,2)
				x = box.maxx-1
				# find plane
				keepGoing = True
				while keepGoing:
					if getBlock(level, x, box.miny+i*FLOORHEIGHT+2, box.minz+pos) != AIR:
						keepGoing = False
					else:
						x = x-1
					if x < box.minx:
						keepGoing = False
				
				if x >= box.minx:
					for z in xrange(box.minz+pos,box.minz+pos+hsz):
						for y in xrange(by,by+vsz):
							if type >= 1 and RAND.randint(1,100) > 30: # embed glass
								(b,d) = getBlock(level,x,y,z)
								if (b,d) != AIR and b != bd and (getBlock(level,x+1,y,z) != AIR or getBlock(level,x-1,y,z) != AIR or getBlock(level,x,y,z+1) != AIR or getBlock(level,x,y,z-1) != AIR): # Not air nor a door
									setBlockForced(level,mWindow,x,y,z)
						# Place something under the window
						if type == 2:
							(bw,dw) = getBlock(level,x+1,by-1,z)
							(b,d) = getBlock(level,x,by,z)
							if (b,d) == mWindow and (bw,dw) == AIR: # Not air nor a door
								setBlockForced(level,mPorch,x+1,by-1,z)
									
					for z in xrange(box.maxz-1-pos-hsz,box.maxz-1-pos):
						for y in xrange(by,by+vsz):
							if type >= 1 and RAND.randint(1,100) > 30: # embed glass
								(b,d) = getBlock(level,x,y,z)
								if (b,d) != AIR and b != bd and (getBlock(level,x+1,y,z) != AIR or getBlock(level,x-1,y,z) != AIR or getBlock(level,x,y,z+1) != AIR or getBlock(level,x,y,z-1) != AIR): # Not air nor a door
									setBlockForced(level,mWindow,x,y,z)
						# Place something under the window
						if type == 2:
							(bw,dw) = getBlock(level,x+1,by-1,z)
							(b,d) = getBlock(level,x,by,z)
							if (b,d) == mWindow and (bw,dw) == AIR: # Not air nor a door
								setBlockForced(level,mPorch,x+1,by-1,z)						

				# Side face -z
				pos = randint(2,int(width/4)) # Position of the Window from either end of the 'width' edge
				hsz = RAND.randint(1,2)
				vsz = RAND.randint(1,2)
				x = box.minx
				# find plane
				keepGoing = True
				while keepGoing:
					if getBlock(level, x, box.miny+i*FLOORHEIGHT+2, box.minz+pos) != AIR:
						keepGoing = False
					else:
						x = x+1
					if x >= box.maxx:
						keepGoing = False
				
				if x < box.maxx:
					for z in xrange(box.minz+pos,box.minz+pos+hsz):
						for y in xrange(by,by+vsz):
							if type >= 1 and RAND.randint(1,100) > 30: # embed glass
								(b,d) = getBlock(level,x,y,z)
								if (b,d) != AIR and b != bd and (getBlock(level,x+1,y,z) != AIR or getBlock(level,x-1,y,z) != AIR or getBlock(level,x,y,z+1) != AIR or getBlock(level,x,y,z-1) != AIR) : # Not air nor a door
									setBlockForced(level,mWindow,x,y,z)
						# Place something under the window
						if type == 2:
							(bw,dw) = getBlock(level,x-1,by-1,z)
							(b,d) = getBlock(level,x,by,z)
							if (b,d) == mWindow and (bw,dw) == AIR: # Not air nor a door
								setBlockForced(level,mPorch,x-1,by-1,z)
									
					for z in xrange(box.maxz-1-pos-hsz,box.maxz-1-pos):
						for y in xrange(by,by+vsz):
							if type == 1 and RAND.randint(1,100) > 30: # embed glass
								(b,d) = getBlock(level,x,y,z)
								if (b,d) != AIR and b != bd and (getBlock(level,x+1,y,z) != AIR or getBlock(level,x-1,y,z) != AIR or getBlock(level,x,y,z+1) != AIR or getBlock(level,x,y,z-1) != AIR): # Not air nor a door
									setBlockForced(level,mWindow,x,y,z)
						# Place something under the window
						if type == 2:
							(bw,dw) = getBlock(level,x-1,by-1,z)
							(b,d) = getBlock(level,x,by,z)
							if (b,d) == mWindow and (bw,dw) == AIR: # Not air nor a door
								setBlockForced(level,mPorch,x-1,by-1,z)		
							
		# Optional planter box.
					
def ahouse(level0,box0,options):
	# Init and log
	method = "AHouse"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level0,box0,options,method) # Log start
	
	SAVE = True
	
	level = MCSchematic((width,height,depth))
	box = BoundingBox((0,0,0),(width,height,depth))
	
	# A house has a number of levels and an interior and exterior. There is a roof.
	# The exterior has windows, doors, balconies, planter boxes, signs, banners, etc. Materials may differ by level
	# The roof may be of various block type construction and is typically pitched. A chimney appears!
	# Even where the face of the house is sloping 

	# Random seeded generators
	(RAND,SEED) = getRandFromSeed(options)
	(RANDMAT,SEEDMAT) = getRandFromSeed(options)
	
	# House geometry/structure
	FLOORHEIGHT = RAND.randint(4,8) 
	NUMFLOORS = int(height/FLOORHEIGHT)
	ROOFLEVELS = 1
	if int(NUMFLOORS/2) > 1:
		ROOFLEVELS = RAND.randint(2,int(NUMFLOORS/2)) # How many levels are devoted to the roofline.
	RECESS = 1 # RAND.randint(1,2)

	# Pallette
	MAT_WALL_EXT = [ (35,0), (35,8),(172,0), (45,0), (82,0), (43,9), (5,2), (5,1)]
	MAT_WALL_EXT2 = [ (35,0), (35,8),(172,0), (45,0), (82,0), (43,9), (5,2), (5,1)]
	MAT_WALL_BEAM = [ (5,5), (5,3),(17,12),(17,13),(17,15), (162,12),(162,13) ]
	MAT_WINDOW = [ (160,8), (160,0), (160,7), (95,8), (95,0) ]
	MAT_FLOOR = [ (5,0), (5,2), (5,3)]
	MAT_DOOR = [ (193,1), (193,3) ]

	# Choose material palette
	mWall = chooseMaterial(MAT_WALL_EXT,RANDMAT)
	mWallBeam = chooseMaterial(MAT_WALL_BEAM,RANDMAT)
	mFloor = chooseMaterial(MAT_FLOOR,RANDMAT)
	mWindow = chooseMaterial(MAT_WINDOW,RANDMAT)
	mDoor = chooseMaterial(MAT_DOOR,RANDMAT)
	oWall = mWall
	
	chopped = True # I have to hand the house geometry into the child procedures for consistency
	for i in xrange(0,NUMFLOORS):
		roomBox = BoundingBox((box.minx+RECESS,box.miny+i*FLOORHEIGHT,box.minz+RECESS),(width-2*RECESS,FLOORHEIGHT,depth-2*RECESS))
		if i == 0: # Ground floor
			if RAND.randint(1,100) >80: # Cobblestone
				mWall = (4,0)
			roomBox = BoundingBox((box.minx+int(RECESS*1.5),box.miny+i*FLOORHEIGHT,box.minz+int(RECESS*1.5)),(width-2*int(RECESS*1.5),FLOORHEIGHT,depth-2*int(RECESS*1.5)))
			mWall = oWall
		if i == 1: # First floor
			if RAND.randint(1,100) > 70: # Randomise wall material?
				mWall = chooseMaterial(MAT_WALL_EXT,RANDMAT)
		if RAND.randint(1,100) > 50:
			chopped = False
		if i == 0 and RAND.randint(1,100) > 50:
			# Special collection of rooms instead of one room only
			for j in xrange(0,RAND.randint(2,5)):
				px = RAND.randint(RECESS,RECESS+int(centreWidth))
				pz = RAND.randint(RECESS,RECESS+int(centreDepth))
				pxd = width-RECESS-px
				pzd = depth-RECESS-pz
				(r,rs1) = getRandFromSeed(options)
				roomBox = BoundingBox((box.minx+px,box.miny+i*FLOORHEIGHT,box.minz+pz),
										(RAND.randint(int(pxd/2),pxd),FLOORHEIGHT,RAND.randint(int(pzd/2),pzd)))
				room(level,roomBox,options,RAND,r,mWall,mWallBeam,mFloor,mWindow,mDoor,chopped)
				doors(level,roomBox,options,RAND,mDoor)
			# Struts
			for y in xrange(box.miny+i*FLOORHEIGHT,box.miny+(i+1)*FLOORHEIGHT):
				setBlockForced(level,mWallBeam,box.minx+2,y,box.minz+2)
				setBlockForced(level,mWallBeam,box.maxx-3,y,box.maxz-3)
				setBlockForced(level,mWallBeam,box.minx+2,y,box.maxz-3)
				setBlockForced(level,mWallBeam,box.maxx-3,y,box.minz+2)
				
		else: # One box only
			(r,rs1) = getRandFromSeed(options)
			room(level,roomBox,options,RAND,r,mWall,mWallBeam,mFloor,mWindow,mDoor,chopped)
			if i == 0:
				doors(level,roomBox,options,RAND,mDoor)
	stairs(level,box,options,RAND,RANDMAT)

	# Detail
	
	# -- Door detail
	placePorch(level,box,options,RAND,RANDMAT,mDoor)
	
	# -- Windows
	placeWindows(level,box,options,RAND,RANDMAT,FLOORHEIGHT,mWindow,mWall,mWallBeam,mDoor)
	
	# Roof(s) - size and shape can be tuned through parameters. Some extreme A-frame high fantasy roofs can occur in the initial version of this generator
	
	roofMaterial = RANDMAT.randint(0,10)
	if depth > width:
		roofNS(level,box,options,RAND,RANDMAT,height-ROOFLEVELS*FLOORHEIGHT,roofMaterial,mWall)
		if RAND.randint(1,100) > 50:
			roofEW(level,box,options,RAND,RANDMAT,height-ROOFLEVELS*FLOORHEIGHT,roofMaterial,mWall)
	else:
		roofEW(level,box,options,RAND,RANDMAT,height-ROOFLEVELS*FLOORHEIGHT,roofMaterial,mWall)
		if RAND.randint(1,100) > 50:
			roofNS(level,box,options,RAND,RANDMAT,height-ROOFLEVELS*FLOORHEIGHT,roofMaterial,mWall)
	if RAND.randint(1,100) > 5:
		if box.maxx-4 > box.minx+3 and box.maxz-4 > box.minz+3:
			chimney(level,box,options,RAND,(RAND.randint(box.minx+3,box.maxx-4),box.miny,RAND.randint(box.minz+3,box.maxz-4)))
		
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level0.copyBlocksFrom(level, box, (box0.minx, box0.miny, box0.minz ),b)
	#level0.markDirtyBox(box0)

	if SAVE == True:
		fn = 'AB_MHOUSE_'+str(SEED)+'.schematic'
		level.saveToFile(filename=fn)
		print "Saved to file "+fn
	
	# End / log
	FuncEnd(level,box,options,method)
	
	return level # Pass back the house for the caller to cache

def ahouseSteps(level0,box0,options,step):
	# Init and log
	method = "AHouse"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level0,box0,options,method) # Log start
	
	SAVE = True
	
	level = MCSchematic((width,height,depth))
	box = BoundingBox((0,0,0),(width,height,depth))
	
	# A house has a number of levels and an interior and exterior. There is a roof.
	# The exterior has windows, doors, balconies, planter boxes, signs, banners, etc. Materials may differ by level
	# The roof may be of various block type construction and is typically pitched. A chimney appears!
	# Even where the face of the house is sloping 

	# Random seeded generators
	(RAND,SEED) = getRandFromSeed(options)
	(RANDMAT,SEEDMAT) = getRandFromSeed(options)
	
	# House geometry/structure
	FLOORHEIGHT = RAND.randint(4,8) 
	NUMFLOORS = int(height/FLOORHEIGHT)
	ROOFLEVELS = 1
	if int(NUMFLOORS/2) > 1:
		ROOFLEVELS = RAND.randint(2,int(NUMFLOORS/2)) # How many levels are devoted to the roofline.
	RECESS = 1 # RAND.randint(1,2)

	# Pallette
	MAT_WALL_EXT = [ (35,0), (35,8),(172,0), (45,0), (82,0), (43,9), (5,2), (5,1)]
	MAT_WALL_EXT2 = [ (35,0), (35,8),(172,0), (45,0), (82,0), (43,9), (5,2), (5,1)]
	MAT_WALL_BEAM = [ (5,5), (5,3),(17,12),(17,13),(17,15), (162,12),(162,13) ]
	MAT_WINDOW = [ (160,8), (160,0), (160,7), (95,8), (95,0) ]
	MAT_FLOOR = [ (5,0), (5,2), (5,3)]
	MAT_DOOR = [ (193,1), (193,3) ]

	# Choose material palette
	mWall = chooseMaterial(MAT_WALL_EXT,RANDMAT)
	mWallBeam = chooseMaterial(MAT_WALL_BEAM,RANDMAT)
	mFloor = chooseMaterial(MAT_FLOOR,RANDMAT)
	mWindow = chooseMaterial(MAT_WINDOW,RANDMAT)
	mDoor = chooseMaterial(MAT_DOOR,RANDMAT)
	oWall = mWall
	
	chopped = True # I have to hand the house geometry into the child procedures for consistency
	for i in xrange(0,NUMFLOORS):
		roomBox = BoundingBox((box.minx+RECESS,box.miny+i*FLOORHEIGHT,box.minz+RECESS),(width-2*RECESS,FLOORHEIGHT,depth-2*RECESS))
		if i == 0: # Ground floor
			if RAND.randint(1,100) >80: # Cobblestone
				mWall = (4,0)
			roomBox = BoundingBox((box.minx+int(RECESS*1.5),box.miny+i*FLOORHEIGHT,box.minz+int(RECESS*1.5)),(width-2*int(RECESS*1.5),FLOORHEIGHT,depth-2*int(RECESS*1.5)))
			mWall = oWall
		if i == 1: # First floor
			if RAND.randint(1,100) > 70: # Randomise wall material?
				mWall = chooseMaterial(MAT_WALL_EXT,RANDMAT)
		if RAND.randint(1,100) > 50:
			chopped = False
		if i == 0 and RAND.randint(1,100) > 50:
			# Special collection of rooms instead of one room only
			for j in xrange(0,RAND.randint(2,5)):
				px = RAND.randint(RECESS,RECESS+int(centreWidth))
				pz = RAND.randint(RECESS,RECESS+int(centreDepth))
				pxd = width-RECESS-px
				pzd = depth-RECESS-pz
				(r,rs1) = getRandFromSeed(options)
				roomBox = BoundingBox((box.minx+px,box.miny+i*FLOORHEIGHT,box.minz+pz),
										(RAND.randint(int(pxd/2),pxd),FLOORHEIGHT,RAND.randint(int(pzd/2),pzd)))
				room(level,roomBox,options,RAND,r,mWall,mWallBeam,mFloor,mWindow,mDoor,chopped)
				doors(level,roomBox,options,RAND,mDoor)
			# Struts
			for y in xrange(box.miny+i*FLOORHEIGHT,box.miny+(i+1)*FLOORHEIGHT):
				setBlockForced(level,mWallBeam,box.minx+2,y,box.minz+2)
				setBlockForced(level,mWallBeam,box.maxx-3,y,box.maxz-3)
				setBlockForced(level,mWallBeam,box.minx+2,y,box.maxz-3)
				setBlockForced(level,mWallBeam,box.maxx-3,y,box.minz+2)
				
		else: # One box only
			(r,rs1) = getRandFromSeed(options)
			room(level,roomBox,options,RAND,r,mWall,mWallBeam,mFloor,mWindow,mDoor,chopped)
			if i == 0:
				doors(level,roomBox,options,RAND,mDoor)
	
	if step == 0 or step > 1:
		stairs(level,box,options,RAND,RANDMAT)

	# Detail
	
	# -- Door detail
	if step == 0 or step > 2:
		placePorch(level,box,options,RAND,RANDMAT,mDoor)
	
	# -- Windows
	if step == 0 or step > 3:
		placeWindows(level,box,options,RAND,RANDMAT,FLOORHEIGHT,mWindow,mWall,mWallBeam,mDoor)
	
	# Roof(s) - size and shape can be tuned through parameters. Some extreme A-frame high fantasy roofs can occur in the initial version of this generator
	
	if step == 0 or step > 4:
		roofMaterial = RANDMAT.randint(0,10)
		if depth > width:
			roofNS(level,box,options,RAND,RANDMAT,height-ROOFLEVELS*FLOORHEIGHT,roofMaterial,mWall)
			if RAND.randint(1,100) > 50:
				roofEW(level,box,options,RAND,RANDMAT,height-ROOFLEVELS*FLOORHEIGHT,roofMaterial,mWall)
		else:
			roofEW(level,box,options,RAND,RANDMAT,height-ROOFLEVELS*FLOORHEIGHT,roofMaterial,mWall)
			if RAND.randint(1,100) > 50:
				roofNS(level,box,options,RAND,RANDMAT,height-ROOFLEVELS*FLOORHEIGHT,roofMaterial,mWall)
		if RAND.randint(1,100) > 5:
			if box.maxx-4 > box.minx+3 and box.maxz-4 > box.minz+3:
				chimney(level,box,options,RAND,(RAND.randint(box.minx+3,box.maxx-4),box.miny,RAND.randint(box.minz+3,box.maxz-4)))
		
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level0.copyBlocksFrom(level, box, (box0.minx, box0.miny, box0.minz ),b)
	#level0.markDirtyBox(box0)

	if SAVE == True:
		fn = 'AB_MHOUSE_'+str(SEED)+'.schematic'
		level.saveToFile(filename=fn)
		print "Saved to file "+fn
	
	# End / log
	FuncEnd(level,box,options,method)
	
	return level # Pass back the house for the caller to cache
	
	
def neighbourhoodSquare(level,box,options,refSchem):
	# first face
	bPLOT = (57,0) #getBlockFromOptions(options,"Plot Material:")
	refBox = BoundingBox((refSchem.Width,refSchem.Height,refSchem.Length))
	
#	for y in xrange(refBox.miny,refBox.maxy):
#		for z in xrange(refBox.minz,refBox.maxz):
#			for x in xrange(refBox.minx,refBox.maxx):
#				print getBlock(refSchem,x,y,z)
	refX = 0
	refY = 0
	refZ = 0
	
	FLANGE = 7
	CORNER = 16
	
	for x in xrange(box.minx+CORNER, box.maxx-CORNER):
		if x%100 == 0:
			print x
		z = box.minz
		refZ = 0
		keepGoing = True
		while keepGoing == True and z < box.maxz:
			# project into the plot from the edges. Find the entire connected shape. This is where we'll re-map the schematic
			block = getBlock(level,x,box.miny,z)
			if block == bPLOT:
				y = box.miny
				# Found the edge of the plot
				#keepGoing = False
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					if sourceBlock != AIR:
						setBlockForced(level,sourceBlock,x,y+1,z-FLANGE) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset
					keepGoing = False # Exit and look at the next x
			z = z+1
		refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge

		
		
		
		
	for z in xrange(box.minz+CORNER, box.maxz-CORNER):
		if z%100 == 0:
			print z
		x = box.maxx-1
		refZ = 0
		keepGoing = True
		while keepGoing == True and x >= box.minx:
			# project into the plot from the edges. Find the entire connected shape. This is where we'll re-map the schematic
			block = getBlock(level,x,box.miny,z)
			if block == bPLOT:
				y = box.miny
				# Found the edge of the plot
				#keepGoing = False
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					if sourceBlock != AIR:
						setBlockForced(level,sourceBlock,x+FLANGE,y+1,z) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset
					keepGoing = False # Exit and look at the next x
			x = x-1
		refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge	

	x = box.maxx-CORNER
	while x >= box.minx+CORNER:
		if x%100 == 0:
			print x
		z = box.maxz
		refZ = 0
		keepGoing = True
		while keepGoing == True and z >= box.minz:
			# project into the plot from the edges. Find the entire connected shape. This is where we'll re-map the schematic
			block = getBlock(level,x,box.miny,z)
			if block == bPLOT:
				y = box.miny
				# Found the edge of the plot
				#keepGoing = False
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					if sourceBlock != AIR:
						setBlockForced(level,sourceBlock,x,y+1,z+FLANGE) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset
					keepGoing = False # Exit and look at the next x
			z = z-1
		refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
		x = x-1

	z = box.maxz-CORNER
	while z >= box.minz+CORNER:
		if z%100 == 0:
			print z
		x = box.minx-1
		refZ = 0
		keepGoing = True
		while keepGoing == True and x < box.maxx:
			# project into the plot from the edges. Find the entire connected shape. This is where we'll re-map the schematic
			block = getBlock(level,x,box.miny,z)
			if block == bPLOT:
				y = box.miny
				# Found the edge of the plot
				#keepGoing = False
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					if sourceBlock != AIR:
						setBlockForced(level,sourceBlock,x-FLANGE,y+1,z) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset
					keepGoing = False # Exit and look at the next x
			x = x+1
		refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
		z = z-1

def fillAIR(level,box,options,dir):
	P = []
	(x,y,z) = (box.minx,box.miny,box.minz)
	if dir == "MAX":
		(x,y,z) = (box.maxx-1,box.maxy-1,box.maxz-1)
	mat = getBlock(level,x,y,z)
	P.append((x,y,z))
	count = 100000
	while len(P) > 0 and count > 0:
		(x,y,z) = P.pop()
		count = count-1
		block = getBlock(level,x,y,z)
		if block == mat:
			P.append((x,y,z+1))
			P.append((x,y+1,z))
			P.append((x+1,y,z))
			P.append((x,y,z-1))
			P.append((x,y-1,z))
			P.append((x-1,y,z))
			setBlockForced(level,AIR,x,y,z)
	
		
def neighbourhoodSquareDir(level,box,options,refSchem,dir):
	# first face
	bPLOT = (57,0) #getBlockFromOptions(options,"Plot Material:")
	refBox = BoundingBox((refSchem.Width,refSchem.Height,refSchem.Length))
	
#	for y in xrange(refBox.miny,refBox.maxy):
#		for z in xrange(refBox.minz,refBox.maxz):
#			for x in xrange(refBox.minx,refBox.maxx):
#				print getBlock(refSchem,x,y,z)
	refX = 0
	refY = 0
	refZ = 0
	
	FLANGE = 7
	CORNER = 0
	
	if dir == 1:
		for x in xrange(box.minx+CORNER, box.maxx-CORNER):
			if x%100 == 0:
				print x
			z = box.minz
			refZ = 0
			keepGoing = True
			while keepGoing == True and z < box.maxz:
				# project into the plot from the edges. Find the entire connected shape. This is where we'll re-map the schematic
				block = getBlock(level,x,box.miny,z)
				if block != (0,0):   #== bPLOT:
					y = box.miny
					# Found the edge of the plot
					#keepGoing = False
					# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
					refY = 0
					for y in xrange(box.miny,box.maxy):
						sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
						# print z,sourceBlock,refX,refY,refZ
						if sourceBlock != AIR:
							setBlockForced(level,sourceBlock,x,y+1,z-FLANGE) # Overwrite the plot with this
						refY = refY + 1
						if refY >= refSchem.Height:
							y = box.maxy # Break
							break
					refZ = refZ+1
					if refZ >= refSchem.Length:
						refZ = 0 # Reset
						keepGoing = False # Exit and look at the next x
				z = z+1
			refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge

		
		
		
	if dir == 2:
		for z in xrange(box.minz+CORNER, box.maxz-CORNER):
			if z%100 == 0:
				print z
			x = box.maxx-1
			refZ = 0
			keepGoing = True
			while keepGoing == True and x >= box.minx:
				# project into the plot from the edges. Find the entire connected shape. This is where we'll re-map the schematic
				block = getBlock(level,x,box.miny,z)
				if block != (0,0):   #== bPLOT:
					y = box.miny
					# Found the edge of the plot
					#keepGoing = False
					# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
					refY = 0
					for y in xrange(box.miny,box.maxy):
						sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
						# print z,sourceBlock,refX,refY,refZ
						if sourceBlock != AIR:
							setBlockForced(level,sourceBlock,x+FLANGE,y+1,z) # Overwrite the plot with this
						refY = refY + 1
						if refY >= refSchem.Height:
							y = box.maxy # Break
							break
					refZ = refZ+1
					if refZ >= refSchem.Length:
						refZ = 0 # Reset
						keepGoing = False # Exit and look at the next x
				x = x-1
			refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge	

	if dir == 3:
		x = box.maxx-CORNER
		while x >= box.minx+CORNER:
			if x%100 == 0:
				print x
			z = box.maxz
			refZ = 0
			keepGoing = True
			while keepGoing == True and z >= box.minz:
				# project into the plot from the edges. Find the entire connected shape. This is where we'll re-map the schematic
				block = getBlock(level,x,box.miny,z)
				if block != (0,0):   #== bPLOT:
					y = box.miny
					# Found the edge of the plot
					#keepGoing = False
					# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
					refY = 0
					for y in xrange(box.miny,box.maxy):
						sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
						# print z,sourceBlock,refX,refY,refZ
						if sourceBlock != AIR:
							setBlockForced(level,sourceBlock,x,y+1,z+FLANGE) # Overwrite the plot with this
						refY = refY + 1
						if refY >= refSchem.Height:
							y = box.maxy # Break
							break
					refZ = refZ+1
					if refZ >= refSchem.Length:
						refZ = 0 # Reset
						keepGoing = False # Exit and look at the next x
				z = z-1
			refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
			x = x-1

	if dir == 4:
		z = box.maxz-CORNER
		while z >= box.minz+CORNER:
			if z%100 == 0:
				print z
			x = box.minx-1
			refZ = 0
			keepGoing = True
			while keepGoing == True and x < box.maxx:
				# project into the plot from the edges. Find the entire connected shape. This is where we'll re-map the schematic
				block = getBlock(level,x,box.miny,z)
				if block != (0,0):   #== bPLOT:
					y = box.miny
					# Found the edge of the plot
					#keepGoing = False
					# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
					refY = 0
					for y in xrange(box.miny,box.maxy):
						sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
						# print z,sourceBlock,refX,refY,refZ
						if sourceBlock != AIR:
							setBlockForced(level,sourceBlock,x-FLANGE,y+1,z) # Overwrite the plot with this
						refY = refY + 1
						if refY >= refSchem.Height:
							y = box.maxy # Break
							break
					refZ = refZ+1
					if refZ >= refSchem.Length:
						refZ = 0 # Reset
						keepGoing = False # Exit and look at the next x
				x = x+1
			refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
			z = z-1
		
def neighbourhoodRayCast(level,box,options,refSchem):
	# first face
	bPLOT = (155,0) #getBlockFromOptions(options,"Plot Material:")
	refBox = BoundingBox((refSchem.Width,refSchem.Height,refSchem.Length))
	
#	for y in xrange(refBox.miny,refBox.maxy):
#		for z in xrange(refBox.minz,refBox.maxz):
#			for x in xrange(refBox.minx,refBox.maxx):
#				print getBlock(refSchem,x,y,z)
	cx = (box.minx+box.maxx)/2
	cz = (box.minz+box.maxz)/2

	# Ray cast around the perimeter of the selection box onto the grass plot. Each 'ray' is a slice of the reference schema
	FLANGE = 4
	
	refX = 0
	refY = 0
	refZ = 0
	# front face
	z = box.minz
	for x in xrange(box.minx,box.maxx):
		if x%100 == 0:
			print x
		# cast a ray from here to the centre.
		dx = x-cx
		dz = z-cz
		angle = atan2(dz,dx)
		dist = sqrt(dx**2+dz**2)
		d = int(dist)
		ppx = 99999999
		ppz = 99999999
		refZ = 0
		while d >= 0: # walk along the ray from the edge, checking for blocks
			px = cx+d*cos(angle)
			pz = cz+d*sin(angle)
#			if int(px) != int(ppx) and int(pz) != int(ppz): # Check this block isn't the same as the prior one due to rounding
			if getBlock(level,int(px),box.miny,int(pz)) == bPLOT: # Grass block from the plot
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					setBlock(level,sourceBlock,int(px),y,int(pz)) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset and go to the next slice
					refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
					d = -1 # exit
			d = d-1
#			ppx = px
#			ppz = pz

	x = box.maxx
	for z in xrange(box.minz,box.maxz):
		if z%100 == 0:
			print z
		# cast a ray from here to the centre.
		dx = x-cx
		dz = z-cz
		angle = atan2(dz,dx)
		dist = sqrt(dx**2+dz**2)
		d = int(dist)
		ppx = 99999999
		ppz = 99999999
		refZ = 0
		while d >= 0: # walk along the ray from the edge, checking for blocks
			px = cx+d*cos(angle)
			pz = cz+d*sin(angle)
			if getBlock(level,int(px),box.miny,int(pz)) == bPLOT: # Grass block from the plot
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					setBlock(level,sourceBlock,int(px),y,int(pz)) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset and go to the next slice
					refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
					d = -1 # exit
			d = d-1

	z = box.maxz
	x = box.maxx
	while x >= box.minx:
		if x%100 == 0:
			print x
		# cast a ray from here to the centre.
		dx = x-cx
		dz = z-cz
		angle = atan2(dz,dx)
		dist = sqrt(dx**2+dz**2)
		d = int(dist)
		ppx = 99999999
		ppz = 99999999
		refZ = 0
		while d >= 0: # walk along the ray from the edge, checking for blocks
			px = cx+d*cos(angle)
			pz = cz+d*sin(angle)
			if getBlock(level,int(px),box.miny,int(pz)) == bPLOT: # Grass block from the plot
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					setBlock(level,sourceBlock,int(px),y,int(pz)) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset and go to the next slice
					refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
					d = -1 # exit
			d = d-1
		x=x-1

	z = box.maxz
	x = box.minx
	while z >= box.minz:
		if z%100 == 0:
			print z
		# cast a ray from here to the centre.
		dx = x-cx
		dz = z-cz
		angle = atan2(dz,dx)
		dist = sqrt(dx**2+dz**2)
		d = int(dist)
		ppx = 99999999
		ppz = 99999999
		refZ = 0
		while d >= 0: # walk along the ray from the edge, checking for blocks
			px = cx+d*cos(angle)
			pz = cz+d*sin(angle)
			if getBlock(level,int(px),box.miny,int(pz)) == bPLOT: # Grass block from the plot
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					setBlock(level,sourceBlock,int(px),y,int(pz)) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset and go to the next slice
					refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
					d = -1 # exit
			d = d-1
		z=z-1
	
def neighbourhoodHouses(level,box,options):   # ,refSchem):
	# first face
	bPLOT = (2,0) #getBlockFromOptions(options,"Plot Material:")
	# refBox = BoundingBox((refSchem.Width,refSchem.Height,refSchem.Length))
	
#	for y in xrange(refBox.miny,refBox.maxy):
#		for z in xrange(refBox.minz,refBox.maxz):
#			for x in xrange(refBox.minx,refBox.maxx):
#				print getBlock(refSchem,x,y,z)
	cx = (box.minx+box.maxx)/2
	cz = (box.minz+box.maxz)/2

	# Ray cast around the perimeter of the selection box onto the grass plot. Each 'ray' is a slice of the reference schema
	FLANGE = 4
	
	refX = 0
	refY = 0
	refZ = 0
	# front face
	z = box.minz
	for x in xrange(box.minx,box.maxx):
		if x%100 == 0:
			print x
		# cast a ray from here to the centre.
		dx = x-cx
		dz = z-cz
		angle = atan2(dz,dx)
		dist = sqrt(dx**2+dz**2)
		d = int(dist)
		ppx = 99999999
		ppz = 99999999
		refZ = 0
		while d >= 0: # walk along the ray from the edge, checking for blocks
			px = cx+d*cos(angle)
			pz = cz+d*sin(angle)
#			if int(px) != int(ppx) and int(pz) != int(ppz): # Check this block isn't the same as the prior one due to rounding
			if getBlock(level,int(px),box.miny,int(pz)) == (2,0): # Grass block from the plot
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					setBlock(level,sourceBlock,int(px),y,int(pz)) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset and go to the next slice
					refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
					d = -1 # exit
			d = d-1
#			ppx = px
#			ppz = pz

	x = box.maxx
	for z in xrange(box.minz,box.maxz):
		if z%100 == 0:
			print z
		# cast a ray from here to the centre.
		dx = x-cx
		dz = z-cz
		angle = atan2(dz,dx)
		dist = sqrt(dx**2+dz**2)
		d = int(dist)
		ppx = 99999999
		ppz = 99999999
		refZ = 0
		while d >= 0: # walk along the ray from the edge, checking for blocks
			px = cx+d*cos(angle)
			pz = cz+d*sin(angle)
			if getBlock(level,int(px),box.miny,int(pz)) == (2,0): # Grass block from the plot
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					setBlock(level,sourceBlock,int(px),y,int(pz)) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset and go to the next slice
					refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
					d = -1 # exit
			d = d-1

	z = box.maxz
	x = box.maxx
	while x >= box.minx:
		if x%100 == 0:
			print x
		# cast a ray from here to the centre.
		dx = x-cx
		dz = z-cz
		angle = atan2(dz,dx)
		dist = sqrt(dx**2+dz**2)
		d = int(dist)
		ppx = 99999999
		ppz = 99999999
		refZ = 0
		while d >= 0: # walk along the ray from the edge, checking for blocks
			px = cx+d*cos(angle)
			pz = cz+d*sin(angle)
			if getBlock(level,int(px),box.miny,int(pz)) == (2,0): # Grass block from the plot
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					setBlock(level,sourceBlock,int(px),y,int(pz)) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset and go to the next slice
					refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
					d = -1 # exit
			d = d-1
		x=x-1

	z = box.maxz
	x = box.minx
	while z >= box.minz:
		if z%100 == 0:
			print z
		# cast a ray from here to the centre.
		dx = x-cx
		dz = z-cz
		angle = atan2(dz,dx)
		dist = sqrt(dx**2+dz**2)
		d = int(dist)
		ppx = 99999999
		ppz = 99999999
		refZ = 0
		while d >= 0: # walk along the ray from the edge, checking for blocks
			px = cx+d*cos(angle)
			pz = cz+d*sin(angle)
			if getBlock(level,int(px),box.miny,int(pz)) == (2,0): # Grass block from the plot
				# Copy all the blocks across the depth of the reference schema into the plot along the depth of the plot.
				refY = 0
				for y in xrange(box.miny,box.maxy):
					sourceBlock = getBlock(refSchem,refX,refY,refZ) # NOTE: NBT is not copied in this method.
					# print z,sourceBlock,refX,refY,refZ
					setBlock(level,sourceBlock,int(px),y,int(pz)) # Overwrite the plot with this
					refY = refY + 1
					if refY >= refSchem.Height:
						y = box.maxy # Break
						break
				refZ = refZ+1
				if refZ >= refSchem.Length:
					refZ = 0 # Reset and go to the next slice
					refX = (refX +1)%(refSchem.Width) # Loop around after running off the edge
					d = -1 # exit
			d = d-1
		z=z-1

def neighbourhoodRow(level,box,options):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	(RAND,SEED) = getRandFromSeed(options)
	x = box.minx
	while x < box.maxx:
		w = RAND.randint(12,24)
		d = RAND.randint(12,depth)
		h = RAND.randint(12,height)
		hBB = BoundingBox((x,box.miny,box.minz),(w,h,d))
		ahouse(level,hBB,options)
		x = x+w

def neighbourhoodRowOfSchematics(level,box,options):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	CACHELIMIT = 10000
	
#	DIRPATH = options["Schematic Folder:"]
	print 'Scanning available schematics...'
	SchematicFileNames = glob.glob("*.schematic")
	for fileName in SchematicFileNames:
		print fileName
	print 'Found %s schematic files' % (len(SchematicFileNames))
	# End cached file names
	CACHE = []
	for fn in SchematicFileNames:
		print 'Loading schematic from file - %s' % (fn)
		sourceSchematic = MCSchematic(filename=fn)
		# (x,y,z) = sourceSchematic.size
		CACHE.append(sourceSchematic)
	
	unit = 10
	overlap = 0
	(RAND,SEED) = getRandFromSeed(options)
	x = box.minx
	z = box.minz

	(w,h,d) = (0,0,0)
	i = 0
	while x < box.maxx:
		print x,i
		newHouse = CACHE[i%len(CACHE)]
		print 'Using cached house: '+str(i)
		(w,h,d) = (newHouse.Width,newHouse.Height,newHouse.Length)
		newBox = BoundingBox((0,0,0),(newHouse.Width,newHouse.Height,newHouse.Length))
		b=range(4096)
		b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		level.copyBlocksFrom(newHouse, newBox, (x, box.miny, z ),b)
		level.markDirtyBox(box)
		x = x+w-overlap #-RAND.randint(0,2) # overlap
		i = i +1

def neighbourhoodColOfSchematics(level,box,options):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	CACHELIMIT = 10000
	
#	DIRPATH = options["Schematic Folder:"]
	print 'Scanning available schematics...'
	SchematicFileNames = glob.glob("*.schematic")
	for fileName in SchematicFileNames:
		print fileName
	print 'Found %s schematic files' % (len(SchematicFileNames))
	# End cached file names
	CACHE = []
	for fn in SchematicFileNames:
		print 'Loading schematic from file - %s' % (fn)
		sourceSchematic = MCSchematic(filename=fn)
		# (x,y,z) = sourceSchematic.size
		CACHE.append(sourceSchematic)
	
	overlap = 0
	# (RAND,SEED) = getRandFromSeed(options)
	x = box.minx
	z = box.minz

	(w,h,d) = (0,0,0)
	i = 0
	while z < box.maxz:
		print z,i
		newHouse = CACHE[i%len(CACHE)]
		print 'Using cached house: '+str(i%len(CACHE))
		(w,h,d) = (newHouse.Width,newHouse.Height,newHouse.Length)
		newBox = BoundingBox((0,0,0),(newHouse.Width,newHouse.Height,newHouse.Length))
		b=range(4096)
		b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		level.copyBlocksFrom(newHouse, newBox, (x, box.miny, z ),b)
		level.markDirtyBox(box)
		z = z+d-overlap #-RAND.randint(0,2) # overlap
		i = i +1
		
def neighbourhoodCol(level,box,options):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	(RAND,SEED) = getRandFromSeed(options)
	z = box.minz
	while z < box.maxz:
		w = RAND.randint(12,width)
		d = RAND.randint(12,24)
		h = RAND.randint(12,height)
		hBB = BoundingBox((box.minx,box.miny,z),(w,h,d))
		ahouse(level,hBB,options)
		z = z+d
		
def neighbourhoodPack1(level,box,options):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	CACHELIMIT = 10000
	
	unit = 10
	depthQ = unit*3
	overlap = 2
	(RAND,SEED) = getRandFromSeed(options)
	x = box.minx
	z = box.minz
	CACHE = []
	(w,d,h) = (0,0,0)
	while z < box.maxz:
		print z
		if RAND.randint(1,100) > 20 and len(CACHE) > 3:
			i = RAND.randint(0,len(CACHE)-1)
			newHouse = CACHE[i]
			print 'Using cached house: '+str(i)
			(w,d,h) = (newHouse.Width,newHouse.Height,newHouse.Length)
			newBox = BoundingBox((newHouse.Width,newHouse.Height,newHouse.Length))
			b=range(4096)
			b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
			level.copyBlocksFrom(newHouse, newBox, (x, box.miny, z ),b)
			level.markDirtyBox(box)
		else:
			w = RAND.randint(unit,2*unit)
			d = RAND.randint(unit,2*unit)
			h = RAND.randint(2*unit,height)
			while x+w >= box.maxx:
				w = w-1
			while z+d >= box.maxz:
				d = d-1
			hBB = BoundingBox((x,box.miny,z),(w,h,d))
			newHaus = ahouse(level,hBB,options)
			if len(CACHE) < CACHELIMIT:
				CACHE.append(newHaus)
		if z+d-overlap+depthQ-d+overlap <= box.maxz:
			hBB = BoundingBox((x,box.miny,z+d-overlap),(w,h,depthQ-d+overlap))
			newHaus = ahouse(level,hBB,options)
			if len(CACHE) < CACHELIMIT:
				CACHE.append(newHaus)
		x = x+w-overlap # overlap
		if x >= box.maxx-1-overlap:
			z = z+depthQ
			x = box.minx

def neighbourhoodPack(level,box,options):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	CACHELIMIT = 10000
	
#	DIRPATH = options["Schematic Folder:"]
	print 'Scanning available schematics...'
	SchematicFileNames = glob.glob("*.schematic")
	for fileName in SchematicFileNames:
		print fileName
	print 'Found %s schematic files' % (len(SchematicFileNames))
	# End cached file names
	CACHE = []
	for fn in SchematicFileNames:
		print 'Loading schematic from file - %s' % (fn)
		sourceSchematic = MCSchematic(filename=fn)
		# (x,y,z) = sourceSchematic.size
		CACHE.append(sourceSchematic)
	
	unit = 10
	overlap = 2
	(RAND,SEED) = getRandFromSeed(options)
	x = box.minx
	z = box.minz

	(w,h,d) = (0,0,0)
	while z < box.maxz:
		print z
		if RAND.randint(1,100) > 2 and len(CACHE) > 20:
			i = RAND.randint(0,len(CACHE)-1)
			newHouse = CACHE[i]
			print 'Using cached house: '+str(i)
			(w,h,d) = (newHouse.Width,newHouse.Height,newHouse.Length)
			print (w,h,d)
			if x+w < box.maxx and z+d < box.maxz:
				newBox = BoundingBox((0,0,0),(newHouse.Width,newHouse.Height,newHouse.Length))
				b=range(4096)
				b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
				level.copyBlocksFrom(newHouse, newBox, (x, box.miny, z ),b)
				# level.markDirtyBox(box)
			else:
				w = RAND.randint(unit,2*unit)
				d = RAND.randint(unit,2*unit)
				h = RAND.randint(2*unit,height)
				while x+w >= box.maxx:
					w = w-1
				while z+d >= box.maxz:
					d = d-1
				if w >= unit and d >= unit:
					hBB = BoundingBox((x,box.miny,z),(w,h,d))
					newHaus = ahouse(level,hBB,options)
					if len(CACHE) < CACHELIMIT:
						CACHE.append(newHaus)

		else:
			w = RAND.randint(unit,2*unit)
			d = RAND.randint(unit,2*unit)
			h = RAND.randint(2*unit,height)
			while x+w >= box.maxx:
				w = w-1
			while z+d >= box.maxz:
				d = d-1
			if w >= unit and d >= unit:
				hBB = BoundingBox((x,box.miny,z),(w,h,d))
				newHaus = ahouse(level,hBB,options)
				if len(CACHE) < CACHELIMIT:
					CACHE.append(newHaus)
		x = x+w-overlap #-RAND.randint(0,2) # overlap
		if x >= box.maxx-1-overlap:
			z = z+unit #-RAND.randint(0,2)
			x = box.minx	

def neighbourhoodPackFromSchematics(level,box,options):
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	CACHELIMIT = 10000
	
#	DIRPATH = options["Schematic Folder:"]
	print 'Scanning available schematics...'
	SchematicFileNames = glob.glob("*.schematic")
	for fileName in SchematicFileNames:
		print fileName
	print 'Found %s schematic files' % (len(SchematicFileNames))
	# End cached file names
	CACHE = []
	for fn in SchematicFileNames:
		print 'Loading schematic from file - %s' % (fn)
		sourceSchematic = MCSchematic(filename=fn)
		# (x,y,z) = sourceSchematic.size
		CACHE.append(sourceSchematic)
	
	unit = 10
	overlap = 2
	(RAND,SEED) = getRandFromSeed(options)
	x = box.minx
	z = box.minz

	(w,h,d) = (0,0,0)
	while z < box.maxz:
		print z
		if True == True: #RAND.randint(1,100) > 2 and len(CACHE) > 20:
			i = RAND.randint(0,len(CACHE)-1)
			newHouse = CACHE[i]
			print 'Using cached house: '+str(i)
			(w,h,d) = (newHouse.Width,newHouse.Height,newHouse.Length)
			newBox = BoundingBox((0,0,0),(newHouse.Width,newHouse.Height,newHouse.Length))
			b=range(4096)
			b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
			level.copyBlocksFrom(newHouse, newBox, (x, box.miny, z ),b)
			level.markDirtyBox(box)
		else:
			w = RAND.randint(unit,2*unit)
			d = RAND.randint(unit,2*unit)
			h = RAND.randint(2*unit,height)
			while x+w >= box.maxx:
				w = w-1
			while z+d >= box.maxz:
				d = d-1
			hBB = BoundingBox((x,box.miny,z),(w,h,d))
			newHaus = ahouse(level,hBB,options)
			if len(CACHE) < CACHELIMIT:
				CACHE.append(newHaus)
		x = x+w-overlap #-RAND.randint(0,2) # overlap
		if x >= box.maxx-1-overlap:
			z = z+unit #-RAND.randint(0,2)
			x = box.minx	
	
def performAHouse(level,box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	global THESTOREDSHAPE
	global THESTOREDBOX

#	SUCCESS = True
#	level = originalLevel.extractSchematic(originalBox) # Working set
#	box = BoundingBox((0,0,0),(width,height,depth))	
	# ToDo: Find the dimensions of the grass plot
	
#	RAND = getRandFromSeed(options)

	if options["Operation"] == "House":
		ahouse(level,box,options)
	elif options["Operation"] == "House (Steps)":
		ahouseSteps(level,box,options,options["Step:"])
	elif options["Operation"] == "Neighbourhood - row":
		neighbourhoodRow(level,box,options)
	elif options["Operation"] == "Neighbourhood - row of schematics":
		neighbourhoodRowOfSchematics(level,box,options)

	elif options["Operation"] == "Neighbourhood - col":
		neighbourhoodCol(level,box,options)
	elif options["Operation"] == "Neighbourhood - col of schematics":
		neighbourhoodColOfSchematics(level,box,options)
	elif options["Operation"] == "Neighbourhood - pack":
		neighbourhoodPack(level,box,options)
	elif options["Operation"] == "Neighbourhood - pack schematics":
		neighbourhoodPackFromSchematics(level,box,options)		
	elif options["Operation"] == "Neighbourhood - copy":
		THESTOREDSHAPE = level.extractSchematic(box)
	elif options["Operation"] == "Neighbourhood - ray cast":
		neighbourhoodRayCast(level,box,options,THESTOREDSHAPE)
	elif options["Operation"] == "Neighbourhood - square":
		neighbourhoodSquare(level,box,options,THESTOREDSHAPE)
	elif options["Operation"] == "Neighbourhood - square 1":
		neighbourhoodSquareDir(level,box,options,THESTOREDSHAPE,1)
	elif options["Operation"] == "Neighbourhood - square 2":
		neighbourhoodSquareDir(level,box,options,THESTOREDSHAPE,2)
	elif options["Operation"] == "Neighbourhood - square 3":
		neighbourhoodSquareDir(level,box,options,THESTOREDSHAPE,3)
	elif options["Operation"] == "Neighbourhood - square 4":
		neighbourhoodSquareDir(level,box,options,THESTOREDSHAPE,4 )

	elif options["Operation"] == "Neighbourhood - houses":
		neighbourhoodHouses(level,box,options)
	elif options["Operation"] == "Fill Air":
		fillAIR(level,box,options,"MIN")
	elif options["Operation"] == "Fill Air from MAX":
		fillAIR(level,box,options,"MAX")

#	if SUCCESS == True: # Copy from work area back into the world
#		b=range(4096)
#		b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
#		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
	level.markDirtyBox(box)		
	# level.markDirtyBox(box)
	FuncEnd(level,box,options,method) # Log end	

def drawSpheres(level,box,options,P,RAND):
	method = "drawSpheres"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	FENCE = (85,0)
	
	RAND = getRandFromSeed(options)
	if RAND.randint(1,100) > 70:
		FENCE = AIR
	material = 95
	if RAND.randint(1,100) > 50:
		material = 35
	
	for ((px,py,pz,pr,pc)) in P:
		print (px,py,pz,pr,pc)
		type = RAND.randint(1,10) # What pattern to apply
		for y in xrange(int(-pr),int(pr)):
			for z in xrange(int(-pr),int(pr)):
				for x in xrange(int(-pr),int(+pr)):
					d = sqrt((x)**2+(y)**2+(z)**2)
					if int(d) == int(pr-1) and int(d) <= int(pr):
						if type == 1:
							setBlockForced(level,(material,((y+z+x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 2 :
							setBlockForced(level,(material,((y-z-x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 3 :
							setBlockForced(level,(material,((y-z+x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 4 :
							setBlockForced(level,(material,((y+z-x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 5 :
							setBlockForced(level,(material,((-y-z+x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 6 :
							setBlockForced(level,(material,((-y+z-x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 7 :
							setBlockForced(level,(material,((-y+z+x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 8 :
							setBlockForced(level,(material,((y*z*x)*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						elif type == 9 :
							setBlockForced(level,(material,((y*(z+x))*pc)%16),box.minx+px+x,box.miny+py+y,box.minz+pz+z) # Random pattern
						else:
							setBlockForced(level,(material,pc),box.minx+px+x,box.miny+py+y,box.minz+pz+z)
						if x%4 == 0 or y%4 == 0 or z%4 == 0:
							setBlock(level,FENCE,box.minx+px+x-1,box.miny+py+y,box.minz+pz+z)
							setBlock(level,FENCE,box.minx+px+x+1,box.miny+py+y,box.minz+pz+z)
							setBlock(level,FENCE,box.minx+px+x,box.miny+py+y-1,box.minz+pz+z)
							setBlock(level,FENCE,box.minx+px+x,box.miny+py+y+1,box.minz+pz+z)
							setBlock(level,FENCE,box.minx+px+x,box.miny+py+y,box.minz+pz+z-1)
							setBlock(level,FENCE,box.minx+px+x,box.miny+py+y,box.minz+pz+z+1)

				
		# Draw a mesh of fences around the sphere to act like ropes

					
	FuncEnd(level,box,options,method)
	
####################################### LIBS
def getRandFromSeed(options):
	PARAM = int(options["Seed:"])
	if PARAM == 0:
		PARAM = randint(0,99999999999)
	print 'Seed: '+str(PARAM)
	return (Random(PARAM),PARAM)

def FuncStart(level, box, options, method):
	# abrightmoore -> shim to prepare a function.
#	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	# other initialisation methods go here
	return (method, (width, height, depth), (centreWidth, centreHeight, centreDepth))

def FuncEnd(level, box, options, method):
	t = 0
#	print '%s: Ended at %s' % (method, time.ctime())
	
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
# Ye Olde GFX Libraries
def createSign(level, x, y, z, text): #abrightmoore - convenience method. Due to Jigarbov - this is not a Sign.
	ALIASKEY = "SHIP NUMBER"
	COMMANDBLOCK = 137
	CHUNKSIZE = 16
	STANDING_SIGN = 63
	
	setBlock(level, (STANDING_SIGN,8), x, y, z)
	setBlock(level, (1,0), x, y-1, z)
	control = TAG_Compound()
	control["id"] = TAG_String("Sign")
	control["Text1"] = TAG_String(ALIASKEY)
	control["Text2"] = TAG_String(text)
	control["Text3"] = TAG_String("Generated by")
	control["Text4"] = TAG_String("@abrightmoore")	
	
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	chunka.TileEntities.append(control)
	chunka.dirty = True

def chaikinSmoothAlgorithm(P): # http://www.idav.ucdavis.edu/education/CAGDNotes/Chaikins-Algorithm/Chaikins-Algorithm.html
	F1 = 0.25
	F2 = 0.75
	Q = []
	(x0,y0,z0) = (-1,-1,-1)
	count = 0
	for (x1,y1,z1) in P:
		if count > 0: # We have a previous point
			(dx,dy,dz) = (x1-x0,y1-y0,z1-z0)
#			Q.append( (x0*F2+x1*F1,0,z0*F2+z1*F1) )
#			Q.append( (x0*F1+x1*F2,0,z0*F1+z1*F2) )

			Q.append( (x0*F2+x1*F1,y0*F2+y1*F1,z0*F2+z1*F1) )
			Q.append( (x0*F1+x1*F2,y0*F1+y1*F2,z0*F1+z1*F2) )

#			Q.append( (x0+dx*F1+*F2,y0*F1+y1*F2,z0*F1+z1*F2) )
#			Q.append( (x0*F2+x1*F1,y0*F2+y1*F1,z0*F2+z1*F1) )
		else:
			count = count+1
		(x0,y0,z0) = (x1,y1,z1)

	return Q

def drawRectangle(level,box,options,p1,p2,p3,p4,material):
	drawTriangle(level, p1, p2, p3,material, material)
	drawTriangle(level, p1, p4, p3,material, material)

	
def drawTriangle(level, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
	if materialFill != (0,0):
		# for each step along the 'base' draw a line from the apex
		dx = p3x - p2x
		dy = p3y - p2y
		dz = p3z - p2z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)
		
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
			
			iter = iter+0.5 # slightly oversample because I lack faith.
			drawLineForced(level, materialFill, (px, py, pz), (p1x, p1y, p1z) )
	
	
	drawLineForced(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLineForced(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLineForced(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def drawTriangleEdge(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge):
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def plotLine(level,material,p1,p2):

	(x1,y1,z1) = p1
	(x2,y2,z2) = p2
	
	dx = x2-x1
	dy = y2-y1
	dz = z2-z1
	
	steps = abs(dx)
	if abs(dy) > abs(dx):
		steps = abs(dy)
	if abs(dz) > abs(dy):
		steps = abs(dz)
	if steps == 0:
		setBlock(level,material,x1,y1,z1)
	else:
		ddx = float(dx)/float(steps)
		ddy = float(dy)/float(steps)
		ddz = float(dz)/float(steps)
		pdx = float(0)
		pdy = float(0)
		pdz = float(0)
		
		for i in xrange(0,int(steps)):
			setBlock(level,material,x1+pdx,y1+pdy,z1+pdz)
			pdx = pdx + ddx
			pdy = pdy + ddy
			pdz = pdz + ddz
	
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	return drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLinesSmooth(level,box,material,SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = drawLines(level,box,material,P)
	return Q

def drawLinesSmoothForced(level,box,material,SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = drawLinesForced(level,box,material,P)
	return Q
	
def drawLines(level,box,material,P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( drawLine(level,material,(box.minx+x0,box.miny+y0,box.minz+z0),(box.minx+x,box.miny+y,box.minz+z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q

def drawLinesForced(level,box,material,P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( drawLineForced(level,material,(box.minx+x0,box.miny+y0,box.minz+z0),(box.minx+x,box.miny+y,box.minz+z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q	
	
def drawLineForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	return drawLineConstrainedForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )
	
def drawLine1(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	for px, py, pz in bresenham.bresenham((x,y,z),(x1,y1,z1)):
		setBlock(scratchpad,(blockID, blockData),px,py,pz)
	setBlock(scratchpad,(blockID, blockData),x1,y1,z1)

def drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)
	P = []
	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(xd,yd,zd) = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)))
			setBlock(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points drawn

def drawLineConstrainedForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)
	P = []
	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(xd,yd,zd) = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)))
			setBlockForced(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points drawn
	
def drawLineConstrainedRandom(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), frequency ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)


	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)

	iter = 0
	while iter <= distance:
		if randint(0,99) < frequency:
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
		iter = iter+0.5 # slightly oversample because I lack faith.
	
def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

def setBlock2(level, (block, data), x, y, z):
	if getBlock(level, x,y,z) == AIR:
		level.setBlockAt(int(x), int(y), int(z), block)
		level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockForced(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
# @TheWorldFoundry

from random import randint
from pymclevel import BoundingBox

class Plot(object):
	''' Represents a proto-structure
	'''
	def __init__(self, label, level, aggregateHeightMap, location, size, materials ):
		self.label = label
		self.level = level
		self.aggregateHeightMap = aggregateHeightMap
		self.location = location
		self.size = size
		self.materials = materials
	
	def render(self):
		(x,y,z) = self.location
		dx,dy,dz = self.size
		markerTape(self.level, BoundingBox(self.location,self.size))
		
class TownSquare(Plot):
    def __init__(self, label, level, aggregateHeightMap, location, size, materials):
        super(TownSquare,self).__init__(label, level, aggregateHeightMap, location, size, materials)

class Farm(Plot):
    def __init__(self, label, level, aggregateHeightMap, location, size, materials):
        super(Farm,self).__init__(label, level, aggregateHeightMap, location, size, materials)

		
inputs = (
		("ABODE", "label"),
		("Max Number of Plots:", 15),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

# Given a region, create a connected abode

NONSURFACE = [ 0, 17, 18, 31, 37, 38, 78, 175 ] # Block IDs for non-surface blocks. Metadata hints. TBD: Add woods and leaves

DEBUG = False # Turn on for verbose logging to stdout / MCEdit log

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
	
def findPlacesToBuildOut(level, box, options):
	''' 
		An area that works for building on has a coherent area of 'land' (solid blocks) and is at least a reasonable size
	'''
	MAXTHINGS = options["Max Number of Plots:"]
	
	SETTLEMENTS = [ # TODO: These could be implemented as classes for ease of extensibility...
					["TownSquare","Farm","Farm","Farm","Farm","Farm"],
				  ]
	SETTLEMENT = SETTLEMENTS[randint(0,len(SETTLEMENTS)-1)] # Choose a pattern of plots to pop()

	plots = [] # All of the places for plots go here. Then we can post-process to join them up
	
	# Profile the environment, based on our preferred configuration of clear spaces
	
	HM = getMyHeightMap(level, box, options) # Raw topographical scan ignoring 'nonsurface' materials
	AHM = generateAggregateHeightMaps(HM) # A set of grids at different scales with the properties 'squares' summarised
	
	keepGoing = True
	count = 0
	
	while count < MAXTHINGS and keepGoing and len(SETTLEMENT) > 0:
		# Choose a plot to work on
		
		plotType = SETTLEMENT.pop()
		if plotType == "TownSquare":
			# A town square wants to be flatish and largish and squarish on solid ground open to the sky
			dimension = 16
			dimensionHeight = 8 # This is a property of the model type and is arbitrary
			result = selectPlot(level,box,plotType,dimension,dimensionHeight,AHM,plots,2)
			if result is not None:
				(px,heightMin,pz,analyseBlocks) = result
				plots.append(TownSquare("Town Square", level, AHM, (px,heightMin,pz), (dimension,dimensionHeight,dimension), analyseBlocks))
			#print "Plot",plot
		if plotType == "Farm":
			# A Farm wants to be big and squarish on solidish ground open to the sky
			dimension = 32
			dimensionHeight = 32 # This is a property of the model type and is arbitrary
			result = selectPlot(level,box,plotType,dimension,dimensionHeight,AHM,plots,16)
			if result is not None:
				(px,heightMin,pz,analyseBlocks) = result
				plots.append(Farm("Farm", level, AHM, (px,heightMin,pz), (dimension,dimensionHeight,dimension), analyseBlocks))
				
		count += 1
	
	# Debug / visualise
	if len(plots) > 0:
		print "Number of plots: ",len(plots)
		for plot in plots:
			print plot.location
			plot.render() 
	

def perform(level, box, options):
	# if DEBUG: dumpEntitiesInSelection(level, box,options)
	ATBO = findPlacesToBuildOut(level,box,options)

	
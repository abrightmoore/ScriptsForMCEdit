# @TheWorldFoundry

from os import listdir
from os.path import isfile, join
from random import randint
from math import pi,sin,cos,atan2,tan,sqrt
import glob
import pygame

from pymclevel import alphaMaterials,MCSchematic,BoundingBox

def extendFreePlots(alreadyPlacedPlots,placedPlots,buildingDelegatedAreas,newPlots):

	for aPlot in placedPlots:
		alreadyPlacedPlots.append(aPlot)
		print "Placed plot count is now",len(alreadyPlacedPlots)
	if randint(1,100) > 99:
		for a in alreadyPlacedPlots:
			print "AlreadyPlacedPlot",a	
	
	buildingDelegatedAreasCounter = 0
	while buildingDelegatedAreasCounter < len(buildingDelegatedAreas):
		freeSpace = buildingDelegatedAreas[buildingDelegatedAreasCounter]
		(Aminx,Aminz,Amaxx,Amaxz) = freeSpace
		saveThisPlot = True # Candidate to save
		newPlotsCounter = 0
		while newPlotsCounter < len(newPlots):
			(Bminx,Bminz,Bmaxx,Bmaxz) = newPlots[newPlotsCounter]
			newPlotsCounter += 1
			if checkBoundingBoxIntersect((Aminx,Aminz,Aminx+Amaxx,Aminz+Amaxz), (Bminx,Bminz,Bminz+Bmaxz,Bminz+Bmaxz)): # If there is no collision with existing plots, add this one
				saveThisPlot = False # Collides with an existing one
				newPlotsCounter = len(newPlots) # break looping
		if saveThisPlot == True: # Candidate to save
			alreadyPlacedPlotsCounter = 0
			while alreadyPlacedPlotsCounter < len(alreadyPlacedPlots):
				(Bminx,Bminz,Bmaxx,Bmaxz) = alreadyPlacedPlots[alreadyPlacedPlotsCounter]
				alreadyPlacedPlotsCounter += 1
				if checkBoundingBoxIntersect((Aminx,Aminz,Aminx+Amaxx,Aminz+Amaxz), (Bminx,Bminz,Bminz+Bmaxz,Bminz+Bmaxz)): # If there is no collision with existing used plots, add this one
					saveThisPlote = False # Collision
					alreadyPlacedPlotsCounter = len(alreadyPlacedPlots)
		if saveThisPlot == True:
			newPlots.append(freeSpace) # Add any remaining space to the list	
		buildingDelegatedAreasCounter += 1
	return newPlots



def checkBoundingBoxIntersect((Aminx,Aminz,Amaxx,Amaxz), (Bminx,Bminz,Bmaxx,Bmaxz)):
	#print 'Checking BB A/B intersection '
	#printBoundingBox(A)
	#printBoundingBox(B)
	# Check for A completely to the left of B. https://github.com/mcedit/pymclevel/blob/master/box.py
	# http://www.toymaker.info/Games/html/3d_collisions.html
	if Amaxx < Bminx:
	    return False
	# Check for A to the right of B
	if Aminx > Bmaxx:
	    return False
	# Check for A in front of B
	if Amaxz < Bminz:
	    return False
	# Check for A behind B
	if Aminz > Bmaxz:
	    return False
	# Check for A above B
#	if A.miny > B.maxy:
#	    return False
	# Check for A below B
#	if A.maxy < B.miny:
#	   return False
	   
	# Collision has occurred
	#print 'Collision occurred'
	return True


def checkBoundingBoxIntersect3D((Aminx,Aminy,Aminz,Amaxx,Amaxy,Amaxz), (Bminx,Bminy,Bminz,Bmaxx,Bmaxy,Bmaxz)):
	#print 'Checking BB A/B intersection '
	#printBoundingBox(A)
	#printBoundingBox(B)
	# Check for A completely to the left of B. https://github.com/mcedit/pymclevel/blob/master/box.py
	# http://www.toymaker.info/Games/html/3d_collisions.html
	if Amaxx < Bminx:
	    return False
	# Check for A to the right of B
	if Aminx > Bmaxx:
	    return False
	# Check for A in front of B
	if Amaxz < Bminz:
	    return False
	# Check for A behind B
	if Aminz > Bmaxz:
	    return False
	# Check for A above B
	if Aminy > Bmaxy:
	    return False
	# Check for A below B
	if Amaxy < Bminy:
	   return False
	   
	# Collision has occurred
	#print 'Collision occurred'
	return True


	
def createZoneMap(numPoints,boxW,boxD):
	zonePoints = []

	# High-rise
	#zonePoints.append((2.0,boxW>>1,boxD>>1,boxW,0)) # Power, x pos, z pos, wavelength, phase shift
	# Residential
	#zonePoints.append((0.5,randint(0,boxW>>1),randint(0,boxW>>1),boxW<<1,pi)) # Power, x pos, z pos, wavelength
	# Based on the value at the location determined by the interference of the zonePoints we will choose what to build in the plot
	# > 0.7 High-rise
	# > 0.4 Medium-rise
	# > 0.1 Low-rise
	# > -.4 Parkland / vacant
	# > -0.8 Residential
	# otherwise ...

	
	# NOTE: This can be an option to load in a prepared zoning map
	AMPLITUDE = 0.5
	zonePoints.append((AMPLITUDE,boxW>>1,boxD>>1,boxW,0)) # Power, x pos, z pos, wavelength, phase shift
	# Residential
	#zonePoints.append((0.5,randint(0,boxW>>1),randint(0,boxW>>1),boxW,pi)) # Power, x pos, z pos, wavelength
	for i in xrange(0,randint(1,numPoints)):
		zonePoints.append((0.1,randint(0,boxW),randint(0,boxW),boxW,pi)) # Power, x pos, z pos, wavelength
		
	# Debug - plot out the zoning pattern as an image 
	zoneImg = pygame.Surface((boxW,boxD))
	px = pygame.surfarray.pixels3d(zoneImg)
	for x in xrange(0,boxW):
		for z in xrange(0,boxD):
			valHere = 0
			cols = []
			count = 0
			for (amp,ppx,ppz,wavelength,offset) in zonePoints:
				dx = x-(ppx)
				dz = z-(ppz)
				dist = sqrt(dx**2+dz**2)
				ratio = dist/wavelength
				contribution = cos(offset+ratio*pi*2.0)
				valHere += valHere+contribution
				cols.append(contribution)
				count += 1
			valHere = (valHere+1.0)/2.0 * 255
			lowerBound = 0
			excess = 0
			if valHere < 0: 
				lowerBound = 0-valHere
				valHere = 0
			if valHere > 255:
				excess = valHere - 255
				valHere = 255
				
			px[x][z] = (int(lowerBound),int(excess),int(valHere))

	del px
	return zoneImg


def loadSchematicsFromDirectory(pathname):
	print "Loading in schematics from directory",pathname
	
	SchematicFileNames = glob.glob(join(pathname, "*.schematic"))
	for fileName in SchematicFileNames:
		print fileName
	print "Found", len(SchematicFileNames), "schematic files"
	# End cached file names
	CACHE = []
	for fn in SchematicFileNames:
		print "Loading schematic from file",fn
		sourceSchematic = MCSchematic(filename=fn)
		CACHE.append((sourceSchematic,fn))
	return CACHE

def createArea(areaGeneratorName,level,areaBox,parentLevel,parentBox,areaPositionInParent):
	module = __import__(areaGeneratorName)
	result = module.create(level,areaBox,parentLevel,parentBox,areaPositionInParent) # This attempts to invoke the create() method on the nominated generator
	print result
	return result

# ---------------- YE OLDE LIBRARIES ----------------

def setBlock(level,x,y,z,material):
	(id,data) = material
	level.setBlockAt(int(x),int(y),int(z),id)
	level.setBlockDataAt(int(x),int(y),int(z),data)

def getBlock(level,x,y,z):
	id = level.blockAt(int(x),int(y),int(z))
	data = level.blockDataAt(int(x),int(y),int(z))
	return (id,data)
	
def getBlockFromOptions(options,label):
	return ( options[label].ID,
			 options[label].blockData
			)
			
def drawSphere(level,(x,y,z), r, material):
	RSQUARED = r*r
	for iterX in xrange(-r,r+1):
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		for iterZ in xrange(-r,r+1):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			for iterY in xrange(-r,r+1):
				if XSQUARED + ZSQUARED + iterY*iterY <= RSQUARED:
					setBlock(level, XOFFSET, y+iterY, ZOFFSET, material)

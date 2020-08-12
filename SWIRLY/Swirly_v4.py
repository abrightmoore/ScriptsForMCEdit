# @abrightmoore

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, floor
from random import *
from os import listdir
from os.path import isfile, join
import glob

from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, alphaMaterials, MCSchematic, MCLevel, BoundingBox

inputs = (
	("SWIRLY", "label"),
	("Wavelength", 64),
	("Path Width", 8),
	("Number of Swirls", 2),
	("Material 1", alphaMaterials.Glass),
	("Use all materials?", False),
	("Material 2", alphaMaterials.Glass),
	("Material 3", alphaMaterials.Glass),
	("Material 4", alphaMaterials.Glass),
	("Material 5", alphaMaterials.Glass),
	("Material 6", alphaMaterials.Glass),
	("Material 7", alphaMaterials.Glass),
	("Material 8", alphaMaterials.Glass),
	("Material 9", alphaMaterials.Glass),
	("Material 10", alphaMaterials.Glass),
	("Material 11", alphaMaterials.Glass),
	("Material 12", alphaMaterials.Glass),
	("Vary Wavelength?", False),
	("Vary Radius?", False),
	("Pinch?",False),
	("Wall?", False),
	("Wall Material", alphaMaterials.Stone),
	("Wall Thickness", 1),
	("abrightmoore@yahoo.com.au", "label"),
	("http://brightmoore.net", "label")
	)
	
def perform(level, box, options):
	if options["Wall?"] == True:
		cylinder(level,box,options)

	swirly(level, box, options)
	level.markDirtyBox(box)	

def setBlock(level,material,point):
	(x,y,z) = point
	(bID,bDATA) = material
	level.setBlockAt(x,y,z,bID)
	level.setBlockDataAt(x,y,z,bDATA)

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)

def cylinder(level,box,options):
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			

	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	cx = width>>1
	cy = height>>1
	cz = depth>>1

	workspace = level.extractSchematic(box)

	material = getBlockFromOptions(options,"Wall Material")
	
	wallThickness = options["Wall Thickness"]
	varyRadius = options["Vary Radius?"]
	
	for z in xrange(0,depth):
		for x in xrange(0,width):
			for y in xrange(0,height):
				dx = x-cx
				dy = y-cy
				dist = sqrt(dx**2+dy**2)
				angle = atan2(dy,dx)
				rdistHere = sqrt((cx*cos(angle))**2+(cy*sin(angle))**2)
				deltaDist = rdistHere-dist
				px = x
				py = y
				if varyRadius == True:
					radiusHere = float(z+1)/float(depth)
					px = radiusHere*dx+cx
					py = radiusHere*dy+cy

				if deltaDist >= 0 and deltaDist <= wallThickness:
					setBlock(workspace,material,(px,py,z))

	level.copyBlocksFrom(workspace, BoundingBox((0,0,0),(width,height,depth)),(box.minx,box.miny,box.minz))

	
def swirly(level, box, options):
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			

	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	cx = width>>1
	cy = height>>1
	cz = depth>>1
	

	
	# r2 = sqrt(cx**2+cy**2)
	stepTheta = atan2(1,cx)
	stepTheta2 = atan2(1,cy)
	if stepTheta2 < stepTheta:
		theta = stepTheta2
	
	# stepScale = cx*cy
	
	pathWidth = 2*options["Path Width"]
	numSwirls = options["Number of Swirls"]
	swirlOffsetAngle = 2.0*pi/numSwirls
	
	workspace = level.extractSchematic(box)
	
	material = getBlockFromOptions(options,"Material 1")
	materials = []
	materials.append(material)
	if options["Use all materials?"] == True:
		materials.append(getBlockFromOptions(options,"Material 2"))
		materials.append(getBlockFromOptions(options,"Material 3"))
		materials.append(getBlockFromOptions(options,"Material 4"))
		materials.append(getBlockFromOptions(options,"Material 5"))
		materials.append(getBlockFromOptions(options,"Material 6"))
		materials.append(getBlockFromOptions(options,"Material 7"))
		materials.append(getBlockFromOptions(options,"Material 8"))
		materials.append(getBlockFromOptions(options,"Material 9"))	
		materials.append(getBlockFromOptions(options,"Material 10"))
		materials.append(getBlockFromOptions(options,"Material 11"))
		materials.append(getBlockFromOptions(options,"Material 12"))

	varyWavelength = options["Vary Wavelength?"]
	varyRadius = options["Vary Radius?"]
	# The wavelength can change along the plot up the 
	dz = options["Wavelength"]
	angleStep = pi*2.0/dz
	
	# Build a swirly thing length-ways
	plotZ = 0
	step = 0
	while plotZ < depth:
		zStep = 1.0
		if int(zStep)%100 == 1:
			print str(plotZ)+" of "+str(depth)
		if varyWavelength == True:
			zStep = 1.0*((plotZ+1)/depth)
		for j in xrange(0,numSwirls):
			angleHere = angleStep
			radiusHere = 1.0
			if varyRadius == True:
				radiusHere = (plotZ+1)/depth
				if options["Pinch?"] == True:
					radiusHere = cos(pi*(plotZ+1)/depth)
			for i in xrange(0,pathWidth):
				angle = swirlOffsetAngle*j+stepTheta*i+angleHere*step
				dx = cx*cos(angle)*radiusHere
				dy = cy*sin(angle)*radiusHere

				setBlock(workspace,materials[j%len(materials)],(int(cx+dx),int(cy+dy),int(plotZ)))
		step += 1
		plotZ += zStep
	
	level.copyBlocksFrom(workspace, BoundingBox((0,0,0),(width,height,depth)),(box.minx,box.miny,box.minz))
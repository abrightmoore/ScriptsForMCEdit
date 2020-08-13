# This filter is for exploding a build into its component parts.
# abrightmoore@yahoo.com.au
# http://brightmoore.net

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0

# GLOBAL
CHUNKSIZE = 16

inputs = (
		("ROTATOR", "label"),
		("Operation", (
			"Rotate","Rotate"
  		    )),
		("Spin (Theta/Horizontal/Y)", 33.5),
		("Pitch (Phi/Vertical/XZ", 55.3),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = options["Operation"]
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = True
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))
	# Operations go here - switch to the function based on selected operation

	if method == "Rotate":
		Rotate(originalLevel, originalBox, options) 
		#b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
#		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
#		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False # Suppress additional copyback

		
		# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end

def Rotate(level, box, options):
	# I pulled the connected-block scan code from my SELECTOR filter
	method = "Rotate"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)
	centreWidth = float(width/2)
	centreHeight = float(height/2)
	centreDepth = float(depth/2)
	AIR = (0,0)
	ANGLE = pi/180
	
	theta = options["Spin (Theta/Horizontal/Y)"]*ANGLE
	phi = options["Pitch (Phi/Vertical/XZ"]*ANGLE
	
	SOURCE = level.extractSchematic(box)
	level.fillBlocks(box,level.materials.blockWithID(0, 0))
	
	c = (cx, cy, cz) = (0,0,0) #(centreWidth, centreHeight, centreDepth)

#	P = [ (0.0,0.0,0.0),
#		  (width,0.0,0.0),
#		  (width,0,depth),
#		  (0.0,0.0,depth),
#		  (0.0,height,0.0),
#		  (width,height,0.0),
#		  (width,height,depth),
#		  (0.0,height,depth)
#		]

		#	print P
#	Q = RotatePoints(P, (cx, cy, cz), theta, phi)
#	print Q


#	minx = 9999999
#	miny = 9999999
#	minz = 9999999
#	maxx = -9999999
#	maxy = -9999999
#	maxz = -9999999
#	for (x,y,z) in Q:
#		if x < minx:
#			minx = x
#		if x > maxx:
#			maxx = x
#		if y < miny:
#			miny = y
#		if y > maxy:
#			maxy = y
#		if z < minz:
#			minz = z
#		if z > maxz:
#			maxz = z
	
#	print 'zz: %s %s %s %s %s %s' % (minx,miny,minz,maxx,maxy,maxz)
	
	# loop through the target box, remapping the source object from it
	
#	(w,h,d) = (int(maxx-minx),int(maxy-miny),int(maxz-minz))
	#WORKING = MCSchematic((w+1,h+1,d+1))
	for iterY in xrange(0,height):
		for iterZ in xrange(0,depth):
			for iterX in xrange(0,width):
				# Plot the new point
				dx = iterX - cx
				dy = iterY - cy
				d = sqrt(dy**2 + dx**2)
				t = atan2(dy, dx) # tilt around the z axis
				(px,py,pz) = ( cos(t+phi)*d, sin(t+phi)*d, iterZ ) # tilt offset around the z axis
				dz = iterZ - cz				
				dx = px - cx
				d = sqrt(dz**2 + dx**2)
				t = atan2(dz, dx) # tilt around the y axis
				(ox,oy,oz) = ( cos(t+theta)*d, py, sin(t+theta)*d ) # tilt offset around the z axis
					
				#((sb,sbData),NBT) = getBlockWithNBT(SOURCE, int(iterX),int(iterY),int(iterZ))
				(sb,sbData) = getBlock(SOURCE, int(iterX),int(iterY),int(iterZ))
				if sb != 0:
					#setBlockWithNBT(level, (sb,sbData),NBT,box.minx+int(ox),box.miny+int(oy),box.minz+int(oz))
					setBlock(level, (sb,sbData),box.minx+int(ox),box.miny+int(oy),box.minz+int(oz))
					#if getBlock(level, box.minx+int(ox+1),box.miny+int(oy),box.minz+int(oz)) == AIR:
					#	setBlockWithNBT(level, (sb,sbData),NBT,box.minx+int(ox+1),box.miny+int(oy),box.minz+int(oz))
					#if getBlock(level, box.minx+int(ox),box.miny+int(oy),box.minz+int(oz+1)) == AIR:
					#	setBlockWithNBT(level, (sb,sbData),NBT,box.minx+int(ox),box.miny+int(oy),box.minz+int(oz+1))

				
	# level.copyBlocksFrom(WORKING, BoundingBox((0,0,0),(w,h,d)), (box.minx, box.miny, box.minz ))
	FuncEnd(level,box,options,method) # Log end			
				
'''				
				(ox,oy,oz) = RotatePoint((int(minx)+iterX,int(miny)+iterY,int(minz)+iterZ), (cx,cy,cz), -theta, -phi) # find the original point location
				
				(ox,oy,oz) = (ox+cx,oy+cy,oz+cz)
				print (ox,oy,oz)
#				print 'O: %s %s %s %s %s' % (ox,oy,oz,theta,phi)
				#if ox >=0 and ox < width and oy >= 0 and oy < height and oz >=0 and oz < depth:
				((sb,sbData),NBT) = getBlockWithNBT(level, int(box.minx+ox+cx),int(box.miny+oy+cy),int(box.minz+oz+cz))
				#setBlockWithNBT(level, (1,0),NBT,box.minx+width*2+iterX,box.miny+iterY,box.minz+iterZ)
				#if sb != 0:
				setBlockWithNBT(level, (sb,sbData),NBT,box.minx+2*width+int(minx)+iterX-cx,box.miny+int(miny)+iterY-cy,box.minz+int(minz)+depth+iterZ-cz)
'''
	
	

def RotatePoints(P, (cx,cy,cz), theta, phi):
	Q = []
	for (x,y,z) in P:
		(tx,ty,tz) = RotatePoint((x,y,z), (cx,cy,cz), theta, phi)
		Q.append((tx,ty,tz))
	return Q

def RotatePoint((x,y,z), (cx,cy,cz), theta, phi):
	(t, p, d) = getDistanceVector( (x, y, z), (cx, cy, cz) )
	return ( cos(t+theta)*cos(p+phi)*d, sin(p+phi)*d, sin(t+theta)*cos(p+phi)*d )
#	return ( cos(t+theta)*sin(p+phi)*d, cos(p+phi)*d, sin(t+theta)*sin(p+phi)*d )

def getDistanceVector( (x1,y1,z1), (x,y,z)  ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z
	distHoriz = dx**2 + dz**2
	distance = sqrt(dy**2 + distHoriz)
	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)
	return (theta, phi, distance)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))
	
def getBlockWithNBT(level,x,y,z):
	(block,data) = getBlock(level, x, y, z)
	NBT = ''
	chunk = level.getChunk(int(x)/CHUNKSIZE, int(z)/CHUNKSIZE)
	for t in chunk.TileEntities:
		x1 = t["x"].value
		y1 = t["y"].value
		z1 = t["z"].value
		if int(x) == x1 and int(y) == y1 and int(z) == z1:
			NBT = t
	return ((block,data),NBT)

def setBlockWithNBT(level, (block, data), NBT, x,y,z):
	setBlock(level, (block, data), x, y, z)
	chunk = level.getChunk(int(x)/CHUNKSIZE, int(z)/CHUNKSIZE)
	if NBT != '':
		NBT["x"] = TAG_Int(int(x))
		NBT["y"] = TAG_Int(int(y))
		NBT["z"] = TAG_Int(int(z))
		chunk.TileEntities.append(NBT)
	
def FuncStart(level, box, options, method):
	# abrightmoore -> shim to prepare a function.
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	# other initialisation methods go here
	return (method, (width, height, depth), (centreWidth, centreHeight, centreDepth))

def FuncEnd(level, box, options, method):
	print '%s: Ended at %s' % (method, time.ctime())
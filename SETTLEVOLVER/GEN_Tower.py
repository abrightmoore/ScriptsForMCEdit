# @TheWorldFoundry

import Settlevolver_v1 as Settlevolver
from pymclevel import BoundingBox

from random import randint, random

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	print "Building a",generatorName,"at", box," by ",str(agent)
	
	# What types of blocks may I use for construction?
	# resourceList = Settlevolver.findResourcesCloseToMe(((box.minx+box.maxx)>>1,(box.minz+box.maxz)>>1), materialScans, 8)
	
	# Settlevolver.fill(level, boxLocal, (35,3))
	
	areas = [] # These are 'rooms' that need to be populated afterwards.
	
	# Some useful material definitions
	AIR = (0,0)
	STONEBRICKS = (98,1)
	COBBLESTONE = (4,0)
	BRICKS = (45,0)
	WOODPLANKS = (5,0)
	FLOORHEIGHT = 5

	width,height,depth = box.maxx-box.minx, box.maxy-box.miny, box.maxz-box.minz # Find out how much space we've been given
	if width >= 16 and depth >= 16: # Minimum viable generation space
		cx = width>>1 # Pre-calculate the centre via halving through a bit shift
		cz = depth>>1 # Pre-calculate the centre via halving through a bit shift
		
		
		# A tower is a cylinder with a hat on it.
		towerHeight = height # This is a normal tower with a flat roof
		if randint(1,10) > 7:
			towerHeight = int(height/3*2) # Leave 33% room for the roof otherwise 
		
		radius = cx-(cx>>1) # Push the tower wall into the box
		r2 = radius * radius # Square of the radius. We'll use this a little later to work out if we are in or outside the tower wall
		for y in xrange(0,towerHeight):
			for z in xrange(0,depth):
				dz = z-cz # distance to centre on z axis
				ddz = dz*dz # pre-calculate the distance squared
				for x in xrange(0,width):
					dx = x-cx # distance to centre on x axis
					ddx = dx*dx # pre-calculate the distance squared
					dist2 = ddx+ddz # square of the distance. No need to square-root this
					if dist2 <= r2: # We're within the tower
						material = AIR # Default to overwriting the tower space with air
						if dist2 > r2-16: # This is the wall thickness
							material = STONEBRICKS # Wall
						else: # Inside the wall within a room. Put a floor at this offset
							if y%FLOORHEIGHT == 1: material = WOODPLANKS
						if y == 0 or (material != AIR and width > 16 and randint(1,10) == 1): material = COBBLESTONE # Bottom layer cobblestone which is allows us to pack in empty space below
						
						setBlock(level,box.minx+x,box.miny+y,box.minz+z,material) # Clear the block from this position regardless of what it is
		# Draw the roof, if this tower has one
		for y in xrange(towerHeight, height):
			scalingRatio = 1.0-float(y-towerHeight)/float(height-towerHeight) # this works out how much to taper the radius
			rad = (cx/3*2)*scalingRatio
			r2 = int(rad*rad) # The radius gets smaller the higher we go
			for z in xrange(0,depth):
				dz = z-cz # distance to centre on z axis
				ddz = dz*dz # pre-calculate the distance squared
				for x in xrange(0,width):
					dx = x-cx # distance to centre on x axis
					ddx = dx*dx # pre-calculate the distance squared
					dist2 = ddx+ddz # square of the distance. No need to square-root this
					if dist2 <= r2: # We're within the roof
						material = BRICKS
						setBlock(level,box.minx+x,box.miny+y,box.minz+z,material) # Draw the roof

		# Window features and doorways
		towerRadius = radius>>1
		for y in xrange(0,towerHeight):
			# Randomly punch windows through
			if y%FLOORHEIGHT == 3 or y == 2: # y == 2 for ground floor access
				for x in xrange(cx-towerRadius+1,cx+towerRadius):
					if x != cx:
						if randint(1,10) == 1:
							hitWall = False
							for z in xrange(0,depth): # Drill through
								theBlock = getBlock(level, box.minx+x, box.miny+y, box.minz+z)
								if theBlock != AIR and hitWall == False:
									hitWall = False
									setBlock(level, box.minx+x, box.miny+y, box.minz+z, AIR)
									setBlock(level, box.minx+x, box.miny+y+1, box.minz+z, AIR)
									z = depth
						
				for z in xrange(cz-towerRadius+1,cz+towerRadius):
					if z != cz:
						if randint(1,10) == 1:
							hitWall = False
							for x in xrange(0,width): # Drill through
								theBlock = getBlock(level, box.minx+x, box.miny+y, box.minz+z)
								if theBlock != AIR and hitWall == False:
									hitWall = False
									setBlock(level, box.minx+x, box.miny+y, box.minz+z, AIR)
									setBlock(level, box.minx+x, box.miny+y+1, box.minz+z, AIR)
									x = width
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			if level.blockAt(x,box.miny,z) != 0:
				Settlevolver.setBlockToGround(level, (x,box.miny-1,z), (98,0)) # Stone Brick

	print "Built!"
	return areas # These are all the rooms
	
	
def setBlock(level,x,y,z,material):
	(id,data) = material
	level.setBlockAt(int(x),int(y),int(z),id)
	level.setBlockDataAt(int(x),int(y),int(z),data)

def getBlock(level,x,y,z):
	id = level.blockAt(int(x),int(y),int(z))
	data = level.blockDataAt(int(x),int(y),int(z))
	return (id,data)
# @TheWorldFoundry

import Settlevolver_v1 as Settlevolver
from pymclevel import BoundingBox

from random import randint, random

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	print "Building a",generatorName,"at", box," by ",str(agent)
	pattern = [ (10,10,10,0.2+0.8*random(),1.0),(0,0,0,0.5+0.5*random(),1.0) ]
	for p in agent.pattern:
		pattern.append(p)
	
	materials = [ (0,0),(98,0), (4,0), (1,1), (1,3), (1,5) ] # (208,0), Path block needs nothing on top.  (2,0), (13,0),
	
	y = box.maxy-1
	#for y in xrange(box.miny, box.maxy):
	if False: # Debug - build a big chunky block
		while y >= box.miny:
			for z in xrange(box.minz, box.maxz):
				for x in xrange(box.minx, box.maxx):
					Settlevolver.placeBlock(level, (x, y, z), materials, pattern)
			y -= 1
		
	
	FENCE = 85,0
	materials.append(FENCE)
	
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	
	RADIUSMIN = 2
	
	diam = width
	if depth < width:
		diam = depth
	radius = randint(RADIUSMIN,diam>>1)
	
	RADIUS = radius
	
	SEGSIZE = 5
	roofHeight = 0 # int(height/3)
	segments = int((height-roofHeight)/SEGSIZE)
	
	y = box.miny
	
	cx = (box.minx+box.maxx)>>1
	cz = (box.minz+box.maxz)>>1
	
	while y < box.maxy:
		for dy in xrange(0,SEGSIZE):
			drawCircle(level,(cx,y+dy,cz), radius, materials, pattern)
		y += SEGSIZE
		radius += randint(-1,1)
		if radius > RADIUS:
			radius = RADIUS
		if radius < RADIUSMIN:
			radius = RADIUSMIN

	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			if level.blockAt(x,box.miny,z) != 0:
				Settlevolver.setBlockToGround(level, (x,box.miny-1,z), (98,0)) # Stone Brick
	
	# Draw the roof
	
def drawCircle(level, pos, radius, materials, pattern):
	cx, y, cz = pos
	
	r2 = radius*radius
	for x in xrange(cx-radius, cx+radius+1):
		for z in xrange(cz-radius, cz+radius+1):
			dx = x-cx
			dz = z-cz
			dist = dx*dx+dz*dz
			if dist < r2:
				# Settlevolver.setBlockToGround(level, (x,y,z), (98,0)) # Stone Brick
				#if level.blockAt(x,y-1,z) == 0:
				#	Settlevolver.placeBlock(level, (x, y, z), materials.remove((0,0)), pattern)
				Settlevolver.placeBlock(level, (x, y, z), materials, pattern)
					
	
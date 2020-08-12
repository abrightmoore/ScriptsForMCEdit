# @TheWorldFoundry

import Settlevolver_v1 as Settlevolver
import GEN_Cottage
from random import randint, random
from pymclevel import BoundingBox

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	print "Building a",generatorName,"at", box," by ",str(agent)
	
	areas = GEN_Cottage.create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent)
	
	# Create a chimney or two
	for i in xrange(0,randint(1,2)):
		size = randint(0,1)
		for area in areas:
			width = area.maxx-area.minx
			depth = area.maxz-area.minz
			cx = (area.maxx+area.minx)>>1
			cz = (area.maxz+area.minz)>>1
			
			px = cx
			pz = cz
			if size > 0 and width > 3 and depth > 3:
				px = randint(area.minx+size,area.maxx-1-size)
				pz = randint(area.minz+size,area.maxz-1-size)
			
			height = box.maxy-area.miny
			chimneyHeight = randint(2*height,3*height)+1
			chimneybox = BoundingBox((px-size,area.miny,pz-size),(size*2+1,chimneyHeight,size*2+1))
			
			Settlevolver.fill(level, chimneybox, (45,0)) # Bricks
			if size > 0:
				chimneybox = BoundingBox((px,area.miny,pz),(1,chimneyHeight,1))
				Settlevolver.fill(level, chimneybox, (0,0)) # Bricks
				chimneybox = BoundingBox((px-size,area.miny,pz),(size*2+1,1,1))
				Settlevolver.fill(level, chimneybox, (0,0)) # Air
				chimneybox = BoundingBox((px,area.miny,pz-size),(1,1,size*2+1))
				Settlevolver.fill(level, chimneybox, (0,0)) # Air
			else:
				level.setBlockAt(px,area.miny+chimneyHeight,pz,145) # Anvil
				level.setBlockDataAt(px,area.miny+chimneyHeight,pz,randint(0,11))			
			if level.blockAt(px,area.miny-1,pz) != 0:
				level.setBlockAt(px,area.miny,pz,61) # Furnace
				level.setBlockDataAt(px,area.miny,cz,randint(2,5))
		
	
	return areas
	
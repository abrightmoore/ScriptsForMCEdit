# @TheWorldFoundry

from pymclevel import BoundingBox
import Settlevolver_v1 as Settlevolver
import GEN_Cottage
import GEN_Library

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	# The hub is where we set out a lot of the settlement information and, if possible, lore
	print "Building a",generatorName,"at", box," by ",str(agent)
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	y = box.miny
	if y < 80:
		y = 80

	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			if level.blockAt(x,y-1,z) == 0:
				Settlevolver.setBlockToGround(level, (x,y-1,z), (98,0)) # Stone Brick

	numAgents = len(agents)
	counter = 0
	
	
	GEN_Library.create(generatorName, level, boxGlobal, BoundingBox((box.maxx-1,y,box.maxz-1),(1,1,1)), agents, allStructures, materialScans, agent)
	
	x = box.minx+1
	z = box.minz+1

	cx = (box.minx+box.maxx)>>1
	cz = (box.minz+box.maxz)>>1
	sz = 12
	cottagebox = BoundingBox((cx-(sz>>1),y,cz-(sz>>1)),(sz,box.maxy-y,sz))

	dirx = 1
	dirz = 0
	while counter < len(agents) and y < box.maxy:
		texts = [ "", agents[counter].fname, agents[counter].sname, ""]
		print "Marking player sign and book at the hub",str(x),str(y),str(z),"for",texts
		Settlevolver.createSign(level, x, y+1, z, texts)
		
		# book = GEN_Library.makeBookNBT(agents[counter].diary.getEntriesAsArray())
		# GEN_Library.placeChestWithItems(level, [book], x, y, z)
		
		counter += 1
		x += dirx
		z += dirz
		if x >= box.maxx-1:
			dirx = 0
			dirz = 1
			x = box.maxx-2
			z = box.minz+2
		elif z >= box.maxz-1:
			dirx = -1
			dirz = 0
			x = box.maxx-3
			z = box.maxz-2
		elif x < box.minx:
			dirx = 0
			dirz = -1
			x = box.minx+1
			z = box.maxz-2
		elif z < box.minz:
			y += 1
			x = box.minx+2
			z = box.minz-1 
			dirx = 1
			dirz = 0

	areas = GEN_Cottage.create(generatorName, level, boxGlobal, cottagebox, agents, allStructures, materialScans, agent)

	# Carve some stairs down
	dirx = 1
	dirz = 0
	x = box.minx+((box.maxx-box.minx)>>1)
	z = box.minz

	y = 255
	counter = 0
	while counter < 100000 and y > 16:
		
		for dy in xrange(0,4):
			level.setBlockAt(x,y+dy,z,0)
			level.setBlockDataAt(x,y+dy,z,0)
		y -= 1		
		counter += 1
		x += dirx
		z += dirz
		if x >= box.maxx:
			dirx = 0
			dirz = 1
			x = box.maxx-1
			z = box.minz+1
		elif z >= box.maxz:
			dirx = -1
			dirz = 0
			x = box.maxx-2
			z = box.maxz-1
		elif x < box.minx:
			dirx = 0
			dirz = -1
			x = box.minx
			z = box.maxz-1
		elif z < box.minz:
			x = box.minx+1
			z = box.minz 
			dirx = 1
			dirz = 0


	
	return areas
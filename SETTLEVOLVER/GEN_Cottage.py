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
	
	MAT_FOUNDATION = 98,0 # stone bricks on Bedrock and Java 1.12.2
	MAT_TRIM = 4,0
	MAT_WALL = 5,0
	MAT_WINDOW = 20,0
	MAT_DOOR = 0,0
	MAT_AIR = 0,0
	MAT_FLOOR = 5,0
	MAT_ROOF = 5,0
	MAT_LOCAL = materialScans[1] # The MAT_WOOD list from findResourcesCloseToMe
	if len(MAT_LOCAL) > 0:
		MAT_FLOOR, tpos = MAT_LOCAL[randint(0,len(MAT_LOCAL)-1)]
		MAT_ROOF, tpos = MAT_LOCAL[randint(0,len(MAT_LOCAL)-1)]
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	
	box_base = BoundingBox((box.minx,box.miny,box.minz),(width,1,depth))
	#Settlevolver.fill(level, box_base, MAT_FOUNDATION)
	
	# Each level of the house
	y = box.miny+1
	while y < box.maxy:
		print "Building level",y
		levelheight = randint(4,6)
		levelminx = box.minx+1
		levelminy = y
		levelminz = box.minz+1
		levelwidth = width-2
		leveldepth = depth-2
		
		gapwidth = 0
		gapdepth = 0
		
		if levelwidth > 4:
			levelwidth = randint(4, levelwidth)
			gapwidth = randint(0,(width-levelwidth)>>1)
		if leveldepth > 4:
			leveldepth = randint(4, leveldepth)
			gapdepth = randint(0,(depth-leveldepth)>>1)

		print "Laying the floor"
		box_floor = BoundingBox((levelminx+gapwidth,levelminy,levelminz+gapdepth),(levelwidth,1,leveldepth))
		Settlevolver.fill(level, box_floor, MAT_FLOOR)
		
		print "Placing the walls"
		box_walls = BoundingBox((levelminx+gapwidth,levelminy+1,levelminz+gapdepth),(levelwidth,levelheight-2,leveldepth))
		Settlevolver.agentFill(agent, level, box_walls)

		print "Hanging the ceiling"
		box_ceiling = BoundingBox((levelminx+gapwidth,levelminy+levelheight-1,levelminz+gapdepth),(levelwidth,1,leveldepth))
		Settlevolver.fill(level, box_ceiling, MAT_FLOOR)

		print "Attaching the trim"
		box_upright = BoundingBox((levelminx+gapwidth,levelminy+1,levelminz+gapdepth),(1,levelheight-2,1))
		Settlevolver.fill(level, box_upright, MAT_FLOOR)
		Settlevolver.setBlockToGround(level, (levelminx+gapwidth,levelminy-1,levelminz+gapdepth), MAT_FLOOR)
		box_upright = BoundingBox((levelminx+gapwidth+levelwidth-1,levelminy+1,levelminz+gapdepth),(1,levelheight-2,1))
		Settlevolver.fill(level, box_upright, MAT_FLOOR)
		Settlevolver.setBlockToGround(level, (levelminx+gapwidth+levelwidth-1,levelminy-1,levelminz+gapdepth), MAT_FLOOR)
		box_upright = BoundingBox((levelminx+gapwidth+levelwidth-1,levelminy+1,levelminz+gapdepth+leveldepth-1),(1,levelheight-2,1))
		Settlevolver.fill(level, box_upright, MAT_FLOOR)
		Settlevolver.setBlockToGround(level, (levelminx+gapwidth+levelwidth-1,levelminy-1,levelminz+gapdepth+leveldepth-1), MAT_FLOOR)
		box_upright = BoundingBox((levelminx+gapwidth,levelminy+1,levelminz+gapdepth+leveldepth-1),(1,levelheight-2,1))
		Settlevolver.fill(level, box_upright, MAT_FLOOR)
		Settlevolver.setBlockToGround(level, (levelminx+gapwidth,levelminy-1,levelminz+gapdepth+leveldepth-1), MAT_FLOOR)
		
		print "Carving the interior"
		box_interior = BoundingBox((levelminx+gapwidth+1,levelminy+1,levelminz+gapdepth+1),(levelwidth-2,levelheight-2,leveldepth-2))
		Settlevolver.fill(level, box_interior, MAT_AIR)
		areas.append(box_interior)

		if generatorName != "GEN_Mine": # No roof on the mine building
			print "Adding the roof"
			# Add a graded roof
			keepGoingRoof = True
			roofCounter = 0
			while keepGoingRoof or roofCounter < 8:
				roofWidthHere = box_ceiling.maxx-box_ceiling.minx+2-2*roofCounter
				roofDepthHere = box_ceiling.maxz-box_ceiling.minz+2-2*roofCounter
				if roofWidthHere > 0 and roofDepthHere > 0:
					box_roof = BoundingBox((box_ceiling.minx-1+roofCounter,box_ceiling.miny+1+roofCounter,box_ceiling.minz-1+roofCounter),(roofWidthHere,1,roofDepthHere))
					Settlevolver.fill(level, box_roof, MAT_ROOF)
				else:
					keepGoingRoof = False
				roofCounter += 1
			

		y += levelheight-1
	print "Built!"
	return areas # These are all the rooms
# @TheWorldFoundry

import Settlevolver_v1 as Settlevolver
import GEN_Cottage
import GEN_Tower
from random import randint, random
from pymclevel import BoundingBox

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	width = box.maxx-box.minx
	height = box.maxy-box.miny
	depth = box.maxz-box.minz
		
	wallThickness = randint(3,5)
	
	
	# Place wall sections around the box
	wallHeight = randint(height>>3,height>>2)
	wallBox = BoundingBox((box.minx+8,box.miny,box.minz+8),(width-16,wallHeight,depth-16))
	Settlevolver.fill(level, wallBox, (98,0)) # Stone Bricks
	wallInteriorBox = BoundingBox((box.minx+8+wallThickness,box.miny+1,box.minz+8+wallThickness),(width-16-wallThickness*2,wallHeight,depth-16-wallThickness*2))
	Settlevolver.fill(level, wallInteriorBox, (0,0)) # Air

	for x in xrange(wallBox.minx, wallBox.maxx):
		if x%2 == 1:
			for y in xrange(wallBox.maxy-2, wallBox.maxy+1):
				level.setBlockAt(x, y, wallBox.minz-1, 98)
				level.setBlockDataAt(x, y, wallBox.minz-1, 0)

				level.setBlockAt(x, y, wallBox.minz+wallThickness, 98)
				level.setBlockDataAt(x, y, wallBox.minz+wallThickness, 0)


				level.setBlockAt(x, y, wallBox.maxz, 98)
				level.setBlockDataAt(x, y, wallBox.maxz, 0)

				level.setBlockAt(x, y, wallBox.maxz-1-wallThickness, 98)
				level.setBlockDataAt(x, y, wallBox.maxz-1-wallThickness, 0)

	for z in xrange(wallBox.minz, wallBox.maxz):
		if z%2 == 1:
			for y in xrange(wallBox.maxy-2, wallBox.maxy+1):
				level.setBlockAt(wallBox.minx-1, y, z, 98)
				level.setBlockDataAt(wallBox.minx-1, y, z, 0)

				level.setBlockAt(wallBox.minx+wallThickness, y, z, 98)
				level.setBlockDataAt(wallBox.minx+wallThickness, y, z, 0)


				level.setBlockAt( wallBox.maxx, y, z, 98)
				level.setBlockDataAt( wallBox.maxx, y, z, 0)

				level.setBlockAt(wallBox.maxx-1-wallThickness, y, z, 98)
				level.setBlockDataAt(wallBox.maxx-1-wallThickness, y, z, 0)
	
	# Put some cottages within the walls
	PLOT_SZ = 12
	tempBox = box # Save
	box = wallInteriorBox
	boxes = [ box ]
	keepGoing = True
	while keepGoing == True:
		results = []
		for A in boxes:
			widthA = A.maxx-box.minx
			depthA = A.maxz-box.minz
			heightA = A.maxy-box.miny

			keepGoing = False
			if widthA >= PLOT_SZ or depthA >= PLOT_SZ:
				splits = Settlevolver.chopBoundingBoxRandom2D(A)
				for B in splits:
					results.append(B)
					if B.maxx-B.minx >= PLOT_SZ or B.maxz-B.minz >= PLOT_SZ and random() < 0.5:
						keepGoing = True
			else:
				results.append(A)
				keepGoing = False
		boxes = results

	resultAreas = []
	# Delegate the buildings out
	for C in results:
		if random() > 0.3: # Skip some space so it's a bit varied
			areas = GEN_Cottage.create(generatorName, level, box, C, agents, allStructures, materialScans, agent)
			for area in areas:
				resultAreas.append(area)
	box = tempBox # Restore

	# Put towers on each corner of the box
	towerSize = randint(16,20)
	towerHeight = randint(height>>2,height>>1)
	towerBox = BoundingBox((box.minx,box.miny,box.minz),(towerSize,towerHeight,towerSize))
	towerBoxA = towerBox
	GEN_Tower.create(generatorName, level, boxGlobal, towerBox, agents, allStructures, materialScans, agent)

	if random() < 0.3: # Re-roll
		towerSize = randint(16,20)
		towerHeight = randint(height>>2,height>>1)
	towerBox = BoundingBox((box.maxx-1-towerSize,box.miny,box.minz),(towerSize,towerHeight,towerSize))
	GEN_Tower.create(generatorName, level, boxGlobal, towerBox, agents, allStructures, materialScans, agent)
	towerBoxB = towerBox

	if random() < 0.3: # Re-roll
		towerSize = randint(16,20)
		towerHeight = randint(height>>2,height>>1)
	towerBox = BoundingBox((box.maxx-1-towerSize,box.miny,box.maxz-1-towerSize),(towerSize,towerHeight,towerSize))
	GEN_Tower.create(generatorName, level, boxGlobal, towerBox, agents, allStructures, materialScans, agent)
	towerBoxC = towerBox

	if random() < 0.3: # Re-roll
		towerSize = randint(16,20)
		towerHeight = randint(height>>2,height>>1)
	towerBox = BoundingBox((box.minx,box.miny,box.maxz-1-towerSize),(towerSize,towerHeight,towerSize))
	GEN_Tower.create(generatorName, level, boxGlobal, towerBox, agents, allStructures, materialScans, agent)
	towerBoxD = towerBox
		
	# Put an assembly of structures within the walls
	# areas = GEN_Cottage.create(generatorName, level, boxGlobal, wallInteriorBox, agents, allStructures, materialScans, agent)
	
	cx = (box.maxx+box.minx)>>1
	cz = (box.maxz+box.minz)>>1
	
	for i in xrange(0,randint(2,5)):
		towerSize = randint(16,24)
		towerHeight = randint(height>>2,height)
		px = cx+randint(-16,16)
		pz = cz+randint(-16,16)
		towerBox = BoundingBox((px-(towerSize>>1),box.miny,pz-(towerSize>>1)),(towerSize+1,towerHeight,towerSize+1))
		GEN_Tower.create(generatorName, level, boxGlobal, towerBox, agents, allStructures, materialScans, agent)
	return resultAreas
	
# @TheWorldFoundry

from random import randint, random
from pymclevel import BoundingBox
import Settlevolver_v1 as Settlevolver
import GEN_Cottage

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	print "Building a Mine at", box," by ",str(agent)

	boxes = [ box ]
	
	MINEPLOT_SZ = 12
	
	keepGoing = True
	while keepGoing == True:
		results = []
		for A in boxes:
			width = A.maxx-box.minx
			depth = A.maxz-box.minz
			height = A.maxy-box.miny

			keepGoing = False
			if width >= MINEPLOT_SZ or depth >= MINEPLOT_SZ:
				splits = Settlevolver.chopBoundingBoxRandom2D(A)
				for B in splits:
					results.append(B)
					if B.maxx-B.minx >= MINEPLOT_SZ or B.maxz-B.minz >= MINEPLOT_SZ and random() < 0.5:
						keepGoing = True
			else:
				results.append(A)
				keepGoing = False
		boxes = results
	
	# Make one or more mineshafts!
	shaft = results.pop(randint(0,len(results)-1))
	MAT_LOCAL = materialScans[1]
	materials = []
	for mat, tpos in MAT_LOCAL:
		materials.append(mat)
	makeShaft(level, shaft, materials, agent.pattern)
	GEN_Cottage.create(generatorName, level, box, BoundingBox((shaft.minx,shaft.miny+4,shaft.minz),(shaft.maxx-shaft.minx,shaft.maxy-shaft.miny,shaft.maxz-shaft.minz)), agents, allStructures, materialScans, agent)
	
	resultAreas = []
	# Delegate the buildings out
	for C in results:
		if random() > 0.3: # Skip some space so it's a bit varied
			areas = GEN_Cottage.create(generatorName, level, box, C, agents, allStructures, materialScans, agent)
			for area in areas:
				resultAreas.append(area)
			
	return resultAreas

def makeShaftRecursive(level, box, materials, pattern):
	# print "makeShaft at", box, material

	# Delete everything in the box
	# Settlevolver.fill(level, box, (0,0))
	
	# Make a frame within the box if there is space
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	
	frameSz = width
	if depth < frameSz:
		frameSz = depth
	if height < frameSz:
		frameSz = height
	frameSz = frameSz>>1
	if frameSz > 2:
		x = box.minx
		while x < box.maxx-frameSz:
			y = box.miny
			while y < box.maxy-frameSz:
				z = box.minz
				while z < box.maxz-frameSz:
					for i in xrange(0,frameSz):
						for j in xrange(0,frameSz):
							for k in xrange(0,frameSz):
								if ((i == 0 or i == frameSz-1) or (k == frameSz-1 or k == 0)) or (j == frameSz-1 or (i == 0 or i == frameSz-1 or k == 0 or k == frameSz-1)):
									Settlevolver.placeBlock(level, (x+i, y+j, z+k), materials, pattern)
								else:
									level.setBlockAt(x+i, y+j, z+k, 0)
									level.setBlockDataAt(x+i, y+j, z+k, 0)
					z += 1
				y += 1
			x += 1

		# Choose other paths to fill with material
		# ... grow a path from the midpoint
		cx = (box.minx+box.maxx)>>1
		cy = (box.miny+box.maxy)>>1
		cz = (box.minz+box.maxz)>>1
		
		dx = int(width/3*2)
		dy = (height/3*2)
		dz = (depth/3*2)
	
		if height <= width and height <= depth:
			# Must be vertical. Go Horizontal
			dir = random.choice([1,2,3,4])
			newX = dy
			newY = dx
			newZ = dx			
			if dir == 2:
				newX = -dy
				newZ = dx
			elif dir == 3:
				newX = dx
				newZ = dy
			elif dir == 4:
				newX = dx
				newZ = -dy
		else: # Must be a horizontal, so go down instead
			newX = dy
			newZ = dy
			newY = -dz
			if dx > dz:
				newY = -dx
		

		px = cx
		py = cy
		pz = cz
		dim = (abs(newX),newY,abs(newZ))
		newBox = BoundingBox((px,py,pz),dim)

		if newX < 0:
			px = cx-newX
			newBox = BoundingBox((px,py,pz),dim)
		elif newZ < 0:
			pz = cz-newZ
			newBox = BoundingBox((px,py,pz),dim)
		
		print "Recursive tunneling",newBox
		#if random() < 0.9:
		makeShaftRecursive(level, newBox, materials, pattern)
	
	# Otherwise... end recursion


def makeShaft(level, box, materials, pattern):
	# print "makeShaft at", box, material
	# TODO: Make a fractal branching thingy
	y = box.miny
	depth = 0
	if y > 2:
		depth = randint(box.miny>>2,box.miny)
	if box.miny-depth < 1:
		depth = depth>>1

	# Delete everything above the shaft (trees and mountain overhangs, etc.
	for i in xrange(y+2, box.maxy):
		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				level.setBlockAt(x,i,z,0)
				level.setBlockDataAt(x,i,z,0)				

	# Dig the hole and shore it up
	# newBox = BoundingBox((box.minx-((box.maxx-box.minx)>>1),y-depth,box.minz-((box.maxz-box.minz)>>1)),(box.maxx-box.minx,depth,box.maxz-box.minz))
	for i in xrange(y-depth, y+2):
		# print "Mining level", i
		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				if x == box.minx or x == box.maxx-1 or z == box.minz or z == box.maxz-1:
					Settlevolver.placeBlock(level, (x, i, z), materials, pattern)
				else:
					level.setBlockAt(x,i,z,0)
					level.setBlockDataAt(x,i,z,0)
	#newBox = BoundingBox((box.minx+1,y-depth,box.minz+1),(box.maxx-box.minx-2,depth+2,box.maxz-box.minz-2))
	
	# 
	#makeShaftRecursive(level, newBox, materials, pattern)
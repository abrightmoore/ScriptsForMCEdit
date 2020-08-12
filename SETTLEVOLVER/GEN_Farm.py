# @TheWorldFoundry

from random import randint, random
from pymclevel import BoundingBox
import Settlevolver_v1 as Settlevolver
import GEN_Cottage

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	print "Building a",generatorName,"at", box,"by",str(agent)

	boxes = [ box ]
	
	PLOT_SZ = randint(9,12)
	
	keepGoing = True
	while keepGoing == True:
		results = []
		for A in boxes:
			width = A.maxx-box.minx
			depth = A.maxz-box.minz
			height = A.maxy-box.miny

			keepGoing = False
			if width >= PLOT_SZ or depth >= PLOT_SZ:
				splits = Settlevolver.chopBoundingBoxRandom2D(A)
				for B in splits:
					results.append(B)
					if B.maxx-B.minx >= PLOT_SZ or B.maxz-B.minz >= PLOT_SZ and random() < 0.5:
						keepGoing = True
			else:
				results.append(A)
				keepGoing = False
		boxes = results
	
	# Make one or more crop areas!
	crops = results.pop(randint(0,len(results)-1))
	MAT_LOCAL = materialScans[1]
	materials = []
	for mat, tpos in MAT_LOCAL:
		materials.append(mat)
	Farmland(level, crops)
	
	resultAreas = []
	# Delegate the buildings out
	for C in results:
		if random() > 0.5: # Skip some space so it's a bit varied
			areas = GEN_Cottage.create(generatorName, level, box, C, agents, allStructures, materialScans, agent)
			for area in areas:
				resultAreas.append(area)
		else:
			Farmland(level, C)
			
	return resultAreas

def Farmland(level,box):
	crops = [ (0,0),(59,0),(59,1),(59,2),(59,3),(59,4),(59,5),(59,6),(59,7),
				(142,0),(142,1),(142,2),(142,3),(142,4),(142,5),(142,6),(142,7),
				(141,0),(141,1),(141,2),(141,3),(141,4),(141,5),(141,6),(141,7),
				# (207,0),(207,1),(207,2),(207,3), # <- This block is ICE on PE and so cannot be used
				(31,1)
			]
	
	CROPS = "RANDOM"
	CROPS_MAT = crops[randint(0,len(crops)-1)]
	
	FARM_MAT = (60,7) 
	EDGE_MAT = (3,0)
	WATER_MAT = (9,0)
	WATERCOVER_MAT = (111,0)
	FENCE_MAT = (85,0)
	SURFACE_MAT = (2,0)
	AIR = (0,0)
	
	(midx,midz) = ((box.minx+box.maxx)>>1,(box.minz+box.maxz)>>1)
	
	# Find the surface blocks
	(surfid,surfdata) = SURFACE_MAT
	surfaceBlocks = []
	for z in xrange(box.minz,box.maxz):
		if z%100 ==0: print "Processing Row: ",z
		for x in xrange(box.minx,box.maxx):
			for y1 in xrange(0,box.maxy-box.miny):
				y = box.maxy-y1-1
				(bid,bdata) = getBlock(level,x,y,z)
				if bid == surfid:
					blockAbove = getBlock(level,x,y+1,z)
					if blockAbove == AIR:
						surfaceBlocks.append((x,y,z))
						break # Found the top of this column, move on
				if bid == 31 and CROPS == "RANDOM":
					setBlock(level,x,y,z,AIR)
	
	# Now, for each of the locations we found, flip to farmland and put the crop on top
	
	print "Found ",len(surfaceBlocks)," blocks. Springtime planting underway"
	
	for (x,y,z) in surfaceBlocks:
		if x == box.minx or x == box.maxx-1 or z == box.minz or z == box.maxz-1:
			if random() > 0.4:
				setBlock(level, x, y+1, z, FENCE_MAT)
			if random() > 0.7:
				setBlock(level, x, y, z, EDGE_MAT)
		else:
			setBlock(level, x, y, z, FARM_MAT)

			if (x-midx)%5 == 0 and (z-midz)%5 == 0: # Place water?
				bw = getBlock(level,x-1,y,z)
				be = getBlock(level,x+1,y,z)
				bn = getBlock(level,x,y,z-1)
				bs = getBlock(level,x,y,z+1)
				if bw != AIR and be != AIR and bn != AIR and bs != AIR:
					setBlock(level, x, y, z, WATER_MAT)
					if getBlock(level, x, y+1, z) == AIR:
						setBlock(level, x, y+1, z, WATERCOVER_MAT)
			else:
				setBlock(level, x, y+1, z, CROPS_MAT)
	
	print "Complete"
	
def setBlock(level,x,y,z,material):
	(id,data) = material
	level.setBlockAt(int(x),int(y),int(z),id)
	level.setBlockDataAt(int(x),int(y),int(z),data)

def getBlock(level,x,y,z):
	id = level.blockAt(int(x),int(y),int(z))
	data = level.blockDataAt(int(x),int(y),int(z))
	return (id,data)
# @TheWorldFoundry
# This filter was created for RAMMANs to support locating the surface features of a landscape
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox

def perform(originalLevel, originalBox, options):
	retainBlockIDList = [2,3,9,172,5,208] # Grass, Dirt, Water, Hardened Clay, Jungle Wood Planks, Path

	print "Block IDs to retain are: ",retainBlockIDList
	print "Copying the selected region"
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(originalBox.maxx-originalBox.minx,originalBox.maxy-originalBox.miny,originalBox.maxz-originalBox.minz))	
	
	print "Scanning from bottom"
	for y in xrange(box.miny,box.maxy):
		print "Examining Layer ",y
		for z in xrange(box.minz,box.maxz):
			for x in xrange(box.minx,box.maxx):
				# blockID = level.blockAt(x,y,z)
				blockAboveID = level.blockAt(x,y+1,z)
				if blockAboveID in retainBlockIDList: # Mark to air
					#print x,y,z
					level.setBlockAt(x,y,z,0)
					level.setBlockDataAt(x,y,z,0)
	
	print "Scanning from top"
	y = box.maxy-1 
	while y > box.miny-1:
		print "Examining Layer ",y
		for z in xrange(box.minz,box.maxz):
			for x in xrange(box.minx,box.maxx):
				# blockID = level.blockAt(x,y,z)
				blockBelowID = level.blockAt(x,y-1,z)
				blockID = level.blockAt(x,y,z)
				if (blockBelowID in retainBlockIDList) or (blockID not in retainBlockIDList and blockBelowID not in retainBlockIDList): # Mark to air
					#print x,y,z
					level.setBlockAt(x,y,z,0)
					level.setBlockDataAt(x,y,z,0)
	
	
	
		y -= 1
		
	if True: # Copy from work area back into the world
		b=range(4096)
		# b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	print "Done"
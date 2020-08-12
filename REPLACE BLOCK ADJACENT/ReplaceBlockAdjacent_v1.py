# @TheWorldFoundry

from pymclevel import alphaMaterials

inputs = (
		("REPLACE BLOCK ADJACENT", "label"),
		("Material to find", alphaMaterials.Stone),
		("Adjacent material", alphaMaterials.BlockofQuartz),
		("Material to replace", alphaMaterials.GlassPane),
		("adrian@theworldfoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

def perform(level,box,options):
	materialFind = getBlockFromOptions(options,"Material to find")
	materialAdjacent = getBlockFromOptions(options,"Adjacent material")
	materialReplace = getBlockFromOptions(options,"Material to replace")
	numReplacements = 0
	for y in xrange(box.miny, box.maxy):
		for z in xrange(box.minz, box.maxz):
			for x in xrange(box.minx, box.maxx):
				if getBlock(level,x,y,z) == materialFind and (getBlock(level,x-1,y,z) == materialAdjacent or getBlock(level,x+1,y,z) == materialAdjacent or getBlock(level,x,y-1,z) == materialAdjacent or getBlock(level,x,y+1,z) == materialAdjacent or getBlock(level,x,y,z-1) == materialAdjacent or getBlock(level,x,y,z+1) == materialAdjacent):
					setBlockForced(level,materialReplace,x,y,z)
					numReplacements += 1
	print "Number of replacements made:",numReplacements
	
	
	
def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

def setBlock(level, (block, data), x, y, z):
	if getBlock(level, x,y,z) == (0,0):
		level.setBlockAt(int(x), int(y), int(z), block)
		level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockForced(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
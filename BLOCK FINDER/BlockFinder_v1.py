# Locates all blocks in the selection box of a specific type, or of a specific type and data combination.
# abrightmoore@yahoo.com.au   http://brightmoore.net

from math import pi, cos, sin, sqrt, acos, atan, asin

inputs = (
  ("Choose the block to locate:", "blocktype"),
  ("What should I look for?", ("Match Block Data", "Match Block Type Only") )
)

AIR = 0

def perform(level, box, options):

	baseBlock = options["Choose the block to locate:"].ID
	baseBlockData = options["Choose the block to locate:"].blockData
	
	modeMatchBlockData = False
	if options["What should I look for?"] == "Match Block Data":
		modeMatchBlockData = True
		
	
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			y = box.maxy
			while y >= box.miny:
				if modeMatchBlockData == True:
					if level.blockAt(x,y,z) == baseBlock and level.blockDataAt(x,y,z) == baseBlockData:
						print 'I found your block %s at %s %s %s with data value %s' % (baseBlock, x, y, z, baseBlockData)
				else:
					if level.blockAt(x,y,z) == baseBlock:
						print 'I found your block %s at %s %s %s' % (baseBlock, x, y, z)
				y = y -1


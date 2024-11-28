# This filter draws a line of blocks between two points.
# Hacked from a baseline filter provided by Sethbling.
# abrightmoore@yahoo.com.au / http://brightmoore.net
# 
# ORIGINAL LICENCE:
# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling
# END LICENCE.

# To do - I want to draw between the selected points. How to get the selection?

inputs = (
  ("Start X", 0.0),
  ("Start Z", 0.0),
  ("Start Y", 0.0),
  ("End X", 10.0),
  ("End Z", 10.0),
  ("End Y", 10.0),
  ("Pick a block:", "blocktype"),
)


def perform(level, box, options):
	x1 = options["Start X"]
	y1 = options["Start Y"]
	z1 = options["Start Z"]
	x2 = options["End X"]
	y2 = options["End Y"]
	z2 = options["End Z"]
	
	
	
	width = x2 - x1
	depth = z2 - z1
	height = y2 - y1

	x1 = box.minx + x1
	y1 = box.miny + y1
	z1 = box.minz + z1

# The block type to use for the line is the one at the selection start
	
	baseBlock = options["Pick a block:"].ID #level.blockAt(x1, y1, z1)
	baseBlockData = options["Pick a block:"].blockData #level.blockDataAt(x1, y1, z1)

# Validate input: Prevent div0 on a vertical line.

	if height == 1:
		return

# Basic geometry - a line slope is 'rise over run'
# In 3d, there are two slopes to a line, both along a plane.
# Step sizes:

	stepX = width / height
	stepZ = depth / height
	stepY = height / width
	
	posX = x1
	posZ = z1

# For each vertical step
	for posY in xrange(box.miny, box.maxy):
		setBlock(level, baseBlock, baseBlockData, (int)(posX), (int)(posY), (int)(posZ)) 
		posX = posX+stepX
		posZ = posZ+stepZ
		
	level.markDirtyBox(box)


def setBlock(level, block, data, x, y, z):
	level.setBlockAt(x, y, z, block)
	level.setBlockDataAt(x, y, z, data)
#### Command Block To Command Block Structure ####
# Filter for MCEdit by destruc7i0n 
# Puts all the command blocks in the region into a structure that can activate them 
# heavily based off of jgierer12's Create Wireless Screen Filter (http://is.gd/CWSJG12)
# With help from @WireSegal or yrsegal

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

# Imports from @Sethbling
from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String
from pymclevel import TAG_Int_Array
from pymclevel import TAG_Float
from pymclevel import TAG_Long
import math




# displayName = "Command Blocks to Command Block Structures"

inputs = [
	(
		("Instructions", "title"),

		("Step I; Select: Select a region with command blocks", "label"),
		("Step II; Generate: Select the region where the Command Blocks are generated", "label"),
		("(Go to the 'General' Tab to select the step; Select or Generate)", "label"),
	),

	(
		("General", "title"),

		("Step: ", ("Select", "Generate")),
	),
	
	(
		("Dev", "title"),
		
		("(Still A Work In Progress Page!)", "label"),
		("Print Commands After Selection", True),
		("Delete Command Blocks After Selection", False)
	),
]

########## Fast data access by SethBling ##########
from pymclevel import ChunkNotPresent
GlobalChunkCache = {}
GlobalLevel = None

def getChunk(x, z):
	global GlobalChunkCache
	global GlobalLevel
	chunkCoords = (x>>4, z>>4)
	if chunkCoords not in GlobalChunkCache:
		try:
			GlobalChunkCache[chunkCoords] = GlobalLevel.getChunk(x>>4, z>>4)
		except ChunkNotPresent:
			return None
	
	return GlobalChunkCache[chunkCoords]

def blockAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.Blocks[x%16][z%16][y]

def dataAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.Data[x%16][z%16][y]
	
def tileEntityAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.tileEntityAt(x, y, z)

def setBlockAt(x, y, z, block):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	chunk.Blocks[x%16][z%16][y] = block

def setDataAt(x, y, z, data):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	chunk.Data[x%16][z%16][y] = data

def tileEntityAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.tileEntityAt(x, y, z)

########## End fast data access ##########

def perform(level, box, options):
	global GlobalLevel
	GlobalLevel = level

	global commandBlocks

	if options["Step: "] == "Select":
		commandBlocks = getCommandBlocks(level, box, options)

		if commandBlocks == []:
			commandBlocks = None;
			raise Exception("Please select an area with command blocks!")

	else:
		if commandBlocks:
			if box.maxx-box.minx < 4:
				raise Exception("The selection must be at least 3 blocks deep (x dimension)")
			elif box.maxz-box.minz < 5:
				raise Exception("The selection must be at least 5 blocks wide (z dimension)")

			#createCmdBlocks(level, box, options, commandBlocks)
			refactorCmdBlocks(level, box, options, commandBlocks)
			level.markDirtyBox(box) # mark the whole area for refresh following completion
		else:
			raise Exception("Please select an area with cmd blocks first!")

			
			
def refactorCmdBlocks(level, box, options, commandBlocks): # abrightmoore - pure cmd block method
	MARKERMATERIAL = 159 # StainedClay
	GREEN = 5
	REDSTONEBLOCK = "minecraft:redstone_block"
	
	column = 0
	row = 0
	layer = 0

	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	
	x = box.minx
	y = box.miny
	z = box.minz

	# Start marker. Execution proceeds along each row (+x) triggering the custom command, clearing the current trigger, and triggering the next one
	level.setBlockAt(x, y, z+1, MARKERMATERIAL) # Block
	level.setBlockDataAt(x, y, z+1, GREEN) # Block Data

	for command in commandBlocks:
		# makeSignalHandler(level, x, y, z) 
		
		# @TwitchNitr0's method - pass redstone blocks past each set of cmd blocks to weakly power them.

		print '%s %s %s' % (x,y,z)
		createCmdBlock(level,x,y,z,"setblock ~ ~1 ~ minecraft:air") # Clear the trigger
		createCmdBlock(level,x, y+1, z+1,command) # in the middle

		prevX = x
		prevY = y
		prevZ = z
		x = x+1
		if x >= box.maxx:
			x = box.minx
			z = z+3
			if z >= box.maxz-2:
				z = box.minz
				y = y+3 # no check - build above the selection box if we have to. USAGE WARNING!!!
			# Because we've bumped the row (and maybe layer) we need to adjust the trigger at the end of the row.
			createCmdBlock(level, prevX, prevY+2, prevZ,"setblock ~"+str(x-prevX)+" ~"+str(y-prevY-1)+" ~"+str(z-prevZ)+" "+REDSTONEBLOCK)
		else:
			createCmdBlock(level,prevX,prevY+2,prevZ,"setblock ~1 ~-1 ~ "+REDSTONEBLOCK) # Trigger the next cmd block
			
def createCmdBlock(level, x, y, z, command): #abrightmoore - convenience method.
	COMMANDBLOCK = 137
	CHUNKSIZE = 16

	level.setBlockAt(x, y, z, COMMANDBLOCK)
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command)
	control["SuccessCount"] = TAG_Int(0)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	chunka.TileEntities.append(control)
	chunka.dirty = True
	
			
def getCommandBlocks(level, box, options):
	command = []

	for (chunk, slices, point) in level.getChunkSlices(box):
		
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if t["id"].value == "Control":
					command.append(t["Command"].value)
					
					if options["Print Commands After Selection"] == True:
						print("Command At: " +str(x)+"(x)"+" "+str(y)+"(y)"+" "+str(z)+ "(z)" + " " +"is: " + t["Command"].value + "													")

					else:
						continue

					if options["Delete Command Blocks After Selection"] == True and level.blockAt(x, y, z) == 137:
						level.setBlockAt(x, y , z , 0)

					else:
						continue

	return command


	################################################## IGNORE ####################################################
	
def createCmdBlocks(level, box, options, commandBlocks):

	i = 0

	x = box.minx
	y = box.miny
	z = box.minz

	level.setBlockAt(x, y+2, z, 159) # Block
	level.setBlockDataAt(x, y+2, z, 5) # Block Data
	chunk = getChunk(x, z)
	chunk.dirty = True

	rsLen = 0
	direction = True
	stepNum = 0
	
	
	for command in commandBlocks:
		# newPos = getNewPos(x, y, z, box, level, rsLen, direction)
		newPos = getNewPos(level, box, stepNum)
		stepNum = stepNum + 1
		
		x = newPos[0]
		y = newPos[1]
		z = newPos[2]

		# rsLen = newPos[3]
		# direction = newPos[4]

		level.setBlockAt(x, y+2, z, 55) # Redstone Dust

		level.setBlockAt(x, y+1, z, 137) # Command Block
		chunk = getChunk(x, z)
		commandBlock = cmdBlock(x, y+1, z, command)
		chunk.TileEntities.append(commandBlock)
		chunk.dirty = True

		i = i+1
	
def addRepeater(level, box, x, y, z, direction): # direction is +x or -x. Repeater is added in previous x position
	if direction > 0:
		level.setBlockAt(x-1, y+1, z, 159) # Block
		level.setBlockDataAt(x-1, y+1, z, 9) # Block Data
		level.setBlockAt(x-1, y+2, z, 93) # Repeater
		level.setBlockDataAt(x-1, y+2, z, 1) # Repeater Data
	else:
		level.setBlockAt(x+1, y+1, z, 159) # Block
		level.setBlockDataAt(x+1, y+1, z, 9) # Block Data
		level.setBlockAt(x+1, y+2, z, 93) # Repeater
		level.setBlockDataAt(x+1, y+2, z, 3) # Repeater Data

def addRowCap(level, box, x, y, z, directionx, directionz): # direction is + or -.
	if directionx > 0 and directionz > 0: # add cap to the +x running +z
		level.setBlockAt(x+1, y+1, z, 159) # Block
		level.setBlockDataAt(x+1, y, z, 9) # Block Data
		level.setBlockAt(x+1, y+2, z, 55) # Redstone dust

		level.setBlockAt(x+1, y+1, z+1, 159) # Block
		level.setBlockDataAt(x+1, y+1, z+1, 9) # Block Data
		level.setBlockAt(x+1, y+2, z+1, 93) # Repeater
		level.setBlockDataAt(x+1, y+2, z+1, 2) # Repeater Data

		level.setBlockAt(x+1, y+1, z+2, 159) # Block
		level.setBlockDataAt(x+1, y, z+2, 9) # Block Data
		level.setBlockAt(x+1, y+2, z+2, 55) # Redstone dust
	elif directionx < 0 and directionz < 0: # add cap to the -x running -z	
		level.setBlockAt(x-1, y+1, z, 159) # Block
		level.setBlockDataAt(x-1, y, z, 9) # Block Data
		level.setBlockAt(x-1, y+2, z, 55) # Redstone dust

		level.setBlockAt(x-1, y+1, z-1, 159) # Block
		level.setBlockDataAt(x-1, y+1, z-1, 9) # Block Data
		level.setBlockAt(x-1, y+2, z-1, 93) # Repeater
		level.setBlockDataAt(x-1, y+2, z-1, 0) # Repeater Data

		level.setBlockAt(x-1, y+1, z-2, 159) # Block
		level.setBlockDataAt(x-1, y, z-2, 9) # Block Data
		level.setBlockAt(x-1, y+2, z-2, 55) # Redstone dust	
	elif directionx < 0 and directionz > 0: # add cap to the -x running +z	
			level.setBlockAt(x-1, y+1, z, 159) # Block
			level.setBlockDataAt(x-1, y, z, 9) # Block Data
			level.setBlockAt(x-1, y+2, z, 55) # Redstone dust

			level.setBlockAt(x-1, y+1, z+1, 159) # Block
			level.setBlockDataAt(x-1, y+1, z+1, 9) # Block Data
			level.setBlockAt(x-1, y+2, z+1, 93) # Repeater
			level.setBlockDataAt(x-1, y+2, z+1, 2) # Repeater Data

			level.setBlockAt(x-1, y+1, z+2, 159) # Block
			level.setBlockDataAt(x-1, y, z+2, 9) # Block Data
			level.setBlockAt(x-1, y+2, z+2, 55) # Redstone dust
	
	else: # directionx > 0 and directionz < 0: # add cap to the +x running -z	
			level.setBlockAt(x+1, y+1, z, 159) # Block
			level.setBlockDataAt(x+1, y, z, 9) # Block Data
			level.setBlockAt(x+1, y+2, z, 55) # Redstone dust

			level.setBlockAt(x+1, y+1, z-1, 159) # Block
			level.setBlockDataAt(x+1, y+1, z-1, 9) # Block Data
			level.setBlockAt(x+1, y+2, z-1, 93) # Repeater
			level.setBlockDataAt(x+1, y+2, z-1, 0) # Repeater Data

			level.setBlockAt(x+1, y+1, z-2, 159) # Block
			level.setBlockDataAt(x+1, y, z-2, 9) # Block Data
			level.setBlockAt(x+1, y+2, z-2, 55) # Redstone dust
		
def getNewPos(level, box, numSteps): # abrightmoore - For your consideration
	# Based on the number of Steps we can work out where in the space we need to be by
	# transforming the distance travelled along the path into a snaking climbing redstone
	# trail.
	# Odd rows run left to right
	# Even rows run right to left
	
	numStepsWithRepeaters = numSteps + (int)(numSteps / 12)
	
	width = box.maxx-box.minx
	width = width - 6 # We need room in the selection box for the 'vertical redstone' between layers
	depth = box.maxz-box.minz
	depth = (int)(depth / 2) # We need a single air row between each command block row.
							 # This reduces the available space within which we may pack blocks
	height = box.maxy-box.miny
	height = (int)(height / 3)
	
	blocksPerLayer = width*depth
	layer = (int)(numStepsWithRepeaters/blocksPerLayer)
	
	layerIsOdd = layer % 2 # 0 is false, 1 is true
	posInLayer = numStepsWithRepeaters - layer*blocksPerLayer
	row = (int)(posInLayer/width) # Bug 1 - This needs a small modification if the prior row was at the end we may be casting forward without capping the end. Same for layer.
	
	lastNumSteps = numSteps-1 # Bugfix 1
	prevNumStepsWithRepeaters = lastNumSteps+(int)(lastNumSteps/12) # Bugfix 1	
	previousLayer = (int)(prevNumStepsWithRepeaters/blocksPerLayer) # Bugfix 1	
	prevPosInLayer = prevNumStepsWithRepeaters - previousLayer*blocksPerLayer # Bugfix 1	
	previousRow = (int)(prevPosInLayer/width) # Bugfix 1
	
	rowIsOdd = row % 2 # 0 is false, 1 is true
	column = numStepsWithRepeaters % width +3
	
	x = column + box.minx
	if (rowIsOdd == 1 and layerIsOdd == 0) or (rowIsOdd == 0 and layerIsOdd == 1):
		x = box.maxx-1-column # odd rows run the opposite way
	z = (2*row) + box.minz
	if (layerIsOdd == 1):
		z = box.maxz-(2*row)
	y = (3*layer) + box.miny

	# Gap Handling
	# Ok - now we have almost everything we need for the build. The missing bit is whether we're at
	# the end of a row and need to shimmy along to the next row, or if we're at the end of a layer
	# and now need to climb upwards, so let's look at that before we move on to build the execution
	# path by returning the command block co-ordinates
	
	if numSteps% 12 == 0: # 12 as far as we may run before a repeater is required
		if (rowIsOdd == 0 and layerIsOdd == 0) or (rowIsOdd == 1 and layerIsOdd == 1):
			addRepeater(level, box, x, y, z, 1)
		else: # if (rowIsOdd == 1 and layerIsOdd == 0):
			addRepeater(level, box, x, y, z, -1)
	
	if column == width+3-1: # End of row handling
		if (rowIsOdd == 0 and layerIsOdd == 0): # even rows
			addRowCap(level, box, x, y, z, 1, 1)
		elif (rowIsOdd == 1 and layerIsOdd == 1):
			addRowCap(level, box, x, y, z, 1, -1)
		elif (rowIsOdd == 1 and layerIsOdd == 0): # odd rows
			addRowCap(level, box, x, y, z, -1, -1)		
		else: # (rowIsOdd == 0 and layerIsOdd == 1): # odd rows
			addRowCap(level, box, x, y, z, -1, 1)	

	if column == width+3 and numSteps%12 == 0: # Bugfix 1
		if (rowIsOdd == 0 and layerIsOdd == 0): # even rows
			addRepeater(level, box, x+1, y, z, 1)
			addRowCap(level, box, x+1, y, z, 1, 1)
		elif (rowIsOdd == 1 and layerIsOdd == 1):
			addRepeater(level, box, x-1, y, z, -1)
			addRowCap(level, box, x-1, y, z, 1, -1)
		elif (rowIsOdd == 1 and layerIsOdd == 0): # odd rows
			addRepeater(level, box, x-1, y, z, -1)
			addRowCap(level, box, x-1, y, z, -1, -1)		
		else: # (rowIsOdd == 0 and layerIsOdd == 1): # odd rows
			addRepeater(level, box, x+1, y, z, -1)
			addRowCap(level, box, x+1, y, z, -1, 1)	
			
		
			
			
	if previousLayer != layer: # Bugfix 1 - detects if we just jumped up a layer
		t =1 # Bugfix 1 stub

	
	elif column == 0 and row == 0 and layer > 0: # We have to hook up from the row cap below
		t = 1 # Put the vertical redstone here. Different behaviour based on which even or odd row termination
		
		
	
	# if this is the last row in this layer I need to path back to the start, one layer up.	
		
	return (x, y, z)
	
def getNewPosOld(x, y, z, box, level, rsLen, direction):
	rsLen = rsLen+1

	if direction == True:

		if z < box.maxz-3:
			z = z+1

			if rsLen >= 12:
				rsLen = 0

				level.setBlockAt(x, y+1, z, 159) # Block
				level.setBlockDataAt(x, y+1, z, 9) # Block Data

				level.setBlockAt(x, y+2, z, 93) # Repeater
				level.setBlockDataAt(x, y+2, z, 2) # Repeater Data
				chunk = getChunk(x, z)
				chunk.dirty = True

				z = z+1

		else:
			direction = False

			rsLen = 2

			level.setBlockAt(x, y+1, z+1, 159) # Block
			level.setBlockDataAt(x, y+1, z+1, 9) # Block Data

			level.setBlockAt(x, y+2, z+1, 93) # Repeater
			level.setBlockDataAt(x, y+2, z+1, 2) # Repeater Data

			level.setBlockAt(x, y+3, z+1, 159) # Block
			level.setBlockDataAt(x, y+3, z+1, 9) # Block Data

			level.setBlockAt(x, y+4, z+1, 55) # Redstone Dust
			chunk = getChunk(x, z+1)
			chunk.dirty = True

			level.setBlockAt(x, y+2, z+2, 159) # Block
			level.setBlockDataAt(x, y+2, z+2, 9) # Block Data

			level.setBlockAt(x, y+3, z+2, 55) # Redstone Dust
			chunk = getChunk(x, z+2)
			chunk.dirty = True

			y = y+3

	else:

		if z > box.minz+3:
			z = z-1

			if rsLen >= 12:
				rsLen = 0

				level.setBlockAt(x, y+1, z, 159) # Block
				level.setBlockDataAt(x, y+1, z, 9) # Block Data

				level.setBlockAt(x, y+2, z, 93) # Repeater
				level.setBlockDataAt(x, y+2, z, 0) # Repeater Data
				chunk = getChunk(x, z)
				chunk.dirty = True

				z = z-1

		else:
			direction = True

			rsLen = 2

			level.setBlockAt(x, y+1, z-1, 159) # Block
			level.setBlockDataAt(x, y+1, z-1, 9) # Block Data

			level.setBlockAt(x, y+2, z-1, 93) # Repeater
			level.setBlockDataAt(x, y+2, z-1, 0) # Repeater Data

			level.setBlockAt(x, y+3, z-1, 159) # Block
			level.setBlockDataAt(x, y+3, z-1, 9) # Block Data

			level.setBlockAt(x, y+4, z-1, 55) # Redstone Dust
			chunk = getChunk(x, z-1)
			chunk.dirty = True

			level.setBlockAt(x, y+2, z-2, 159) # Block
			level.setBlockDataAt(x, y+2, z-2, 9) # Block Data

			level.setBlockAt(x, y+3, z-2, 55) # Redstone Dust
			chunk = getChunk(x, z-2)
			chunk.dirty = True

			y = y+3

	if y+3 > box.maxy:
		raise Exception("The selection must be higher (y dimension)")

	return (x, y, z, rsLen, direction)
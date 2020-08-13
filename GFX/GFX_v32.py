# This filter is for drawing blocky thingies. See http://mathworld.wolfram.com/QuadraticSurface.html
# abrightmoore@yahoo.com.au
# http://brightmoore.net

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy

# For Reference (see @Texelelf and @CodeWarrior0 examples)
# 	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Mirror the blocks - in memory working read only copy
# 	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
#	setBlock(schematic, (BLOCKID, BLOCKDATA), (int)(centreWidth+xx), (int)(centreHeight+yy), (int)(centreDepth+zz))

# YOUR CODE GOES HERE \/ \/ \/ \/ \/ \/ \/ \/ \/

ITEMS_COMMON = [
	"minecraft:stone",
	"minecraft:grass",
	"minecraft:dirt",
	"minecraft:cobblestone",
	"minecraft:planks",
	"minecraft:sapling",
	"minecraft:sand",
	"minecraft:gravel",
	"minecraft:log",
	"minecraft:leaves",
	"minecraft:glass",
	"minecraft:sandstone",
	"minecraft:deadbush",
	"minecraft:wool",
	"minecraft:yellow_flower",
	"minecraft:red_flower",
	"minecraft:brown_mushroom",
	"minecraft:red_mushroom",
	"minecraft:cactus",
	"minecraft:clay",
	"minecraft:reeds",
	"minecraft:wooden_slab",
	"minecraft:carrots",
	"minecraft:potatoes",
	"minecraft:carpet",
	"minecraft:stick",
	"minecraft:string",
	"minecraft:feather",
	"minecraft:wooden_hoe",
	"minecraft:wheat_seeds",
	"minecraft:leather_boots",
	"minecraft:flint",
	"minecraft:fish",
	"minecraft:cookie",
	"minecraft:pumpkin_seeds",
	"minecraft:melon_seeds",
	"minecraft:rotten_flesh",
	"minecraft:carrot",
	"minecraft:potato",
	"minecraft:poisonous_potato"
]

ITEMS_RARE = [
	"minecraft:iron_ore",
	"minecraft:coal_ore",
	"minecraft:sponge",
	"minecraft:lapis_ore",
	"minecraft:stone_slab",
	"minecraft:mossy_cobblestone",
	"minecraft:torch",
	"minecraft:oak_stairs",
	"minecraft:redstone_wire",
	"minecraft:wheat",
	"minecraft:ladder",
	"minecraft:stone_stairs",
	"minecraft:wall_sign",
	"minecraft:wooden_pressure_plate",
	"minecraft:stone_button",
	"minecraft:snow",
	"minecraft:fence",
	"minecraft:pumpkin",
	"minecraft:stonebrick",
	"minecraft:melon_block",
	"minecraft:vine",
	"minecraft:waterlily",
	"minecraft:cocoa",
	"minecraft:wooden_button",
	"minecraft:wooden_sword",
	"minecraft:wooden_shovel",
	"minecraft:wooden_pickaxe",
	"minecraft:wooden_axe",
	"minecraft:stone_sword",
	"minecraft:stone_shovel",
	"minecraft:stone_pickaxe",
	"minecraft:stone_axe",
	"minecraft:bowl",
	"minecraft:gunpowder",
	"minecraft:stone_hoe",
	"minecraft:wheat",
	"minecraft:leather_helmet",
	"minecraft:leather_chestplate",
	"minecraft:leather_leggings",
	"minecraft:porkchop",
	"minecraft:sign",
	"minecraft:wooden_door",
	"minecraft:cooked_fished",
	"minecraft:dye",
	"minecraft:bone",
	"minecraft:sugar",
	"minecraft:beef",
	"minecraft:chicken",
	"minecraft:glass_bottle",
	"minecraft:spider_eye",
	"minecraft:experience_bottle",
	"minecraft:writable_book",
	"minecraft:flower_pot",
	"minecraft:baked_potato",
	"minecraft:map",
	"minecraft:name_tag"
]

ITEMS_VERYRARE = [
	"minecraft:gold_ore",
	"minecraft:lapis_block",
	"minecraft:dispenser",
	"minecraft:golden_rail",
	"minecraft:detector_rail",
	"minecraft:sticky_piston",
	"minecraft:piston",
	"minecraft:brick_block",
	"minecraft:chest",
	"minecraft:diamond_ore",
	"minecraft:furnace",
	"minecraft:rail",
	"minecraft:lever",
	"minecraft:stone_pressure_plate",
	"minecraft:redstone_ore",
	"minecraft:redstone_torch",
	"minecraft:trapdoor",
	"minecraft:iron_bars",
	"minecraft:glass_pane",
	"minecraft:fence_gate",
	"minecraft:brick_stairs",
	"minecraft:stone_brick_stairs",
	"minecraft:sandstone_stairs",
	"minecraft:emerald_ore",
	"minecraft:tripwire_hook",
	"minecraft:tripwire",
	"minecraft:spruce_stairs",
	"minecraft:birch_stairs",
	"minecraft:jungle_stairs",
	"minecraft:cobblestone_wall",
	"minecraft:flower_pot",
	"minecraft:light_weighted_pressure_plate",
	"minecraft:heavy_weighted_pressure_plate",
	"minecraft:redstone_block",
	"minecraft:quartz_ore",
	"minecraft:quartz_block",
	"minecraft:quartz_stairs",
	"minecraft:activator_rail",
	"minecraft:dropper",
	"minecraft:stained_hardened_clay",
	"minecraft:hay_block",
	"minecraft:hardened_clay",
	"minecraft:coal_block",
	"minecraft:packed_ice",
	"minecraft:iron_shovel",
	"minecraft:iron_pickaxe",
	"minecraft:iron_axe",
	"minecraft:flint_and_steel",
	"minecraft:apple",
	"minecraft:bow",
	"minecraft:arrow",
	"minecraft:coal",
	"minecraft:iron_ingot",
	"minecraft:gold_ingot",
	"minecraft:iron_hoe",
	"minecraft:bread",
	"minecraft:cooked_porkchop",
	"minecraft:bucket",
	"minecraft:redstone",
	"minecraft:snowball",
	"minecraft:boat",
	"minecraft:leather",
	"minecraft:milk_bucket",
	"minecraft:brick",
	"minecraft:clay_ball",
	"minecraft:reeds",
	"minecraft:paper",
	"minecraft:book",
	"minecraft:slime_ball",
	"minecraft:chest_minecart",
	"minecraft:furnace_minecart",
	"minecraft:egg",
	"minecraft:compass",
	"minecraft:fishing_rod",
	"minecraft:clock",
	"minecraft:glowstone_dust",
	"minecraft:shears",
	"minecraft:melon",
	"minecraft:cooked_beef",
	"minecraft:cooked_chicken",
	"minecraft:fire_charge",
	"minecraft:pumpkin_pie",
	"minecraft:fireworks",
	"minecraft:firework_charge",
	"minecraft:quartz",
	"minecraft:lead"
]

ITEMS_UNIQUE = [
	"minecraft:noteblock",
	"minecraft:bed",
	"minecraft:gold_block",
	"minecraft:iron_block",
	"minecraft:tnt",
	"minecraft:bookshelf",
	"minecraft:obsidian",
	"minecraft:diamond_block",
	"minecraft:crafting_table",
	"minecraft:wooden_door",
	"minecraft:iron_door",
	"minecraft:ice",
	"minecraft:jukebox",
	"minecraft:netherrack",
	"minecraft:soul_sand",
	"minecraft:glowstone",
	"minecraft:cake",
	"minecraft:unpowered_repeater",
	"minecraft:brown_mushroom_block",
	"minecraft:red_mushroom_block",
	"minecraft:mycelium",
	"minecraft:nether_brick",
	"minecraft:nether_brick_fence",
	"minecraft:nether_brick_stairs",
	"minecraft:nether_wart",
	"minecraft:enchanting_table",
	"minecraft:brewing_stand",
	"minecraft:cauldron",
	"minecraft:end_stone",
	"minecraft:redstone_lamp",
	"minecraft:ender_chest",
	"minecraft:emerald_block",
	"minecraft:skull",
	"minecraft:anvil",
	"minecraft:trapped_chest",
	"minecraft:powered_comparator",
	"minecraft:daylight_detector",
	"minecraft:hopper",
	"minecraft:diamond",
	"minecraft:iron_sword",
	"minecraft:diamond_sword",
	"minecraft:diamond_shovel",
	"minecraft:diamond_pickaxe",
	"minecraft:diamond_axe",
	"minecraft:mushroom_stew",
	"minecraft:golden_sword",
	"minecraft:golden_shovel",
	"minecraft:golden_pickaxe",
	"minecraft:golden_axe",
	"minecraft:diamond_hoe",
	"minecraft:golden_hoe",
	"minecraft:chainmail_helmet",
	"minecraft:chainmail_chestplate",
	"minecraft:chainmail_leggings",
	"minecraft:chainmail_boots",
	"minecraft:iron_helmet",
	"minecraft:iron_chestplate",
	"minecraft:iron_leggings",
	"minecraft:iron_boots",
	"minecraft:diamond_helmet",
	"minecraft:diamond_chestplate",
	"minecraft:diamond_leggings",
	"minecraft:diamond_boots",
	"minecraft:golden_helmet",
	"minecraft:golden_chestplate",
	"minecraft:golden_leggings",
	"minecraft:golden_boots",
	"minecraft:painting",
	"minecraft:golden_apple",
	"minecraft:water_bucket",
	"minecraft:lava_bucket",
	"minecraft:minecart",
	"minecraft:saddle",
	"minecraft:iron_door",
	"minecraft:cake",
	"minecraft:bed",
	"minecraft:repeater",
	"minecraft:filled_map",
	"minecraft:ender_pearl",
	"minecraft:blaze_rod",
	"minecraft:ghast_tear",
	"minecraft:gold_nugget",
	"minecraft:nether_wart",
	"minecraft:potion",
	"minecraft:fermented_spider_eye",
	"minecraft:blaze_powder",
	"minecraft:magma_cream",
	"minecraft:brewing_stand",
	"minecraft:cauldron",
	"minecraft:ender_eye",
	"minecraft:speckled_melon",
	"minecraft:emerald",
	"minecraft:item_frame",
	"minecraft:golden_carrot",
	"minecraft:skull",
	"minecraft:carrot_on_a_stick",
	"minecraft:nether_star",
	"minecraft:comparator",
	"minecraft:netherbrick",
	"minecraft:tnt_minecart",
	"minecraft:hopper_minecart",
	"minecraft:iron_horse_armor",
	"minecraft:golden_horse_armor",
	"minecraft:diamond_horse_armor",
	"minecraft:record_13",
	"minecraft:record_cat",
	"minecraft:record_blocks",
	"minecraft:record_chirp",
	"minecraft:record_far",
	"minecraft:record_mall",
	"minecraft:record_mellohi",
	"minecraft:record_stal",
	"minecraft:record_strad",
	"minecraft:record_ward",
	"minecraft:record_11",
	"minecraft:record_wait"
]

inputs = (
		("GFX", "label"),
		("Operation", (
			"Scan selection",
			"Scale to selection",
			"Test Transform selection 1",
			"City Block",
			"Butterfly Random",
			"Make Jar",
			"Puzzle",
			"Interior Design",
			"Lines",
			"Chunk Chequers",
			"Pattern",
			"Mob Riding Matrix",
			"City",
			"City Grid",
			"Circular City",
			"Angled Building",
			"Ruined Building",
			"Antenna",
			"Park",
			"Disc",
			"Disc Edge",
			"Disc Strip",
			"Splodge",
			"Splodge Edge",
			"Splodge Strip",
			"Death Star 2",
			"Death Star Bands",
			"Sculpt",
			"Fill 'er up",
  		    "Toffee",
			"Fractree",
			"3DTree",
			"Forest",
			"Test Intersecting Spheres",
			"Solve Quadratic for Destruc7i0n",
			"VietnameseSnake",
  		    )),
		("Edge block:", alphaMaterials.BlockofQuartz),
		("Fill block:", alphaMaterials.Stone),
		("Light block:", alphaMaterials.GlassPane), # Randomly assigned
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

CHUNKSIZE = 16

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	global THESTOREDSHAPE

	method = options["Operation"]
	if method == "Toffee":
		Toffee(level, box, options)
	elif method == "Mob Riding Matrix":
		MobRidingMatrix(level, box, options)
	elif method == "Death Star 2":
		DeathStar2(level, box, options)
	elif method == "Death Star Bands":
		DeathStarBands(level, box, options,(box.maxx-box.minx)/2)
	elif method == "Sculpt":
		Sculpt(level, box, options)
	elif method == "Test Intersecting Spheres":
		drawSphereIntersection(level,(box.minx, box.miny, box.minz), (box.maxx-box.minx)/3*4, (1,0), (box.maxx, box.maxy, box.maxz), (box.maxx-box.minx)/3*4)
	elif method == "Solve Quadratic for Destruc7i0n":
		print [[x, y] for x in xrange(-10,11) for y in xrange(-10, 11) if x + y == -10 and x <= y and x * y == 21]
	elif method == "Ruined Building":
		RuinedBuilding(level, box, options)
	elif method == "Angled Building":
		BuildingAngledShim(level, box, options)
	elif method == "City":
		City(level, box, options)
	elif method == "City Grid":
		CityGrid(level, box, options)
	elif method == "Circular City":
		CircularCity(level, box, options)
	elif method == "Fractree":
		Fractree(level, box, options)
	elif method == "Park":
		Park(level, box, options)
	elif method == "Disc":
		drawFullDisc(level, box, options, (options["Fill block:"].ID, options["Fill block:"].blockData), -1, False)
	elif method == "Disc Edge":
		drawFullDisc(level, box, options, (options["Fill block:"].ID, options["Fill block:"].blockData), -1, True)
	elif method == "Disc Strip":
		drawFullDisc(level, box, options, (options["Fill block:"].ID, options["Fill block:"].blockData), 10, False)
	elif method == "Splodge":
		drawRandomSplodge(level, box, options, (options["Fill block:"].ID, options["Fill block:"].blockData), -1, False, 0.2, 360, 5)
	elif method == "Splodge Edge":
		drawRandomSplodge(level, box, options, (options["Fill block:"].ID, options["Fill block:"].blockData), -1, True, 0.2, 360, 3)
	elif method == "Splodge Strip":
		drawRandomSplodge(level, box, options, (options["Fill block:"].ID, options["Fill block:"].blockData), 10, False, 0.2, 360, 3)
	elif method == "Splodge Random":
		drawRandomSplodge(level, box, options, (options["Fill block:"].ID, options["Fill block:"].blockData), -1, False, 0.1*randint(1,5), randint(4,720), randint(2,6))
	elif method == "3DTree":
		draw3DTree(level, box, options)
	elif method == "Forest":
		Forest(level, box, options)
	elif method == "Antenna":
		Antenna(level, box, options)	
	elif method == "Chunk Chequers":
		ChunkChequers(level, box, options)	
	elif method == "Interior Design":
		InteriorDesign(level, box, options)
	elif method == "Make Jar":
		makeJar(level, box, options)
	elif method == "Puzzle":
		Puzzle(level, box, options)
	elif method == "Butterfly Random":
		ButterflyRandom(level, box, options)
	elif method == "Test space transformation1":
		testSpaceTransformation1(level, box, options)
	elif method == "Test space transformation2":
		testSpaceTransformation2(level, box, options)
	elif method == "Test space transformation3":
		testSpaceTransformation3(level, box, options)
	elif method == "Scale to selection":
		#print THESTOREDSHAPE
		scaleToSelection(level, box, options, THESTOREDSHAPE)
	elif method == "Test Transform selection 1":
		#print THESTOREDSHAPE
		RESULTSHAPE = []
		buildShape(level, box, options, RESULTSHAPE, THESTOREDSHAPE, [(0.3*width,0.3*height,0),(0,0.3*height,0.3*depth),(0.3*width,0,0.3*depth)])
		scaleToSelection(level, box, options, RESULTSHAPE)
	elif method == "Scan selection":
		THESTOREDSHAPE = scanSelection(level, box, options)
		#print THESTOREDSHAPE
	elif method == "Fill 'er up":
		fillErUp(level, box, options)
	elif method == "VietnameseSnake":
		VietnameseSnake(level, box, options)
	elif method == "Lines":
		Lines(level, box, options)
	elif method == "City Block":
		CityBlock(level, box, options)

	level.markDirtyBox(box)

def Hollow(level, box, options, material, coat):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Hollow"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	PURGEAMOUNT = 9+8+9
#	material = (options["Material:"].ID, options["Material:"].blockData)
#	coat = options["Coat:"]
	# END CONSTANTS


	# First pass, scan and count neighbours
	F = zeros( (width, height, depth) ) # This field holds the count of how many neighbour blocks there are

	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				thisBlock = level.blockAt(box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				if thisBlock != AIRBLOCK: # Now I need to push this block's contribution into all the neighbour blocks in a 3x3 grid
					for dx in xrange(-1,2):
						for dy in xrange(-1,2):
							for dz in xrange(-1,2):
								if dx == 0 and dy == 0 and dz == 0:  # Ignore the current block as it is not a neighbour to itself
									T = 0 # ignore
								else:
									(x, y, z) = (iterX + dx, iterY + dy, iterZ + dz)
									if x > 0 and x < (width-1) and y > 0 and y < (height-1) and z > 0 and z < (depth-1):
										F[x][y][z] = F[x][y][z] + 1

	# Pass 2 - purge anywhere the neighbour count indicates the block is completely encased in other blocks
	for iterX in xrange(1, width-1):
		for iterY in xrange(1, height-1):
			for iterZ in xrange(1, depth-1):
				# print '%s' % (F[iterX][iterY][iterZ])
				
				if coat == False:
					if F[iterX][iterY][iterZ] >= PURGEAMOUNT:
						setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				else:
					if F[iterX][iterY][iterZ] < PURGEAMOUNT and F[iterX][iterY][iterZ] > 0:
						setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
					
	print '%s: Ended at %s' % (method, time.ctime())
	
def CityBlock(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	AIR = (0,0)
	
	# Build the block - working memory
	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth)))
	
	# Build the base
	bbox1 = BoundingBox((0,0,0),(width,1,depth))
	drawFullDisc(schematic, bbox1, options, (fillMaterialBlock, fillMaterialData), -1, False)
	edgeSize = randint(3,10)
	bbox2 = BoundingBox((edgeSize,0,edgeSize),(width-2*edgeSize,1,depth-2*edgeSize))
	drawFullDisc(schematic, bbox2, options, (edgeMaterialBlock, edgeMaterialData), -1, False)
	drawRandomSplodge(schematic, bbox2, options, (fillMaterialBlock, fillMaterialData), -1, False, 0.1*randint(1,5), randint(4,720), randint(2,6))	

	# Add the trees
	numTrees = randint(0,16)
	treeOpts = { 'Edge block:': alphaMaterials.Leaves,
				 'Operation': 'City Block', 
				'Light block:': alphaMaterials.Wood, 
				'Fill block:': alphaMaterials.Wood}
	
	
	for iter in xrange(0,numTrees):
		treeSizeHeight = randint(16,30)
		treeSizeWidthDelta = randint(0,8)
		angle = pi/180*randint(0,359)
		px = centreWidth+float((centreWidth/3*2-edgeSize) * cos(angle))
		pz = centreDepth+float((centreDepth/3*2-edgeSize) * sin(angle))
		bbox = BoundingBox((px,1,pz),(treeSizeHeight-treeSizeWidthDelta,treeSizeHeight+1,treeSizeHeight-treeSizeWidthDelta))
		draw3DTree(schematic, bbox, treeOpts)
	
	sizer = randint(3,7)
	bbox = BoundingBox((centreWidth-width/sizer/2,1,centreDepth-depth/sizer/2),(width/sizer,height-1,depth/sizer))
	City(schematic, bbox, options)
	Hollow(schematic, bbox, options, AIR, False)

	
	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
	print options
	print '%s: Ended at %s' % (method, time.ctime())
	
def VietnameseSnake(level, box, options):
	for iter1 in xrange(1,10):
		for iter2 in xrange(1,10):
			for iter3 in xrange(1,10):
				for iter4 in xrange(1,10):
					for iter5 in xrange(1,10):
						for iter6 in xrange(1,10):
							for iter7 in xrange(1,10):
								for iter8 in xrange(1,10):
									for iter9 in xrange(1,10):
										R = []
										R.append(iter1)
										if not iter2 in R:
											R.append(iter2)
											if not iter3 in R:
												R.append(iter3)
												if not iter4 in R:
													R.append(iter4)	
													if not iter5 in R:
														R.append(iter5)
														if not iter6 in R:
															R.append(iter6)
															if not iter7 in R:
																R.append(iter7)
																if not iter8 in R:
																	R.append(iter8)
																	if not iter9 in R:
																		R.append(iter9)
																		if VietnameseSnakeFunction(iter1,iter2,iter3,iter4,iter5,iter6,iter7,iter8,iter9) == 66.0:
																			print "%s %s %s %s %s %s %s %s %s" % (iter1,iter2,iter3,iter4,iter5,iter6,iter7,iter8,iter9)
													
def VietnameseSnakeFunction(A2, E2, G2, I2, M2, O2, S2, U2, W2):
	C2 = 13.0
	K2 = 12.0
	Q2 = 11.0
	Y2 = 10.0

	result = float(A2)+float(C2)*float(E2)/float(G2)+float(I2)+float(K2)*float(M2)-float(O2)-float(Q2)+float(S2)*float(U2)/float(W2)-float(Y2)
	return result
		
def fillErUp(level, box, options):
	# Testing the fillBlocks method
	method = 'Fill er up'
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	deltaX = randint(1,centreWidth-1)
	deltaY = randint(1,centreHeight-1)
	deltaZ = randint(1,centreDepth-1)
	print deltaX
	print deltaY
	print deltaZ
	bb = BoundingBox((box.minx+deltaX,box.miny+deltaY,box.minz+deltaZ),(width-1-deltaX,height-1-deltaY,depth-1-deltaZ))
	print box
	print bb
	level.fillBlocks(bb,alphaMaterials.Clay)
	
	print '%s: Ended at %s' % (method, time.ctime())
	
def testSpaceTransformation1(level, box, options):
	# Test harness. Draw a circle on a tilted plane
	method = 'testSpaceTransformation1'
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	radius = centreWidth
	if centreDepth < centreWidth:
		radius = centreDepth

	ANGLE = pi/180
	o = (centreWidth, centreHeight, centreDepth)

	# Normal space
	vx = (1.0, 0.0, 0.0)
	vy = (0.0, 1.0, 0.0)
	vz = (0.0, 0.0, 1.0)
	
	phi = 90 # 
	for theta in xrange(0,360):
		p = (radius * cos(theta * ANGLE) * sin(phi * ANGLE), radius * cos(phi * ANGLE), radius * sin(theta * ANGLE) * sin(phi * ANGLE))
		(ptx, pty, ptz) = transformPoint( p, o, vx, vy, vz )
		print '%s %s %s' % (ptx, pty, ptz)
		setBlock(level, (fillMaterialBlock, fillMaterialData), int(box.minx+ptx), int(box.miny+pty), int(box.minz+ptz)) # Learning - need a setBlock that takes a tuple

	# Skewed space
	vx = (0.5, 0.5, 0.0)
	vy = (0.0, 0.5, 0.5)
	vz = (0.5, 0.0, 0.5)
	
	phi = 90 # 
	for theta in xrange(0,360):
		p = (radius * cos(theta * ANGLE) * sin(phi * ANGLE), radius * cos(phi * ANGLE), radius * sin(theta * ANGLE) * sin(phi * ANGLE))
		(ptx, pty, ptz) = transformPoint( p, o, vx, vy, vz )
		print '%s %s %s' % (ptx, pty, ptz)
		setBlock(level, (edgeMaterialBlock, edgeMaterialData), int(box.minx+ptx), int(box.miny+pty), int(box.minz+ptz)) # Learning - need a setBlock that takes a tuple

	# Skewed space 2
	theta = ANGLE * 45.0
	phi = ANGLE * 0.0
	vx = rotateVector( (1.0, 0.0, 0.0), theta, phi)
	vy = rotateVector( (0.0, 1.0, 0.0), theta, phi)
	vz = rotateVector( (0.0, 0.0, 1.0), theta, phi)
	
	phi = 80 # 
	for theta in xrange(0,360):
		p = (radius * cos(theta * ANGLE) * sin(phi * ANGLE), radius * cos(phi * ANGLE), radius * sin(theta * ANGLE) * sin(phi * ANGLE))
		(ptx, pty, ptz) = transformPoint( p, o, vx, vy, vz )
		print '%s %s %s' % (ptx, pty, ptz)
		setBlock(level, (lightMaterialBlock, lightMaterialData), int(box.minx+ptx), int(box.miny+pty), int(box.minz+ptz)) # Learning - need a setBlock that takes a tuple

	print '%s: Ended at %s' % (method, time.ctime())	

def testSpaceTransformation2(level, box, options):
	# Test harness. Draw a butterfly
	method = 'testSpaceTransformation2'
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	radius = centreWidth
	if centreDepth < centreWidth:
		radius = centreDepth

	ANGLE = pi/180
	o = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)

	# Draw a butterfly
	# Body
	material = (fillMaterialBlock, fillMaterialData)

	drawLineWithOffset(level, material, o, (radius/5,0,0),(radius/2,radius/7,radius/7)) # Antenna
	drawLineWithOffset(level, material, o, (radius/5,0,0),(radius/2,radius/7,-radius/7))# Antenna
	drawLineWithOffset(level, material, o, (radius/4,0,0),(radius/5,0,radius/8)) # Body
	drawLineWithOffset(level, material, o, (radius/4,0,0),(radius/5,0,-radius/8)) # Body
	drawLineWithOffset(level, material, o, (radius/5,0,-radius/8),(-radius/2,0,0)) # Body
	drawLineWithOffset(level, material, o, (radius/5,0,radius/8),(-radius/2,0,0)) # Body
	drawLineWithOffset(level, material, o, (radius/4,0,0),(-radius/2,0,0)) # Body
	
	# Front Wing Right - draw in a flat plane, but apply a transformation that lifts the wing above the plane the farther out we go
	vx = (1.0, 0.0, 0.0)
	vy = (0.0, 1.0, 0.0)
	vz = (0.0, 0.7, 1.2)
	step = 0
	stepDelta = radius/2/(90-40)
	for theta in xrange(40,89): # Sweep out an angle of the wing
		d = 1 #sin(theta*2*ANGLE)
		p = ((radius-step) * cos(theta * ANGLE)*d, 0, (radius-step) * sin(theta * ANGLE)*d)
		pt = transformPoint( p, (0,0,0), vx, vy, vz )
		drawLineWithOffset(level, material, o, (radius/9,0,radius/9), pt)
		step = step + stepDelta

	# Front Wing Left - draw in a flat plane, but apply a transformation that lifts the wing above the plane the farther out we go
	vx = (1.0, 0.0, 0.0)
	vy = (0.0, 1.0, 0.0)
	vz = (0.0, -0.7, 1.2)
	step = radius/2
	stepDelta = -radius/2/(90-40)
	for theta in xrange(-89,-40): # Sweep out an angle of the wing
		d = 1 #sin(theta*2*ANGLE)
		p = ((radius-step) * cos(theta * ANGLE)*d, 0, (radius-step) * sin(theta * ANGLE)*d)
		pt = transformPoint( p, (0,0,0), vx, vy, vz )
		drawLineWithOffset(level, material, o, (radius/9,0,-radius/9), pt)
		step = step + stepDelta
		
	material = (edgeMaterialBlock, edgeMaterialData)
	# Rear Wing Right - draw in a flat plane, but apply a transformation that lifts the wing above the plane the farther out we go
	vx = (1.0, -0.1, 0.0)
	vy = (0.0, 1.0, 0.0)
	vz = (0.0, 0.1, 1.0)
	for theta in xrange(91,155): # Sweep out an angle of the wing
		# Add a sin function
		d = 1 #sin(theta*2*ANGLE)
		p = (radius/3*2 * cos(theta * ANGLE)*d, 0, radius/3*2 * sin(theta * ANGLE)*d)
		pt = transformPoint( p, (0,0,0), vx, vy, vz )
		drawLineWithOffset(level, material, o, (radius/9,0,radius/9), pt)

	material = (lightMaterialBlock, lightMaterialData)
	# Rear Wing left - draw in a flat plane, but apply a transformation that lifts the wing above the plane the farther out we go
	vx = (1.0, -0.1, 0.0)
	vy = (0.0, 1.0, 0.0)
	vz = (0.0, -0.1, 1.0)
	for theta in xrange(-155,-91): # Sweep out an angle of the wing
		# Add a sin function
		d = 1 #sin(theta*2*ANGLE)
		p = (radius/3*2 * cos(theta * ANGLE)*d, 0, radius/3*2 * sin(theta * ANGLE)*d)
		pt = transformPoint( p, (0,0,0), vx, vy, vz )
		drawLineWithOffset(level, material, o, (radius/9,0,-radius/9), pt)

	print '%s: Ended at %s' % (method, time.ctime())	

def testSpaceTransformation3(level, box, options):
	# Test harness
	method = 'testSpaceTransformation3'
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	R = centreWidth
	if centreDepth < centreWidth:
		R = centreDepth

	ANGLE = pi/180
	o = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
	
	# Create some shapes
	BUTTERFLY_BODY = []
	material = (fillMaterialBlock, fillMaterialData)
	P1 = (0.5,0,0)
	P2 = (0.3,0.0,0.15)
	P3 = (-0.6,0,0)
	P4 = (0.3,0.1,0.0)
	makeSolid(BUTTERFLY_BODY, material,P1, P2, P3, P4) # Upper
	P5 = (0.3,-0.06,0.0)
	makeSolid(BUTTERFLY_BODY, material,P1, P2, P3, P5) # Lower
	BUTTERFLY_BODY.append( ("Line", material, [(0.5,0,0),(0.7,0.3,0.15)] ) ) # Antenna
	BUTTERFLY_BODY.append( ("Line", material, [(0.3,0.0,0.03),(0.3,-0.1,0.15)] ) ) # Leg
	BUTTERFLY_BODY.append( ("Line", material, [(0.25,0.0,0.03),(0.2,-0.09,0.1)] ) ) # Leg
	BUTTERFLY_BODY.append( ("Line", material, [(0.2,0.0,0.03),(0.1,-0.11,0.1)] ) ) # Leg
	
	BUTTERFLY_FRONTWING = []
	material = (edgeMaterialBlock, edgeMaterialData)
	step = 0
	stepDelta = 0.9/2/(90-40)
	for theta in xrange(40,89): # Sweep out an angle of the wing
		p = ((0.9-step) * cos(theta * ANGLE), 0, (0.9-step) * sin(theta * ANGLE))
		p = transformPoint( p, (0,0,0), [(1.0, 0.0, 0.0),(0.0, 1.0, 0.0),(0.0, 0.7, 1.2)] )
		BUTTERFLY_FRONTWING.append( ("Line", material, [ (0.2,0,0.05), p]) ) # Anchor to the 
		step = step + stepDelta
	
	BUTTERFLY_BACKWING = []
	material = (lightMaterialBlock, lightMaterialData)
	for theta in xrange(91,155): # Sweep out an angle of the wing
		p = (0.9/3*2 * cos(theta * ANGLE), 0, 0.9/3*2 * sin(theta * ANGLE))
		p = transformPoint( p, (0,0,0), [(1.0, -0.1, 0.0),(0.0, 1.0, 0.0),(0.0, 0.3, 1.0)])
		BUTTERFLY_BACKWING.append( ("Line", material, [(0.2,0,0.05), p] ) )

	# Shapes... ASSEMBLE!
#	drawShape(level, box, options, BUTTERFLY_BODY, [(R,0,0),(0,R,0),(0,0,R)], o)
#	drawShape(level, box, options, BUTTERFLY_BODY, [(R,0,0),(0,R,0),(0,0,-R)], o)
#	drawShape(level, box, options, BUTTERFLY_FRONTWING, [(R,0,0),(0,R,0),(0,0,R)], o)
#	drawShape(level, box, options, BUTTERFLY_FRONTWING, [(R,0,0),(0,R,0),(0,0,-R)], o)
#	drawShape(level, box, options, BUTTERFLY_BACKWING, [(R,0,0),(0,R,0),(0,0,R)], o)
#	drawShape(level, box, options, BUTTERFLY_BACKWING, [(R,0,0),(0,R,0),(0,0,-R)], o)

	BUTTERFLY = []
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BODY, [(1,0,0),(0,1,0),(0,0,1)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BODY, [(1,0,0),(0,1,0),(0,0,-1)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_FRONTWING, [(1,0,0),(0,1,0),(0,0,1)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_FRONTWING, [(1,0,0),(0,1,0),(0,0,-1)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BACKWING, [(1,0,0),(0,1,0),(0,0,1)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BACKWING, [(1,0,0),(0,1,0),(0,0,-1)])

	drawShape(level, box, options, BUTTERFLY, [(R,0,0),(0,R,0),(0,0,R)], o)
	
def ButterflyRandom(level, box, options):
	method = 'ButterflyRandom'
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)

	R = centreWidth
	if centreDepth < centreWidth:
		R = centreDepth

	ANGLE = pi/180
	o = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
	materials = [(fillMaterialBlock, randint(0,15)),(edgeMaterialBlock, randint(0,15)),(lightMaterialBlock, randint(0,15))]
	
	# Choose a colour pallette
	print 'Pallette Selection'
	pallette = InteriorDesign_getBalancedColourPallette(1)	
	palletteType = randint(0,100)
	if palletteType >98:
		pallette = InteriorDesign_getRandomColourPallette()
	elif palletteType >50:
		pallette = InteriorDesign_getBalancedColourPallette(randint(2,5))
	print 'Pallette Selection Complete'
	
	triangleType = "Triangle"
	if randint(0,100) > 70:
		triangleType = "Triangledge" # For dragonflies
	
	# Create some shapes
	BUTTERFLY_BODY = []
	material = (fillMaterialBlock, pallette[randint(0,len(pallette)-1)])
	P1 = (0.5,0,0)
	P2 = (0.3,0.0,0.15)
	P3 = (-0.6,0,0)
	P4 = (0.3,0.1,0.0)
	makeSolid(BUTTERFLY_BODY, material,P1, P2, P3, P4) # Upper
	P5 = (0.3,-0.06,0.0)
	makeSolid(BUTTERFLY_BODY, material,P1, P2, P3, P5) # Lower
	material = (fillMaterialBlock, 15) # Black
	BUTTERFLY_BODY.append( ("Line", material, [(0.5,0,0),(0.5+0.1*randint(1,4),0.1*randint(1,4),0.15)] ) ) # Antenna
	BUTTERFLY_BODY.append( ("Line", material, [(0.3,0.0,0.03),(0.3,-0.1,0.15)] ) ) # Leg
	BUTTERFLY_BODY.append( ("Line", material, [(0.25,0.0,0.03),(0.2,-0.09,0.1)] ) ) # Leg
	BUTTERFLY_BODY.append( ("Line", material, [(0.2,0.0,0.03),(0.1,-0.11,0.1)] ) ) # Leg

	materialEdge = (edgeMaterialBlock, randint(0,len(pallette)-1))
	BUTTERFLY_FRONTWING = []
	incline = 0.5*0.05*randint(0,50)
	BUTTERFLY_FRONTWING.append( (triangleType, (edgeMaterialBlock, pallette[randint(0,len(pallette)-1)]), [(0.2,0.0,0.05),(0.2,0.0,0.5),(0.5,0.0,0.6)] ) )
	BUTTERFLY_FRONTWING.append( (triangleType, (edgeMaterialBlock, pallette[randint(0,len(pallette)-1)]), [(0.2,0.0,0.05),(0.5,0.0,0.6),(0.6,0.0,0.6)] ) )
	BUTTERFLY_FRONTWING.append( (triangleType, (edgeMaterialBlock, pallette[randint(0,len(pallette)-1)]), [(0.2,0.0,0.05),(0.6,0.0,0.6),(0.7,0.0,0.55)] ) )
	BUTTERFLY_FRONTWING.append( (triangleType, (edgeMaterialBlock, pallette[randint(0,len(pallette)-1)]), [(0.2,0.0,0.05),(0.7,0.0,0.55),(0.7,0.0,0.4)] ) )
	BUTTERFLY_FRONTWING.append( (triangleType, (edgeMaterialBlock, pallette[randint(0,len(pallette)-1)]), [(0.2,0.0,0.05),(0.7,0.0,0.4),(0.6,0.0,0.25)] ) )
	BUTTERFLY_FRONTWING.append( (triangleType, (edgeMaterialBlock, pallette[randint(0,len(pallette)-1)]), [(0.2,0.0,0.05),(0.6,0.0,0.25),(0.4,0.0,0.15)] ) )
	# Edge
	BUTTERFLY_FRONTWING.append( ("Linesegment", materialEdge, [(0.2,0.0,0.05),(0.2,0.0,0.5),(0.5,0.0,0.6),(0.6,0.0,0.6),(0.7,0.0,0.55),(0.7,0.0,0.4),(0.6,0.0,0.25),(0.4,0.0,0.15),(0.2,0.0,0.05)] ) )
	# Interior edging
	BUTTERFLY_FRONTWING.append( ("Linesegment", materialEdge, [(0.4,0.0,0.55),(0.5,0.0,0.5),(0.6,0.0,0.4),(0.6,0.0,0.25)] ) )
	
	# Highlights
	material = (edgeMaterialBlock, 0) # White
	if randint(0,100) > 70:
		material = (edgeMaterialBlock, 15) # Black
	if randint(0,100) > 50:
		BUTTERFLY_FRONTWING.append( (triangleType, material, [(0.25,0.0,0.1),(0.35,0.0,0.25),(0.5,0.0,0.3)] ) )
	if randint(0,100) > 50:
		BUTTERFLY_FRONTWING.append( (triangleType, material, [(0.25,0.0,0.15),(0.25,0.0,0.45),(0.32,0.0,0.37)] ) )
	if randint(0,100) > 50:
		BUTTERFLY_FRONTWING.append( (triangleType, material, [(0.35,0.0,0.3),(0.4,0.0,0.5),(0.45,0.0,0.45)] ) )
	
	BUTTERFLY_BACKWING = []
	P1 = (0.0,0.0,0.05)
	BUTTERFLY_BACKWING.append( (triangleType, (lightMaterialBlock, pallette[randint(0,len(pallette)-1)]), [P1, (-0.3,0.0,0.4), (-0.3,0.0,0.5)] ) )
	BUTTERFLY_BACKWING.append( (triangleType, (lightMaterialBlock, pallette[randint(0,len(pallette)-1)]), [P1, (-0.3,0.0,0.5), (-0.2,0.0,0.6)] ) )
	BUTTERFLY_BACKWING.append( (triangleType, (lightMaterialBlock, pallette[randint(0,len(pallette)-1)]), [P1, (-0.2,0.0,0.6), (-0.1,0.0,0.65)] ) )
	BUTTERFLY_BACKWING.append( (triangleType, (lightMaterialBlock, pallette[randint(0,len(pallette)-1)]), [P1, (-0.1,0.0,0.65), (0.0,0.0,0.65)] ) )
	BUTTERFLY_BACKWING.append( (triangleType, (lightMaterialBlock, pallette[randint(0,len(pallette)-1)]), [P1, (0.0,0.0,0.65), (0.1,0.0,0.6)] ) )
	BUTTERFLY_BACKWING.append( (triangleType, (lightMaterialBlock, pallette[randint(0,len(pallette)-1)]), [P1, (0.1,0.0,0.05), (0.1,0.0,0.6)] ) )
	BUTTERFLY_BACKWING.append( (triangleType, (lightMaterialBlock, pallette[randint(0,len(pallette)-1)]), [(0.1,0.0,0.05), (0.1,0.0,0.6), (0.2,0.0,0.5)] ) )
	BUTTERFLY_BACKWING.append( (triangleType, (lightMaterialBlock, pallette[randint(0,len(pallette)-1)]), [(0.1,0.0,0.05), (0.2,0.0,0.4), (0.3,0.0,0.05)] ) )
	# Edge
	BUTTERFLY_BACKWING.append( ("Linesegment", materialEdge, [P1, (-0.3,0.0,0.4),(-0.3,0.0,0.5),(-0.2,0.0,0.6),(-0.1,0.0,0.65),(0.0,0.0,0.65),(0.1,0.0,0.6),(0.2,0.0,0.5),(0.2,0.0,0.4), (0.1,0.0,0.05)]))
	# Inner Edge
	BUTTERFLY_BACKWING.append( ("Linesegment", materialEdge, [(-0.3,0.0,0.4), (-0.2,0.0,0.5), (-0.1,0.0,0.55), (-0.0,0.0,0.55), (0.1,0.0,0.5), (0.2,0.0,0.4)]) )

	wingLengthModifier = 0
	if type == "Triangledge": # Used for Dragonflies
		wingLengthModifier = 2.0
		
	# Shapes... ASSEMBLE!
	BUTTERFLY = []
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BODY, [(1+wingLengthModifier,0,0),(0,1,0),(0,0,1)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BODY, [(1+wingLengthModifier,0,0),(0,1,0),(0,0,-1)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_FRONTWING, [(1.0, 0.0, 0.0),(0.0, incline, 0.0),(0.0, incline, 1.7 + wingLengthModifier)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_FRONTWING, [(1.0, 0.0, 0.0),(0.0, incline, 0.0),(0.0, incline, -(1.7 + wingLengthModifier))])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BACKWING, [(1.0, 0.0, 0.0),(0.0, incline/2, 0.0),(0.0, incline/2, 1.0 + wingLengthModifier)])
	buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BACKWING, [(1.0, 0.0, 0.0),(0.0, incline/2, 0.0),(0.0, incline/2, -(1.0+wingLengthModifier))])
	
	if randint(0,100) > 50:
		buildShape(level, box, options, BUTTERFLY, BUTTERFLY_FRONTWING, [(1.0, 0.0, 0.0),(0.0, incline/2, 0.0),(0.0, incline/2, 1.9+wingLengthModifier)])
		buildShape(level, box, options, BUTTERFLY, BUTTERFLY_FRONTWING, [(1.0, 0.0, 0.0),(0.0, incline/2, 0.0),(0.0, incline/2, -(1.9+wingLengthModifier))])
		if randint(0,100) > 50: 
			buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BACKWING, [(1.0, 0.0, 0.0),(0.0, incline/2, 0.0),(0.0, incline/2, 1.5+wingLengthModifier)])
			buildShape(level, box, options, BUTTERFLY, BUTTERFLY_BACKWING, [(1.0, 0.0, 0.0),(0.0, incline/2, 0.0),(0.0, incline/2, -(1.5+wingLengthModifier))])

	drawShape(level, box, options, BUTTERFLY, [(centreWidth,0,0),(0,centreHeight,0),(0,0,centreDepth)], o)
	
	for iterC in xrange(0,len(pallette)):
		setBlock(level, (fillMaterialBlock, pallette[iterC]), box.minx, box.maxy-1, box.minz+iterC)

def scaleToSelection(level, box, options, THESHAPE):
	method = 'scaleToSelection'
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	drawShape(level, box, options, THESHAPE, [(width,0,0),(0,height,0),(0,0,depth)], (box.minx, box.miny, box.minz))
		
def scanSelection(level, box, options):
	method = 'scanSelection'
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	# returns a shape ready for transforming
	# Normalise the dimensions - each block is to be scaled so the whole selection is a factor of the unit cube.
	unitX = 1.0/width
	unitY = 1.0/height
	unitZ = 1.0/depth
	DELTA = 0.0
	THESHAPE = []
	for iterX in xrange(0,width): # Speed up - us PYMCLEVEL methods to do a build fill.
		for iterY in xrange(0,height):
			for iterZ in xrange(0,depth):
				(posnX, posnY, posnZ) = (iterX*unitX, iterY*unitY, iterZ*unitZ)
				material = (level.blockAt(int(box.minx + iterX), int(box.miny+iterY),int(box.minz+iterZ)),level.blockDataAt(int(box.minx + iterX), int(box.miny+iterY),int(box.minz+iterZ)))
				
				THESHAPE.append( ("Triangle", material,
				[(posnX, posnY, posnZ),
				 (posnX+unitX-DELTA, posnY, posnZ),
				 (posnX, posnY+unitY-DELTA, posnZ),
				 ])
				) # Optimise this.
				THESHAPE.append( ("Triangle", material,
				[(posnX+unitX-DELTA, posnY, posnZ),
				 (posnX, posnY+unitY-DELTA, posnZ),
				 (posnX+unitX-DELTA, posnY+unitY-DELTA, posnZ)
				 ])
				) # Optimise this.

				THESHAPE.append( ("Triangle", material,
				[(posnX, posnY, posnZ+unitZ-DELTA),
				 (posnX+unitX-DELTA, posnY, posnZ+unitZ-DELTA),
				 (posnX, posnY+unitY-DELTA, posnZ+unitZ-DELTA),
				 ])
				) # Optimise this.
				THESHAPE.append( ("Triangle", material,
				[(posnX+unitX-DELTA, posnY, posnZ+unitZ-DELTA),
				 (posnX, posnY+unitY-DELTA, posnZ+unitZ-DELTA),
				 (posnX+unitX-DELTA, posnY+unitY-DELTA, posnZ+unitZ-DELTA)
				 ])
				) # Optimise this.
				
				THESHAPE.append( ("Triangle", material,
				[(posnX, posnY, posnZ),
				 (posnX, posnY, posnZ+unitZ-DELTA),
				 (posnX, posnY+unitY-DELTA, posnZ),
				 ])
				) # Optimise this.
				THESHAPE.append( ("Triangle", material,
				[(posnX, posnY+unitY-DELTA, posnZ+unitZ-DELTA),
				 (posnX, posnY, posnZ+unitZ-DELTA),
				 (posnX, posnY+unitY-DELTA, posnZ),
				 ])
				) # Optimise this.
				
				THESHAPE.append( ("Triangle", material,
				[(posnX+unitX-DELTA, posnY, posnZ),
				 (posnX+unitX-DELTA, posnY, posnZ+unitZ-DELTA),
				 (posnX+unitX-DELTA, posnY+unitY-DELTA, posnZ),
				 ])
				) # Optimise this.
				THESHAPE.append( ("Triangle", material,
				[(posnX+unitX-DELTA, posnY+unitY-DELTA, posnZ+unitZ-DELTA),
				 (posnX+unitX-DELTA, posnY, posnZ+unitZ-DELTA),
				 (posnX+unitX-DELTA, posnY+unitY-DELTA, posnZ),
				 ])
				) # Optimise this.

				THESHAPE.append( ("Triangle", material,
				[(posnX, posnY, posnZ),
				 (posnX+unitX-DELTA, posnY, posnZ),
				 (posnX, posnY, posnZ+unitZ-DELTA),
				 ])
				) # Optimise this.
				THESHAPE.append( ("Triangle", material,
				[(posnX+unitX-DELTA, posnY, posnZ+unitZ-DELTA),
				 (posnX+unitX-DELTA, posnY, posnZ),
				 (posnX, posnY, posnZ+unitZ-DELTA),
				 ])
				) # Optimise this.

				THESHAPE.append( ("Triangle", material,
				[(posnX, posnY+unitY-DELTA, posnZ),
				 (posnX+unitX-DELTA, posnY+unitY-DELTA, posnZ),
				 (posnX, posnY+unitY-DELTA, posnZ+unitZ-DELTA),
				 ])
				) # Optimise this.
				THESHAPE.append( ("Triangle", material,
				[(posnX+unitX-DELTA, posnY+unitY-DELTA, posnZ+unitZ-DELTA),
				 (posnX+unitX-DELTA, posnY+unitY-DELTA, posnZ),
				 (posnX, posnY+unitY-DELTA, posnZ+unitZ-DELTA),
				 ])
				) # Optimise this.
				
	return THESHAPE
				
def makeSolid(THESHAPE, material, P1, P2, P3, P4):
	THESHAPE.append( ("Triangle", material, [P1,P2,P3] ) ) # Base
	THESHAPE.append( ("Triangle", material, [P1,P4,P3] ) ) # Vertical
	THESHAPE.append( ("Triangle", material, [P1,P4,P2] ) ) # Front face
	THESHAPE.append( ("Triangle", material, [P4,P2,P3] ) ) # Rear face

def buildShape(level, box, options, RESULTSHAPE, THESHAPE, TRANSFORM):
	for (type, material, points) in THESHAPE:
		if type == "Line":
			p = transformPoint( points[0], (0,0,0), TRANSFORM )
			q = transformPoint( points[1], (0,0,0), TRANSFORM )
			RESULTSHAPE.append( (type, material, [p,q] ) )
		elif type == "Triangle" or type == "Triangledge":
			p = transformPoint( points[0], (0,0,0), TRANSFORM )
			q = transformPoint( points[1], (0,0,0), TRANSFORM )
			r = transformPoint( points[2], (0,0,0), TRANSFORM )
			RESULTSHAPE.append( (type, material, [p,q,r] ) )
		elif type == "Linesegment":
			for index in xrange(0,len(points)-1):
				p = transformPoint( points[index], (0,0,0), TRANSFORM )			
				q = transformPoint( points[index+1], (0,0,0), TRANSFORM )
				RESULTSHAPE.append(("Line", material, [p, q] ))
		else:
			print 'Ignored shape type: %s' % type
	
def drawShape(level, box, options, THESHAPE, TRANSFORM, origin):
	for (type, material, points) in THESHAPE:
		if type == "Line":
			p = transformPoint( points[0], (0,0,0), TRANSFORM )
			q = transformPoint( points[1], (0,0,0), TRANSFORM )
			drawLineWithOffset(level, material, origin, p, q )
		elif type == "Triangle":
			p = transformPoint( points[0], (0,0,0), TRANSFORM )
			q = transformPoint( points[1], (0,0,0), TRANSFORM )
			r = transformPoint( points[2], (0,0,0), TRANSFORM )
			drawTriangleWithOffset(level, box, options, origin, p, q, r, material, material)
		elif type == "Triangledge":
			p = transformPoint( points[0], (0,0,0), TRANSFORM )
			q = transformPoint( points[1], (0,0,0), TRANSFORM )
			r = transformPoint( points[2], (0,0,0), TRANSFORM )
			drawLineWithOffset(level, material, origin, p, q )
			drawLineWithOffset(level, material, origin, q, r )
			drawLineWithOffset(level, material, origin, r, p )
		elif type == "Linesegment":
			for index in xrange(0,len(points)-1):
				p = transformPoint( points[index], (0,0,0), TRANSFORM )			
				q = transformPoint( points[index+1], (0,0,0), TRANSFORM )
				drawLineWithOffset(level, material, origin, p, q )
		elif type == "3DFillRect": # Ignored in build.
			#print points
			(px, py, pz) = transformPoint( points[0], (0,0,0), TRANSFORM )
			(qx, qy, qz) = transformPoint( points[1], (0,0,0), TRANSFORM )
			(ox, oy, oz) = origin
			for iterX in xrange(int(px),int(qx)): # Speed up - us PYMCLEVEL methods to do a build fill.
				print iterX
				for iterY in xrange(int(py),int(qy)):
					for iterZ in xrange(int(pz),int(qz)):
						#print px, py, pz
						setBlock(level, material, int(ox+iterX), int(oy+iterY), int(oz+iterZ))
		else:
			print 'Unknown shape type: %s' % type
	
def drawLineWithOffset( level, material, (ox, oy, oz), (px, py, pz), (qx, qy, qz) ): # Shim for ease of use
	drawLine(level, material,(int(ox+px),int(oy+py),int(oz+pz)), (int(ox+qx),int(oy+qy),int(oz+qz)))

def drawTriangleWithOffset(level, box, options, (ox, oy, oz), (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
	if materialFill != (0,0):
		# for each step along the 'base' draw a line from the apex
		dx = p3x - p2x
		dy = p3y - p2y
		dz = p3z - p2z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)
		
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
			
			iter = iter+0.5 # slightly oversample because I lack faith.
			drawLine(level, materialFill, (ox+px, oy+py, oz+pz), (ox+p1x, oy+p1y, oz+p1z) )
	
	
	drawLine(level, materialEdge, (ox+p1x, oy+p1y, oz+p1z), (ox+p2x, oy+p2y, oz+p2z) )
	drawLine(level, materialEdge, (ox+p1x, oy+p1y, oz+p1z), (ox+p3x, oy+p3y, oz+p3z) )
	drawLine(level, materialEdge, (ox+p2x, oy+p2y, oz+p2z), (ox+p3x, oy+p3y, oz+p3z) )
	
def rotateVector( (x, y, z), theta, phi):
	d1 = sqrt(x*x + z*z) # planar distance
	r = sqrt(d1*d1 + y*y)
	startTheta = atan2(z, x)
	startPhi = acos(y/r)
	return (r * cos(theta+startTheta)*sin(phi+startPhi), r * cos(phi+startPhi), r * sin(theta+startTheta)*sin(phi+startPhi))

def transformPoint( (px, py, pz), (ox, oy, oz), TRANSFORM ):
	# Given the point p in the frame of reference given by Origin o and axis vectors x, y, z, work out where it is in the world
	method = 'Transform Point'
	#print '%s: Started at %s' % (method, time.ctime())
	(xx, xy, xz) = TRANSFORM[0]
	(yx, yy, yz) = TRANSFORM[1]
	(zx, zy, zz) = TRANSFORM[2]
	# What are the distances along each vector for point P in that space defined by those vectors x, y, z?
	(vxx, vxy, vxz) = (px * xx, px * xy, px * xz)
	(vyx, vyy, vyz) = (py * yx, py * yy, py * yz)
	(vzx, vzy, vzz) = (pz * zx, pz * zy, pz * zz)
	# What is the resultant point in 'ordinary cartesian space'
	(rx, ry, rz) = (vxx + vyx + vzx, vxy + vyy + vzy, vxz + vyz + vzz)
	# Now take into account the origin, O, of the space
	(rx, ry, rz) = (rx + ox, ry + oy, rz +oz)

	#print '%s: Ended at %s' % (method, time.ctime())

	return (rx, ry, rz)
	
def Puzzle(level, box, options):
	method = "Puzzle"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)

	# Work out how many pieces we need
	patternSch = level.extractSchematic(box)
	patternBB = analyse(patternSch) # a custom method I wrote to look at how large the non-air object is within the selection
	# .length, .width, .height
	tgtHeight = patternBB.height
	numPieces = int((height - patternBB.height)/patternBB.height)
	# Ok - we need to make some choices about the size of the pieces.
	D = Factorise(numPieces) # find me two numbers that multiply to give the number of pieces X x Y
	d = D[randint(0,len(D)-1)]
	keepGoing = True
	while keepGoing:
		if len(D) > 2 and (d == 1 or d == numPieces):
			d = D[randint(0,len(D)-1)] # try again
		else:
			keepGoing = False
	e = numPieces / d
	# Ok, for good or ill, d x e is the way we'll chop this thing up
	
	y = patternBB.height
	#pieceX = (int)(width / d)
	#pieceZ = (int)(depth / e)
	pieceX = 32
	pieceZ = 32
	for iterX in xrange(0,int(width/pieceX)):
		print '%s: %s of %s' % (method, iterX, int(width/pieceX)-1)
		for iterZ in xrange(0,int(depth/pieceZ)):
			for iterLocalY in xrange(0,patternBB.height):
				for iterC in xrange(0,pieceX):
					for iterD in xrange(0,pieceZ):
						sourceBlock = (level.blockAt(int(box.minx +iterX*pieceX + iterC),
												box.miny+iterLocalY, 
												int(box.minz + iterZ*pieceZ + iterD)),
										level.blockDataAt(int(box.minx +iterX*pieceX + iterC),
												box.miny+iterLocalY, 
												int(box.minz + iterZ*pieceZ + iterD))
								  )# remember to check height
						setBlock(level, sourceBlock, int(box.minx + iterC),
											int(box.miny + y),
											int(box.minz + iterD))
				y = y+1
					
	print '%s: Ended at %s' % (method, time.ctime())

def makeJar(level, box, options):
	# Track two positions. One is the source map, which are blocks in the selection area base that should be wrapped around
	# ... and the second is a target position which is the jar / gourd shape above the block selection area
	#
	method = "makeJar"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)
	AIR = 0
	ONEDEGREE = pi/180
	MAXBASEDEGREE = 160

	# Scan the selection to work out how much space is available for the jar
	patternSch = level.extractSchematic(box)
	patternBB = analyse(patternSch) # a custom method I wrote to look at how large the non-air object is within the selection
	# .length, .width, .height
	tgtHeight = patternBB.height
	
	# For each part of the jar, draw the block at that position using the corresponding block from the original pattern.
	# At this point we know how big the source block pattern is, as well as how high the user has asked for the target 
	
	sourcePosX = 0
	sourcePosZ = 0
	sourcePosY = 0
	
	tgtPosTheta = 0 # longitude
	tgtPosPhi = 0 # latitude
	tgtPosDist = 0 # radius
	
	# Do the bottom "bowl" bit
	radiusBase = centreWidth
	ratio = 3 # Magic - move to options

	wallLength = 2*centreWidth*pi + 2*centreWidth*pi*2/3 + 2*centreWidth/4*pi + 2*centreWidth/4*pi # Number of blocks in the curve of the wall. Lots of magic numbers in here!
	# Now we know what the length of the wall is, we can think about mapping our pattern onto it and drawing out the jar

	# Start plotting:
	theta = 0.0
	dX = 0.0
	dY = 0.0
	dZ = 0.0
	phiF = 0.0
	thetaF = 0.0
	stepSizeAngle = abs(360/(2*pi*centreWidth))
	
	while theta <= 360:
		for phi in xrange(0,MAXBASEDEGREE):
			for iterY in xrange(0,tgtHeight):
				# How many blocks are there around the jar?
				radius = sin(ONEDEGREE*phi)*centreWidth-iterY
				circumference =	abs(int(ceil(2*pi*radius)))
				print '%s: Circumference %s' % (method,circumference)
				sourceBlock = (level.blockAt(int(box.minx + theta*width/360),
											box.miny+iterY, 
											int(box.minz + phi*depth/360)),
								level.blockDataAt(int(box.minx + theta*width/360),
											box.miny+iterY, 
											int(box.minz + phi*depth/360))
							  )# remember to check height
				phiF = phi*ONEDEGREE
				thetaF = theta*ONEDEGREE
				print '%s: PhiF %s, cos(PhiF)=%s sin(phiF)=%s ThetaF %s' % (method, phiF, cos(phiF), sin(phiF), thetaF)
				dX = centreWidth + radius*cos(thetaF)
				dY = tgtHeight + centreHeight-centreHeight*0.65*cos(phiF)
				dZ = centreDepth + radius*sin(thetaF)
				setBlock(level, sourceBlock, int(box.minx + dX),
										int(box.miny + dY),
										int(box.minz + dZ))

			# That's the base. Now do the 'lip' which curves outwards
			# For each theta, cast a concave arc outwards from the position last calculated

		for lipPhi in xrange(0,360-MAXBASEDEGREE):
			lipRadius = radius / 3
			# dX, dY, and dZ are set to the position of the last block placed. I can base the next bit on them.
			# Work out the position to draw the lip...
			sourceBlock = (level.blockAt(int(box.minx + theta*width/360),
									box.miny, 
									int(box.minz + (phi+lipPhi)*depth/360)),
						level.blockDataAt(int(box.minx + theta*width/360),
									box.miny, 
									int(box.minz + (phi+lipPhi)*depth/360))
					  )# remember to check height
			dX2 = -lipRadius*cos(thetaF)*sin(ONEDEGREE*lipPhi)
			dZ2 = -lipRadius*sin(thetaF)*sin(ONEDEGREE*lipPhi)
			dY2 = 2*lipRadius-2*lipRadius*cos(ONEDEGREE*lipPhi)+lipRadius-3
			setBlock(level, sourceBlock, int(box.minx + dX+dX2),
										int(box.miny + dY+dY2),
										int(box.minz + dZ+dZ2))
		theta = theta + stepSizeAngle
	
	
	
#	for iterY in xrange(0,height):
#		for iterZ in xrange(0,depth):
#			for iterX in xrange(0,width):
#				tempBlock = level.blockAt(box.minx + iterX, box.miny + iterY, box.minz + iterZ)
#				if tempBlock != AIR:
#					maxY = iterY
	
	return True
	
def InteriorDesign(level, box, options):
	# Given a selection area
	# Locate a bounded region within the area
	# Create an interior design consisting of:
	#     Cupboards
	#     Benches
	#     Carpet
	#     Furniture
	#     Wall designs
	#     Plants
	#     Windows
	#     Features
	
	method = "InteriorDesign"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)

	# ----------------------------
	
	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Because Rubisk says I write inefficient code :[

	# Choose a colour pallette
	print 'Pallette Selection'
	pallette = InteriorDesign_getBalancedColourPallette(1)	
	palletteType = randint(0,100)
	if palletteType >98:
		pallette = InteriorDesign_getRandomColourPallette()
	elif palletteType >50:
		pallette = InteriorDesign_getBalancedColourPallette(randint(2,5))
	print 'Pallette Selection Complete'

	print 'Space mapping'
	blockProperties = InteriorDesign_AnalyseRoom(schematic) # Determine the distance to walls for each block
	print 'Space mapping complete'
	
	floorBase = 0
	while floorBase < height:
		print 'Checking for floor, base is %s %s %s' % (floorBase, blockProperties[centreWidth,floorBase,centreDepth,4],blockProperties[centreWidth,floorBase,centreDepth,6])
		# Find a floor! A solid block with two layers of air above
		if blockProperties[centreWidth,floorBase,centreDepth,6] != 0 and blockProperties[centreWidth,floorBase,centreDepth,4] > 2:
			# Found what might be a room layer
			(x,y,z) = (centreWidth, floorBase+1, centreDepth)
			
			roomTypeRand = randint(0,100)
			
			if roomTypeRand < 50:
				# Kitchen ---------------------------------------------------------------------------
				kTypeRand = randint(1,6) * 20
				if y < height:
					print 'Kitchen 1'
					InteriorDesign_KitchenBenches(schematic, pallette, blockProperties, x,y,z,kTypeRand)
				if y+2 < height:
					print 'Kitchen 2'
					InteriorDesign_KitchenBenches(schematic, pallette, blockProperties, x,y+2,z,kTypeRand)
			
			# Carpet ----------------------------------------------------------------------------
			# Magic numbers for block IDs
			MAT_CARPET_ID = 171 # Is this in a new Materials file?
			
			# Spiral out the floor with carpet
			carpetStyle = randint(0,100)
			if carpetStyle > 90:
				(x,y,z) = (centreWidth, floorBase+1, centreDepth)
				MAXLENGTH = (width+depth) / 2
				length = randint(5, MAXLENGTH)
				dir = 1
				InteriorDesign_spiralCarpet(schematic,MAT_CARPET_ID,pallette,x,y,z,dir,length)
				InteriorDesign_spiralCarpet(schematic,MAT_CARPET_ID,pallette,x,y,z-1,dir+2,length)
			else:
				(x,y,z) = (centreWidth, floorBase+1, centreDepth)
				MAXLENGTH = (width+depth) / 2
				length = randint(5, MAXLENGTH)
				dir = 1
				InteriorDesign_chequerCarpet(schematic,MAT_CARPET_ID,pallette,x,y,z,dir,length)
				InteriorDesign_chequerCarpet(schematic,MAT_CARPET_ID,pallette,x,y,z-1,dir+2,length)

			floorBase = floorBase+3 # Height of kitchen
			
		floorBase = floorBase+1
	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
	return True

def getRandomItemId():
	# Simple algorithm - random id
	id = randint(0,5000)
	blockIDstr = str(id)
	if blockIDstr in ITEMNAMES:
		return blockIDstr
	else:
		return "280" # stick
	
def InteriorDesign_KitchenBenches(schematic, pallette, blockProperties, x, y, z, frequency):
	# Benches - For each wall, find a space
	# Magic numbers for block IDs
	MAT_CARPET_ID = 171 # Is this in a new Materials file?
	CARPETCOL = randint(0,len(pallette)-1)
	MAT_FURNACE_ID = 61
	MAT_CAULDRON = 118
	AIR = 0
	PASSAGESIZE = 3
	(width,height,depth) = schematic.size
	
	
	for iterX in xrange(0,width):
		for iterZ in xrange(0,depth):
			# print '%s %s %s %s' % (iterX,y,iterZ, blockProperties[x,y,z,0])
			if blockProperties[iterX,y,iterZ,6] != AIR:
				chanceOfBlock = randint(1,100)
				if blockProperties[iterX,y,iterZ,0] > PASSAGESIZE and blockProperties[iterX,y,(iterZ-1)%depth,6] == AIR and blockProperties[(iterX+1)%width,y,iterZ,6]!=AIR and blockProperties[(iterX-1)%width,y,iterZ,6] != AIR and blockProperties[iterX,(y-1)%height,iterZ,6] != AIR and blockProperties[(iterX-1)%width,(y-1)%height,iterZ,6] != AIR and blockProperties[(iterX+1)%width,(y-1)%height,iterZ,6] != AIR:
					if randint(1,100) > 95:
						if chanceOfBlock < frequency: setBlock(schematic, (MAT_FURNACE_ID, 2), iterX, y, (iterZ-1)%depth)
					elif randint(1,100) >95:
						if blockProperties[iterX,(y-1)%height,(iterZ-1)%depth,6] != AIR:
							if chanceOfBlock < frequency: setBlock(schematic, (MAT_CAULDRON, 0), iterX, y, (iterZ-1)%depth)
					else:
						if chanceOfBlock < frequency: createChestBlockDataWithItems(schematic, 2, iterX, y, (iterZ-1)%depth) # NOTE: Need to add contents to the chest
					if blockProperties[iterX,(y+1)%height,(iterZ-1)%depth,6] == AIR and getBlock(schematic,iterX,y,(iterZ-1)%depth) != (MAT_CAULDRON,0):
						if chanceOfBlock < frequency: setBlock(schematic, (MAT_CARPET_ID, CARPETCOL), iterX, (y+1)%height, (iterZ-1)%depth)
					
				if blockProperties[iterX,y,iterZ,2] > PASSAGESIZE and blockProperties[iterX,y,(iterZ+1)%depth,6] == AIR and blockProperties[(iterX+1)%width,y,iterZ,6]!=AIR and blockProperties[(iterX-1)%width,y,iterZ,6]!=AIR and blockProperties[iterX,(y-1)%height,iterZ,6] != AIR and blockProperties[(iterX-1)%width,(y-1)%height,iterZ,6] != AIR and blockProperties[(iterX+1)%width,(y-1)%height,iterZ,6] != AIR: 
					if randint(1,100) > 95:
						if chanceOfBlock < frequency: setBlock(schematic, (MAT_FURNACE_ID, 3), iterX, y, (iterZ+1)%depth)
					elif randint(1,100) >95:
						if blockProperties[iterX,(y-1)%height,(iterZ+1)%depth,6] != AIR:
							if chanceOfBlock < frequency: setBlock(schematic, (MAT_CAULDRON, 0), iterX, y, (iterZ+1)%depth)
					else:
						if chanceOfBlock < frequency: createChestBlockDataWithItems(schematic, 3, iterX, y, (iterZ+1)%depth) # NOTE: Need to add contents to the chest
					if blockProperties[iterX,(y+1)%height,(iterZ+1)%depth,6] == AIR and getBlock(schematic,iterX,y,(iterZ+1)%depth) != (MAT_CAULDRON,0):
						if chanceOfBlock < frequency: setBlock(schematic, (MAT_CARPET_ID, CARPETCOL), iterX, (y+1)%height, (iterZ+1)%depth)

				if blockProperties[iterX,y,iterZ,3] > PASSAGESIZE and blockProperties[(iterX-1)%width,y,iterZ,6] == AIR and blockProperties[iterX,y,(iterZ+1)%depth,6]!=AIR and blockProperties[iterX,y,(iterZ-1)%depth,6]!=AIR and blockProperties[iterX,(y-1)%height,iterZ,6] != AIR and blockProperties[iterX,(y-1)%height,(iterZ+1)%depth,6] != AIR and blockProperties[iterX,(y-1)%height,(iterZ-1)%depth,6] != AIR:
					if randint(1,100) > 95:
						if chanceOfBlock < frequency: setBlock(schematic, (MAT_FURNACE_ID, 4), (iterX-1)%width, y, iterZ)
					elif randint(1,100) >95:
						if blockProperties[ (iterX-1)%width,(y-1)%height,iterZ,6] != AIR:
							if chanceOfBlock < frequency: setBlock(schematic, (MAT_CAULDRON, 0), (iterX-1)%width, y, iterZ)
					else:
						if chanceOfBlock < frequency: createChestBlockDataWithItems(schematic, 4, (iterX-1)%width, y, iterZ) # NOTE: Need to add contents to the chest
					if blockProperties[(iterX-1)%width,(y+1)%height,iterZ,6] == AIR and getBlock(schematic,(iterX-1)%width,y,iterZ) != (MAT_CAULDRON,0):
						if chanceOfBlock < frequency: setBlock(schematic, (MAT_CARPET_ID, CARPETCOL), (iterX-1)%width, (y+1)%height, iterZ)
	
				if blockProperties[iterX,y,iterZ,1] > PASSAGESIZE and blockProperties[iterX+1,y,iterZ,6] == AIR and blockProperties[iterX,y,(iterZ+1)%depth,6]!=AIR and blockProperties[iterX,y,(iterZ-1)%depth,6]!=AIR and blockProperties[iterX,(y-1)%height,iterZ,6] != AIR and blockProperties[iterX,(y-1)%height,(iterZ+1)%depth,6] != AIR and blockProperties[iterX,(y-1)%height,(iterZ-1)%depth,6] != AIR: 
					if randint(1,100) > 95:
						if chanceOfBlock < frequency: setBlock(schematic, (MAT_FURNACE_ID, 5), (iterX+1)%width, y, iterZ)
					elif randint(1,100) >95:
						if blockProperties[ (iterX+1)%width,(y-1)%height,iterZ,6] != AIR:
							if chanceOfBlock < frequency: setBlock(schematic, (MAT_CAULDRON, 0), (iterX+1)%width, y, iterZ)
					else:
						if chanceOfBlock < frequency: createChestBlockDataWithItems(schematic, 5, (iterX+1)%width, y, iterZ) # NOTE: Need to add contents to the chest
					if blockProperties[(iterX+1)%width,(y+1)%height,iterZ,6] == AIR and getBlock(schematic,(iterX+1)%width,y,iterZ) != (MAT_CAULDRON,0):
						if chanceOfBlock < frequency: setBlock(schematic, (MAT_CARPET_ID, CARPETCOL), (iterX+1)%width, (y+1)%height, iterZ)
			
def createChestBlockDataWithItems(level, dir, x, y, z):
	SLOTS = 27
	items = []

	if randint(0,100) > 70:
		# build a list from a selection of Common items
		numberOfItems = randint(0,(int)(SLOTS/2))
		for item in xrange(numberOfItems):
			items.append(ITEMS_COMMON[randint(0,len(ITEMS_COMMON)-1)]) # @Codewarrior0 says "use random.choice"

	if randint(0,100) > 90:
		# build a list from a selection of Rare items
		numberOfItems = randint(0,4)
		for item in xrange(numberOfItems):
			items.append(ITEMS_RARE[randint(0,len(ITEMS_RARE)-1)])

	if randint(0,100) > 95:
		# build a list from a selection of Very Rare items
		numberOfItems = randint(0,2)
		for item in xrange(numberOfItems):
			items.append(ITEMS_VERYRARE[randint(0,len(ITEMS_VERYRARE)-1)])

	if randint(0,100) > 98:
		# build a list from a selection of Unique items
		items.append(ITEMS_UNIQUE[randint(0,len(ITEMS_UNIQUE)-1)])

	createChestBlockData(level, dir, x, y, z, items)
			
def createChestBlockData(level, dir, x, y, z, items): #, blockID, maxData):
	#Choose a chest type that won't conflict with it's neighbours
	chID = CHEST_ID = 54
	TCHEST_ID = 146
	if (x+y+z) % 2 == 1:
		chID = TCHEST_ID

	SLOTS = 27
	chunk = level.getChunk(x/CHUNKSIZE, z/CHUNKSIZE)
	
	setBlock(level, (chID,dir), x, y, z)
	e = TAG_Compound()
	e["x"] = TAG_Int(x)
	e["y"] = TAG_Int(y)
	e["z"] = TAG_Int(z)
	e["id"] = TAG_String("Chest")
	e["Lock"] = TAG_String("")
	e["Items"] = TAG_List()
	# Item access below modified from @Texelelf's MapIt filter
	item = TAG_Compound()
	item["id"] = TAG_String("minecraft:stone")
	item["Count"] = TAG_Byte(1)
	item["Damage"] = TAG_Short(0)
	item["Slot"] = TAG_Byte(randint(0,27))
	for theItem in items:
		print '%s' % (theItem)
		newitem = deepcopy(item)
		newitem["id"] = TAG_String(theItem)
		item["Count"] = TAG_Byte(1)
		newitem["Slot"] = TAG_Byte(randint(0,SLOTS))
		newitem["Damage"] = TAG_Short(0)
		e["Items"].append(newitem)
		chunk.TileEntities.append(e)
	return e
		
def InteriorDesign_AnalyseRoom(schematic):
	(width, height, depth) = schematic.size
	AIR = 0
	BIGNUMBER = 1000000000
	
	blockProperties = zeros((width,height,depth,8)) # N, E, S, W, U, D, BlockID, BlockData

	for iterY in xrange(0,height):
		for iterX in xrange(0,width):
			for iterZ in xrange(0,depth):
				blockProperties[iterX,iterY,iterZ,6] = schematic.blockAt(iterX,iterY,iterZ)
				blockProperties[iterX,iterY,iterZ,7] = schematic.blockDataAt(iterX,iterY,iterZ)
				# for each block, walk in each direction and count how much air there is until we hit a wall
				
				dist = -1 # default for 'no wall found'
				blockProperties[iterX,iterY,iterZ,0] = dist
				# north
				if iterZ > 0:
					iterStep = 1
					while iterStep < iterZ+1:
					#for iterStep in xrange(1,iterZ+1):
						if schematic.blockAt(iterX,iterY,iterZ-iterStep) == AIR: # void, count it
							dist = dist +1
						else:
							dist = dist +1
							iterStep = BIGNUMBER # break loop
							blockProperties[iterX,iterY,iterZ,0] = dist
						iterStep = iterStep +1
#						print 'iterStep 1'
				
				dist = -1 # default for 'no wall found'
				blockProperties[iterX,iterY,iterZ,1] = dist
				# east
				if iterX < width-1:
					iterStep = iterX+1
					while iterStep < width:
					#for iterStep in xrange(iterX+1,width):
						if schematic.blockAt(iterStep,iterY,iterZ) == AIR: # void, count it
							dist = dist +1
						else:
							dist = dist +1
							iterStep = BIGNUMBER # break loop
							blockProperties[iterX,iterY,iterZ,1] = dist
						iterStep = iterStep +1
#						print 'iterStep 2'
						
				dist = -1 # default for 'no wall found'
				blockProperties[iterX,iterY,iterZ,2] = dist
				# south
				if iterZ < depth-1:
					iterStep = iterZ+1
					while iterStep < depth:
					#for iterStep in xrange(iterZ+1,depth):
						if schematic.blockAt(iterX,iterY,iterStep) == AIR: # void, count it
							dist = dist +1
						else:
							dist = dist +1
							iterStep = BIGNUMBER # break loop
							blockProperties[iterX,iterY,iterZ,2] = dist
						iterStep = iterStep +1
#						print 'iterStep 3'
						
				dist = -1 # default for 'no wall found'
				blockProperties[iterX,iterY,iterZ,3] = dist
				# west
				if iterX > 0:
					iterStep = 1
					while iterStep < iterX+1:
					#for iterStep in xrange(1,iterX+1):
						if schematic.blockAt(iterX-iterStep,iterY,iterZ) == AIR: # void, count it
							dist = dist +1
						else:
							dist = dist +1
							iterStep = BIGNUMBER # break loop
							blockProperties[iterX,iterY,iterZ,3] = dist
						iterStep = iterStep +1
#						print 'iterStep 4'
						
				dist = -1 # default for 'no wall found'
				blockProperties[iterX,iterY,iterZ,4] = dist
				# up
				if iterY < height-1:
					iterStep = iterY+1
					while iterStep < height:
					# for iterStep in xrange(iterY,height):
						if schematic.blockAt(iterX,iterStep,iterZ) == AIR: # void, count it
							dist = dist +1
						else:
							dist = dist +1
							iterStep = BIGNUMBER # break loop
							blockProperties[iterX,iterY,iterZ,4] = dist
						iterStep = iterStep +1
#						print 'iterStep 5'
#				print 'iterStep 5 complete'		
				dist = -1 # default for 'no wall found'
				blockProperties[iterX,iterY,iterZ,5] = dist
				# down
				if iterY > 0:
					iterStep = 1
					while iterStep < iterY+1:
					#for iterStep in xrange(1,iterY+1):
						if schematic.blockAt(iterX,iterY-iterStep,iterZ) == AIR: # void, count it
							dist = dist +1
						else:
							dist = dist +1
							iterStep = BIGNUMBER # break loop
							blockProperties[iterX,iterY,iterZ,5] = dist
						iterStep = iterStep +1
#						print 'iterStep 6'
					
	return blockProperties
	
def InteriorDesign_cupboards(schematic,pallette,x,y,z,dir,length):
	# Make benches around the edge of the wall sections. Line them with carpet. Add cupboards on top. Put things in them.

	AIR = (0,0)
	CARPET_ID = 171
	CHEST_ID = 54
	TCHEST_ID = 146
	
	CARPETCOL = randint(0,len(pallette)-1)
	
	for iterR in xrange(0, length):
		for steps in xrange(0,iterR-1):
			(bid,bdata) = tempBlock = getBlock(schematic,x,y,z)
			print '%s %s' % (iterR,steps)
			if tempBlock != AIR and bid != CARPET_ID:
				if dir == 1:
					if (x+z)%2 == 0:
						setBlockIfEmpty(schematic,(CHEST_ID,1),x,y,z+1)
					else:
						setBlockIfEmpty(schematic,(TCHEST_ID,1),x,y,z+1)
				if dir == 2:
					if (x+z)%2 == 0:
						setBlockIfEmpty(schematic,(CHEST_ID,1),x-1,y,z)
					else:
						setBlockIfEmpty(schematic,(TCHEST_ID,1),x-1,y,z)
				if dir == 3:
					if (x+z)%2 == 0:
						setBlockIfEmpty(schematic,(CHEST_ID,1),x,y,z-1)
					else:
						setBlockIfEmpty(schematic,(TCHEST_ID,1),x,y,z-1)
				if dir == 4:
					if (x+z)%2 == 0:
						setBlockIfEmpty(schematic,(CHEST_ID,1),x+1,y,z)
					else:
						setBlockIfEmpty(schematic,(TCHEST_ID,1),x+1,y,z)

			if dir == 1:
				x = x+1
			if dir == 2:
				z = z+1
			if dir == 3:
				x = x-1
			if dir == 4:
				z = z-1
		if dir == 1:
			dir = 2
		elif dir == 2:
			dir = 3
		elif dir == 3:
			dir = 4
		else:
			dir = 1

def InteriorDesign_spiralCarpet(schematic,blockID,pallette,x,y,z,dir,length):
	AIR = (0,0)

	CARPETCOL = randint(0,len(pallette)-1)
	for iterR in xrange(0, length):
		for steps in xrange(0,iterR-1):
			tempBlock = getBlock(schematic,x,y,z)
			if tempBlock == AIR:
				setBlock(schematic,(blockID,(int)(pallette[CARPETCOL])),x,y,z)
			else:
				iterR = length
				break
			if dir == 1:
				x = x+1
			if dir == 2:
				z = z+1
			if dir == 3:
				x = x-1
			if dir == 4:
				z = z-1
		if dir == 1:
			dir = 2
		elif dir == 2:
			dir = 3
		elif dir == 3:
			dir = 4
		else:
			dir = 1

def InteriorDesign_chequerCarpet(schematic,blockID,pallette,x,y,z,dir,length):
	# Magic numbers for block IDs
	MAT_CARPET_ID = 171 # Is this in a new Materials file?
	AIR = (0,0)

	CARPETCOL1 = randint(0,len(pallette)-1)
	CARPETCOL2 = randint(0,len(pallette)-1)
	CARPETCOL3 = randint(0,len(pallette)-1)
	for iterR in xrange(0, length):
		for steps in xrange(0,iterR-1):
			tempBlock = getBlock(schematic,x,y,z)
			if tempBlock == AIR:
				if (x+z)%3 == 0:
					setBlock(schematic,(blockID,(int)(pallette[CARPETCOL1])),x,y,z)
				if (x+z)%3 == 1:
					setBlock(schematic,(blockID,(int)(pallette[CARPETCOL2])),x,y,z)
				if (x+z)%3 == 2:
					setBlock(schematic,(blockID,(int)(pallette[CARPETCOL3])),x,y,z)				
			else:
				iterR = length
				break
			if dir == 1:
				x = x+1
			if dir == 2:
				z = z+1
			if dir == 3:
				x = x-1
			if dir == 4:
				z = z-1
		if dir == 1:
			dir = 2
		elif dir == 2:
			dir = 3
		elif dir == 3:
			dir = 4
		else:
			dir = 1

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))
	
def InteriorDesign_getRandomColourPallette():
	colours = "15 7 8 0 6 2 10 11 3 9 13 5 4 1 14 12".split() # I like this sequence
	coloursList = map(int, colours)
	coloursListLen = len(coloursList)
	baseIndex = randint(0,coloursListLen)
	pallette = zeros(randint(3,5))
	gap = randint(0,coloursListLen-1)
	for iterC in xrange(0,len(pallette)):
		pallette[iterC] = (int)(coloursList[(baseIndex+iterC*gap)%coloursListLen])
	return pallette

def InteriorDesign_getBalancedColourPallette(gap):
	colours = "15 7 8 0 6 2 10 11 3 9 13 5 4 1 14 12".split() # I like this sequence
	coloursList = map(int, colours)
	coloursListLen = len(coloursList)
	baseIndex = randint(0,coloursListLen)
	pallette = zeros(randint(3,5))
	for iterC in xrange(0,len(pallette)):
		pallette[iterC] = (int)(coloursList[(baseIndex+iterC*gap)%coloursListLen])
	return pallette
	
def Lines(level, box, options):
	(width, height, depth) = getBoxSize(box)
	material = (fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	
	W = Factorise(width/8)
	w = W[randint(0,len(W)-1)]
	D = Factorise(depth/8)
	d = D[randint(0,len(D)-1)]
	H = Factorise(height/8)
	h = H[randint(0,len(H)-1)]
	#w = d = h = 0
	if w == 0:
		w = 5
	if d == 0:
		d = 5
	if h == 5:
		h = 5
		
	
	iterX1 = 0
	iterZ1 = depth
	while iterX1 < width and iterZ1 > 0:
		print '%s' % (iterX1)
		drawLine(level, material,(box.minx+iterX1,box.miny,box.minz), (box.minx,box.miny,box.minz+iterZ1))
		iterX1 = iterX1 + w
		iterZ1 = iterZ1 - d
					
def MobRidingMatrix(level, box, options):
	MOBS = [ 
			"Villager",
			"VillagerGolem",
			"SnowMan",
			"EntityHorse",
			"Cow",
			"MushroomCow",
			"Sheep",
			"Pig",
			"Wolf",
			"Ozelot",
			"Chicken",
			"Rabbit",
			"Squid",
			"Bat",
			
			"Slime",
			"LavaSlime",
			"Blaze",
			"Silverfish",
			"Spider",
			"CaveSpider",
			"Zombie",
			"PigZombie",
			"Witch",
			"Skeleton",
			"Creeper",
			"Enderman",
			"Endermite",
			"Ghast",
			"Giant",
			"Guardian",
			"WitherBoss",
			"EnderDragon",

			"MinecartRideable",
			"MinecartHopper",
			"MinecartFurnace",
			"MinecartChest",
			"MinecartSpawner",
			"Boat",
			"Painting",
			"ArmorStand",
			"EnderCrystal",
			
			"Item",
			"LeashKnot",
			"Arrow",
			"SmallFireball",
			"Fireball",
			"FireworksRocketEntity",
			"WitherSkull",
			"ThrownExpBottle",
			"Snowball",
			"ThrownPotion",
			"ThrownEnderpearl",
			"EyeOfEnderSignal",
			"LightningBolt"
				
	
#			"Chicken",
#			"Cow",
#			"Ozelot",
#			"Pig",
#			"Sheep",
#			"Rabbit",
#			"EntityHorse",
#			"Squid",
#			"Bat",
#			"Villager",
#			"MushroomCow",
#			"CaveSpider",
#			"Enderman",
#			"Endermite",
#			"Spider",
#			"Wolf",
#			"PigZombie",
#			"Blaze",
#			"Creeper",
#			"Ghast",
#			"LavaSlime",
#			"Silverfish",
#			"Skeleton",
#			"Slime",
#			"Witch",
#			"WitherSkeleton",
#			"Zombie",
#			"ZombieVillager",
#			"ChickenJockey",
#			"SnowMan",
#			"VillagerGolem",
#			"Giant",
#			"WitherBoss"
#			"EnderDragon"
			]
	colours = "15 7 8 0 6 2 10 11 3 9 13 5 4 1 14 12".split()
	coloursList = map(int, colours)
			
	# CONSTANTS AND GLOBAL VARIABLES
	method = "MobRidingMatrix"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	COMMANDBLOCK = (137,0)
	STONE_BUTTON = (77,5)
	CHUNKSIZE = 16
	edgeMaterial = (edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	material = (fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	lightMaterial = (lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)

	iterX = 0
	iterY = 0
	iterZ = 5
	for rider in MOBS:
		offset = ""
		(dX, dY, dZ) = (box.minx+iterX+iterZ%2*2, box.miny+iterY, box.minz+iterZ)
		chunk = level.getChunk(dX/CHUNKSIZE, dZ/CHUNKSIZE)
		setBlock(level, COMMANDBLOCK, dX, dY, dZ)
		if rider == "Ghast":
			offset = "-5"
		theCommand = "summon "+rider+" ~"+offset+" ~2 ~ {NoAI:1,CustomName:Rider"+rider+",Invulnerable:1,PersistenceRequired:1,direction:[90.0,0.0,0.0],Motion:[0.0,0.0,0.0],Riding:{id:ArmorStand,Marker:1,NoGravity:1,Invulnerable:1,direction:[90.0,0.0,0.0]},Template:1}"
		chunk.TileEntities.append(createCommandBlockData(dX, dY, dZ, theCommand))
		chunk.dirty = True
		setBlock(level, lightMaterial, dX, dY+1, dZ)
		setBlock(level, STONE_BUTTON, dX, dY+2, dZ)
		iterZ = iterZ + 1
		
	iterX = 5
	iterY = 0
	iterZ = 0
	for ridden in MOBS:
		offset = ""
		(dX, dY, dZ) = (box.minx+iterX, box.miny+iterY, box.minz+iterZ+iterX%2*2)
		chunk = level.getChunk(dX/CHUNKSIZE, dZ/CHUNKSIZE)
		setBlock(level, COMMANDBLOCK, dX, dY, dZ)
		if ridden == "Ghast":
			offset = "-5"
		theCommand = "summon "+ridden+" ~ ~2 ~"+offset+" {NoAI:1,CustomName:Ridden"+ridden+",Invulnerable:1,PersistenceRequired:1,direction:[0.0,0.0,0.0],Motion:[0.0,0.0,0.0],Riding:{id:ArmorStand,Marker:1,NoGravity:1,Invulnerable:1},Template:1}"
		chunk.TileEntities.append(createCommandBlockData(dX, dY, dZ, theCommand))
		chunk.dirty = True
		setBlock(level, lightMaterial, dX, dY+1, dZ)
		setBlock(level, STONE_BUTTON, dX, dY+2, dZ)
		iterX = iterX +1

	iterX = 5
	iterY = 0
	iterZ = 5	
	for rider in MOBS:
		iterX = 5
		for ridden in MOBS:
			(dX, dY, dZ) = (box.minx+iterX, box.miny+iterY, box.minz+iterZ)
			chunk = level.getChunk(dX/CHUNKSIZE, dZ/CHUNKSIZE)
			theCommand = "summon "+rider+" ~ ~2 ~ {Riding:{id:"+ridden+",Invulnerable:1,PersistenceRequired:1,direction:[0.0,0.0,0.0],Motion:[0.0f,0.0f,0.0f],CustomName:"+"Ridden"+ridden+",Spliced:1},CustomName:"+rider+"Riding"+ridden+",Invulnerable:1,PersistenceRequired:1,direction:[0.0,0.0,0.0],Motion:[0.0f,0.0f,0.0f],Spliced:1}"
			chunk.TileEntities.append(createCommandBlockData(dX, dY, dZ, theCommand))
			chunk.dirty = True
			setBlock(level, COMMANDBLOCK, dX, dY, dZ)
			if (iterZ)%2 == 0:	
				setBlock(level, (fillMaterialBlock,coloursList[iterX%16]), dX, dY+1, dZ)
			else:
				setBlock(level, (edgeMaterialBlock,coloursList[iterX%16]), dX, dY+1, dZ)
			setBlock(level, STONE_BUTTON, dX, dY+2, dZ)
			iterX = iterX + 1
		iterZ = iterZ+1
	print '%s: Ended at %s' % (method, time.ctime())	

def ChunkChequers(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	material = (fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)

	CHUNKSIZE = 16
	
	for iterY in xrange(0,height):
		print '%s: Layer %s of %s' % (method,iterY+1,height)
		for iterZ in xrange(0,depth):
			for iterX in xrange(0,width):
				#			drawLine(level, material,
	#						(box.minx+width-1,box.miny,box.minz+iter), 
	#						(box.minx+width-1,box.miny+randint(1,height-1),box.minz+iter))
				CHUNKX = (int)((box.minx+iterX)/CHUNKSIZE)
				CHUNKZ = (int)((box.minz+iterZ)/CHUNKSIZE)
				CHUNKY = (int)((box.miny+iterY)/CHUNKSIZE)

				if (CHUNKX + CHUNKZ +CHUNKY) % 2 == 0:
					setBlock(level, (fillMaterialBlock, fillMaterialData), box.minx+iterX, box.miny+iterY, box.minz+iterZ)
				else:
					setBlock(level, (edgeMaterialBlock, edgeMaterialData), box.minx+iterX, box.miny+iterY, box.minz+iterZ)
	
def Forest(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	
	# Work out how 'big' to build. Loosely explained, this affects the number of floors in each module
	MINSIZE = 8 # Residential is if the maximum dimension of the selection box is less than 12 times this number (i.e. 48 when drafting this code)
	buildType = height
	if width > buildType:
		buildType = width
	if depth > buildType:
		buildType = depth
	if buildType > MINSIZE * 12:
		MINSIZE = MINSIZE * 2 # Commercial
	
	# Places random buildings radially within the selection box
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	O = (box.minx+centreWidth, box.miny, box.minz+centreDepth) # Origin

	# buildings = (width + height + depth) / 3
	buildings = height
	buildings = randint(buildings/2,buildings*MINSIZE)+1
	
	for iter in xrange(1,buildings):
		print 'Constructing forest %s of %s' % (iter,buildings)
		r = randint(0,centreWidth/8*7)
		theta = randint(0,360)*angleSize
		phi = 0 * angleSize #randint (0,360)*angleSize
		(x1,y1,z1) = getRelativePolar(O, (theta, phi, r))  # p2 is now the position of a new building!
		
		# Work out how big this building needs to be based on where it is in relation to the centre of the box (with occasional variation)
		
		w = width /MINSIZE
		if w < MINSIZE:
			w = MINSIZE +1
		w = randint(MINSIZE,w)
		w = w/2
		
		coef = (float)(r/(centreWidth/8.0*7.0)) # Scale the buildings further out downwards
		if randint(1,20) < 2:
			h = height
		else:
			h = (int)((float)(height * (float)(1.0-coef)))
		
		if h < MINSIZE:
			h = MINSIZE +1
		h = randint(MINSIZE,h)
		d = depth /MINSIZE
		if d < MINSIZE:
			d = MINSIZE +1		
		d = randint(MINSIZE,d)
		d = d/2
		if w < MINSIZE:
			w = MINSIZE
		if w > MINSIZE*2:
			if randint(1,10) < 2:
				w = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
			else:
				w = MINSIZE*2
		if h < MINSIZE:
			h = MINSIZE
		if d < MINSIZE:
			d = MINSIZE
		if d > MINSIZE*2:
			if randint(1,10) < 2:
				d = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
			else:
				d = MINSIZE*2
		
		print '%s %s %s, %s %s %s' % (x1, y1, z1, w, h, d)
		
		(tx1, ty1, tz1) = (x1-w, y1, z1-d)
		(tx2, ty2, tz2) = (abs(w*2), abs(h), abs(d*2))
		
		print '%s %s %s, %s %s %s' % (tx1, ty1, tz1, tx2, ty2, tz2)
		
		newBox = BoundingBox((tx1, ty1, tz1), (tx2, ty2, tz2))
#		(width1, height1, depth1) = getBoxSize(newBox)
#		print '%s %s %s' % (width1, height1, depth1)
		draw3DTree(level,newBox,options)
	
	print '%s: Ended at %s' % (method, time.ctime())

def draw3DTree(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	material = (fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	ANGLESTEP = pi/180
	TwoPI = 2*pi

	(x0,y0,z0) = (centreWidth,0,centreDepth)
	
	drawLine(level, material,
					(box.minx+x0-1,box.miny+y0,box.minz+z0), 
					(box.minx+x0-1,box.miny+y0+height/3,box.minz+z0))
	drawLine(level, material,
					(box.minx+x0+1,box.miny+y0,box.minz+z0), 
					(box.minx+x0+1,box.miny+y0+height/3,box.minz+z0))
	drawLine(level, material,
					(box.minx+x0,box.miny+y0,box.minz+z0+1), 
					(box.minx+x0,box.miny+y0+height/3,box.minz+z0+1))
	drawLine(level, material,
					(box.minx+x0,box.miny+y0,box.minz+z0-1), 
					(box.minx+x0,box.miny+y0+height/3,box.minz+z0-1))
	drawLine(level, material,
					(box.minx+x0,box.miny+y0,box.minz+z0), 
					(box.minx+x0,box.miny+y0+height/3,box.minz+z0))

	MANGLE = 90*((width+depth)/2)/height
	

	draw3DTreeBranch(level, box, options, height/3, (x0,y0+height/3,z0), randint(0,360)*ANGLESTEP, (90+randint(-MANGLE,MANGLE))*ANGLESTEP, randint(30,60)) 
	
	t = (int)(MANGLE / 4)
	if t < 4:
		t = 4
	for iter in xrange(0,t):
		draw3DTreeBranch(level, box, options, height/3, (x0,y0+randint(height/5,height/3),z0), randint(0,360)*ANGLESTEP, (90+randint(-MANGLE,MANGLE))*ANGLESTEP, randint(MANGLE/3,MANGLE)) 

#	draw3DTreeBranch(level, box, options, height/3, (x0,y0+randint(height/5,height/3),z0), randint(0,360)*ANGLESTEP, (90+randint(-80,80))*ANGLESTEP, randint(30,60)) 
	
def draw3DTreeBranch(level, box, options, depth, (x0,y0,z0), theta, phi, angle):
	ANGLESTEP = pi/180
	TwoPI = 2*pi
	ANGLERANGE = angle
	
	#material = (options["Light block:"].ID, options["Light block:"].blockData)
	material = (options["Fill block:"].ID, options["Fill block:"].blockData)
	
	if depth == 1:
		material = (options["Edge block:"].ID, options["Edge block:"].blockData)

	if depth:
		print '%s %s %s %s %s' % (x0, theta, cos(theta), phi, depth)
		(x2, y2, z2) = getRelativePolar((x0,y0,z0), (theta, phi, depth))
		
		drawLine(level, material,
						(box.minx+x0,box.miny+y0,box.minz+z0), 
						(box.minx+x2,box.miny+y2,box.minz+z2))

		for iter in xrange(0,randint(3,11)):
			draw3DTreeBranch(level, box, options, depth/2, (x2, y2, z2), theta+randint(-ANGLERANGE,ANGLERANGE)*ANGLESTEP, phi+randint(-ANGLERANGE,ANGLERANGE)*ANGLESTEP,angle)	

def drawRandomSplodge(level, box, options, material, innerRadius, edgeOnly, STEPSIZE, ANGLES, PARTITION):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Determine the profile of the Radius around the circumference of the disc
	if ANGLES < 360:
		ANGLES = 360
	
	ANGLE = 2*pi/ANGLES
	numberOfWaves = randint(1,3)
	
#	periods = []
#	for iter in xrange(0,numberOfWaves):
#		scalar = randint(1,5)
#		periods.append(0.4*scalar)
#	theShape = []
#	for iter in xrange(0,360):
#		theShape.append(1.0)
#		for iterX in xrange(0, len(periods)):
#			theShape[iter] = theShape[iter]*sin(ANGLE*iter*periods[iterX])
#
#	print periods
#	print theShape

	if STEPSIZE < 0.1:
		STEPSIZE = 0.2
	if STEPSIZE > 1.0:
		STEPSIZE = 0.2
		
	theShape = []
	for iter in xrange(0,ANGLES):
		theShape.append(1.0)

	randWalker=1.0
	startPos = randint(0,ANGLES-1)
	for iter in xrange(0,ANGLES):
#		theShape.append(1.0)
		r = randint(0,100)
		if r < 30:
			randWalker = randWalker+STEPSIZE
		elif r > 70:
			randWalker = randWalker-STEPSIZE
		if randWalker < 0:
			randWalker = 0
		if randWalker > 10:
			randWalker = 10
		
		if randWalker - ((startPos+ANGLES-iter)%ANGLES) > theShape[startPos]:
			randWalker = randWalker - 1
		theShape[(startPos+iter)%ANGLES] = 0.1*randWalker
			
	for iterX in xrange(-centreWidth,centreWidth):
		for iterZ in xrange(-centreDepth,centreDepth):
			angle = atan2(iterZ,iterX)
			radiusHere = float(sqrt(iterX * iterX + iterZ * iterZ))
			eRX = float(centreWidth * cos(angle))
			eRZ = float(centreDepth * sin(angle))
#			print theShape[int(angle/ANGLE)]
#			print int(angle/ANGLE)
			edgeRadiusHere = float(sqrt(eRX*eRX+eRZ*eRZ))
			edgeRadiusHere = edgeRadiusHere/PARTITION*(PARTITION-1) + edgeRadiusHere/PARTITION*abs(theShape[int(angle/ANGLE)])
			#print '%s %s %s %s %s %s %s' % (angle,rX,rZ,radiusHere,eRX,eRZ,edgeRadiusHere)
			if radiusHere > innerRadius and ((radiusHere < edgeRadiusHere) and edgeOnly == False) or ((abs(radiusHere-(edgeRadiusHere-1))<=1.0) and edgeOnly == True):
				for iterY in xrange(0,height):
						setBlock(level, material, box.minx+centreWidth+iterX,box.miny+iterY,box.minz+centreDepth+iterZ )
			
						
				#drawLine(level, material, (box.minx+centreWidth+iterX,box.miny,box.minz+centreDepth+iterZ), (box.minx+centreWidth+iterX,box.miny+height-1,box.minz+centreDepth+iterZ) )
	print '%s: Ended at %s' % (method, time.ctime())	
	
def drawFullDisc(level, box, options, material, innerRadius, edgeOnly):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	
	# builds a disc in the selection area. Solid blocks of material wherever the diameter is less than the box dimensions
	
	for iterX in xrange(-centreWidth,centreWidth):
		for iterZ in xrange(-centreDepth,centreDepth):
			angle = atan2(iterZ,iterX)
			radiusHere = float(sqrt(iterX * iterX + iterZ * iterZ))
			eRX = float(centreWidth * cos(angle))
			eRZ = float(centreDepth * sin(angle))
			edgeRadiusHere = float(sqrt(eRX*eRX+eRZ*eRZ))
			#print '%s %s %s %s %s %s %s' % (angle,rX,rZ,radiusHere,eRX,eRZ,edgeRadiusHere)
			if radiusHere > innerRadius and ((radiusHere < edgeRadiusHere) and edgeOnly == False) or ((abs(radiusHere-(edgeRadiusHere-1))<=1.0) and edgeOnly == True):
				for iterY in xrange(0,height):
						setBlock(level, material, box.minx+centreWidth+iterX,box.miny+iterY,box.minz+centreDepth+iterZ )
			
						
				#drawLine(level, material, (box.minx+centreWidth+iterX,box.miny,box.minz+centreDepth+iterZ), (box.minx+centreWidth+iterX,box.miny+height-1,box.minz+centreDepth+iterZ) )
	print '%s: Ended at %s' % (method, time.ctime())	
			
def drawDisc(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Draws concentric circles out to the border in the nominated materials
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	ANGLESTEP = pi/180
	TwoPI = 2*pi

	SideLength = centreWidth


	Orientation = randint(0,45)
	
	offsetX = 0
	offsetZ = 0
	
	angle = TwoPI/360
	
	numSides = SideLength

	y = 0
	radius = (int)(SideLength)

	for y in xrange(0, height):
		for r in xrange(1,radius):
			MATERIAL = (fillMaterialBlock, fillMaterialData)
			x = r * cos(Orientation*angle)
			z = r * sin(Orientation*angle)
					
			for sides in xrange(0,numSides+3):
				x1 = r * cos((Orientation+360/numSides*sides)*angle)
				z1 = r * sin((Orientation+360/numSides*sides)*angle)
				drawLine(level, MATERIAL, (box.minx+centreWidth+x+offsetX,box.miny+y,box.minz+offsetZ+centreDepth+z), (box.minx+centreWidth+x1+offsetX,box.miny+y,box.minz+centreDepth+z1+offsetZ) )
				x = x1
				z = z1

	print '%s: Ended at %s' % (method, time.ctime())
	drawTorus(level, box, options, centreWidth/2, centreWidth-2, (edgeMaterialBlock, edgeMaterialData) )
	
def drawTorus(level, box, options, startR, endR, material):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Draws concentric circles out to the border in the nominated materials

	ANGLESTEP = pi/180
	TwoPI = 2*pi

	SideLength = centreWidth


	Orientation = randint(0,45)
	
	offsetX = 0
	offsetZ = 0
	
	angle = TwoPI/360
	
	numSides = SideLength

	y = 0
	radius = (int)(SideLength)

	for y in xrange(0, height):
		for r in xrange(startR,endR):
			MATERIAL = material
			x = r * cos(Orientation*angle)
			z = r * sin(Orientation*angle)
					
			for sides in xrange(0,numSides+3):
				x1 = r * cos((Orientation+360/numSides*sides)*angle)
				z1 = r * sin((Orientation+360/numSides*sides)*angle)
				drawLine(level, MATERIAL, (box.minx+centreWidth+x+offsetX,box.miny+y,box.minz+offsetZ+centreDepth+z), (box.minx+centreWidth+x1+offsetX,box.miny+y,box.minz+centreDepth+z1+offsetZ) )
				x = x1
				z = z1

	print '%s: Ended at %s' % (method, time.ctime())
	
def Fractree(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	drawTree(level, box, options, (fillMaterialBlock, fillMaterialData), centreWidth, 0, centreDepth, 90, height/5)
	
def drawTree(level, box, options, material, x1, y1, z1, angle, depth):
    if depth:
		x2 = x1 + int(math.cos(math.radians(angle)) * depth * 1.0)
		y2 = y1 + int(math.sin(math.radians(angle)) * depth * 1.0)
		z2 = z1
		
		drawLine(level, material,
						(box.minx+x1,box.miny+y1,box.minz+z1), 
						(box.minx++x2,box.miny+y2,box.minz+z2))

		drawTree(level, box, options, material, x2, y2, z2, angle - 20, depth - 1)
		drawTree(level, box, options, material, x2, y2, z2, angle + 20, depth - 1)	

def Factorise(number):
	Q = []
	
	for iter in xrange(1,(int)(number+1)):
		p = (int)(number/iter)
		if number - (p * iter) == 0:
			if iter not in Q:
				Q.append(iter)
			if p not in Q:
				Q.append(p)

#	print 'Factors of %s are:' % (number)
#	for iter in Q:
#		print '%s,' % (iter)
	
	return Q

def CircularCity(level, box, options): # NOT YET IMPLEMENTED.
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	
	# Draw a circular city 
	# 1. Locate the centre of the selection box. This is the hub
	# 2. Draw a plot (park, complex, building, etc. there. Add the bounding box to a queue
	# 3. Around the park, draw a circular road
	# 4. At a random location on the road, draw a road of a random length going away from the hub to another hub that does not intersect with any known box. Make a bounding box there, add it to a queue.
	# 5. Repeat 4 until consecutive placement failures occur.
	
#	keepGoing = True
#	while keepGoing == True:
		
	
#	hubPos = (centreWidth, 0, centreDepth)
#	hubSize = 20 + random(width / 20)
	
def CityGrid(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Work out how 'big' to build. Loosely explained, this affects the number of floors in each module
	MINSIZE = 4 # Residential is if the maximum dimension of the selection box is less than 12 times this number
	buildType = height
	if width > buildType:
		buildType = width
	if depth > buildType:
		buildType = depth
	if buildType > MINSIZE * 12:
		MINSIZE = MINSIZE * 2 # Commercial
	
	# Places random buildings in an 8x8 grid from the selection box with a quarter of the box gab between each row.
#	angleSize = pi/180
#	TwoPI = 2*pi
#	angleSize = pi/180
#	O = (box.minx+centreWidth, box.miny, box.minz+centreDepth) # Origin

	# buildings = (width + height + depth) / 3
#	buildings = height/MINSIZE
#	if width/MINSIZE < buildings:
#		buildings = width/MINSIZE
#	if depth/MINSIZE < buildings:
#		buildings = depth/MINSIZE
#	if buildings < 2:
#		buildings = 2
#	buildings = randint(buildings/2,buildings*MINSIZE)+1

	buildings = 8
	buildings2 = buildings * buildings
	gapX = width
	gapZ = depth
	
	counter = 1
	for iterX in xrange(0,buildings):
		for iterY in xrange(0,buildings):
			counter = counter + 1
			print 'Constructing buildings - step %s of %s %s' % (counter,buildings2,buildings)
#		r = randint(0,centreWidth/8*7)
#		theta = randint(0,360)*angleSize
#		phi = 0 * angleSize #randint (0,360)*angleSize
#		(x1,y1,z1) = getRelativePolar(O, (theta, phi, r))  # p2 is now the position of a new building!
		
		# Work out how big this building needs to be based on where it is in relation to the centre of the box (with occasional variation)
			w = width
			if w < MINSIZE:
				w = MINSIZE +1
			w = randint(MINSIZE,w)
			w = w/2
			
#		coef = (float)(r/(centreWidth/8.0*7.0)) # Scale the buildings further out downwards
#		if randint(1,20) < 2:
			h = height
#		else:
#			h = (int)((float)(height * (float)(1.0-coef)))
		
			if h < MINSIZE:
				h = MINSIZE +1
			h = randint(MINSIZE,h)
			d = depth
			if d < MINSIZE:
				d = MINSIZE +1		
			d = randint(MINSIZE,d)
			d = d/2
			if h < MINSIZE:
				h = MINSIZE
			if d < MINSIZE:
				d = MINSIZE
			if d > MINSIZE*2:
				if randint(1,10) < 2:
					d = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
				else:
					d = MINSIZE*2
			
			y1 = 0
			(tx1, ty1, tz1) = (iterX*(buildings+gapX), y1, iterY*(buildings+gapZ))			
			(tx2, ty2, tz2) = (width, h, depth)
		
			print '%s %s %s, %s %s %s' % (tx1, ty1, tz1, tx2, ty2, tz2)
		
			newBox = BoundingBox((box.minx+tx1, box.miny+ty1, box.minz+tz1), (tx2, ty2, tz2))
#		(width1, height1, depth1) = getBoxSize(newBox)
#		print '%s %s %s' % (width1, height1, depth1)
			RuinedBuilding(level,newBox,options)

	
	print '%s: Ended at %s' % (method, time.ctime())
	
def City(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Work out how 'big' to build. Loosely explained, this affects the number of floors in each module
	MINSIZE = 4 # Residential is if the maximum dimension of the selection box is less than 12 times this number (i.e. 48 when drafting this code)
	buildType = height
	if width > buildType:
		buildType = width
	if depth > buildType:
		buildType = depth
	if buildType > MINSIZE * 12:
		MINSIZE = MINSIZE * 2 # Commercial
	
	# Places random buildings radially within the selection box
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	O = (box.minx+centreWidth, box.miny, box.minz+centreDepth) # Origin

	buildings = (width + height + depth) / 3
	#buildings = height/MINSIZE
	#if width/MINSIZE < buildings:
	#	buildings = width/MINSIZE
	#if depth/MINSIZE < buildings:
	#	buildings = depth/MINSIZE
	#if buildings < 2:
	#	buildings = 2
	#buildings = randint(buildings/2,buildings*MINSIZE)+1
	
	for iter in xrange(1,buildings):
		print 'Constructing building %s of %s' % (iter,buildings)
		r = randint(0,centreWidth/8*7)
		theta = randint(0,360)*angleSize
		phi = 0 * angleSize #randint (0,360)*angleSize
		(x1,y1,z1) = getRelativePolar(O, (theta, phi, r))  # p2 is now the position of a new building!
		
		# Work out how big this building needs to be based on where it is in relation to the centre of the box (with occasional variation)
		
		w = width /MINSIZE
		if w < MINSIZE:
			w = MINSIZE +1
		w = randint(MINSIZE,w)
		w = w/2
		
		coef = (float)(r/(centreWidth/8.0*7.0)) # Scale the buildings further out downwards
		if randint(1,20) < 2:
			h = height
		else:
			h = (int)((float)(height * (float)(1.0-coef)))
		
		if h < MINSIZE:
			h = MINSIZE +1
		h = randint(MINSIZE,h)
		d = depth /MINSIZE
		if d < MINSIZE:
			d = MINSIZE +1		
		d = randint(MINSIZE,d)
		d = d/2
		if w < MINSIZE:
			w = MINSIZE
		if w > MINSIZE*2:
			if randint(1,10) < 2:
				w = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
			else:
				w = MINSIZE*2
		if h < MINSIZE:
			h = MINSIZE
		if d < MINSIZE:
			d = MINSIZE
		if d > MINSIZE*2:
			if randint(1,10) < 2:
				d = MINSIZE*2 + randint(MINSIZE,MINSIZE*2)
			else:
				d = MINSIZE*2
		
		print '%s %s %s, %s %s %s' % (x1, y1, z1, w, h, d)
		
		(tx1, ty1, tz1) = (x1-w, y1, z1-d)
		(tx2, ty2, tz2) = (abs(w*2), abs(h), abs(d*2))
		
		print '%s %s %s, %s %s %s' % (tx1, ty1, tz1, tx2, ty2, tz2)
		
		newBox = BoundingBox((tx1, ty1, tz1), (tx2, ty2, tz2))
#		(width1, height1, depth1) = getBoxSize(newBox)
#		print '%s %s %s' % (width1, height1, depth1)
		if MINSIZE > 4 and randint(0,100) < 10:
			BuildingAngledShim(level,newBox,options)
		else:
			RuinedBuilding(level,newBox,options)
#			if height > ty2+8:
#				nmx = tx2+1+randint(1,width-2)
#				nmz = tz2+1+randint(1,depth-2)
#				antennaBox = BoundingBox((nmx, ty2+1, nmz), (nmx+2, ty2+randint(8,15), nmz+2))
#				Antenna(level, antennaBox, options)
	print '%s: Ended at %s' % (method, time.ctime())

def Antenna(level, box, options):
	method = "Antenna"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	material = (alphaMaterials.Fence.ID,alphaMaterials.Fence.blockData)
	if randint(0,100) < 20:
		material = (alphaMaterials.NetherBrickFence.ID,alphaMaterials.NetherBrickFence.blockData)
	if randint(0,100) < 10:
		material = (alphaMaterials.FenceGate.ID,alphaMaterials.FenceGate.blockData)
	
	# take in a tall thin box, and render the antenna within
	drawLine(level, material,
		(box.minx+centreWidth,box.miny,box.minz+centreDepth), 
		(box.minx+centreWidth,box.miny+randint(centreHeight+1,height-1),box.minz+centreDepth))
	drawLine(level, material,
		(box.minx+centreWidth+1,box.miny+centreHeight,box.minz+centreDepth), 
		(box.minx+centreWidth+1,box.miny+randint(centreHeight,height-1),box.minz+centreDepth))
	drawLine(level, material,
		(box.minx+centreWidth-1,box.miny+centreHeight,box.minz+centreDepth), 
		(box.minx+centreWidth-1,box.miny+randint(centreHeight,height-1),box.minz+centreDepth))
	drawLine(level, material,
		(box.minx+centreWidth,box.miny+centreHeight,box.minz+centreDepth+1), 
		(box.minx+centreWidth,box.miny+randint(centreHeight,height-1),box.minz+centreDepth+1))
	drawLine(level, material,
		(box.minx+centreWidth,box.miny+centreHeight,box.minz+centreDepth-1), 
		(box.minx+centreWidth,box.miny+randint(centreHeight,height-1),box.minz+centreDepth-1))
	
	
#	for iter in xrange(0, width):
#		if randint(0,100) < 5:
#			drawLine(level, material,
#						(box.minx+iter,box.miny,box.minz), 
#						(box.minx+iter,box.miny+randint(1,height-1),box.minz))
#		if randint(0,100) < 5:
#			drawLine(level, material,
#						(box.minx+iter,box.miny,box.minz+depth-1), 
#						(box.minx+iter,box.miny+randint(1,height-1),box.minz+depth-1))
#				
#	for iter in xrange(0, depth):
#		if randint(0,100) < 5:
#			drawLine(level, material,
#						(box.minx,box.miny,box.minz+iter), 
#						(box.minx,box.miny+randint(1,height-1),box.minz+iter))
#		if randint(0,100) < 5:
#			drawLine(level, material,
#						(box.minx+width-1,box.miny,box.minz+iter), 
#						(box.minx+width-1,box.miny+randint(1,height-1),box.minz+iter))

	
def BuildingAngledShim(level, box, options): # After the ENT filter
	BuildingAngled(level, box, options, randint(0,45), randint(3,11))
	
def BuildingAngled(level, box, options, Orientation, numSides): # After the ENT filter
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	if randint(1,100) < 30:
		t1 = (fillMaterialBlock, fillMaterialData)
		(fillMaterialBlock, fillMaterialData) = (edgeMaterialBlock, edgeMaterialData)
		(edgeMaterialBlock, edgeMaterialData) = t1
	
	ANGLESTEP = pi/180
	TwoPI = 2*pi
	
	SideLength = centreWidth
	RINGS = randint(1,SideLength/4+1)

	if Orientation == -1: # Randomise
		Orientation = randint(0,45)
	
	offsetX = 0
	offsetZ = 0
	
	angle = TwoPI/360
	
	if numSides < 3:
		numSides = 3+randint(0,15)
	
	banding = False
	bandType = 1
	bandingSize1 = 0
	bandingSize2 = 0
	if randint(1,20) < 10:
		banding = True
		bandingSize1 = randint(2,8)
		bandingSize2 = randint(1,bandingSize1)
	if randint(1,20) < 5:
		bandType = 2
	
	for y in xrange(0, height):
		print '%s: %s of %s' % (method, y, height)
		radius = (int)(SideLength)
		
		for r in xrange(1,radius):
			MATERIAL = (fillMaterialBlock, fillMaterialData)
			ringR = (int)(SideLength/RINGS)
			if ringR == 0:
				ringR == 2
			if r == radius-1:
				MATERIAL = (lightMaterialBlock, lightMaterialData)
				if banding == True:
					t = y%(bandingSize1+bandingSize2)
					if t < bandingSize1:
						MATERIAL = (edgeMaterialBlock, edgeMaterialData)
						
			elif r%ringR == 0: # Interior walls
				MATERIAL = (edgeMaterialBlock, edgeMaterialData)
			if (MATERIAL == (fillMaterialBlock, fillMaterialData) and y%4 == 0) or (MATERIAL == (lightMaterialBlock, lightMaterialData)) or (MATERIAL == (edgeMaterialBlock, edgeMaterialData)):
				x = r * cos(Orientation*angle)
				z = r * sin(Orientation*angle)
				
				for sides in xrange(0,numSides+1):
					x1 = r * cos((Orientation+360/numSides*sides)*angle)
					z1 = r * sin((Orientation+360/numSides*sides)*angle)
					drawLine(level, MATERIAL, (box.minx+centreWidth+x+offsetX,box.miny+y,box.minz+offsetZ+centreDepth+z), (box.minx+centreWidth+x1+offsetX,box.miny+y,box.minz+centreDepth+z1+offsetZ) )
					x = x1
					z = z1
		
		if SideLength < 1:
			break
	
	print '%s: Ended at %s' % (method, time.ctime())
	
def RuinedBuilding(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	
	W = Factorise(width-1)
	H = Factorise(height-1)
	D = Factorise(depth-1)
	
	w = W.pop(randint(0,len(W)-1))
	h = H.pop(randint(0,len(H)-1))
	d = D.pop(randint(0,len(D)-1))

	drawGlass = False
	if randint(1,20) > 1:
		drawGlass = True
	
	banding = False
	bandType = 1
	bandingSize1 = 0
	bandingSize2 = 0
	if randint(1,20) < 10:
		banding = True
		bandingSize1 = randint(2,8)
		bandingSize2 = randint(1,bandingSize1)
	if randint(1,20) < 5:
		bandType = 2
	
	#Floors
	print '%s: Floors' % (method)
	for iterY in xrange(0,height-1):
		if iterY == 0 or (iterY % 4 == 0 and randint(1,10) > 1):
			for iterX in xrange(1,width-1):
				for iterZ in xrange(1,depth-1):
					setBlock(level, (fillMaterialBlock, fillMaterialData), box.minx+iterX, box.miny+iterY, box.minz+iterZ)
	
	roomSize = randint(6,12)		
	#Uprights
	print '%s: Uprights' % (method)
	for iterX in xrange(0,width):
		for iterZ in xrange(0,depth):
			if drawGlass == True and (iterX == 0 or iterX == width-1 or iterZ == 0 or iterZ == depth-1): # Walls
				if banding == False:
					drawLine(level, (lightMaterialBlock, lightMaterialData),
							(box.minx+iterX,box.miny,box.minz+iterZ), 
							(box.minx+iterX,box.miny+height-1,box.minz+iterZ))
				else:
					iterY = 0
					while iterY < height:
						if bandType == 1:
							drawLine(level, (edgeMaterialBlock, edgeMaterialData),
								(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
								(box.minx+iterX,box.miny+iterY+bandingSize1,box.minz+iterZ))
						else:
							if iterY < height-1:
								if iterY+bandingSize1 >= height-1:
									drawLine(level, (fillMaterialBlock, fillMaterialData),
										(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
										(box.minx+iterX,box.miny+height-1,box.minz+iterZ))
								else:
									drawLine(level, (fillMaterialBlock, fillMaterialData),
										(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
										(box.minx+iterX,box.miny+iterY+bandingSize1,box.minz+iterZ))
										
						iterY = iterY + bandingSize1
						
						if iterY < height-1:
							if iterY+bandingSize2 >= height-1:
								drawLine(level, (lightMaterialBlock, lightMaterialData),
									(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
									(box.minx+iterX,box.miny+height-1,box.minz+iterZ))
							else:
								drawLine(level, (lightMaterialBlock, lightMaterialData),
									(box.minx+iterX,box.miny+iterY,box.minz+iterZ), 
									(box.minx+iterX,box.miny+iterY+bandingSize2,box.minz+iterZ))
						iterY = iterY + bandingSize2

			if (iterZ % d == 0 and iterX % w == 0) or (iterZ % roomSize == 0 and iterX % roomSize == 0):
				drawLine(level, (edgeMaterialBlock, edgeMaterialData),
							(box.minx+iterX,box.miny,box.minz+iterZ), 
							(box.minx+iterX,box.miny+height-1,box.minz+iterZ))
	
	#Bounding
	print '%s: Bounding' % (method)
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+0,box.minz+0), 
			(box.minx+width-1,box.miny+0,box.minz+0))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+0,box.minz+depth-1), 
			(box.minx+width-1,box.miny+0,box.minz+depth-1))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+0,box.minz+0), 
			(box.minx+0,box.miny+0,box.minz+depth-1))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+width-1,box.miny+0,box.minz+0), 
			(box.minx+width-1,box.miny+0,box.minz+depth-1))

	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+height-1,box.minz+0), 
			(box.minx+width-1,box.miny+height-1,box.minz+0))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+height-1,box.minz+depth-1), 
			(box.minx+width-1,box.miny+height-1,box.minz+depth-1))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+0,box.miny+height-1,box.minz+0), 
			(box.minx+0,box.miny+height-1,box.minz+depth-1))
	drawLine(level, (edgeMaterialBlock, edgeMaterialData),
			(box.minx+width-1,box.miny+height-1,box.minz+0), 
			(box.minx+width-1,box.miny+height-1,box.minz+depth-1))

	# Damage
#	print '%s: Damage' % (method)
#	purgeDepth = centreHeight
#
#	for iterX in xrange(0,width):
#		purgeDepth = purgeDepth + randint(-h,h)
#		if purgeDepth < 0:
#			purgeDepth = 0
#		if purgeDepth > height-1:
#			purgeDepth = height-1
#		for iterY in xrange(0,purgeDepth):
#			drawLine(level, AIR,
#				(box.minx+iterX,box.maxy-1,box.minz), 
#				(box.minx+iterX,box.maxy-1-iterY,box.minz+depth-1))
#
#	purgeDepth = centreHeight
#	
#	for iterZ in xrange(0,depth):
#		purgeDepth = purgeDepth + randint(-h,h)
#		if purgeDepth < 0:
#			purgeDepth = 0
#		if purgeDepth > height-1:
#			purgeDepth = height-1
#		for iterY in xrange(0,purgeDepth):
#			drawLine(level, AIR,
#				(box.minx,box.maxy-1,box.minz+iterZ), 
#				(box.minx+width-1,box.maxy-1-iterY,box.minz+iterZ))

	print '%s: Ended at %s' % (method, time.ctime())

def getDistanceVector( (x,y,z), (x1,y1,z1) ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)
	
	return (theta, phi, distance)
	
def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
	
def Toffee(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	for i in xrange(0, randint(1,16)):
		drawRandomTriangle(level, box, options, (edgeMaterialBlock, i%16), (fillMaterialBlock, i%16))
	print '%s: Ended at %s' % (method, time.ctime())
		
def DeathStar2(level, box, options):
	# draw a spherical object reminiscent of a certain non-moon
	# for each 'layer' draw a random line from the edge of the sphere at this point to random depth
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	AIR = (0,0)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
		
	r = centreWidth
	r=r-2
	rr = r*r
	
	tr = r/16
	while tr < r:
		DeathStarBands(level, box, options, tr)
		if r/16 > 2:
			tr = tr + randint(2,r/16)
		else:
			tr = tr + 2

	
	print '%s: Internal pipes %s' % (method, time.ctime())
	for iterY in xrange(0,height):
		print '%s: Layer %s of %s' % (method, iterY, height-1)
		dy = centreHeight - iterY
		dydy = dy * dy
		for iterX in xrange(0, width):
			dx = centreWidth - iterX
			dxdx = dx * dx
			for iterZ in xrange(0, depth):
				dz = centreDepth - iterZ
				dzdz = dz * dz
				posn = abs(dxdx + dydy + dzdz - rr)
				if posn >= 0 and posn < 121: # this block is on the sphere surface
					if dz > 0 and (iterY%5 == 0 or iterZ%5 == 0):
						randomDepth = randint(0,2*dz) # percent depth to render with 
						drawLine(level, (fillMaterialBlock, fillMaterialData), (box.minx+iterX, box.miny+iterY, box.minz+iterZ),
											      (box.minx+iterX, box.miny+iterY, box.minz+iterZ+randomDepth) )
					chanceOfSurface = (float)((1.0-(float)((float)(1.3*iterZ)/(float)(depth)))*100.0)
					# print '%s: Chance %s' % (method, chanceOfSurface)
					if chanceOfSurface > (float)(randint(1,80)):
						if 2 > (float)(randint(1,100)):
							setBlock(level, (lightMaterialBlock, lightMaterialData), box.minx+iterX, box.miny+iterY, box.minz+iterZ)
						else:
							setBlock(level, (edgeMaterialBlock, edgeMaterialData), box.minx+iterX, box.miny+iterY, box.minz+iterZ)

	r = r + 2
	# Bands
	print '%s: Bands %s' % (method, time.ctime())
	DeathStarBands(level, box, options, r)
	
	# Back
	print '%s: Open back %s' % (method, time.ctime())
	#DeathStarRemoveBackChunks(level, box, options, r, (int)(r/2))
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/4))
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/8))
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/10))
	DeathStarRemoveBackChunks(level, box, options, r, (int)(r/16))

	# Open Panelling
	print '%s: Open panelling %s' % (method, time.ctime())
	DeathStarPanels(level, box, options, r, AIR)

	# Random walk
	print '%s: Channels %s' % (method, time.ctime())
	for s in xrange(5, randint(1,r)):
		theta = randint(0,360)*angleSize
		phi = randint (0,360)*angleSize
		for t in xrange(10, r):
			u = randint(5,10)*angleSize
			phiU = phi+u
			phiT = phi
			while phiT < phiU:
				p2 = getRelativePolar(p1, (theta, phiT, r))
				p3 = getRelativePolar(p1, (theta, phiT+angleSize, r))
				drawLine(level, AIR, p3, p2)
				p2 = getRelativePolar(p1, (theta, phiT, r-1))
				p3 = getRelativePolar(p1, (theta, phiT+angleSize, r-1))
				drawLine(level, AIR, p3, p2)
				p2 = getRelativePolar(p1, (theta, phiT, r-2))
				p3 = getRelativePolar(p1, (theta, phiT+angleSize, r-2))
				drawLine(level, AIR, p3, p2)
				phiT = phiT+angleSize
			phi = phi+randint(-1,1)*angleSize
			theta = theta+randint(-1,1)*angleSize

	r=r-3

	# LASER
	print '%s: LASER %s' % (method, time.ctime())
	theta = -pi/2
	phi = pi/6

	size = r/2
	radius = r+(size*3/4)
	(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
	drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (0,0))
	drawSphereIntersection(level, ((int)(x), (int)(y), (int)(z)), (int)(size+2), (fillMaterialBlock, fillMaterialData), (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth), (int)(r+1))

	# Interior chambers
	drawSphere(level, ((int)(box.minx+centreWidth), (int)(box.miny+centreHeight), (int)(box.minz+centreDepth)), (int)(r/8), (edgeMaterialBlock, edgeMaterialData))
	drawSphere(level, ((int)(box.minx+centreWidth), (int)(box.miny+centreHeight), (int)(box.minz+centreDepth)), (int)(r/8-2), (0,0))

#	size = r/2
#	radius = r+(size*3/4)
#	t = randint(5,10)
#	for numholes in xrange(0, t):
#		theta = angleSize * randint(0,180)
#		phi = angleSize * randint(-90,90)
#		(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
#		drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (0,0))
		
#	theta = 0
#	phi = 0
#	(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
#	drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (2,0))

#	theta = 90 * angleSize
#	phi = 0
#	(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
#	drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (3,0))

#	theta = 0
#	phi = 90 * angleSize
#	(x, y, z) = getRelativePolar(p1, (theta, phi, radius))
#	drawSphere(level, ((int)(x), (int)(y), (int)(z)), (int)(size), (4,0))


	
	print '%s: Ended at %s' % (method, time.ctime())

def DeathStarPanels(level, box, options, r, material):
	# draw a spherical object reminiscent of a certain non-moon
	# for each 'layer' draw a random line from the edge of the sphere at this point to random depth
	method = options["Operation"]
	print '%s DeathStarPanels: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)

	# Bands
	t = randint(r,2*r)
	for i in xrange(0,t):
		print '%s: Vertical band %s of %s' % (method, i, t)
		vertAngle1 = angleSize * randint(-90,83)
		vertAngle2 = vertAngle1 + angleSize * randint(3,7)
		horizAngle = angleSize * randint(0,180)
		if vertAngle1 > vertAngle2:
			temp = vertAngle1
			vertAngle1 = vertAngle2
			vertAngle2 = temp
		vertAngle = vertAngle1
		while vertAngle <= vertAngle2:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			vertAngle = vertAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 5 > (float)(randint(1,100)):
				drawLine(level, material, p3, p2)
			else:
				drawLine(level, material, p3, p2)

	t = randint(r,4*r)
	for i in xrange(0,t):
		print '%s: Horizontal band %s of %s' % (method, i, t)
		horizAngle1 = angleSize * randint(0,173)
		horizAngle2 = horizAngle1 + angleSize * randint(3,7)
		vertAngle = angleSize * randint(-90,90)
		if horizAngle1 > horizAngle2:
			temp = horizAngle1
			horizAngle1 = horizAngle2
			horizAngle2 = temp
		horizAngle = horizAngle1
		while horizAngle <= horizAngle2:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 66 > (float)(randint(1,100)):
				drawLine(level, material, p3, p2)
			else:
				drawLine(level, material, p3, p2)

	print '%s: Ended at %s' % (method, time.ctime())
				
def DeathStarRemoveBackChunks(level, box, options, r, CHUNKSIZE):
	# draw a spherical object reminiscent of a certain non-moon
	# remove cubic chunks from the back to a certain depth
	method = options["Operation"]
	print '%s DeathStarRemoveBackChunks: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)
	
	if CHUNKSIZE < 4:
		CHUNKSIZE = 4
	band = (int)(r/16)
		
	iterY = 0
	while iterY < height:
		print '%s: Removing back chunks %s of %s' % (method, iterY, height)
		iterX = 0

		while iterX < width:
			t = randint(0, (int)(r/CHUNKSIZE))
			print '%s: Removing back chunks - row %s of %s' % (method, iterX, width)
			iterZ = 0
			while iterZ < t:
				print '%s: Removing back chunks - column %s of %s' % (method, iterZ, t)
				for x in xrange(0,CHUNKSIZE):
					for y in xrange(0,CHUNKSIZE):
						for z in range(0,CHUNKSIZE):
							if (iterY+y) < (centreHeight-band) or (iterY+y) > (centreHeight+band): # Preserve most of the equator
								setBlock(level, (0,0), box.minx+iterX+x, box.miny+iterY+y, box.maxz-iterZ*CHUNKSIZE-z)
							elif randint(0,10) < 3: # but destroy bits of the equator too
								setBlock(level, (0,0), box.minx+iterX+x, box.miny+iterY+y, box.maxz-iterZ*CHUNKSIZE-z)
								#drawLine(level, (0,0), (box.minx+iterX, box.miny+iterY, box.maxz-1), (box.minx+iterX, box.miny+iterY, box.maxz-1-t))
					iterZ = iterZ + 1
				iterX = iterX + CHUNKSIZE
		iterY = iterY + CHUNKSIZE
				
def DeathStarRemoveBackOneLine(level, box, options, r):
	# draw a spherical object reminiscent of a certain non-moon
	# for each 'layer' draw a random line from the edge of the sphere at this point to random depth
	method = options["Operation"]
	print '%s DeathStarRemoveBackOneLine: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)

	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			t = randint(0, r)
			drawLine(level, (0,0), (box.minx+iterX, box.miny+iterY, box.maxz-1), (box.minx+iterX, box.miny+iterY, box.maxz-1-t))
	
def DeathStarBands(level, box, options, r):
	# draw a spherical object reminiscent of a certain non-moon
	# for each 'layer' draw a random line from the edge of the sphere at this point to random depth
	method = options["Operation"]
	print '%s DeathStarBands: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
	(lightMaterialBlock, lightMaterialData) = (options["Light block:"].ID, options["Light block:"].blockData)
	angleSize = pi/180
	TwoPI = 2*pi
	angleSize = pi/180
	p1 = (box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth)


	# Bands
	t = randint(r,2*r)
	for i in xrange(0,t):
		print '%s: Vertical band %s of %s' % (method, i, t)
		vertAngle1 = angleSize * randint(0,360)
		vertAngle2 = vertAngle1 + angleSize * randint(16,360)
		horizAngle = angleSize * randint(0,360)
		if vertAngle1 > vertAngle2:
			temp = vertAngle1
			vertAngle1 = vertAngle2
			vertAngle2 = temp
		vertAngle = vertAngle1
		while vertAngle <= vertAngle2:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			vertAngle = vertAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 5 > (float)(randint(1,100)):
				drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			else:
				drawLine(level, (fillMaterialBlock, fillMaterialData), p3, p2)

	t = randint(r,4*r)
	for i in xrange(0,t):
		print '%s: Horizontal band %s of %s' % (method, i, t)
		horizAngle1 = angleSize * randint(0,360)
		horizAngle2 = horizAngle1 + angleSize * randint(45,360)
		vertAngle = angleSize * randint(0,360)
		if horizAngle1 > horizAngle2:
			temp = horizAngle1
			horizAngle1 = horizAngle2
			horizAngle2 = temp
		horizAngle = horizAngle1
		while horizAngle <= horizAngle2:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 10 > (float)(randint(1,100)):
				drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			else:
				drawLine(level, (edgeMaterialBlock, edgeMaterialData), p3, p2)

		
	vertAngle = 0
	vertAngles = [angleSize,-angleSize,2*angleSize,-3*angleSize] #,3*angleSize,-3*angleSize]
	for vertAngle in vertAngles:
		horizAngle = 0
		while horizAngle < TwoPI:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			if 5 > (float)(randint(1,100)):
				drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			else:
				drawLine(level, (edgeMaterialBlock, edgeMaterialData), p3, p2)

	vertAngle = 0
	vertAngles = [0,-angleSize*2] # Central bands
	for vertAngle in vertAngles:
		horizAngle = 0
		while horizAngle < TwoPI:
			p2 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			p2a = getRelativePolar(p1, ( horizAngle, vertAngle, r-1))
			p2b = getRelativePolar(p1, ( horizAngle, vertAngle, r-2))
			horizAngle = horizAngle + angleSize
			p3 = getRelativePolar(p1, ( horizAngle, vertAngle, r))
			p3a = getRelativePolar(p1, ( horizAngle, vertAngle, r-1))
			p3b = getRelativePolar(p1, ( horizAngle, vertAngle, r-2))
			#if 66 > (float)(randint(1,100)):
			#	drawLine(level, (lightMaterialBlock, lightMaterialData), p3, p2)
			#else:
			#	drawLine(level, (edgeMaterialBlock, edgeMaterialData), p3, p2)
			drawLine(level, (0,0), p3, p2)
			drawLine(level, (0,0), p3a, p2a)
			drawLine(level, (0,0), p3b, p2b)

	print '%s: Ended at %s' % (method, time.ctime())

def Sculpt(level, box, options):
	method = options["Operation"]
	print '%s: Started at %s' % (method, time.ctime())
	(edgeMaterialBlock, edgeMaterialData) = (options["Edge block:"].ID, options["Edge block:"].blockData)
	(fillMaterialBlock, fillMaterialData) = (options["Fill block:"].ID, options["Fill block:"].blockData)
#TBD
	print '%s: Ended at %s' % (method, time.ctime())
				
# END YOUR CODE BIT /\ /\ /\ /\ /\ /\ /\ /\ /\ /\

# Support libraries

# GFX Tests

def drawRandomTriangle(level, box, options, edgeMaterial, fillMaterial):
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	
	drawTriangle(level, box, options, 
					(box.minx+(int)(randint(0,width-1)), box.miny+(int)(randint(0,height-1)), box.minz+(int)(randint(0,depth-1))),
					(box.minx+(int)(randint(0,width-1)), box.miny+(int)(randint(0,height-1)), box.minz+(int)(randint(0,depth-1))),
					(box.minx+(int)(randint(0,width-1)), box.miny+(int)(randint(0,height-1)), box.minz+(int)(randint(0,depth-1))),
					edgeMaterial,
					fillMaterial
				)
	
# GFX primitives

def drawTriangle(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
	if materialFill != (0,0):
		# for each step along the 'base' draw a line from the apex
		dx = p3x - p2x
		dy = p3y - p2y
		dz = p3z - p2z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)
		
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
			
			iter = iter+0.5 # slightly oversample because I lack faith.
			drawLine(level, materialFill, (px, py, pz), (p1x, p1y, p1z) )
	
	
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def drawPoint(level, (block, data), x, y, z):
	setBlock(level, (block, data), x, y, z)
	
# Ye Olde GFX Libraries
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.

def drawPolygon(level, box, options, sides, radius, Orientation, (offsetX, offsetY, offsetZ), material):
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	ANGLESTEP = pi/180
	TwoPI = 2*pi
	angle = TwoPI/360
	r = radius
	
	x = r * cos(Orientation*angle)
	z = r * sin(Orientation*angle)
				
	for sides in xrange(0,numSides+1):
		x1 = r * cos((Orientation+360/numSides*sides)*angle)
		z1 = r * sin((Orientation+360/numSides*sides)*angle)
		drawLine(level, material, (x+offsetX,offsetY,offsetZ+z), (x1+offsetX,offsetY,z1+offsetZ) )
		x = x1
		z = z1
			
def Cube(level, block, (x1,y1,z1),(x2,y2,z2)):
	# Draws a wireframe cube
	method = "CUBE"
	print '%s: Started at %s' % (method, time.ctime())

	# Render all the vertices
	
	drawLine(level, block, (x1, y1, z1), (x2, y1, z1) )
	drawLine(level, block, (x1, y1, z1), (x1, y2, z1) )
	drawLine(level, block, (x1, y1, z1), (x1, y1, z2) )
	drawLine(level, block, (x2, y2, z1), (x2, y2, z2) )
	drawLine(level, block, (x2, y2, z1), (x1, y2, z1) )
	drawLine(level, block, (x2, y2, z1), (x2, y1, z1) )
	drawLine(level, block, (x1, y2, z2), (x1, y2, z1) )
	drawLine(level, block, (x1, y2, z2), (x1, y1, z2) )
	drawLine(level, block, (x1, y2, z2), (x2, y2, z2) )
	drawLine(level, block, (x2, y1, z2), (x1, y1, z2) )
	drawLine(level, block, (x2, y1, z2), (x2, y2, z2) )
	drawLine(level, block, (x2, y1, z2), (x2, y1, z1) )
	
	print '%s: Ended at %s' % (method, time.ctime())	

def drawSphere(level,(x,y,z), r, material):
	RSQUARED = r*r
	for iterX in xrange(-r,r):
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			for iterY in xrange(-r,r):
				if XSQUARED + ZSQUARED + iterY*iterY <= RSQUARED:
					setBlock(level, material, XOFFSET, y+iterY, ZOFFSET)

def drawSphereIntersection(level,(x,y,z), r, material, (x2,y2,z2), r2):
	RSQUARED = r*r
	R2SQUARED = r2*r2
	for iterX in xrange(-r,r): # for each point in the sphere
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		X2OFFSET = XOFFSET-x2
		X2SQUARED = X2OFFSET * X2OFFSET
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			Z2OFFSET = ZOFFSET-z2
			Z2SQUARED = Z2OFFSET * Z2OFFSET
			for iterY in xrange(-r,r):
				YSQUARED = iterY * iterY
				YOFFSET = y+iterY
				Y2OFFSET = YOFFSET-y2
				Y2SQUARED = Y2OFFSET * Y2OFFSET
				if abs(XSQUARED + ZSQUARED + YSQUARED - RSQUARED) < 100: # point is on the sphere surface to be drawn
					if X2SQUARED + Z2SQUARED + Y2SQUARED <= R2SQUARED: # point is within the intersecting sphere
						setBlock(level, material, XOFFSET, YOFFSET, ZOFFSET)
#				if XSQUARED + ZSQUARED + YSQUARED < RSQUARED: # point is on the sphere surface to be drawn
#					if X2SQUARED + Z2SQUARED + Y2SQUARED <= R2SQUARED: # point is within the intersecting sphere
#						setBlock(level, (0,0), XOFFSET, YOFFSET, ZOFFSET)

						
def drawSphereSprinkles(level, (x,y,z), r, materialBase, materialOption, chance):
	RSQUARED = r*r
	for iterX in xrange(-r,r):
		XSQUARED = iterX*iterX
		XOFFSET = x+iterX
		for iterZ in xrange(-r,r):
			ZSQUARED = iterZ*iterZ
			ZOFFSET = z+iterZ
			for iterY in xrange(-r,r):
				if XSQUARED + ZSQUARED + iterY*iterY <= RSQUARED:
					if randint(0,100) < chance:
						setBlock(level, materialBase, XOFFSET, y+iterY, ZOFFSET)
					else:
						setBlock(level, materialOption, XOFFSET, y+iterY, ZOFFSET)

def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
						
# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt(x,y,z)
    if tempBlock == 0:
	setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
	level.setBlockDataAt(x, y, z, data)

#def setBlock(level, (block, data), (x, y, z)): # 2015 ajb
#	level.setBlockAt(int(x), int(y), int(z), block)
#	level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, y):
    	setBlockIfEmpty(level, (block, data), x, iterY, z)

def findSurface(x, y, z, level, box, options):
	# Find a candidate surface
	iterY = 250
	miny = y
	foundy = y
	while iterY > miny:
		block = level.blockAt(x,iterY,z)
		if block != 0: # not AIR
			foundy = iterY
			iterY = miny # end search, block found was a legitimate candidate for the surface				
		iterY = iterY -1
	return foundy

# Boxes
		
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
				
def	copyBlocksFromDBG(level,schematic, A, cursorPosn):
	(x1,y1,z1,x2,y2,z2) = (A.minx,A.miny,A.minz,A.maxx,A.maxy,A.maxz)
	(width, height, depth) = getBoxSize(schematic.bounds)

	if x2 > width or y2 > height or z2 > depth:
		return False
	else:
		level.copyBlocksFrom(schematic, A, cursorPosn)
	return True

def printBoundingBox(A):
	print 'BoundingBox %s %s %s %s %s %s' % (A.minx,A.miny,A.minz,A.maxx,A.maxy,A.maxz)
	
def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	#print 'ANALYSE %s %s %s' % (width, height, depth)

	minX = width
	minY = height
	minZ = depth
	maxX = 0
	maxY = 0
	maxZ = 0
	found = False
	
	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depth):
				if level.blockAt(iterX, iterY, iterZ) != 0:
					#print 'ANALYSING %s %s %s' % (iterX, iterY, iterZ)
					if iterX > maxX:
						maxX = iterX
					if iterY > maxY:
						maxY = iterY
					if iterZ > maxZ:
						maxZ = iterZ
				
					if iterX < minX:
						minX = iterX
					if iterY < minY:
						minY = iterY
					if iterZ < minZ:
						minZ = iterZ
						
					found = True

	#print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	#print '%s: Ended at %s' % (method, time.ctime())
	
	if found == False:
		return BoundingBox((0, 0, 0), (width, height, depth))	
	else:
		return BoundingBox((minX, 0, minZ), (maxX+1, maxY+1, maxZ+1))

def checkBoundingBoxIntersect(A, B):
	#print 'Checking BB A/B intersection '
	#printBoundingBox(A)
	#printBoundingBox(B)
	# Check for A completely to the left of B. https://github.com/mcedit/pymclevel/blob/master/box.py
	# http://www.toymaker.info/Games/html/3d_collisions.html
	if A.maxx < B.minx:
	    return False
	# Check for A to the right of B
	if A.minx > B.maxx:
	    return False
	# Check for A in front of B
	if A.maxz < B.minz:
	    return False
	# Check for A behind B
	if A.minz > B.maxz:
	    return False
	# Check for A above B
	if A.miny > B.maxy:
	    return False
	# Check for A below B
	if A.maxy < B.miny:
	   return False
	   
	# Collision has occurred
	#print 'Collision occurred'
	return True
	
def makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS):
	if COORDS == True:
		cX = cX - spawnerX
		cY = cY - spawnerY
		cZ = cZ - spawnerZ 
		theCommand = "/"+PREFIX+" ~"+str(cX)+" ~"+str(cY)+" ~"+str(cZ)+" "+str(SUFFIX)
	else:
		theCommand = "/"+PREFIX+" "+str(cX)+" "+str(cY)+" "+str(cZ)+" "+str(SUFFIX)

	chunk.TileEntities.append( 	createCommandBlockData(spawnerX, 
									spawnerY, 
									spawnerZ, 
									theCommand
								))
								
def createCommandBlockData(x, y, z, theCommand):
	e = TileEntity.Create("Control")
	e["Command"] = TAG_String(theCommand)
	TileEntity.setpos(e, (x, y, z))
	return e
	
def makePNGTicles(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "PNGTicles"
	print '%s: Started at %s' % (method, time.ctime())
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16
	PACKEDCHUNKSIZE = options["Generator Width"]
	if PACKEDCHUNKSIZE == 0:
		PACKEDCHUNKSIZE = CHUNKSIZE
	LAYERGAP = options["Layer Separation"]+1
	ORIENTATION = options["Orientation"]
	COORDS = options["Relative coordinates?"]	
	TRANSPARENCY_T = options["Transparency Threshold"]
	baseX = options["Generator X"]
	baseY = options["Generator Y"]
	baseZ = options["Generator Z"]
	Dx = options["Draw X"]
	Dy = options["Draw Y"]
	Dz = options["Draw Z"]
	OFFSET = options["Offset"]+1
	PREFIX = options["Prefix"]
	SUFFIX = options["Suffix"]
	SCALE = options["Scale"]
	METHOD = options["Method"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2


	packedSpawnerCount = 0
	CHUNKSIZE = 16
	PACKEDCHUNKSIZE = options["Generator Width"]
	if PACKEDCHUNKSIZE == 0:
		PACKEDCHUNKSIZE = CHUNKSIZE
	LAYERGAP = options["Layer Separation"]+1
	
	if METHOD == "Draw Line": # Create command blocks that creat particles alone a 3D line
		print '%s: Processing a Line' % (method)
		x = options["Line Start X"]
		y = options["Line Start Y"]
		z = options["Line Start Z"]
		x1 = options["Line End X"]
		y1 = options["Line End Y"]
		z1 = options["Line End Z"]
		dx = x1 - x
		dy = y1 - y
		dz = z1 - z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)

		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
			spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
			spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
			setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
			setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
			chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
						
			cX = (x+iter*cos(theta)*cos(phi))
			cY = (y+iter*sin(phi))
			cZ = (z+iter*sin(theta)*cos(phi))
		
			makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS)
			iter = iter+SCALE
			packedSpawnerCount = packedSpawnerCount+1
			chunk.dirty = True

	if METHOD == "Render PNG": # Draw picture
		print '%s: Processing a picture' % (method)
		filename = options["Path and Filename"]
		filename = filename.strip()
		if filename == "":
			filename = askOpenFile("Select an image...", False)
		f = open(filename, "rb")
		data = f.read()
		f.close()

		reader = png.Reader(bytes=data) # @Sethbling
		(width, height, pixels, metadata) = reader.asRGBA8() # @Sethbling
		pixels = list(pixels) # @Sethbling
		
		for iterY in xrange(0, height):
			print '%s: Processing row %s of %s' % (method, iterY, height)
			for iterX in xrange(0, width):
					colour = getPixel(pixels, iterX, iterY) # after @Sethbling	
					if opaque(colour, TRANSPARENCY_T): # @Sethbling
						(theBlock, theBlockData) = closestMaterial(colour) # @Sethbling
						(r,g,b,a) = colour
		
						spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
						spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
						spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
						setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
						chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
						cX = Dx+iterX*SCALE
						cY = Dy+(height-1-iterY)*SCALE # Fix inverted image
						cZ = Dz+0
						if ORIENTATION == "Z-Y":
							cX = Dx+0
							cY = Dy+(height-1-iterY)*SCALE # Fix inverted image
							cZ = Dz+iterX*SCALE
						elif ORIENTATION == "X-Z":
							cX = Dx+iterX*SCALE
							cY = Dy+0
							cZ = Dz+(height-1-iterY)*SCALE
						
						makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS)
						packedSpawnerCount = packedSpawnerCount+1
						chunk.dirty = True

	if METHOD == "Block Model": # Create command blocks that creat particles alone a 3D line
		MATERIALID = options["Material"].ID
		print '%s: Examining the selection box for material %s' % (method, MATERIALID)
	
		# Scan through the selection box and make a command block particle for each block of the right type
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				for iterX in xrange(0, width):
					tempBlock = level.blockAt(box.minx + iterX, box.miny + iterY, box.minz + iterZ)
					if tempBlock == MATERIALID: # We are in business! Man the hatches! Batten the mainsail! Create a particle command block
						# Manage the stack of spawners
						spawnerX = baseX + (packedSpawnerCount%PACKEDCHUNKSIZE)*OFFSET
						spawnerY = baseY + ((int)(packedSpawnerCount/(PACKEDCHUNKSIZE*PACKEDCHUNKSIZE)))*OFFSET*LAYERGAP
						spawnerZ = baseZ + ((int)(packedSpawnerCount/PACKEDCHUNKSIZE)%PACKEDCHUNKSIZE)*OFFSET
						setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
						setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
						chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)

						cX = (Dx+iterX*SCALE)
						cY = (Dy+iterY*SCALE)
						cZ = (Dz+iterZ*SCALE)						

						makePNGTicleCommandBlock(chunk,(cX,cY,cZ),(spawnerX,spawnerY,spawnerZ),PREFIX,SUFFIX,COORDS)
						packedSpawnerCount = packedSpawnerCount+1
						chunk.dirty = True
						
	print '%s: Ended at %s' % (method, time.ctime())

def councilWorks(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "COUNCIL WORKS"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (options["Material:"].ID, options["Material:"].blockData)
	edgeMaterial = (options["Edge Material:"].ID, options["Edge Material:"].blockData)
	supportMaterial = (options["Support Material:"].ID, options["Support Material:"].blockData)
	mixMaterial = (options["Mix Material:"].ID, options["Mix Material:"].blockData)
	MIXMATERIALCHANCE = options["Mix Material Chance 0-100:"]
	NOMATERIALCHANCE = options["No Material Chance 0-100:"]
	TUNNELSUPPORT = options["Tunnel Support?"]
	ARCHES = options["Arches?"]
	MEANDER = options["Meander?"]
	AUTOMATIC = options["... Or Automatic Mode?"]
	supportGap = options["Support Gap:"]
	(startX, startY, startZ) = (options["Start X:"], options["Start Y:"], options["Start Z:"] )
	(endX, endY, endZ) = (options["End X:"], options["End Y:"], options["End Z:"] )
	bWidth = options["Width:"]
	bHeight = options["Height:"]
	STEPSIZE = 0.25
	AIR = (0,0)
	# END CONSTANTS

	if AUTOMATIC == True:
		bHeight = height
		startY = box.miny
		endY = startY
		MEANDER = False
		if width < depth:
			bWidth = width
			startX = (int)(box.minx+width/2)
			endX = startX
			startZ = box.minz
			endZ = box.maxz
		else:
			bWidth = depth
			startX = box.minx
			endX = box.maxx
			startZ = (int)(box.minz+depth/2)
			endZ = startZ
	
	if supportGap < 1:
		supportGap = randint(2,16)
	
	squiggliness = 20 * randint(1,10)
	squiggleCounter = 0
	(basePosX, basePosY, basePosZ) = (startX,startY,startZ)
	(theta,phi,distance) = getDistanceVector( (basePosX, basePosY, basePosZ), (endX,endY,endZ))
	
	hWidth = (int)(bWidth / 2)
	for pathIter in xrange(0,(int)(distance/STEPSIZE)):
		ARCH = (int)(pathIter/STEPSIZE)%supportGap
		SUPPORTBLOCK = level.blockAt((int)(basePosX), (int)(basePosY+bHeight), (int)(basePosZ))
		for iter in xrange(-hWidth,hWidth):
			 # start block
			squiggleCounter = squiggleCounter+1
			if MEANDER == True and squiggleCounter % squiggliness == 0:
				theta = theta + randint(-1,1)*pi/32
			
			(x1, y1, z1) = getRelativePolar( (basePosX, basePosY, basePosZ), (theta+pi/2, 0, iter) )
			
			for iterY in xrange(0,bHeight):
				theMaterial = AIR
				if iterY == 0:
					if abs(iter) >= hWidth-1:
						theMaterial = edgeMaterial
					else:
						if randint(0,100) < NOMATERIALCHANCE:
							theMaterial = AIR
						elif randint(0,100) < MIXMATERIALCHANCE:
							theMaterial = mixMaterial
						else:
							theMaterial = material
				else:
					if ARCH == 0 and (ARCHES == True or (TUNNELSUPPORT == True and SUPPORTBLOCK != 0)):
						if abs(iter) >= hWidth-1 or iterY >= bHeight-1 or (bHeight - iterY) <= abs(iter*2):
							theMaterial = supportMaterial
						

				setBlock(level, theMaterial, x1, y1+iterY, z1)
		(basePosX, basePosY, basePosZ) = getRelativePolar( (basePosX, basePosY, basePosZ), (theta, phi, 0.25)) # oversample to prevent columns of missed blocks.
	
	print '%s: Ended at %s' % (method, time.ctime())
	
def Voronoi(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Voronoi"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	DOEDGES = options["Edges?"]
	MATERIALEDGE = (options["Edge Material"].ID,options["Edge Material"].blockData)
	# END CONSTANTS

	Q = []
	# Pass 1 - identify the location and type of each block in the selection box (use sparse regions)
	for iterX in xrange(box.minx, box.maxx):
		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				thisBlock = (level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ))
				if thisBlock != AIR:
					Q.append( (thisBlock, iterX, iterY, iterZ )  )

	# Pass 2 - identify the closest block to each point in space.
	for iterX in xrange(box.minx, box.maxx):
		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				thisBlock = (level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ))
				if thisBlock == AIR:
					# Work out the distance of this block from each of the anchor blocks.
					newBlock = AIR
					lastDistance = 999999999
					for iterQ in xrange(0, len(Q)):
						(controlBlock, x, y, z) = Q[iterQ]
						deltaX = x - iterX
						deltaY = y - iterY
						deltaZ = z - iterZ
						thisDistance = deltaX*deltaX + deltaY*deltaY + deltaZ*deltaZ
						if thisDistance < lastDistance:
							newBlock = controlBlock
							lastDistance = thisDistance # New champion to be beaten
					if newBlock != AIR:
						setBlock(level, newBlock, iterX, iterY, iterZ)
	
	# Optional Pass 3 - identify edges and mark them as the Edge block
	if DOEDGES == True:
		PQ = []
		for iterX in xrange(box.minx, box.maxx):
			print 'Do Edges: %s of %s' % (iterX, box.maxx)
			for iterY in xrange(box.miny, box.maxy):
				for iterZ in xrange(box.minz, box.maxz):
					thisBlock = (level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ))	
					if (level.blockAt(iterX+1, iterY, iterZ), level.blockDataAt(iterX+1, iterY, iterZ)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX-1, iterY, iterZ), level.blockDataAt(iterX-1, iterY, iterZ)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX, iterY+1, iterZ), level.blockDataAt(iterX, iterY+1, iterZ)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX, iterY-1, iterZ), level.blockDataAt(iterX, iterY-1, iterZ)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX, iterY, iterZ+1), level.blockDataAt(iterX, iterY, iterZ+1)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX, iterY, iterZ-1), level.blockDataAt(iterX, iterY, iterZ-1)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
		for ( block, x, y, z ) in PQ:
			setBlock(level, block, x, y, z)
					
	print '%s: Ended at %s' % (method, time.ctime())
		
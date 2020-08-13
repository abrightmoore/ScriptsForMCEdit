# This filter creates chests with every game block as an enumeration within them
# Suggested by @Dragnoz
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net) and @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from pymclevel import alphaMaterials, indevMaterials

from pymclevel import TAG_String # @Texelelf
#from pymclevel import TileEntity # @Texelelf  -- I can't believe I ever bothered importing that

# import from @Texelelf
from copy import deepcopy

from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long


# Block ID to name mapping table by FrodCube (youtube.com/FrodCube)
# http://www.mediafire.com/view/xyc135otvoj8n71/blockIDtoName3.py
names = {"0": "minecraft:air",
		"1": "minecraft:stone",
		"2": "minecraft:grass",
		"3": "minecraft:dirt",
		"4": "minecraft:cobblestone",
		"5": "minecraft:planks",
		"6": "minecraft:sapling",
		"7": "minecraft:bedrock",
		"8": "minecraft:flowing_water",
		"9": "minecraft:water",
		"10": "minecraft:flowing_lava",
		"11": "minecraft:lava",
		"12": "minecraft:sand",
		"13": "minecraft:gravel",
		"14": "minecraft:gold_ore",
		"15": "minecraft:iron_ore",
		"16": "minecraft:coal_ore",
		"17": "minecraft:log",
		"18": "minecraft:leaves",
		"19": "minecraft:sponge",
		"20": "minecraft:glass",
		"21": "minecraft:lapis_ore",
		"22": "minecraft:lapis_block",
		"23": "minecraft:dispenser",
		"24": "minecraft:sandstone",
		"25": "minecraft:noteblock",
		"26": "minecraft:bed",
		"27": "minecraft:golden_rail",
		"28": "minecraft:detector_rail",
		"29": "minecraft:sticky_piston",
		"30": "minecraft:web",
		"31": "minecraft:tallgrass",
		"32": "minecraft:deadbush",
		"33": "minecraft:piston",
		"34": "minecraft:piston_head",
		"35": "minecraft:wool",
		"36": "minecraft:piston_extension",
		"37": "minecraft:yellow_flower",
		"38": "minecraft:red_flower",
		"39": "minecraft:brown_mushroom",
		"40": "minecraft:red_mushroom",
		"41": "minecraft:gold_block",
		"42": "minecraft:iron_block",
		"43": "minecraft:double_stone_slab",
		"44": "minecraft:stone_slab",
		"45": "minecraft:brick_block",
		"46": "minecraft:tnt",
		"47": "minecraft:bookshelf",
		"48": "minecraft:mossy_cobblestone",
		"49": "minecraft:obsidian",
		"50": "minecraft:torch",
		"51": "minecraft:fire",
		"52": "minecraft:mob_spawner",
		"53": "minecraft:oak_stairs",
		"54": "minecraft:chest",
		"55": "minecraft:redstone_wire",
		"56": "minecraft:diamond_ore",
		"57": "minecraft:diamond_block",
		"58": "minecraft:crafting_table",
		"59": "minecraft:wheat",
		"60": "minecraft:farmland",
		"61": "minecraft:furnace",
		"62": "minecraft:lit_furnace",
		"63": "minecraft:standing_sign",
		"64": "minecraft:wooden_door",
		"65": "minecraft:ladder",
		"66": "minecraft:rail",
		"67": "minecraft:stone_stairs",
		"68": "minecraft:wall_sign",
		"69": "minecraft:lever",
		"70": "minecraft:stone_pressure_plate",
		"71": "minecraft:iron_door",
		"72": "minecraft:wooden_pressure_plate",
		"73": "minecraft:redstone_ore",
		"74": "minecraft:lit_redstone_ore",
		"75": "minecraft:unlit_redstone_torch",
		"76": "minecraft:redstone_torch",
		"77": "minecraft:stone_button",
		"78": "minecraft:snow_layer",
		"79": "minecraft:ice",
		"80": "minecraft:snow",
		"81": "minecraft:cactus",
		"82": "minecraft:clay",
		"83": "minecraft:reeds",
		"84": "minecraft:jukebox",
		"85": "minecraft:fence",
		"86": "minecraft:pumpkin",
		"87": "minecraft:netherrack",
		"88": "minecraft:soul_sand",
		"89": "minecraft:glowstone",
		"90": "minecraft:portal",
		"91": "minecraft:lit_pumpkin",
		"92": "minecraft:cake",
		"93": "minecraft:unpowered_repeater",
		"94": "minecraft:powered_repeater",
		"95": "minecraft:chest_locked_aprilfools_super_old_legacy_we_should_not_even_have_this",
		"96": "minecraft:trapdoor",
		"97": "minecraft:monster_egg",
		"98": "minecraft:stonebrick",
		"99": "minecraft:brown_mushroom_block",
		"100": "minecraft:red_mushroom_block",
		"101": "minecraft:iron_bars",
		"102": "minecraft:glass_pane",
		"103": "minecraft:melon_block",
		"104": "minecraft:pumpkin_stem",
		"105": "minecraft:melon_stem",
		"106": "minecraft:vine",
		"107": "minecraft:fence_gate",
		"108": "minecraft:brick_stairs",
		"109": "minecraft:stone_brick_stairs",
		"110": "minecraft:mycelium",
		"111": "minecraft:waterlily",
		"112": "minecraft:nether_brick",
		"113": "minecraft:nether_brick_fence",
		"114": "minecraft:nether_brick_stairs",
		"115": "minecraft:nether_wart",
		"116": "minecraft:enchanting_table",
		"117": "minecraft:brewing_stand",
		"118": "minecraft:cauldron",
		"119": "minecraft:end_portal",
		"120": "minecraft:end_portal_frame",
		"121": "minecraft:end_stone",
		"122": "minecraft:dragon_egg",
		"123": "minecraft:redstone_lamp",
		"124": "minecraft:lit_redstone_lamp",
		"125": "minecraft:double_wooden_slab",
		"126": "minecraft:wooden_slab",
		"127": "minecraft:cocoa",
		"128": "minecraft:sandstone_stairs",
		"129": "minecraft:emerald_ore",
		"130": "minecraft:ender_chest",
		"131": "minecraft:tripwire_hook",
		"132": "minecraft:tripwire",
		"133": "minecraft:emerald_block",
		"134": "minecraft:spruce_stairs",
		"135": "minecraft:birch_stairs",
		"136": "minecraft:jungle_stairs",
		"137": "minecraft:command_block",
		"138": "minecraft:beacon",
		"139": "minecraft:cobblestone_wall",
		"140": "minecraft:flower_pot",
		"141": "minecraft:carrots",
		"142": "minecraft:potatoes",
		"143": "minecraft:wooden_button",
		"144": "minecraft:skull",
		"145": "minecraft:anvil",
		"146": "minecraft:trapped_chest",
		"147": "minecraft:light_weighted_pressure_plate",
		"148": "minecraft:heavy_weighted_pressure_plate",
		"149": "minecraft:unpowered_comparator",
		"150": "minecraft:powered_comparator",
		"151": "minecraft:daylight_detector",
		"152": "minecraft:redstone_block",
		"153": "minecraft:quartz_ore",
		"154": "minecraft:hopper",
		"155": "minecraft:quartz_block",
		"156": "minecraft:quartz_stairs",
		"157": "minecraft:activator_rail",
		"158": "minecraft:dropper",
		"159": "minecraft:stained_hardened_clay",
		"170": "minecraft:hay_block",
		"171": "minecraft:carpet",
		"172": "minecraft:hardened_clay",
		"173": "minecraft:coal_block",
		"174": "minecraft:packed_ice",
		"175": "minecraft:double_plant",
		"256": "minecraft:iron_shovel",
		"257": "minecraft:iron_pickaxe",
		"258": "minecraft:iron_axe",
		"259": "minecraft:flint_and_steel",
		"260": "minecraft:apple",
		"261": "minecraft:bow",
		"262": "minecraft:arrow",
		"263": "minecraft:coal",
		"264": "minecraft:diamond",
		"265": "minecraft:iron_ingot",
		"266": "minecraft:gold_ingot",
		"267": "minecraft:iron_sword",
		"268": "minecraft:wooden_sword",
		"269": "minecraft:wooden_shovel",
		"270": "minecraft:wooden_pickaxe",
		"271": "minecraft:wooden_axe",
		"272": "minecraft:stone_sword",
		"273": "minecraft:stone_shovel",
		"274": "minecraft:stone_pickaxe",
		"275": "minecraft:stone_axe",
		"276": "minecraft:diamond_sword",
		"277": "minecraft:diamond_shovel",
		"278": "minecraft:diamond_pickaxe",
		"279": "minecraft:diamond_axe",
		"280": "minecraft:stick",
		"281": "minecraft:bowl",
		"282": "minecraft:mushroom_stew",
		"283": "minecraft:golden_sword",
		"284": "minecraft:golden_shovel",
		"285": "minecraft:golden_pickaxe",
		"286": "minecraft:golden_axe",
		"287": "minecraft:string",
		"288": "minecraft:feather",
		"289": "minecraft:gunpowder",
		"290": "minecraft:wooden_hoe",
		"291": "minecraft:stone_hoe",
		"292": "minecraft:iron_hoe",
		"293": "minecraft:diamond_hoe",
		"294": "minecraft:golden_hoe",
		"295": "minecraft:wheat_seeds",
		"296": "minecraft:wheat",
		"297": "minecraft:bread",
		"298": "minecraft:leather_helmet",
		"299": "minecraft:leather_chestplate",
		"300": "minecraft:leather_leggings",
		"301": "minecraft:leather_boots",
		"302": "minecraft:chainmail_helmet",
		"303": "minecraft:chainmail_chestplate",
		"304": "minecraft:chainmail_leggings",
		"305": "minecraft:chainmail_boots",
		"306": "minecraft:iron_helmet",
		"307": "minecraft:iron_chestplate",
		"308": "minecraft:iron_leggings",
		"309": "minecraft:iron_boots",
		"310": "minecraft:diamond_helmet",
		"311": "minecraft:diamond_chestplate",
		"312": "minecraft:diamond_leggings",
		"313": "minecraft:diamond_boots",
		"314": "minecraft:golden_helmet",
		"315": "minecraft:golden_chestplate",
		"316": "minecraft:golden_leggings",
		"317": "minecraft:golden_boots",
		"318": "minecraft:flint",
		"319": "minecraft:porkchop",
		"320": "minecraft:cooked_porkchop",
		"321": "minecraft:painting",
		"322": "minecraft:golden_apple",
		"323": "minecraft:sign",
		"324": "minecraft:wooden_door",
		"325": "minecraft:bucket",
		"326": "minecraft:water_bucket",
		"327": "minecraft:lava_bucket",
		"328": "minecraft:minecart",
		"329": "minecraft:saddle",
		"330": "minecraft:iron_door",
		"331": "minecraft:redstone",
		"332": "minecraft:snowball",
		"333": "minecraft:boat",
		"334": "minecraft:leather",
		"335": "minecraft:milk_bucket",
		"336": "minecraft:brick",
		"337": "minecraft:clay_ball",
		"338": "minecraft:reeds",
		"339": "minecraft:paper",
		"340": "minecraft:book",
		"341": "minecraft:slime_ball",
		"342": "minecraft:chest_minecart",
		"343": "minecraft:furnace_minecart",
		"344": "minecraft:egg",
		"345": "minecraft:compass",
		"346": "minecraft:fishing_rod",
		"347": "minecraft:clock",
		"348": "minecraft:glowstone_dust",
		"349": "minecraft:fish",
		"350": "minecraft:cooked_fished",
		"351": "minecraft:dye",
		"352": "minecraft:bone",
		"353": "minecraft:sugar",
		"354": "minecraft:cake",
		"355": "minecraft:bed",
		"356": "minecraft:repeater",
		"357": "minecraft:cookie",
		"358": "minecraft:filled_map",
		"359": "minecraft:shears",
		"360": "minecraft:melon",
		"361": "minecraft:pumpkin_seeds",
		"362": "minecraft:melon_seeds",
		"363": "minecraft:beef",
		"364": "minecraft:cooked_beef",
		"365": "minecraft:chicken",
		"366": "minecraft:cooked_chicken",
		"367": "minecraft:rotten_flesh",
		"368": "minecraft:ender_pearl",
		"369": "minecraft:blaze_rod",
		"370": "minecraft:ghast_tear",
		"371": "minecraft:gold_nugget",
		"372": "minecraft:nether_wart",
		"373": "minecraft:potion",
		"374": "minecraft:glass_bottle",
		"375": "minecraft:spider_eye",
		"376": "minecraft:fermented_spider_eye",
		"377": "minecraft:blaze_powder",
		"378": "minecraft:magma_cream",
		"379": "minecraft:brewing_stand",
		"380": "minecraft:cauldron",
		"381": "minecraft:ender_eye",
		"382": "minecraft:speckled_melon",
		"383": "minecraft:spawn_egg",
		"384": "minecraft:experience_bottle",
		"385": "minecraft:fire_charge",
		"386": "minecraft:writable_book",
		"387": "minecraft:written_book",
		"388": "minecraft:emerald",
		"389": "minecraft:item_frame",
		"390": "minecraft:flower_pot",
		"391": "minecraft:carrot",
		"392": "minecraft:potato",
		"393": "minecraft:baked_potato",
		"394": "minecraft:poisonous_potato",
		"395": "minecraft:map",
		"396": "minecraft:golden_carrot",
		"397": "minecraft:skull",
		"398": "minecraft:carrot_on_a_stick",
		"399": "minecraft:nether_star",
		"400": "minecraft:pumpkin_pie",
		"401": "minecraft:fireworks",
		"402": "minecraft:firework_charge",
		"403": "minecraft:enchanted_book",
		"404": "minecraft:comparator",
		"405": "minecraft:netherbrick",
		"406": "minecraft:quartz",
		"407": "minecraft:tnt_minecart",
		"408": "minecraft:hopper_minecart",
		"417": "minecraft:iron_horse_armor",
		"418": "minecraft:golden_horse_armor",
		"419": "minecraft:diamond_horse_armor",
		"420": "minecraft:lead",
		"421": "minecraft:name_tag",
		"422": "minecraft:command_block_minecart",
		"2256": "minecraft:record_13",
		"2257": "minecraft:record_cat",
		"2258": "minecraft:record_blocks",
		"2259": "minecraft:record_chirp",
		"2260": "minecraft:record_far",
		"2261": "minecraft:record_mall",
		"2262": "minecraft:record_mellohi",
		"2263": "minecraft:record_stal",
		"2264": "minecraft:record_strad",
		"2265": "minecraft:record_ward",
		"2266": "minecraft:record_11",
		"2267": "minecraft:record_wait"}

inputs = (
	  ("CHESTER", "label"),
	  #("Container", alphaMaterials.Chest), # https://github.com/codys/minecraft.print/blob/master/pymclevel/materials.py
	  ("Start Block", alphaMaterials.Stone),
	  ("End Block", alphaMaterials.Dropper),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
	tempBlock = level.blockAt(x,y,z)
	if tempBlock == 0:
		setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
	level.setBlockDataAt(x, y, z, data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, y):
    	setBlockIfEmpty(level, (block, data), x, iterY, z)
    	

def getBoxSize(box):
	return box.size


def createCommandBlockData(x, y, z, theCommand):
	e = TileEntity.Create("Control")
	e["Command"] = TAG_String(theCommand)
	TileEntity.setpos(e, (x, y, z))
	return e

def	CreateWallSign(x, y, z, text):
	e = TAG_Compound()
	e["x"] = TAG_Int(x)
	e["y"] = TAG_Int(y)
	e["z"] = TAG_Int(z)
	e["id"] = TAG_String("Sign")
	e["Text1"] = TAG_String("")
	e["Text2"] = TAG_String(text)
	e["Text3"] = TAG_String("")
	e["Text4"] = TAG_String("")
	return e
	
def createChestBlockData(x, y, z, blockID, maxData):
	e = TAG_Compound()
	e["x"] = TAG_Int(x)
	e["y"] = TAG_Int(y)
	e["z"] = TAG_Int(z)
	e["id"] = TAG_String("Chest")
	e["Lock"] = TAG_String("")
	e["Items"] = TAG_List()
	# TileEntity.setpos(e, (x, y, z))
	# Item access below modified from @Texelelf's MapIt filter
	item = TAG_Compound()
	item["id"] = TAG_String(names[blockID])
	item["Count"] = TAG_Byte(64)
	item["Damage"] = TAG_Short(0)
	item["Slot"] = TAG_Byte(0)
	if blockID in names:
		for blockData in xrange(0,27):
			newitem = deepcopy(item)
			newitem["Slot"] = TAG_Byte(blockData)
			newitem["Damage"] = TAG_Short(blockData%maxData)
			e["Items"].append(newitem)
	return e

# CreateItemFrame() below stolen/modified a little from @texelelf's MapIt filter
def CreateItemFrame(x, y, z, dir, blockID, invuln):
	TileY = y
	posy = float(y) + 0.5
	if dir == 1:
		direction = dir
		rotation = 90.0
		TileX = x + 1
		TileZ = z
		posx = float(x) + 0.9375
		posz = float(z) + 0.5
	elif dir == 3:
		rotation = 270.0
		direction = dir
		TileX = x - 1
		TileZ = z
		posx = float(x) + 0.0625
		posz = float(z) + 0.5
	elif dir == 0:
		rotation = 0.0
		direction = 2
		TileZ = z + 1
		TileX = x
		posz = float(z) + 0.9375
		posx = float(x) + 0.5
	elif dir == 2:
		rotation = 180.0
		direction = 0
		TileZ = z - 1
		TileX = x
		posz = float(z) + 0.0625
		posx = float(x) + 0.5
	iframe = TAG_Compound()
	iframe["id"] = TAG_String("ItemFrame")
	iframe["Pos"] = TAG_List()
	iframe["Pos"].append(TAG_Double(posx))
	iframe["Pos"].append(TAG_Double(posy))
	iframe["Pos"].append(TAG_Double(posz))
	iframe["Facing"] = TAG_Byte(dir)
	iframe["Dir"] = TAG_Byte(dir)
	iframe["Direction"] = TAG_Byte(direction)
	iframe["Facing"] = TAG_Byte(direction)  #new tag here
	iframe["Invulnerable"] = TAG_Byte(invuln)
	iframe["Motion"] = TAG_List()
	iframe["Motion"].append(TAG_Double(0.0))
	iframe["Motion"].append(TAG_Double(0.0))
	iframe["Motion"].append(TAG_Double(0.0))
	iframe["TileX"] = TAG_Int(TileX)
	iframe["TileY"] = TAG_Int(TileY)
	iframe["TileZ"] = TAG_Int(TileZ)
	iframe["Rotation"] = TAG_List()
	iframe["Rotation"].append(TAG_Float(rotation))
	iframe["Rotation"].append(TAG_Float(0.0))
	iframe["Item"] = TAG_Compound()
	iframe["Item"]["id"] = TAG_String(names[blockID])
	iframe["Item"]["Damage"] = TAG_Short(0)
	iframe["Item"]["Count"] = TAG_Byte(1)
	return iframe	

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Chester(level, box, options)		
	level.markDirtyBox(box)
	
def Chester(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "CHESTER"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	STARTBLOCK_ID = options["Start Block"].ID
	ENDBLOCK_ID = options["End Block"].ID
#	CONTAINER = (options["Container"].ID,options["Container"].blockData)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	CHUNKSIZE = 16
	
	if ENDBLOCK_ID < STARTBLOCK_ID: # Input validation: Swap if the user screwed up the order of block IDs
		t = STARTBLOCK_ID
		STARTBLOCK_ID = ENDBLOCK_ID
		ENDBLOCK_ID = t
	
	iterX = box.minx
	iterZ = box.minz
	iterY = box.miny
	
	for blockID in xrange(STARTBLOCK_ID, ENDBLOCK_ID): # for each block ID, create a chest and populate it with all the block data variants.
		blockIDstr = str(blockID)
		if blockIDstr in names:
			print '%s: Block ID %s (%s) at %s' % (method, blockID, names[blockIDstr], time.ctime())
			chunk = level.getChunk(iterX/CHUNKSIZE, iterZ/CHUNKSIZE)
			setBlock(level, (54,3), iterX, iterY, iterZ)
			chunk.TileEntities.append( createChestBlockData(iterX, iterY, iterZ, blockIDstr, 16))
			chunk.Entities.append( CreateItemFrame(iterX-1, iterY, iterZ, 1, blockIDstr, True))
			setBlock(level, (68,5), iterX+1, iterY, iterZ)
			chunk.TileEntities.append( CreateWallSign(iterX+1, iterY, iterZ, names[blockIDstr][10:]))
#			setBlock(level, (blockID,0), iterX-1, iterY, iterZ)
			chunk.dirty = True
			
			iterY = iterY + 1 # Calculate the next chest position
			if iterY >= box.maxy:
				iterY = box.miny
				iterX = iterX + 3
				if iterX >= box.maxx:
					iterX = box.minx
					iterZ = iterZ +2
					if iterZ >= box.maxz-1:
						iterZ = box.minz
			

			
	print '%s: Ended at %s' % (method, time.ctime())
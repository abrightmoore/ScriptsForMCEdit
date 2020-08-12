# This filter is for creating an Entity Zoo. See https://redd.it/5mqpmv and http://www.brightmoore.net/builds/mobridingmatrix
# abrightmoore@yahoo.com.au
# http://brightmoore.net

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0

def perform(level, box, options):

	MobRidingMatrix(level, box, options)

def createCommandBlockData(x, y, z, theCommand):
	e = TileEntity.Create("Control")
	e["Command"] = TAG_String(theCommand)
	TileEntity.setpos(e, (x, y, z))
	return e

	
def MobRidingMatrix(level, box, options):
	MOBS = [ 
#			"minecraft:area_effect_cloud", 
			"minecraft:armor_stand", 
			"minecraft:arrow", 
			"minecraft:bat", 
			"minecraft:blaze", 
			"minecraft:boat", 
			"minecraft:cave_spider", 
			"minecraft:chest_minecart",
			"minecraft:chicken",
			"minecraft:commandblock_minecart",
			"minecraft:cow",
			"minecraft:creeper",
			"minecraft:donkey",
			"minecraft:dragon_fireball",
			"minecraft:egg",
			"minecraft:elder_guardian",
			"minecraft:ender_crystal",
			"minecraft:ender_dragon",
			"minecraft:ender_pearl",
			"minecraft:enderman",
			"minecraft:endermite",
			"minecraft:evocation_fangs",
			"minecraft:evocation_illager",
			"minecraft:eye_of_ender_signal",
			"minecraft:falling_block",
			"minecraft:fireball",
			"minecraft:fireworks_rocket",
			"minecraft:furnace_minecart",
			"minecraft:ghast",
			"minecraft:giant",
			"minecraft:guardian",
			"minecraft:hopper_minecart",
			"minecraft:horse",
			"minecraft:husk",
			"minecraft:item",
			"minecraft:item_frame",
			"minecraft:leash_knot",
			"minecraft:lightning_bolt",
			"minecraft:llama",
			"minecraft:llama_spit",
			"minecraft:magma_cube",
			"minecraft:minecart",
			"minecraft:mooshroom",
			"minecraft:mule",
			"minecraft:ocelot",
			"minecraft:painting",
			"minecraft:pig",
			"minecraft:polar_bear",
			"minecraft:potion",
			"minecraft:rabbit",
			"minecraft:sheep",
			"minecraft:shulker",
			"minecraft:shulker_bullet",
			"minecraft:silverfish",
			"minecraft:skeleton",
			"minecraft:skeleton_horse",
			"minecraft:slime",
			"minecraft:small_fireball",
			"minecraft:snowball",
			"minecraft:snowman",
			"minecraft:spawner_minecart",
			"minecraft:spectral_arrow",
			"minecraft:spider",
			"minecraft:squid",
			"minecraft:stray",
#			"minecraft:tnt",
			"minecraft:tnt_minecart",
			"minecraft:vex",
			"minecraft:villager",
			"minecraft:villager_golem",
			"minecraft:vindication_illager",
			"minecraft:witch",
#			"minecraft:wither",
			"minecraft:wither_skeleton",
			"minecraft:wither_skull",
			"minecraft:wolf",
#			"minecraft:xp_bottle",
#			"minecraft:xp_orb",
			"minecraft:zombie",
			"minecraft:zombie_horse",
			"minecraft:zombie_pigman",
			"minecraft:zombie_villager"
			]				
	
	colours = "15 7 8 0 6 2 10 11 3 9 13 5 4 1 14 12".split()
	coloursList = map(int, colours)
	lightMaterial = (1,0)
			
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
		# /summon Enderman ~ ~ ~ {NoAI:1,Rotation:[90f],Passengers:[{id:CaveSpider,Rotation:[90f],NoAI:1}]}
		theCommand = "summon minecraft:armor_stand ~"+offset+" ~2 ~ {Invisible:1,Marker:1,NoGravity:1,Invulnerable:1,direction:[90.0,0.0,0.0],Passengers:[{id:"+rider+",NoAI:1,CustomName:Rider"+rider+",Invulnerable:1,PersistenceRequired:1,direction:[90.0,0.0,0.0],Motion:[0.0,0.0,0.0]}]}"
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
		# /summon Enderman ~ ~ ~ {NoAI:1,Rotation:[90f],Passengers:[{id:CaveSpider,Rotation:[90f],NoAI:1}]}
		theCommand = "summon minecraft:armor_stand ~"+offset+" ~2 ~ {Invisible:1,Marker:1,NoGravity:1,Invulnerable:1,direction:[90.0,0.0,0.0],Passengers:[{id:"+ridden+",NoAI:1,CustomName:Ridden"+ridden+",Invulnerable:1,PersistenceRequired:1,direction:[90.0,0.0,0.0],Motion:[0.0,0.0,0.0]}]}"
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
			theCommand = "summon "+ridden+" ~ ~2 ~ {Passengers:[{id:"+rider+",Invulnerable:1,PersistenceRequired:1,direction:[0.0,0.0,0.0],Motion:[0.0f,0.0f,0.0f],CustomName:"+"Rider"+rider+"}],CustomName:"+rider+"Riding"+ridden+",Invulnerable:1,PersistenceRequired:1,direction:[0.0,0.0,0.0],Motion:[0.0f,0.0f,0.0f]}"
			chunk.TileEntities.append(createCommandBlockData(dX, dY, dZ, theCommand))
			chunk.dirty = True
			setBlock(level, COMMANDBLOCK, dX, dY, dZ)
			if (iterZ)%2 == 0:	
				setBlock(level, (159,coloursList[iterX%16]), dX, dY+1, dZ)
			else:
				setBlock(level, (35,coloursList[iterX%16]), dX, dY+1, dZ)
			setBlock(level, STONE_BUTTON, dX, dY+2, dZ)
			iterX = iterX + 1
		iterZ = iterZ+1
	print '%s: Ended at %s' % (method, time.ctime())	

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

# @TheWorldFoundry

import Settlevolver_v1 as Settlevolver
from pymclevel import BoundingBox, TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from random import randint, random


def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	# Build the lore of the settlement by compiling it through the agents
	# Build a library to house the lore within
	
	print "Building a",generatorName,"at", box," by ",str(agent)

	cx = (box.minx+box.maxx)>>1
	cz = (box.minz+box.maxz)>>1
	
	y = box.miny
	
	# Make the chronicle...
	newline = "\n"	

	settlementTypes = [ " Village", " Vale", "ville", "town", " Borough", "burg" , " District", " City" ]

	settlementSuffix = settlementTypes[int(len(allStructures)/100)%len(settlementTypes)]	

	settlementName,discard = Settlevolver.nameRandom()
	
	settlementName = settlementName[::-1].title()+settlementSuffix
	
	print settlementName

	texts = []
	texts.append("Welcome to"+newline+"8888888888888888"+newline+"8000000000000008"+newline+"80MMMMMMMMMMMM08"+newline+"80MLLLLLLLLLLM08"+newline+"80MLCCCCCCCCLM08"+newline+newline+settlementName+newline+newline+"80MLCCCCCCCCLM08"+newline+"80MLLLLLLLLLLM08"+newline+"80MMMMMMMMMMMM08"+newline+"8000000000000008"+newline+"8888888888888888")


	lineNumber = 1
	text = "This place was built by"+newline
	for agent in agents:
		text += str(lineNumber)+": "+agent.name+newline
		if lineNumber%10 == 0 or agent == agents[len(agents)-1]:
			texts.append(text)
			text = ""
		lineNumber += 1
	
	texts.append("There are "+str(len(allStructures))+newline+"structures built"+newline+"by "+str(len(agents))+" people.")
	
	texts.append("We hope you enjoy your visit.")
	
	texts.append(newline+"8888888888888888"+newline+"8000000000000008"+newline+"80MMMMMMMMMMMM08"+newline+"80MLLLLLLLLLLM08"+newline+"80MLCCCCCCCCLM08"+newline+newline+settlementName+newline+"Almanac"+newline+newline+"80MLCCCCCCCCLM08"+newline+"80MLLLLLLLLLLM08"+newline+"80MMMMMMMMMMMM08"+newline+"8000000000000008"+newline+"8888888888888888")
	
	for agent in agents:
		texts.append(str(agent))
	
	theBook = makeBookNBT(texts) # Settlement Almanac - location of all the graves with personal stories
	placeChestWithItems(level, [theBook], cx, y, cz)

def placeMobSpawner(level, type, x, y, z):
	CHUNKSIZE = 16
	SPAWNER = 52
	
	if level.blockAt(x,y,z) != SPAWNER: # Don't try to create a duplicate set of NBT - it confuses the game.
		level.setBlockAt(x,y,z,SPAWNER)
		level.setBlockDataAt(x,y,z,0)
		
		control = TAG_Compound()
		control["x"] = TAG_Int(x)
		control["y"] = TAG_Int(y)
		control["z"] = TAG_Int(z)
		# control["id"] = TAG_String("minecraft:mob_spawner")

		nbt = makeMobSpawnerNBT(type)
		for key in nbt.keys():
			control[key] = nbt[key]
		
		try:
			chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
			chunka.TileEntities.append(control)
			chunka.dirty = True
		except ChunkNotPresent:
			print "ChunkNotPresent",(int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE)
	

def placeChestWithItems(level, things, x, y, z):
	CHUNKSIZE = 16
	CHEST = 54
	
	if level.blockAt(x,y,z) != CHEST: # Don't try to create a duplicate set of NBT - it confuses the game.
		level.setBlockAt(x,y,z,CHEST)
		level.setBlockDataAt(x,y,z,randint(2,5))
		
		control = TAG_Compound()
		control["x"] = TAG_Int(x)
		control["y"] = TAG_Int(y)
		control["z"] = TAG_Int(z)
		control["id"] = TAG_String("minecraft:chest")
		control["Lock"] = TAG_String("")
		items = TAG_List()
		control["Items"] = items
		slot = 0
		print things
		for thing in things:
			# if thing["id"].value != "minecraft:Nothing": # Handle empty slots
			if True:
				item = TAG_Compound()
				items.append(item)
				item["Slot"] = TAG_Byte(slot)
				slot += 1
				for key in thing.keys():
					item[key] = thing[key]
		
		try:
			chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
			chunka.TileEntities.append(control)
			chunka.dirty = True
		except ChunkNotPresent:
			print "ChunkNotPresent",(int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE)

def makeItemNBTWithDefaults(id):
	return makeItemNBT(id, 1, 0)

def makeItemNBT(id, count, damage):
	'''
		Prepare an item of the form:
	
	TAG_Compound({
      "Slot": TAG_Byte(21),
      "id": TAG_String(u'minecraft:iron_boots'),
      "Count": TAG_Byte(1),
      "Damage": TAG_Short(0),
    }),
	'''
	
	item = TAG_Compound()
	item["id"] = TAG_String("minecraft:"+id)
	item["Count"] = TAG_Byte(int(count))
	item["Damage"] = TAG_Short(int(damage))
	return item

def makeBookNBT(texts):
	book = TAG_Compound()
	book["id"] = TAG_String("minecraft:writable_book")
	book["Count"] = TAG_Byte(1)
	book["Damage"] = TAG_Short(0)

	tag = TAG_Compound()
	pages = TAG_List()
	LIMIT = 150
	discarded = False
	for page in texts:
		if len(pages) < LIMIT:
			pages.append(TAG_String(page))
		else:
			discarded = True
	if discarded == True:
		print "WARNING: Book length exceeded "+str(LIMIT)+" pages. Truncated!"
	book["tag"] = tag
	tag["pages"] = pages
	return book

def makeMobSpawnerNBT(type):
	obj = TAG_Compound()
	obj["id"] = TAG_String("minecraft:mob_spawner")
	obj["MaxNearbyEntities"] = TAG_Short(6)
	obj["RequiredPlayerRange"] = TAG_Short(8)
	obj["SpawnCount"] = TAG_Short(1)
	obj["MaxSpawnDelay"] = TAG_Short(800)
	obj["Delay"] = TAG_Short(371)
	obj["SpawnRange"] = TAG_Short(4)
	obj["MinSpawnDelay"] = TAG_Short(200)
	spawnData = TAG_Compound()
	obj["SpawnData"] = spawnData
	spawnData["id"] = TAG_String(type)
	
	spawnPotentials = TAG_List()
	obj["SpawnPotentials"] = spawnPotentials
	entity = TAG_Compound()
	spawnPotentials.append(entity)

	entity["Entity"] = TAG_Compound()
	entity["Entity"]["id"] = TAG_String(type)
	entity["Weight"] = TAG_Int(1)
	
	return obj

'''
EXAMPLE


TAG_Int(2130) TAG_Int(64) TAG_Int(-25) TAG_Compound({
  "MaxNearbyEntities": TAG_Short(6),
  "RequiredPlayerRange": TAG_Short(16),
  "SpawnCount": TAG_Short(4),
  "SpawnData": TAG_Compound({
    "id": TAG_String(u'minecraft:zombie'),
  }),
  "MaxSpawnDelay": TAG_Short(800),
  "Delay": TAG_Short(371),
  "x": TAG_Int(2130),
  "y": TAG_Int(64),
  "z": TAG_Int(-25),
  "id": TAG_String(u'minecraft:mob_spawner'),
  "SpawnRange": TAG_Short(4),
  "MinSpawnDelay": TAG_Short(200),
  "SpawnPotentials": TAG_List([
    TAG_Compound({
      "Entity": TAG_Compound({
        "id": TAG_String(u'minecraft:zombie'),
      }),
      "Weight": TAG_Int(1),
    }),
  ]),
})


TAG_Int(-1611) TAG_Int(64) TAG_Int(2139) TAG_Compound({
  "x": TAG_Int(-1611),
  "y": TAG_Int(64),
  "z": TAG_Int(2139),
  "Items": TAG_List([
    TAG_Compound({
      "Slot": TAG_Byte(12),
      "id": TAG_String(u'minecraft:writable_book'),
      "Count": TAG_Byte(1),
      "tag": TAG_Compound({
        "pages": TAG_List([
          TAG_String(u'   This is the chronicle of our settlement.'),
          TAG_String(u'Chapter 1. The beginning.\n\n\nIn the beginning there was nothing.'),
          TAG_String(u'Chapter 2. The building.\n\nSo we built it up.\n\n\nLots of it.\n\nBuilt.\n'),
          TAG_String(u'Woohoo!\n\n'),
        ]),
      }),
      "Damage": TAG_Short(0),
    }),
  ]),
  "id": TAG_String(u'minecraft:chest'),
  "Lock": TAG_String(u''),
})

'''
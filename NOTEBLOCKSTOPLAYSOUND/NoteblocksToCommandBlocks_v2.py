# Quick hack of BrianAwesomenes filter for note block / command block mapping. http://www.youtube.com/user/BrianAwesomenes
# Hack by @abrightmoore

#Original:
#Made by BrianAwesomenes
#This is my first filter, so don't get too excited
#http://www.youtube.com/user/BrianAwesomenes

from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String
from pymclevel import TAG_Int_Array
from pymclevel import TileEntity

displayName = "Noteblocks to Command Blocks"

inputs = (
	("Ludvig de Verdier's note filter", "label"),
	("Pitch", 0.5),
)

def resolveSound(theType, note):
	# Ludvig's mapping table
	
	sound = "NA"
	
	print '%s %s' % (theType, note)
	
	if theType == "harp":
		theSounds = ["ambient.cave.cave",
						"ambient.weather.rain",
						"ambient.weather.thunder",
						"dig.cloth",
						"dig.grass",
						"dig.gravel",
						"dig.sand",
						"dig.snow",
						"dig.stone",
						"dig.wood",
						"fire.fire",
						"fire.ignite",
						"fireworks.blast_far",
						"fireworks.blast",
						"fireworks.largeBlast_far",
						"fireworks.largeBlast",
						"fireworks.launch",
						"fireworks.twinkle_far",
						"fireworks.twinkle",
						"liquid.lava",
						"liquid.lavapop",
						"liquid.splash",
						"liquid.swim",
						"liquid.water",
						"minecart.base"
					]
		sound = theSounds[note]

	if theType == "bass":
		theSounds = ["minecart.inside",
						"mob.bat.death",
						"mob.bat.hurt",
						"mob.bat.idle",
						"mob.bat.loop",
						"mob.bat.takeoff",
						"mob.blaze.breathe",
						"mob.blaze.death",
						"mob.blaze.hit",
						"mob.cat.hiss",
						"mob.cat.hitt",
						"mob.cat.meow",
						"mob.cat.purr",
						"mob.cat.purreow",
						"mob.chicken.hurt",
						"mob.checken.plop",
						"mob.chicken.say",
						"mob.checken.step",
						"mob.cow.hurt",
						"mob.cow.say",
						"mob.cow.step",
						"mob.creeper.death",
						"mob.creeper.say",
						"mob.enderdragon.end",
						"mob.enderdragon.growl"
					]
		sound = theSounds[note]
					
	if theType == "bd":
		theSounds = ["mob.enderdragon.hit",
						"mob.enderdragon.wings",
						"mob.endermen.death",
						"mob.endermen.hit",
						"mob.endermen.idle",
						"mob.endermen.portal",
						"mob.endermen.scream",
						"mob.endermen.stare",
						"mob.ghast.affectionate_scream",
						"mob.ghast.charge",
						"mob.ghast.death",
						"mob.ghast.fireball",
						"mob.ghast.moan",
						"mob.ghast.scream",
						"mob.horse.angry",
						"mob.horse.armor",
						"mob.horse.breathe",
						"mob.horse.death",
						"mob.horse.gallop",
						"mob.horse.hit",
						"mob.horse.idle",
						"mob.horse.jump",
						"mob.horse.land",
						"mob.horse.leather",
						"mob.horse.soft"
					]
		sound = theSounds[note]
					
	if theType == "snare":
		theSounds = ["mob.horse.wood",
					"mob.horse.donkey.angry",
					"mob.horse.donkey.death",
					"mob.horse.donkey.hit",
					"mob.horse.donkey.idle",
					"mob.horse.skeleton.death",
					"mob.horse.skeleton.hit",
					"mob.horse.skeleton.idle",
					"mob.horse.zombie.death",
					"mob.horse.zombie.hit",
					"mob.horse.zombie.idle",
					"mob.irongolem.death",
					"mob.irongolem.hit",
					"mob.irongolem.throw",
					"mob.irongolem.walk",
					"mob.magmacube.big",
					"mob.magmacube.jump",
					"mob.magmacube.small",
					"mob.pig.death",
					"mob.pig.say",
					"mob.pig.step",
					"mob.sheep.say",
					"mob.sheep.shear",
					"mob.sheep.step",
					"mob.silverfish.hit"
				]
		sound = theSounds[note]
				
	if theType == "hat":
		theSounds = ["mob.silverfish.kill",
						"mob.silverfish.say",
						"mob.silverfish.step",
						"mob.skeleton.death",
						"mob.skeleton.hurt",
						"mob.skeleton.say",
						"mob.skeleton.step",
						"mob.slime.attack",
						"mob.slime.big",
						"mob.slime.small",
						"mob.spider.death",
						"mob.spider.say",
						"mob.spider.step",
						"mob.villager.death",
						"mob.villager.haggle",
						"mob.villager.hit",
						"mob.villager.idle",
						"mob.villager.no",
						"mob.villager.yes",
						"mob.wither.death",
						"mob.wither.hurt",
						"mob.wither.idle",
						"mob.wither.shoot",
						"mob.wither.spawn",
						"mob.wolf.bark"
					]
		sound = theSounds[note]
					
		# is pling going to be used?
					
	return sound
	

def perform(level, box, options):
	nBlocks = []
	removeTiles = []
	#Materials (If you are wondering I did not do these by hand)
	#There may be a few new blocks that aren't included in this list, but it shouldn't really matter anyway
	rock = [1, 4, 7, 14, 15, 16, 21, 22, 23, 24, 43, 44, 45, 48, 49, 52, 56, 61, 62, 67, 70, 73, 74, 87, 98, 108, 109, 112, 113, 114, 116, 120, 121, 128, 129, 130, 139]
	wood = [5, 17, 25, 47, 53, 54, 58, 63, 64, 68, 72, 84, 85, 95, 96, 99, 100, 107, 125, 126, 134, 135, 136]
	glass = [20, 89, 102, 138]
	sand = [12, 13, 88]
	
	for (chunk, slices, point) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz and t["id"].value == "Music":
				nBlocks.append(t)
			for n in nBlocks:
				if "note" in n:
					note = n["note"].value
					#pitch = round(0.5*(1.0594632**note),8)
					#pitchString = str(pitch)
					pitchString = options["Pitch"] 
					
					type = "harp"
					below = level.blockAt(x, y - 1, z)
					if below in rock:
						
						type = "bd"
					elif below in wood:
						type = "bass"
					elif below in glass:
						type = "hat"
					elif below in sand:
						type = "snare"
					elif below == 42:
						type = "pling"
					
					theSoundCommand = resolveSound(type, note)
					
					command = "/playsound " + theSoundCommand + " @a ~0 ~0 ~0 1 " + str(pitchString)
					level.setBlockAt(x,y,z,137)
					n["Command"] = TAG_String(command)
					n["id"] = TAG_String("Control")
					if "note" in n:
						del n["note"]
				
	#for (chunk, tileEntity) in removeTiles:
		#chunk.TileEntities.remove(tileEntity)
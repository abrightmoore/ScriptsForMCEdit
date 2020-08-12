# This filter is for creating ArmorStand entities above each command block found in the selection region, per @CocoaMix86
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_
import time # for timing

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from numpy import *
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import *
from random import Random # @Codewarrior0
import inspect # @Texelelf
from PIL import Image
import png

# GLOBAL
CHUNKSIZE = 16

# Filter pseudocode:
#

inputs = (
		("ArmourStands", "label"),
		("Method", ("Exact","Range","Sphere")),
		("Chance", 10),
		("Base Blocks", ("string","value=1 2")),
		("CustomName", ("string","value=AS")),
		("CustomNameVisible", 0),
		("Invulnerable", 1),
		("Invisible", 0),
		("NoGravity",1),
		("Marker", 1),
		("Small", 0),
		("ShowArms", 1),
		("NoBasePlate", 1),
		("HandItem 1", ("string","value=diamond_sword")),
		("HandItem 2", ("string","value=iron_sword")),
		("ArmorItem 1", ("string","value=diamond_boots")),
		("ArmorItem 2", ("string","value=diamond_leggings")),
		("ArmorItem 3", ("string","value=diamond_chestplate")),
		("ArmorItem 4", ("string","value=skull")),
		("ArmorItem 4 Data", 2),
		("Pose Body X", 10),
		("Pose Body Y", 10),
		("Pose Body Z", 10),
		("Pose Head X", 30),
		("Pose Head Y", 20),
		("Pose Head Z", 10),
		("Pose RightArm X", 30),
		("Pose RightArm Y", 20),
		("Pose RightArm Z", 10),
		("Pose LeftArm X", 30),
		("Pose LeftArm Y", 20),
		("Pose LeftArm Z", 10),
		("Pose RightLeg X", 10),
		("Pose RightLeg Y", 10),
		("Pose RightLeg Z", 10),
		("Pose LeftLeg X", 10),
		("Pose LeftLeg Y", 10),
		("Pose LeftLeg Z", 10),
		("MotionX",0.0),
		("MotionY",0.0),
		("MotionZ",0.0),
		("RotationX",179.0),
		("RotationY",179.0),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	armourCommand(level, box, options)

	FuncEnd(level,box,options,method) # Log end	

def armourCommand(level, box, options):
	# Local variables
	method = "armourCommand"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	AIR = (0,0)
	matWeapons = ["wooden","stone","iron","diamond","golden"]
	Weapons = ["hoe","axe","sword","shovel","pickaxe"]
	# matArmour = ["leather","chainmail","iron","diamond","golden"]
	matArmour = ["leather","iron","diamond","golden"]
	Armour = ["boots","leggings","chestplate","helmet"]
	
	CMDBLOCKS = options["Base Blocks"] # [137, 210, 211]
	CMDBLOCKSPLIT = CMDBLOCKS.split()
	CMDBLOCK = map(int, CMDBLOCKSPLIT)
	METHOD = options["Method"]
	as_CustomName = options["CustomName"]
	as_Invisible = options["Invisible"]
	as_CustomNameVisible = options["CustomNameVisible"]
	as_Invulnerable = options["Invulnerable"]
	as_Marker = options["Marker"]
	as_NoGravity = options["NoGravity"]
	as_MotionX = options["MotionX"]
	as_MotionY = options["MotionY"]
	as_MotionZ = options["MotionZ"]
	as_RotationX = options["RotationX"]
	as_RotationY = options["RotationY"]
	as_Small = options["Small"]
	as_ShowArms = options["ShowArms"]
	as_NoBasePlate = options["NoBasePlate"]
	as_HandItem1 = options["HandItem 1"]
	as_HandItem2 = options["HandItem 2"]
	as_ArmorItem1 = options["ArmorItem 1"]
	as_ArmorItem2 = options["ArmorItem 2"]
	as_ArmorItem3 = options["ArmorItem 3"]
	as_ArmorItem4 = options["ArmorItem 4"]
	as_ArmorItem4Data = options["ArmorItem 4 Data"]
	as_PoseBodyX = options["Pose Body X"]
	as_PoseBodyY = options["Pose Body Y"]
	as_PoseBodyZ = options["Pose Body Z"]
	as_PoseHeadX = options["Pose Head X"]
	as_PoseHeadY = options["Pose Head Y"]
	as_PoseHeadZ = options["Pose Head Z"]
	as_PoseRightArmX = options["Pose RightArm X"]
	as_PoseRightArmY = options["Pose RightArm Y"]
	as_PoseRightArmZ = options["Pose RightArm Z"]
	as_PoseLeftArmX = options["Pose LeftArm X"]
	as_PoseLeftArmY = options["Pose LeftArm Y"]
	as_PoseLeftArmZ = options["Pose LeftArm Z"]
	as_PoseRightLegX = options["Pose RightLeg X"]
	as_PoseRightLegY = options["Pose RightLeg Y"]
	as_PoseRightLegZ = options["Pose RightLeg Z"]
	as_PoseLeftLegX = options["Pose LeftLeg X"]
	as_PoseLeftLegY = options["Pose LeftLeg Y"]
	as_PoseLeftLegZ = options["Pose LeftLeg Z"]
	CHANCE = options["Chance"]

	if METHOD != "Sphere":
		for x in xrange(box.minx,box.maxx):
			for z in xrange(box.minz,box.maxz):
				for y in xrange(box.miny,box.maxy):
					(theBlock, theBlockData) = getBlock(level, x, y, z)
					print theBlock
					if theBlock in CMDBLOCK and randint(1,100) <= CHANCE and getBlock(level, x, y+1, z) == AIR and getBlock(level, x, y+2, z) == AIR:
						# Create a new ArmorStand Entity above this block with the nominated string as the NBT
						print 'Taking a stand'
						if METHOD == "Exact":
							createArmorStand(level, x, y+1, z, as_CustomName, as_Invisible, as_CustomNameVisible, as_Invulnerable, as_Marker, as_NoGravity, as_MotionX, as_MotionY, as_MotionZ, as_RotationX, as_RotationY,as_Small,as_ShowArms,as_NoBasePlate,as_HandItem1,as_HandItem2,as_ArmorItem1,as_ArmorItem2,as_ArmorItem3,as_ArmorItem4,as_ArmorItem4Data,as_PoseBodyX,as_PoseBodyY,as_PoseBodyZ,as_PoseHeadX,as_PoseHeadY,as_PoseHeadZ,as_PoseRightArmX,as_PoseRightArmY,as_PoseRightArmZ,as_PoseLeftArmX,as_PoseLeftArmY,as_PoseLeftArmZ,as_PoseRightLegX,as_PoseRightLegY,as_PoseRightLegZ,as_PoseLeftLegX,as_PoseLeftLegY,as_PoseLeftLegZ) # After @Sethbling
						elif METHOD == "Range":
							as_HandItem1 = matWeapons[randint(0,len(matWeapons)-1)]+"_"+Weapons[randint(0,len(Weapons)-1)]
							as_HandItem2 = matWeapons[randint(0,len(matWeapons)-1)]+"_"+Weapons[randint(0,len(Weapons)-1)]
							if randint(1,100) < 5:
								as_HandItem1 = "bow"
							elif randint(1,100) < 2:
								as_HandItem1 = "shield"
							elif randint(1,100) < 2:
								as_HandItem1 = "arrow"
							elif randint(1,100) < 2:
								as_HandItem1 = ""
							if randint(1,100) < 5:
								as_HandItem2 = "shield"
							elif randint(1,100) < 2:
								as_HandItem2 = "bow"
							elif randint(1,100) < 2:
								as_HandItem2 = "arrow"
							elif randint(1,100) < 2:
								as_HandItem2 = ""
								
							as_Boots = matArmour[randint(0,len(matArmour)-1)]+"_"+Armour[0]
							as_Pants = matArmour[randint(0,len(matArmour)-1)]+"_"+Armour[1]
							as_Chest = matArmour[randint(0,len(matArmour)-1)]+"_"+Armour[2]
							ai4 = as_ArmorItem4
							as_Helmet = matArmour[randint(0,len(matArmour)-1)]+"_"+Armour[3]
						
							phx = randint(-as_PoseHeadX,as_PoseHeadX)
							phy = randint(-as_PoseHeadY,as_PoseHeadY)
							phz = randint(-as_PoseHeadZ,as_PoseHeadZ)
							pbx = randint(-as_PoseBodyX,as_PoseBodyX)
							pby = randint(-as_PoseBodyY,as_PoseBodyY)
							pbz = randint(-as_PoseBodyZ,as_PoseBodyZ)
							prax = randint(-as_PoseRightArmX,as_PoseRightArmX)
							pray = randint(-as_PoseRightArmY,as_PoseRightArmY)
							praz = randint(-as_PoseRightArmZ,as_PoseRightArmZ)
							plax = randint(-as_PoseLeftArmX,as_PoseLeftArmX)
							play = randint(-as_PoseLeftArmY,as_PoseLeftArmY)
							plaz = randint(-as_PoseLeftArmZ,as_PoseLeftArmZ)
							prlx = randint(-as_PoseRightLegX,as_PoseRightLegX)
							prly = randint(-as_PoseRightLegY,as_PoseRightLegY)
							prlz = randint(-as_PoseRightLegZ,as_PoseRightLegZ)
							pllx = randint(-as_PoseLeftLegX,as_PoseLeftLegX)
							plly = randint(-as_PoseLeftLegY,as_PoseLeftLegY)
							pllz = randint(-as_PoseLeftLegZ,as_PoseLeftLegZ)
							rx = randint(-as_RotationX,as_RotationX)
							ry = randint(-as_RotationY,as_RotationY)
							createArmorStand(level, x, y+1, z, as_CustomName, as_Invisible, as_CustomNameVisible, as_Invulnerable, as_Marker, as_NoGravity, as_MotionX, as_MotionY, as_MotionZ, rx,ry,as_Small,as_ShowArms,as_NoBasePlate,as_HandItem1,as_HandItem2,as_Boots,as_Pants,as_Chest,as_Helmet,0,pbx,pby,pbz,phx,phy,phz,prax,pray,praz,plax,play,plaz,prlx,prly,prlz,pllx,plly,pllz) # After @Sethbling
							
							# as_ArmorItem4 = "skull"
							createArmorStand(level, x, y+1, z, as_CustomName, 1, 0, as_Invulnerable, as_Marker, as_NoGravity, as_MotionX, as_MotionY, as_MotionZ, rx,ry,as_Small,0,0,"","","","","",ai4,as_ArmorItem4Data,pbx,pby,pbz,phx,phy,phz,prax,pray,praz,plax,play,plaz,prlx,prly,prlz,pllx,plly,pllz) # After @Sethbling
	elif METHOD == "Sphere":
		BS = 10
		if as_Small == 1:
			BS = BS/2
		BLOCKRADIUS = 1.0/16*BS/2
		ANGLE = pi/180
		radius = (centreWidth+centreDepth+centreHeight)/3
		for theta in xrange(-180,181):
			if theta%10 == 0:
				for phi in xrange(-90,91):
					# create an ArmorStand with a block in the headslot at a location in a sphere defined by theta and phi.
					if phi%10 == 0:
						print theta,phi
						dx = cos(ANGLE*theta)*cos(ANGLE*phi)
						dy = sin(ANGLE*(phi))
						dz = sin(ANGLE*theta)*cos(ANGLE*phi)
						x = box.minx+centreWidth+(radius+BLOCKRADIUS)*dx #+(radius+BLOCKRADIUS)*dx #+BLOCKRADIUS*dx
						y = box.miny+centreHeight+(radius+BLOCKRADIUS)*dy #+(radius+BLOCKRADIUS)*dy #+BLOCKRADIUS*dy
						z = box.minz+centreDepth+(radius+BLOCKRADIUS)*dz #+(radius+BLOCKRADIUS)*dz #+BLOCKRADIUS*dz
						phx = as_PoseHeadX
						phy = as_PoseHeadY
						phz = as_PoseHeadZ+int(-degrees(dy))
						rx = as_RotationX+theta
						
						# I need to move the armorstand in the OPPOSITE direction of the vertical rotation a little to keep it centred on the centre of the block and avoid nasty issues with things lining up.
					
						createArmorStand(level, x, y, z, as_CustomName, as_Invisible, as_CustomNameVisible, as_Invulnerable, as_Marker, as_NoGravity, as_MotionX, as_MotionY, as_MotionZ, rx, as_RotationY,as_Small,as_ShowArms,as_NoBasePlate,as_HandItem1,as_HandItem2,as_ArmorItem1,as_ArmorItem2,as_ArmorItem3,as_ArmorItem4,as_ArmorItem4Data,as_PoseBodyX,as_PoseBodyY,as_PoseBodyZ,phx,phy,phz,as_PoseRightArmX,as_PoseRightArmY,as_PoseRightArmZ,as_PoseLeftArmX,as_PoseLeftArmY,as_PoseLeftArmZ,as_PoseRightLegX,as_PoseRightLegY,as_PoseRightLegZ,as_PoseLeftLegX,as_PoseLeftLegY,as_PoseLeftLegZ)
								
					
	FuncEnd(level,box,options,method) # Log end	

def createArmorStand(level, x, y, z, customName, Invisible, CustomNameVisible, Invulnerable, Marker, NoGravity, MotionX, MotionY, MotionZ, RotationX, RotationY, Small,ShowArms,NoBasePlate,HandItem1,HandItem2,ArmorItem1,ArmorItem2,ArmorItem3,ArmorItem4,ArmorItem4Data,PoseBodyX,PoseBodyY,PoseBodyZ,PoseHeadX,PoseHeadY,PoseHeadZ,PoseRightArmX,PoseRightArmY,PoseRightArmZ,PoseLeftArmX,PoseLeftArmY,PoseLeftArmZ,PoseRightLegX,PoseRightLegY,PoseRightLegZ,PoseLeftLegX,PoseLeftLegY,PoseLeftLegZ): # After @Sethbling
	print("New ArmorStand named "+customName)
	
	mob = TAG_Compound()
	mob["CustomName"] = TAG_String(customName)
	mob["Invisible"] = TAG_Byte(Invisible)
	mob["Small"] = TAG_Byte(Small)
	mob["ShowArms"] = TAG_Byte(ShowArms)
	mob["NoBasePlate"] = TAG_Byte(NoBasePlate)
	mob["CustomNameVisible"] = TAG_Byte(CustomNameVisible)
	mob["Invulnerable"] = TAG_Byte(Invulnerable)
	mob["Marker"] = TAG_Byte(Marker)
	mob["NoGravity"] = TAG_Byte(NoGravity)
	mob["OnGround"] = TAG_Byte(1)
	mob["Air"] = TAG_Short(300)
	mob["DeathTime"] = TAG_Short(0)
	mob["Fire"] = TAG_Short(-1)
	mob["Health"] = TAG_Short(20)
	mob["HurtTime"] = TAG_Short(0)
	mob["Age"] = TAG_Int(0)
	mob["FallDistance"] = TAG_Float(0)
	mob["Motion"] = TAG_List()
	mob["Motion"].append(TAG_Double(MotionX))
	mob["Motion"].append(TAG_Double(MotionY))
	mob["Motion"].append(TAG_Double(MotionZ))
	mob["Pos"] = TAG_List()
	mob["Pos"].append(TAG_Double(x + 0.5))
	mob["Pos"].append(TAG_Double(y))
	mob["Pos"].append(TAG_Double(z + 0.5))
	mob["Rotation"] = TAG_List()
	mob["Rotation"].append(TAG_Float(RotationX))
	mob["Rotation"].append(TAG_Float(RotationY))

	tl_AI = TAG_List()
	tc_AI1 = TAG_Compound()
	tc_AI1["Count"] = TAG_Byte(1)
	tc_AI1["id"] = TAG_String(HandItem1)
	tl_AI.append(tc_AI1)
	tc_AI1 = TAG_Compound()
	tc_AI1["Count"] = TAG_Byte(1)
	tc_AI1["id"] = TAG_String(HandItem2)
	tl_AI.append(tc_AI1)
	mob["HandItems"] = tl_AI
	
	tl_AI = TAG_List()
	tc_AI1 = TAG_Compound()
	tc_AI1["Count"] = TAG_Byte(1)
	tc_AI1["id"] = TAG_String(ArmorItem1)
	tl_AI.append(tc_AI1)
	tc_AI1 = TAG_Compound()
	tc_AI1["Count"] = TAG_Byte(1)
	tc_AI1["id"] = TAG_String(ArmorItem2)
	tl_AI.append(tc_AI1)
	tc_AI1 = TAG_Compound()
	tc_AI1["Count"] = TAG_Byte(1)
	tc_AI1["id"] = TAG_String(ArmorItem3)
	tl_AI.append(tc_AI1)
	tc_AI1 = TAG_Compound()
	tc_AI1["Count"] = TAG_Byte(1)
	tc_AI1["id"] = TAG_String(ArmorItem4)
	tc_AI1["Damage"] = TAG_Short(ArmorItem4Data)
	tl_AI.append(tc_AI1)
	mob["ArmorItems"] = tl_AI

	tc_Pose = TAG_Compound()
	tl_Pose = TAG_List()
	tl_Pose.append(TAG_Float(PoseBodyX))
	tl_Pose.append(TAG_Float(PoseBodyY))
	tl_Pose.append(TAG_Float(PoseBodyZ))
	tc_Pose["Body"] = tl_Pose
	tl_Pose = TAG_List()
	tl_Pose.append(TAG_Float(PoseHeadX))
	tl_Pose.append(TAG_Float(PoseHeadY))
	tl_Pose.append(TAG_Float(PoseHeadZ))
	tc_Pose["Head"] = tl_Pose
	tl_Pose = TAG_List()
	tl_Pose.append(TAG_Float(PoseRightArmX))
	tl_Pose.append(TAG_Float(PoseRightArmY))
	tl_Pose.append(TAG_Float(PoseRightArmZ))
	tc_Pose["RightArm"] = tl_Pose
	tl_Pose = TAG_List()
	tl_Pose.append(TAG_Float(PoseLeftArmX))
	tl_Pose.append(TAG_Float(PoseLeftArmY))
	tl_Pose.append(TAG_Float(PoseLeftArmZ))
	tc_Pose["LeftArm"] = tl_Pose
	tl_Pose = TAG_List()
	tl_Pose.append(TAG_Float(PoseRightLegX))
	tl_Pose.append(TAG_Float(PoseRightLegY))
	tl_Pose.append(TAG_Float(PoseRightLegZ))
	tc_Pose["RightLeg"] = tl_Pose
	tl_Pose = TAG_List()
	tl_Pose.append(TAG_Float(PoseLeftLegX))
	tl_Pose.append(TAG_Float(PoseLeftLegY))
	tl_Pose.append(TAG_Float(PoseLeftLegZ))
	tc_Pose["LeftLeg"] = tl_Pose	
	mob["Pose"] = tc_Pose
	
	mob["id"] = TAG_String("ArmorStand")
	chunk = level.getChunk(int(x) / CHUNKSIZE, int(z) / CHUNKSIZE)
	chunk.Entities.append(mob)
	chunk.dirty = True

	
	
####################################### LIBS
	
def FuncStart(level, box, options, method):
	# abrightmoore -> shim to prepare a function.
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	# other initialisation methods go here
	return (method, (width, height, depth), (centreWidth, centreHeight, centreDepth))

def FuncEnd(level, box, options, method):
	print '%s: Ended at %s' % (method, time.ctime())
	
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	

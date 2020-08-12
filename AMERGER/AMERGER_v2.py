# @TheWorldFoundry

from pymclevel import alphaMaterials

inputs = (
		("AMERGER", "label"),
		("Mode:", ( "Copy","Merge")),
		("Condition:", ( "AND","XOR" )),
		("Replace only?", False),
		("Replace material:", alphaMaterials.WhiteWool),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)



AIR = (0,0)

def perform(level,box,options):
	''' Capture an object with air spaces and merge it with the target - but only where the target and the TEMPLATE have a block
	''' 
	global TEMPLATE
	
	
	if options["Mode:"] == "Copy":
		print "Copying",box
		TEMPLATE = level.extractSchematic(box)
	elif options["Mode:"] == "Merge":
		height = box.maxy-box.miny
		width = box.maxx-box.minx
		depth = box.maxz-box.minz
	
		for y in xrange(0,height):
			for z in xrange(0,depth):
				for x in xrange(0,width):
					tempBlock = getBlock(TEMPLATE,x,y,z)
					(px,py,pz) = (box.minx+x,box.miny+y,box.minz+z)
					targetBlock = getBlock(level,px,py,pz)
					if options["Condition:"] == "AND" and tempBlock != AIR and targetBlock != AIR and ((options["Replace only?"] == True and targetBlock == (options["Replace material:"].ID,options["Replace material:"].blockData)) or options["Replace only?"] == False): # Both are present
						setBlock(level,px,py,pz,tempBlock)
					elif options["Condition:"] == "XOR" and ((tempBlock == AIR and targetBlock != AIR) or (tempBlock != AIR and targetBlock == AIR)):
						if tempBlock != AIR:
							setBlock(level,px,py,pz,tempBlock)
						elif targetBlock != AIR:
							setBlock(level,px,py,pz,AIR)
	level.markDirtyBox(box)			

	
# VOXEL DRAWING PRIMITIVES
def setBlock(level,x,y,z,material):
	(bID,bData) = material
	level.setBlockAt(x,y,z,bID)
	level.setBlockDataAt(x,y,z,bData)

def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

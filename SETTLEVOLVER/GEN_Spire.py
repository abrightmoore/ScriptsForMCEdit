# @TheWorldFoundry

import Settlevolver_v1 as Settlevolver
from pymclevel import BoundingBox, TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from random import randint, random
from math import pi,cos

class Stats:
	def __init__(self):
		self.setBlock = 0
		
	def setBlock(self):
		self.setBlock += 1

def perform(level, box, options):
	print "perform"

	stats = Stats()
	
	makeATower(stats, level, box, [(98,0), (35,0), (35,15)], [(35,7)], [(35,13)], [(98,2)])
	print "Blocks placed:", stats.setBlock

def makeATower(stats, level, box, wallMaterials, floorMaterials, glassMaterials, lightMaterials):
	width = box.maxx-box.minx
	height = box.maxy-box.miny
	depth = box.maxz-box.minz

	roofy = int(height/4)*randint(2,3)
	roofBox = BoundingBox((box.minx,box.maxy-roofy,box.minz),(width,roofy,depth))
	makeASpire(stats, level, roofBox, wallMaterials, floorMaterials, glassMaterials, lightMaterials)


	y = 0
	while y < height-roofy:
		dy = randint(3,5)
		dr = randint(3,9)
		w = 2+int(width/dr)
		d = 2+int(depth/dr)
		
		h = dr
		baseBox = BoundingBox((box.minx+(w>>1), box.miny+y, box.minz+(d>>1)),(width-w,h,depth-d))
		cylinderVertical(stats, level, baseBox, wallMaterials[0])
		baseBox = BoundingBox((box.minx+(w>>1)+1, box.miny+y+1, box.minz+(d>>1)+1),(width-w-2,h-2,depth-d-2))
		cylinderVertical(stats, level, baseBox, (0,0))
		y += dr

#	w = int(width/5)
#	d = int(depth/5)
#	h = int(height/3)
#	y = h
#	baseBox = BoundingBox((box.minx+(w>>1), box.miny+y, box.minz+(d>>1)),(width-w,h,depth-w))
#	cylinderVertical(stats, level, baseBox, wallMaterials[0])


def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	stats = Stats()
	
	makeATower(stats, level, box, [(98,0), (35,0), (35,15)], [(35,7)], [(35,13)], [(98,2)])
	print "Spire blocks placed:", stats.setBlock
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			if level.blockAt(x,box.miny,z) != 0:
				Settlevolver.setBlockToGround(level, (x,box.miny-1,z), (98,0)) # Stone Brick
	return []
	
def makeASpire(stats, level, box, wallMaterials, floorMaterials, glassMaterials, lightMaterials):
	height = box.maxy-box.miny
	
	pi2 = pi/2.0
	offset = pi2
	for y in xrange(0, height):
		heightHere = float(y)/float(height)
		widthHere = 1.0-abs(cos(heightHere*pi2+offset))
		
		w = box.maxx-box.minx
		d = box.maxz-box.minz
		width = float(w)*widthHere
		depth = float(d)*widthHere
		width = int(width)
		depth = int(depth)
		if width < 1:
			width = 1
		if depth < 1:
			depth = 1
		theBox = BoundingBox((box.minx+((w-width)>>1), box.miny+y, box.minz+((d-depth)>>1)),(width,1,depth))
		
		cylinderVertical(stats, level, theBox, wallMaterials[y%len(wallMaterials)])
	
	
def cylinderVertical(stats, level, box, material):
	# Vertical cylinder
	cx = (box.minx+box.maxx)>>1
	cz = (box.minz+box.maxz)>>1
	
	rx = box.maxx-cx
	rz = box.maxz-cz
	
	rx2 = rx*rx
	rz2 = rz*rz
	
	if rx > 0 and rz > 0:
		for z in xrange(box.minz, box.maxz):
			dz = cz-z
			dz2 = dz*dz
			zr = float(dz2)/float(rz2)
			for x in xrange(box.minx, box.maxx):
				dx = cx-x
				dist = float(dx*dx)/float(rx2) + zr
				# print cx,cz, rx,rz, rx2,rz2, dx,dz, zr, dist
				if dist < 1.0:
					for y in xrange(box.miny, box.maxy):
						setBlock(stats, level, x, y, z, material)

	
	
def setBlock(stats, level, x, y, z, material):
	id,data = material
	level.setBlockAt(x, y, z, id)
	level.setBlockDataAt(x, y, z, data)
	
	stats.setBlock += 1
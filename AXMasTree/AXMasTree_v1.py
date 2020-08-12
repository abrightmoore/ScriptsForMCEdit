# @Jigarbov
# randomly draw lines of a material,
# i can specify min/max length and 
# i specify density where 100 basically fills the whole space. 
# There should be a checkbox for allowing intersecting lines or not
# abrightmoore@yahoo.com.au

# 2017-08-10 01:40 - 03:20

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, floor
from random import *
from os import listdir
from os.path import isfile, join
import glob
from mcplatform import *
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity, alphaMaterials, MCSchematic, MCLevel, BoundingBox
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0

# from AJBHelper import *

inputs = (
		("JIG Selected Adjustment Worker", "label"),
		("Operation",(
			"XMas Tree",
  		    )),
		("Trunk:", alphaMaterials.Wood),
		("Leaf:", alphaMaterials.Leaves),
		("Tinsel 1:", alphaMaterials.Glowstone),
		("Tinsel 2:", alphaMaterials.BlockofQuartz),
		("String:", alphaMaterials.Fence),
		("Bauble Coat:", alphaMaterials.WhiteWool),
		("Bauble Fill:", alphaMaterials.Sponge),
		("Base diameter:", 5),
		("Branches:",7),
		("Branch Angle:",-10),
		("Branch Gap:",8),
		("Leaf Gap:",5),
		("Spines:",5),
		("Spine Length:",3),
		("Bauble Radius:", 2),
		("String Length:", 4),
		("Bauble Chance:", 40),
		("Seed:", 0),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(originalLevel, originalBox, options):
	op = options["Operation"]
	#matPen = getBlockFromOptions(options, "Pen Block:")
	seed = options["Seed:"]
	if seed == 0:
		seed = randint(1,999999999999)
	R = Random(seed)
	#minLength = options["Min Length:"]
	#maxLength = options["Max Length:"]
	#spacing = options["Spacing:"]
	#vspacing = options["Vertical Spacing:"]
	#numAttempts = options["Num Attempts:"]
	#smoothamount = options["Smoothness:"]
	#ores = options["Ore clumps?"]
	
	SUCCESS = True
	level = []
	box = []
	if op != "Meshy":
		level = originalLevel.extractSchematic(originalBox) # Working set
		box = BoundingBox((0,0,0),(originalBox.width,originalBox.height,originalBox.length))

	if op == "Random Lines":
		RandomLines(level,box,R,minLength,maxLength,spacing,numAttempts,smoothamount,matPen,False,False)
	elif op == "Random Non-Intersecting Lines":
		RandomLines(level,box,R,minLength,maxLength,spacing,numAttempts,smoothamount,matPen,True,False)
	elif op == "Lattice":
		Lattice(originalLevel,originalBox,spacing)
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False
	elif op == "Surface":
		Surface(originalLevel,originalBox,spacing)
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False
	elif op == "Mesh":
		Surface(originalLevel,originalBox,spacing)
		Bands(originalLevel,originalBox,spacing)
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False
	elif op == "Matrix":
		Matrix(originalLevel,originalBox,R,spacing)
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False
	elif op == "Sticks (Cluster)":
		surflevel = originalLevel.extractSchematic(originalBox) # Working set
		surfbox = BoundingBox((0,0,0),(originalBox.width,originalBox.height,originalBox.length))
		
		Surface(surflevel,surfbox,spacing)
		sticksCluster(originalLevel,originalBox,R)
		b=range(4096)
		b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(surflevel, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)
		SUCCESS = False
	elif op == "Materials Metadata":
		for i in xrange(0,256):
			for j in xrange(0,16):
				#print level.materials.block_map[i].name
				#print level.materials[i, j].internalName
					#str(level.materials.block_map[i])+" "+
				block = level.materials[i,j]
				# name, ID, blockData, aka, color, brightness, opacity, blockTextures
				print str(i)+"*"+str(j)+"*"+block.name
				#+"*"+block.brightness+"*"+block.opacity #+" "+str(level.materials[i,j])
	elif op == "Mesh 2D":
		surflevel = originalLevel.extractSchematic(originalBox) # Working set
		surfbox = BoundingBox((0,0,0),(originalBox.width,originalBox.height,originalBox.length))
		Surface(surflevel,surfbox,spacing)
		mesh2D(surflevel,originalBox,spacing)

		originalLevel.copyBlocksFrom(surflevel, box, (originalBox.minx, originalBox.miny, originalBox.minz ))
		originalLevel.markDirtyBox(originalBox)		
		SUCCESS = False
	elif op == "Meshy":
		meshy(originalLevel,originalBox,spacing,vspacing,ores)
		SUCCESS = False
	elif op == "Meshy 2":
		meshy2(originalLevel,originalBox,spacing,vspacing,ores)
		SUCCESS = False
	elif op == "XMas Tree":
		treeXMas(level,box,options,R)
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096)
		b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

def treeXMas(level,box,options,R):
	# christmas tree filter? branches have a predictable pattern, random baubles, random tinsel draping? variable: radius of base/based on size of selection box, height % of stump/tree ratio? 
	# of baubles? checkbox for tree tapering on the top or not, default on. thoughts?
	# of tinsel drapes
	# tree branch density?
	op = "treeXMas"
	print str(time.ctime())+" Starting "+op

	width = (box.maxx+box.minx)
	height = (box.maxy+box.miny)
	depth = (box.maxz+box.minz)
	SMOOTHAMOUNT = 4
	centreWidth = width>>1
	centreDepth = depth>>1
	(ox,oz) = (box.minx+(width>>1),box.minz+(depth>>1))
	
	chanceBauble = options["Bauble Chance:"]
	chanceTinsel = R.randint(10,50)
	baseRadius = (width+depth)>>2
	
	matBark = getBlockFromOptions(options,"Trunk:") #(17, 13)
	#matWood = options["Trunk:"] #(5,1)
	matLeaf = getBlockFromOptions(options,"Leaf:") #(18, 1)
	matTinsel = getBlockFromOptions(options,"Tinsel 1:") #(89,0)
	matTinsel2 = getBlockFromOptions(options,"Tinsel 2:") #(169,0)
	matString = getBlockFromOptions(options,"String:") #(85,0)
	matBauble = getBlockFromOptions(options,"Bauble Coat:") #(95,0)
	matBaubleFill = getBlockFromOptions(options,"Bauble Fill:") #(19,0)
	leafGap = options["Leaf Gap:"]
	spines = options["Spines:"]
	spineLength = options["Spine Length:"]
	
	
	taper = True
	anAngle = 2.0*pi/180.0
	branchGap = options["Branch Gap:"]
#	if height/10 > branchGap:
#		branchGap = R.randint(4,int(height/10)) 	# Decide on the gap (height) between branches
	drawBranches = True

		
	# Draw base
	baseDiameter = options["Base diameter:"]
	if baseDiameter < 3:
		baseDiameter = 3
	trunkDx = 0
	trunkDz = 0
	
	branchEndPoints = []
	branchLayers = []
	
	# Draw branches and leaves
	if drawBranches == True:
		# Decide on a vertical angle for the branches
		branchPhi = anAngle*options["Branch Angle:"]
		# Decide on how many branches there are around the trunk
		branchNum = options["Branches:"]
		print "Number of Branches: "+str(branchNum)
		branchAngle = pi*2.0/float(branchNum)

		for y in xrange(box.miny+int(height/7), box.maxy):
			if y%branchGap == branchGap-1: # at each point on the trunk just below the height of the branchGap
				sizeHere = int(baseDiameter/3*2)

				# cast a layer of branches out from the point on the trunk just here
				heightRatio = float(y)/float(height)
				trunkX = trunkDx * heightRatio + centreWidth
				trunkY = y
				trunkZ = trunkDz * heightRatio + centreDepth
				branchLength = (centreWidth+centreDepth)/2*(1.0-heightRatio)

				sizeHere = int(float(1.0-sizeHere) * heightRatio)
				if sizeHere < 1:
					sizeHere = 1
				
				branchStartAngle = R.random()*2.0*pi/branchNum
				branchLayer = []
				for i in xrange(0,branchNum):
					(x0,y0,z0) = (box.minx+trunkX,y,box.minz+trunkZ)
					theta = branchStartAngle+i*branchAngle
					drawBranch(level,matBark,matLeaf,(x0,y0,z0),sizeHere,theta,branchPhi,branchLength,leafGap,spines,spineLength)
	
					# Track tinsel points
					#(x1,y1,z1) = getRelativePolar((x0,y0,z0), (theta, branchPhi, branchLength))  # End pos
					tinselBufferDist = R.randint(1,6)
					(x1,y1,z1) = getRelativePolar((x0,y0,z0), (theta, branchPhi, branchLength-tinselBufferDist))
					y1 += 1 # Lift the decoration a bit
					if y1 > box.miny:
						branchEndPoints.append((x1,y1,z1))
						branchLayer.append((x1,y1,z1))
				branchLayers.append(branchLayer)
					
	# Draw tinsel
	print str(time.ctime())+" Drawing Tinsel "+op
	counter = 0
	for branchLayer in branchLayers:
		if counter%4 == 1:
			print str(time.ctime())+" Drawing Tinsel "+op
			P = []
			for i in xrange(0,len(branchLayer)):
				P.append((branchLayer[i]))
				P.append((branchLayer[i]))
				(x1,y1,z1) = (branchLayer[i])
				(x2,y2,z2) = (branchLayer[(i+1)%len(branchLayer)])
				drapeDist = int(getLineSegmentLength((x1,y1,z1),(x2,y2,z2)))
				if drapeDist > branchGap<<1:
					drapeDist = branchGap<<1
				(xmid,ymid,zmid) = (int(x1+x2)>>1,(int(y1+y2)>>1)-drapeDist,int(z1+z2)>>1)
				P.append((xmid,ymid,zmid))
				P.append((branchLayer[(i+1)%len(branchLayer)]))
				P.append((branchLayer[(i+1)%len(branchLayer)]))
			drawLinesSmooth(level,box,matTinsel,SMOOTHAMOUNT,P)

		elif counter%4 == 3:
			print str(time.ctime())+" Drawing Tinsel2 "+op
			P = []
			for i in xrange(0,len(branchLayer)):
				P.append((branchLayer[i]))
				P.append((branchLayer[i]))
				(x1,y1,z1) = (branchLayer[i])
				(x2,y2,z2) = (branchLayer[(i+1)%len(branchLayer)])
				drapeDist = int(getLineSegmentLength((x1,y1,z1),(x2,y2,z2)))
				if drapeDist > branchGap<<1:
					drapeDist = branchGap<<1
				(xmid,ymid,zmid) = (int(x1+x2)>>1,(int(y1+y2)>>1)-randint(drapeDist>>2,drapeDist),int(z1+z2)>>1)
				P.append((xmid,ymid,zmid))
				P.append((branchLayer[(i+1)%len(branchLayer)]))
				P.append((branchLayer[(i+1)%len(branchLayer)]))
			drawLinesSmooth(level,box,matTinsel2,SMOOTHAMOUNT,P)
		
		counter += 1

	print str(time.ctime())+" Drawing Baubles "+op
	for branchLayer in branchLayers:
		for (x,y,z) in branchLayer:
			if chanceBauble <= R.randint(1,100):
				(mat,col) = matBauble
				col = R.randint(0,15)
				drawBauble(level,matBaubleFill,(mat,col),matString,(x,y-2,z),options["String Length:"],options["Bauble Radius:"]) # Draw baubles

		
	
	
	# Draw star

	# Draw trunk

	for x in xrange(ox-baseDiameter,ox+baseDiameter+1):
		for z in xrange(ox-baseDiameter,oz+baseDiameter+1):
			drawLine(level, matBark, (x,box.miny,z), (ox,box.maxy-1,oz) )

	print str(time.ctime())+" Ended "+op

def drawBauble(level,matFill,matCoat,matString,(x0,y0,z0),length,radius):
	drawLine(level, matString, (x0,y0-length,z0),(x0,y0,z0) )
	drawSphere(level,matFill,matCoat,radius,(x0,y0-length-radius,z0))
	
def drawSphere(level,matFill,matCoat,radius,(x0,y0,z0)):
	r2 = radius**2
	for y in xrange(-radius,radius+1):
		for z in xrange(-radius,+radius+1):
			for x in xrange(-radius,radius+1):
				dist2 = y**2+z**2+x**2
				if dist2 <= r2:
					if (r2-dist2) <= 2:
						setBlock(level,matCoat,x0+x,y0+y,z0+z)
					else:
						setBlock(level,matFill,x0+x,y0+y,z0+z)
				
def drawBranch(level,matBark,matLeaf,(x0,y0,z0),startRadius,theta,phi,length,leafGap,spines,spineLength):
	(x1,y1,z1) = getRelativePolar((x0,y0,z0), (theta, phi, length)) # Branch end point
	
	# Draw the leaves
	startPhi = random()*2.0*pi
	dphi = 2.0*pi/spines
	for iter in xrange(0,int(length)):
		(xl1,yl1,zl1) = getRelativePolar((x0,y0,z0), (theta, phi, iter)) # StartPos
#		for iter2 in xrange(0,spines):
		(xl2,yl2,zl2) = getRelativePolar((xl1,yl1,zl1), (theta+pi/2, startPhi+dphi*(int(iter)%leafGap), spineLength))
		drawLine(level, matLeaf, (xl1,yl1,zl1), (xl2,yl2,zl2) )

	dy = 0 
	#drawLine(level, material, (x0,y0,z0), (x1,y1,z1) )
	for dx in xrange(-startRadius,startRadius+1):
		for dz in xrange(-startRadius,startRadius+1):
			if dx**2+dz**2 <= startRadius**2:
				drawLine(level, matBark, (x0+dx,y0+dy,z0+dz), (x1,y1,z1) )
		
	# branchlets
	segments = 3
	segmentSize = int(length/segments)
	if segmentSize > 5:
		segmentPhi = phi*0
		segmentTheta = pi/5
		for iter in xrange(1,segments):
			(x2,y2,z2) = getRelativePolar((x0,y0,z0), (theta, phi, iter*segmentSize)) # How far down the branch do we start
			drawBranch(level,matBark,matLeaf,(x2,y2,z2),0,theta+segmentTheta,segmentPhi,((segments-iter)*segmentSize)>>1,leafGap,spines,spineLength)
			drawBranch(level,matBark,matLeaf,(x2,y2,z2),0,theta-segmentTheta,segmentPhi,((segments-iter)*segmentSize)>>1,leafGap,spines,spineLength)

	
def getLineSegmentLength((x0,y0,z0),(x1,y1,z1)):
	dx = x1-x0
	dy = y1-y0
	dz = z1-z0
	
	length = sqrt(dx**2+dy**2+dz**2)
	
	return length
	
def meshy(level,box,spacing,vspacing,ores):
	op = "meshy"
	l2 = MCSchematic((box.width,box.height,box.length))
	b2 = BoundingBox((0,0,0),(box.width,box.height,box.length))
	print "Clearing:"
	# Clear the landscape of all superfluous blocks
	blockTo = level.materials.Air
	blockFrom = [ level.materials.Sapling,
				  level.materials.SpruceSapling,
				  level.materials.BirchSapling,
				  level.materials.WaterActive,
				  level.materials.Water,
				  level.materials.LavaActive,
				  level.materials.Lava,
				  level.materials.UnusedShrub,
				  level.materials.TallGrass,
				  level.materials.Shrub,
				  level.materials.DesertShrub2,
				  level.materials.Flower,
				  level.materials.Rose,
				  level.materials.BrownMushroom,
				  level.materials.RedMushroom,
				  level.materials.SnowLayer,
				  level.materials.Lilypad,
				  level.materials.Wood,
				#  level.materials.IronWood,
				  level.materials.BirchWood,
				  level.materials.PineWood,
 				  level.materials.Leaves,
				  level.materials.PineLeaves,
				  level.materials.BirchLeaves,
				  level.materials.JungleLeaves,
 				  level.materials.LeavesPermanent,
				  level.materials.PineLeavesPermanent,
				  level.materials.BirchLeavesPermanent,
				  level.materials.JungleLeavesPermanent,
				  level.materials.LeavesDecaying,
				  level.materials.PineLeavesDecaying,
				  level.materials.BirchLeavesDecaying,
				  level.materials.JungleLeavesDecaying,
				  level.materials[175,10],
				  level.materials[17,4],
				  level.materials[17,8],
				  level.materials[9,0],
				  level.materials[9,1],
				  level.materials[9,2],
				  level.materials[9,3],
				  level.materials[9,4],
				  level.materials[9,5],
				  level.materials[9,6],
				  level.materials[9,7],

			  ]

	for block in blockFrom:
		print block
		level.fillBlocks(box, blockTo, [block])
	
	
	# Traverse the landscape surface, taking only solid blocks onto the workspace
	x = box.minx
	while x < box.maxx:
		print x
		z = box.minz
		while z < box.maxz:
			y = box.maxy
			while y >= box.miny:
				block = level.blockAt(x,y,z)
				if block != 0:
					block = level.blockAt(x,y,z)
					data = level.blockDataAt(x,y,z)
					setBlock(l2,(block,data),x-box.minx,y-box.miny,z-box.minz)
					y = box.miny
				y -= 1
			z += 1
		x += spacing

	x = box.minx
	while x < box.maxx:
		print x
		z = box.minz
		while z < box.maxz:
			y = box.maxy
			while y >= box.miny:
				block = level.blockAt(x,y,z)
				if block != 0:
					block = level.blockAt(x,y,z)
					data = level.blockDataAt(x,y,z)
					setBlock(l2,(block,data),x-box.minx,y-box.miny,z-box.minz)
					y = box.miny
				y -= 1
			z += spacing
		x += 1
	
	if ores == True:
		print "Keeping ores"
		oreList = [ 14,15,16,21,56,73,129,153 ]
		for x in xrange(box.minx,box.maxx):
			for z in xrange(box.minz,box.maxz):
				for y in xrange(box.miny,box.maxy):
					block = level.blockAt(x,y,z)
					if block in oreList:
						setBlock(l2,(block,level.blockDataAt(x,y,z)),x-box.minx,y-box.miny,z-box.minz)
	
	# Sides and base

	for z in (box.minz,box.maxz-1):
		y = box.miny
		while y < box.maxy:
			for x in xrange(box.minx,box.maxx):
				setBlock(l2,(level.blockAt(x,y,z),level.blockDataAt(x,y,z)),x-box.minx,y-box.miny,z-box.minz)
				if (x-box.minx)%spacing == 0 or x == box.maxx-1:
					y2 = box.miny
					while y2 < box.maxy:
						setBlock(l2,(level.blockAt(x,y2,z),level.blockDataAt(x,y2,z)),x-box.minx,y2-box.miny,z-box.minz)
						y2 += 1	
			y = y+vspacing
	print "Drawing grid"
	for x in (box.minx,box.maxx-1):
		y = box.miny
		while y < box.maxy:
			for z in xrange(box.minz,box.maxz):
				setBlock(l2,(level.blockAt(x,y,z),level.blockDataAt(x,y,z)),x-box.minx,y-box.miny,z-box.minz)
				if (z-box.minz)%spacing == 0 or z == box.maxz-1:
					y2 = box.miny
					while y2 < box.maxy:
						setBlock(l2,(level.blockAt(x,y2,z),level.blockDataAt(x,y2,z)),x-box.minx,y2-box.miny,z-box.minz)
						y2 += 1
			y = y+vspacing
			
	# Copy the workspace over the original area
	level.copyBlocksFrom(l2, b2, (box.minx, box.miny, box.minz ))
		
def meshy2(level,box,spacing,vspacing,ores):
	op = "meshy2"
	l2 = MCSchematic((box.width,box.height,box.length))
	b2 = BoundingBox((0,0,0),(box.width,box.height,box.length))
	print "Clearing:"
	# Clear the landscape of all superfluous blocks
	blockTo = level.materials.Air
	blockFrom = [ level.materials.Sapling,
				  level.materials.SpruceSapling,
				  level.materials.BirchSapling,
				  level.materials.WaterActive,
				  level.materials.Water,
				  level.materials.LavaActive,
				  level.materials.Lava,
				  level.materials.UnusedShrub,
				  level.materials.TallGrass,
				  level.materials.Shrub,
				  level.materials.DesertShrub2,
				  level.materials.Flower,
				  level.materials.Rose,
				  level.materials.BrownMushroom,
				  level.materials.RedMushroom,
				  level.materials.SnowLayer,
				  level.materials.Lilypad,
				  level.materials.Wood,
				#  level.materials.IronWood,
				  level.materials.BirchWood,
				  level.materials.PineWood,
 				  level.materials.Leaves,
				  level.materials.PineLeaves,
				  level.materials.BirchLeaves,
				  level.materials.JungleLeaves,
 				  level.materials.LeavesPermanent,
				  level.materials.PineLeavesPermanent,
				  level.materials.BirchLeavesPermanent,
				  level.materials.JungleLeavesPermanent,
				  level.materials.LeavesDecaying,
				  level.materials.PineLeavesDecaying,
				  level.materials.BirchLeavesDecaying,
				  level.materials.JungleLeavesDecaying,
				  level.materials[175,10],
				  level.materials[17,4],
				  level.materials[17,8],
				  level.materials[9,0],
				  level.materials[9,1],
				  level.materials[9,2],
				  level.materials[9,3],
				  level.materials[9,4],
				  level.materials[9,5],
				  level.materials[9,6],
				  level.materials[9,7],

			  ]

	for block in blockFrom:
		print block
		level.fillBlocks(box, blockTo, [block])
	
	
	# Traverse the landscape surface, taking only solid blocks onto the workspace
	x = box.minx
	while x < box.maxx:
		print x
		z = box.minz
		while z < box.maxz:
			y = box.maxy
			while y > box.miny:
				y -= 1
				block = level.blockAt(x,y,z)
				if block != 0:
					while y > box.miny:
						block = level.blockAt(x,y,z)
						data = level.blockDataAt(x,y,z)
						setBlock(l2,(block,data),x-box.minx,y-box.miny,z-box.minz)
						y -= vspacing
			z += 1
		x += spacing

	x = box.minx
	while x < box.maxx:
		print x
		z = box.minz
		while z < box.maxz:
			y = box.maxy
			while y > box.miny:
				y -= 1
				block = level.blockAt(x,y,z)
				if block != 0:
					while y > box.miny:
						block = level.blockAt(x,y,z)
						data = level.blockDataAt(x,y,z)
						setBlock(l2,(block,data),x-box.minx,y-box.miny,z-box.minz)
						y -= vspacing
			z += spacing
		x += 1
	
	if ores == True:
		print "Keeping ores"
		oreList = [ 14,15,16,21,56,73,129,153 ]
		for x in xrange(box.minx,box.maxx):
			for z in xrange(box.minz,box.maxz):
				for y in xrange(box.miny,box.maxy):
					block = level.blockAt(x,y,z)
					if block in oreList:
						setBlock(l2,(block,level.blockDataAt(x,y,z)),x-box.minx,y-box.miny,z-box.minz)
	
	# Copy the workspace over the original area
	level.copyBlocksFrom(l2, b2, (box.minx, box.miny, box.minz ))	
	
def mesh2D(level,box,spacing):
	op = "mesh2D"
	#level2 = level.extractSchematic(box) # Working set
	level2 = MCSchematic((box.width,box.height,box.length))
	box2 = BoundingBox((0,0,0),(box.width,box.height,box.length))
	
	smoothamount = 1

	ox = box.minx
	oy = box.miny
	oz = box.minz
	
	w = box.width
	h = box.height
	d = box.length
	PSet = []

	x,z = ox,oz
	
	while x < box.maxx:
		while z < box.maxz:
			y = box.maxy-1
			while y >= box.miny:
				block = getBlock(level,x,y,z)
				if block != (0,0):
					PSet.append((block,x-box.minx,y-box.miny,z-box.minz))
					y = box.miny
				y -= 1
			z += spacing
		x += spacing
	
	for (b,x,y,z) in PSet:
		setBlock(level2,b,x,y,z)
	level.copyBlocksFrom(level2, box2, (box.minx, box.miny, box.minz ))	
			
def sticksCluster(level,box,R):
	op = "sticksCluster"
	#level2 = level.extractSchematic(box) # Working set
	level2 = MCSchematic((box.width,box.height,box.length))
	box2 = BoundingBox((0,0,0),(box.width,box.height,box.length))
	
	smoothamount = 1
	LIM = 8

	ox = box.minx
	oy = box.miny
	oz = box.minz
	
	w = box.width
	h = box.height
	d = box.length
	PSet = []
	numClusters = R.randint(1,5)*2+1
	for i in xrange(0,numClusters):
		print i
		(x,y,z) = (box.minx+(R.randint(0,w)>>1)+(w>>2),box.miny+(R.randint(0,h)>>1)+(h>>2),box.minz+(R.randint(0,d)>>1)+(d>>2))
		for k in xrange(0,R.randint(3,5)*2+1):
			(x1,y1,z1) = pointRandomByDistanceVRange(R,(w+h+d)>>3,w,h,d,0.1)
			numRays = R.randint(1,5)*2+1
			for j in xrange(0,numRays):
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[(x,y,z),(x+x1+R.randint(-LIM,LIM),y+y1+R.randint(-LIM,LIM),z+z1+R.randint(-LIM,LIM))])))
	#print PSet
	for PLine in PSet:
		for (x1,y1,z1) in PLine:
			setBlock(level2,getBlock(level,x1,y1,z1),x1-box.minx,y1-box.miny,z1-box.minz)	
	level.copyBlocksFrom(level2, box2, (box.minx, box.miny, box.minz ))		
	
def Matrix(level,box,R,spacing):
	op = "Matrix"
	#level2 = level.extractSchematic(box) # Working set
	level2 = MCSchematic((box.width,box.height,box.length))
	box2 = BoundingBox((0,0,0),(box.width,box.height,box.length))

	smoothamount = 1
	
	ox = box.minx
	oy = box.miny
	oz = box.minz
	
	w = box.width
	h = box.height
	d = box.length
	
	
	(x,y,z) = (ox,oy,oz)
	
	while y < box.maxy:
		if y%10 == 0:
			print str(time.ctime())+" Running X "+op+" "+str(y)
			
		z = oz
		while z < box.maxz:
			x = ox
			while x < box.maxx:
				p000 = (x,y,z)
				p001 = (x,y,z+spacing)
				p010 = (x,y+spacing,z)
				p011 = (x,y+spacing,z+spacing)
				p100 = (x+spacing,y,z)
				p101 = (x+spacing,y,z+spacing)
				p110 = (x+spacing,y+spacing,z)
				p111 = (x+spacing,y+spacing,z+spacing)
				PSet = []

				
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p000,p001])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p000,p010])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p000,p100])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p001,p011])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p100,p110])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p010,p110])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p010,p011])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p100,p101])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p001,p101])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p101,p111])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p011,p111])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p110,p111])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p000,p111])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p010,p101])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p100,p001])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p110,p011])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p110,p001])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p011,p100])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p000,p101])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p010,p111])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p000,p110])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p010,p100])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p000,p011])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p010,p001])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p010,p001])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p011,p101])))
				PSet.append(makePathUnique(calcLinesSmooth1(smoothamount,[p001,p110])))


				
				#  PSet = flatten(PSet)
				#print PSet
				for PLine in PSet:
					for (x1,y1,z1) in PLine:
						setBlock(level2,getBlock(level,x1,y1,z1),x1-box.minx,y1-box.miny,z1-box.minz)
				x += spacing
			z += spacing
		y += spacing
		
	
	# Calculate the cube here
	level.copyBlocksFrom(level2, box2, (box.minx, box.miny, box.minz ))	
	
def calcLinesSmooth1(smoothamount,P):
	Q = []
	Q.append(P[0])
	Q.append(P[0])
	for i in xrange(1,len(P)):
		Q.append(P[i])
	Q.append(P[len(P)-1])
	Q.append(P[len(P)-1])
	return calcLinesSmooth(smoothamount,Q)
		
def Bands(level,box,spacing):
	op = "Bands"
	#level2 = level.extractSchematic(box) # Working set
	level2 = MCSchematic((box.width,box.height,box.length))
	box2 = BoundingBox((0,0,0),(box.width,box.height,box.length))

	airlevel = MCSchematic((box.width,box.height,box.length))
	airbox = BoundingBox((0,0,0),(box.width,box.height,box.length))
	
	x = box.minx
	while x < box.maxx:
		if x%10 == 0:
			print str(time.ctime())+" Running X "+op+" "+str(x)
		for z in xrange(box.minz,box.maxz):
			for y in xrange(box.miny,box.maxy):
				if getBlock(level,x,y,z) != (0,0): # This is a surface
					setBlock(level2,getBlock(level,x,y,z),x-box.minx,y-box.miny,z-box.minz)
		x += spacing
		
	y = box.miny
	while y < box.maxy:
		if y%10 == 0:
			print str(time.ctime())+" Running Y "+op+" "+str(x)
		for z in xrange(box.minz,box.maxz):
			for x in xrange(box.minx,box.maxx):
				if getBlock(level,x,y,z) != (0,0): # This is a surface
					setBlock(level2,getBlock(level,x,y,z),x-box.minx,y-box.miny,z-box.minz)
		y += spacing
					
	z = box.minz
	while z < box.maxz:
		if z%10 == 0:
			print str(time.ctime())+" Running Z "+op+" "+str(x)
		for y in xrange(box.miny,box.maxy):
			for x in xrange(box.minx,box.maxx):
				if getBlock(level,x,y,z) != (0,0): # This is a surface
					setBlock(level2,getBlock(level,x,y,z),x-box.minx,y-box.miny,z-box.minz)
		z += spacing
		
	level.copyBlocksFrom(level2, box2, (box.minx, box.miny, box.minz ))
		
def Surface(level,box,spacing):
	op = "Surface"
	#level2 = level.extractSchematic(box) # Working set
	level2 = MCSchematic((box.width,box.height,box.length))
	box2 = BoundingBox((0,0,0),(box.width,box.height,box.length))

	airlevel = MCSchematic((box.width,box.height,box.length))
	airbox = BoundingBox((0,0,0),(box.width,box.height,box.length))
	
	for x in xrange(box.minx,box.maxx):
		if x%10 == 0:
			print str(time.ctime())+" Scanning for surfaces "+op+" "+str(x)
		for z in xrange(box.minz,box.maxz):
			for y in xrange(box.miny,box.maxy):
				if getBlock(level,x,y,z) != (0,0):
					for ddx in xrange(-1,2):
						for ddz in xrange(-1,2):
							for ddy in xrange(-1,2):
								if not (ddx == 0 and ddy == 0 and ddz == 0):
									if getBlock(level,x+ddx,y+ddy,z+ddz) == (0,0):
										setBlock(airlevel,(1,0),x-box.minx,y-box.miny,z-box.minz) # Adjacent to air / surface
				else:
					setBlock(airlevel,(2,0),x-box.minx,y-box.miny,z-box.minz) # Airblock here
							
	for x in xrange(box.minx,box.maxx):
		if x%10 == 0:
			print str(time.ctime())+" Running "+op+" "+str(x)

		for z in xrange(box.minz,box.maxz):
			for y in xrange(box.miny,box.maxy):
				if getBlock(airlevel,x-box.minx,y-box.miny,z-box.minz) == (1,0): # This is a surface block
					setBlock(level2,getBlock(level,x,y,z),x-box.minx,y-box.miny,z-box.minz)
	level.copyBlocksFrom(level2, box2, (box.minx, box.miny, box.minz ))
		
def Lattice(level,box,spacing):
	op = "Lattice"
	#level2 = level.extractSchematic(box) # Working set
	level2 = MCSchematic((box.width,box.height,box.length))
	box2 = BoundingBox((0,0,0),(box.width,box.height,box.length))
	
	for x in xrange(box.minx,box.maxx):
		if x%10 == 0:
			print str(time.ctime())+" Running "+op+" "+str(x)

		for z in xrange(box.minz,box.maxz):
			for y in xrange(box.miny,box.maxy):
				if ((x%spacing == 0 and z%spacing == 0 and y%spacing == 0)
					or (x%spacing != 0 and z%spacing == 0 and y%spacing == 0)
					or (x%spacing == 0 and z%spacing != 0 and y%spacing == 0)
					or (x%spacing == 0 and z%spacing == 0 and y%spacing != 0)
					):
					setBlock(level2,getBlock(level,x,y,z),x-box.minx,y-box.miny,z-box.minz)
	level.copyBlocksFrom(level2, box2, (box.minx, box.miny, box.minz ))
				
def pointRandomByDistanceVRange(R,dist,width,height,depth,phiDivisor):
	dirh = random()*2.0*pi
	dirv = random()*pi*phiDivisor-pi/2.0*phiDivisor
	if height == 1:
		dirv = 0
	if depth == 1:
		dirh = pi/2.0+pi*R.randint(0,1)
	if width == 1:
		dirh = pi*R.randint(0,1)
	(dx,dy,dz) = (
					dist*cos(dirh)*cos(dirv),
					dist*sin(dirv),
					dist*sin(dirh)*cos(dirv)
					)
	return (dx,dy,dz)
				
def pointRandomByDistance(R,dist,width,height,depth):
	dirh = random()*2.0*pi
	dirv = random()*pi-pi/2.0
	if height == 1:
		dirv = 0
	if depth == 1:
		dirh = pi/2.0+pi*R.randint(0,1)
	if width == 1:
		dirh = pi*R.randint(0,1)
	(dx,dy,dz) = (
					dist*cos(dirh)*cos(dirv),
					dist*sin(dirv),
					dist*sin(dirh)*cos(dirv)
					)
	return (dx,dy,dz)
		
def RandomLines(level,box,R,minLength,maxLength,spacing,numAttempts,smoothamount,matPen,checkIntersect,cluster):
	op = "RandomLines"
	print str(time.ctime())+" Starting "+op
	metricPlacedLines = 0
	width = (box.maxx+box.minx)
	height = (box.maxy+box.miny)
	depth = (box.maxz+box.minz)
	
	(x0,y0,z0) = (R.randint(box.minx,box.maxx-1),R.randint(box.miny,box.maxy-1),R.randint(box.minz,box.maxz-1))
	
	while numAttempts > 0:
		if numAttempts%100 == 0:
			print str(time.ctime())+" Running "+op+" "+str(numAttempts)
		tries = 3
		while tries > 0:
			
			lineLength = R.randint(minLength,maxLength)
			boundsAttempt = True
			(x1,y1,z1) = (0,0,0)
			count = 1000
			while boundsAttempt == True and count > 0:
				(dx,dy,dz) = pointRandomByDistance(R,lineLength,width,height,depth)
				(x1,y1,z1) = (x0+dx,y0+dy,z0+dz)
				if x1 >= box.minx and x1 < box.maxx and y1 >= box.miny and y1 < box.maxy and z1 >= box.minz and z1 < box.maxz:
					boundsAttempt = False
				count -= 1
				
			P = []
			P.append((x0,y0,z0))
			P.append(P[0])
			P.append((x1,y1,z1))
			P.append(P[len(P)-1])
			
			LINEPOINTS = makePathUnique(calcLinesSmooth(smoothamount,P))

			collision = False
			if checkIntersect == True:
				for (x,y,z) in LINEPOINTS:
					for ddx in xrange(-1,1):
						for ddz in xrange(-1,1):
							for ddy in xrange(-1,1):
								block = level.blockAt(x+ddx,y+ddy,z+ddz)
								if block != 0:
									collision = True

			if collision == False:
				for (x,y,z) in LINEPOINTS:
					setBlock(level,matPen,x,y,z)
				tries = 0
				metricPlacedLines += 1
			tries -= 1

			# New start point
			if cluster == True:
				(dx,dy,dz) = pointRandomByDistance(R,spacing,width,height,depth)
				(x0,y0,z0) = (x1+dx,y1+dy,z1+dz)

				if x0 >= box.maxx:
					x0 -= width
				if x0 < box.minx:
					x0 += width
				if y0 >= box.maxy:
					y0 -= height
				if y0 < box.miny:
					y0 += height
				if z0 >= box.maxz:
					z0 -= depth
				if z0 < box.minz:
					z0 += depth
			else:
				(x0,y0,z0) = (R.randint(box.minx,box.maxx-1),R.randint(box.miny,box.maxy-1),R.randint(box.minz,box.maxz-1))
				
					
		numAttempts -= 1

	print str(time.ctime())+" Complete "+op+" Placed Lines "+str(metricPlacedLines)
		
	print str(time.ctime())+" Ended "+op
	
#############################################################################	

def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation

	return (x+xDelta, y+yDelta, z+zDelta)
	
def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def flatten(anArray):
	result = []
	for a in anArray:
		for b in a:
			result.append(b)
	return result

def drawLinesSmooth(level,box,material,SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = drawLines(level,box,material,P)
	return Q

def drawLinesSmoothForced(level,box,material,SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = drawLinesForced(level,box,material,P)
	return Q
	
def drawLines(level,box,material,P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( drawLine(level,material,(box.minx+x0,box.miny+y0,box.minz+z0),(box.minx+x,box.miny+y,box.minz+z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q

def drawLinesForced(level,box,material,P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( drawLineForced(level,material,(box.minx+x0,box.miny+y0,box.minz+z0),(box.minx+x,box.miny+y,box.minz+z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q
	
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

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
# Ye Olde GFX Libraries
def createSign(level, x, y, z, text): #abrightmoore - convenience method. Due to Jigarbov - this is not a Sign.
	ALIASKEY = "SHIP NUMBER"
	COMMANDBLOCK = 137
	CHUNKSIZE = 16
	STANDING_SIGN = 63
	
	setBlock(level, (STANDING_SIGN,8), x, y, z)
	setBlock(level, (1,0), x, y-1, z)
	control = TAG_Compound()
	control["id"] = TAG_String("Sign")
	control["Text1"] = TAG_String(ALIASKEY)
	control["Text2"] = TAG_String(text)
	control["Text3"] = TAG_String("Generated by")
	control["Text4"] = TAG_String("@abrightmoore")	
	
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	chunka.TileEntities.append(control)
	chunka.dirty = True

def chaikinSmoothAlgorithm(P): # http://www.idav.ucdavis.edu/education/CAGDNotes/Chaikins-Algorithm/Chaikins-Algorithm.html
	F1 = 0.25
	F2 = 0.75
	Q = []
	(x0,y0,z0) = (-1,-1,-1)
	count = 0
	for (x1,y1,z1) in P:
		if count > 0: # We have a previous point
			(dx,dy,dz) = (x1-x0,y1-y0,z1-z0)
#			Q.append( (x0*F2+x1*F1,0,z0*F2+z1*F1) )
#			Q.append( (x0*F1+x1*F2,0,z0*F1+z1*F2) )

			Q.append( (x0*F2+x1*F1,y0*F2+y1*F1,z0*F2+z1*F1) )
			Q.append( (x0*F1+x1*F2,y0*F1+y1*F2,z0*F1+z1*F2) )

#			Q.append( (x0+dx*F1+*F2,y0*F1+y1*F2,z0*F1+z1*F2) )
#			Q.append( (x0*F2+x1*F1,y0*F2+y1*F1,z0*F2+z1*F1) )
		else:
			count = count+1
		(x0,y0,z0) = (x1,y1,z1)

	return Q

def drawTriangle(level, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
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

def drawTriangleEdge(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge):
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )

def plotLine(level,material,p1,p2):

	(x1,y1,z1) = p1
	(x2,y2,z2) = p2
	
	dx = x2-x1
	dy = y2-y1
	dz = z2-z1
	
	steps = abs(dx)
	if abs(dy) > abs(dx):
		steps = abs(dy)
	if abs(dz) > abs(dy):
		steps = abs(dz)
	if steps == 0:
		setBlock(level,material,x1,y1,z1)
	else:
		ddx = float(dx)/float(steps)
		ddy = float(dy)/float(steps)
		ddz = float(dz)/float(steps)
		pdx = float(0)
		pdy = float(0)
		pdz = float(0)
		
		for i in xrange(0,int(steps)):
			setBlock(level,material,x1+pdx,y1+pdy,z1+pdz)
			pdx = pdx + ddx
			pdy = pdy + ddy
			pdz = pdz + ddz
	
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	return drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLineForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	return drawLineConstrainedForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )
	
def drawLine1(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	for px, py, pz in bresenham.bresenham((x,y,z),(x1,y1,z1)):
		setBlock(scratchpad,(blockID, blockData),px,py,pz)
	setBlock(scratchpad,(blockID, blockData),x1,y1,z1)

def drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)
	P = []
	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(xd,yd,zd) = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)))
			setBlock(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points drawn

def drawLineConstrainedForced(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)
	P = []
	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(xd,yd,zd) = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)))
			setBlockForced(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points drawn

	
def drawLineConstrainedRandom(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), frequency ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)


	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)

	iter = 0
	while iter <= distance:
		if randint(0,99) < frequency:
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
		iter = iter+0.5 # slightly oversample because I lack faith.
	
def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockForced(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
	
def calcLinesSmooth(SMOOTHAMOUNT,P):
	Q = []
	for i in xrange(0,SMOOTHAMOUNT):
		P = chaikinSmoothAlgorithm(P)
	Q = calcLines(P)
	return flatten(Q)
	
def calcLine((x,y,z), (x1,y1,z1) ):
	return calcLineConstrained((x,y,z), (x1,y1,z1), 0 )
	
def calcLines(P):
	Q = []
	count = 0
	(x0,y0,z0) = (0,0,0)
	for (x,y,z) in P:
		if count > 0:
			Q.append( calcLine((x0,y0,z0),(x,y,z)) )
		count = count+1
		(x0,y0,z0) = (x,y,z)
	return Q

def calcLineConstrained((x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)
	P = []
	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(xd,yd,zd) = ((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)))
			# setBlock(scratchpad,(blockID,blockData),xd,yd,zd)
			P.append((xd,yd,zd))
			iter = iter+0.5 # slightly oversample because I lack faith.
	return P # The set of all the points calc'd

def makePathUnique(P):
	Q = []
	(prevX,prevY,prevZ) = (int(-1),int(-1),int(-1)) # Dummy
	for (x,y,z) in P:
		if (int(x),int(y),int(z)) != (int(prevX),int(prevY),int(prevZ)):
			Q.append((x,y,z))
			(prevX,prevY,prevZ) = (int(x),int(y),int(z))
#		else: # Debug
#			print "Duplicate discarded: "+str(x)+",	"+str(y)+", "+str(z)
	return Q
	
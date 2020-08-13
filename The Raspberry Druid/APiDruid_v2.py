# This MCEdit filter is for creating plants around the player
# Implementation by @abrightmoore http://brightmoore.net

import minecraft.minecraft as minecraft # Martin O'Hanlon - http://raspberrypi.mythic-beasts.com/magpi/The-MagPi-issue-11-en.pdf
import minecraft.block as block

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel
from mcplatform import *


inputs = (
	("abrightmoore@yahoo.com.au", "label"),
	("http://brightmoore.net", "label"),
	("Number of iterations", 1000),
	("Host:", ("string","value=localhost")),
	("Port:", 4711),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt((int)(x),(int)(y),(int)(z))
    if tempBlock == 0:
	setBlock(level, (block, data), (int)(x),(int)(y),(int)(z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, (int)(y)):
    	setBlockIfEmpty(level, (block, data), (int)(x),(int)(iterY),(int)(z))
    	

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def fix(angle):
	while angle > pi:
		angle = angle - 2 * pi
	while angle < -pi:
		angle = angle + 2 * pi
	return angle

def drawLinePI(mc, theBlock, (x,y,z), (x1,y1,z1) ):
	drawLineConstrainedPI(mc, theBlock, (x,y,z), (x1,y1,z1), 0 )

def drawLineConstrainedPI(mc, theBlock, (x,y,z), (x1,y1,z1), maxLength ):
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
			mc.setBlock((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), theBlock)
			iter = iter+0.5 # slightly oversample because I lack faith.


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	APiDruid(level, box, options)		
	level.markDirtyBox(box)

def log(method, message):
	print '%s: %s %s' % (method, time.ctime(), message)

def APiDruid(level, box, options): 
	# CONSTANTS AND GLOBAL VARIABLES
	method = "APiDruid"
	log(method, "Started")
	#print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	host = options["Host:"]
	port = options["Port:"]
	
	ITERATIONS = options["Number of iterations"]

	mc = minecraft.Minecraft.create(host, port)
	print 'Connected to %s:%s' % (host, port)
	
	mc.postToChat("An ancient power runs through you.")
	mc.postToChat("You feel... Alive!")
	
	currentTask = "Available"
	currentPos = (0,0,0)
	playerPos = (0,0,0)
	interTaskCounter = 0
	taskPos = (0,0,0)
	
	for cycling in xrange(0, ITERATIONS):
		print '%s: %s Iteration of %s' % (method, cycling, ITERATIONS)
		print '%s: %s Current task is %s' % (method, time.ctime(), currentTask)
		
		if currentTask == "Available":
			dice = randint(1,100)
			if dice < 10:
				print 'Fetching the player position'
				playerPos = mc.player.getPos()
				prevPlayerPos = playerPos
				print 'Player is at %s %s %s' % (playerPos.x, playerPos.y, playerPos.z)
				dice = randint(1,100)
				if dice < 10:
					currentTask = "Planting Flowers"
					mc.postToChat("You smell pollen.")
				elif dice < 20:
					tgtBlock = mc.getBlockWithData((int)(playerPos.x),(int)(playerPos.y),(int)(playerPos.z))
					tgtBlockBeneath = mc.getBlockWithData((int)(playerPos.x),(int)(playerPos.y-1),(int)(playerPos.z))
					if (tgtBlock == block.AIR or tgtBlock == block.SNOW) and (tgtBlockBeneath != block.AIR and tgtBlockBeneath != block.SNOW):
						taskPos = playerPos
						currentTask = "Grow a Pole"
						mc.postToChat("From little things...")
				elif dice < 30:
					tgtBlock = mc.getBlockWithData((int)(playerPos.x),(int)(playerPos.y),(int)(playerPos.z))
					tgtBlockBeneath = mc.getBlockWithData((int)(playerPos.x),(int)(playerPos.y-1),(int)(playerPos.z))
					if (tgtBlock == block.AIR or tgtBlock == block.SNOW) and (tgtBlockBeneath != block.AIR and tgtBlockBeneath != block.SNOW):
						taskPos = playerPos
						currentTask = "Grow a Tree"
						mc.postToChat("From little things...")

				interTaskCounter = 0
		
		if currentTask == "Grow a Tree":
			CANOPYHEIGHT = 10
			interTaskCounter = (interTaskCounter + 1)
			if randint(1,10) < 4: # Roots
				rx = randint(-5,5)
				rz = randint(-5,5)
				ry = randint(-2,0)				
				drawLinePI(mc, block.WOOD, 
						((int)(taskPos.x),(int)(taskPos.y+randint(1,3)),(int)(taskPos.z)),
						((int)(taskPos.x+rx),(int)(taskPos.y+ry),(int)(taskPos.z+rz)))
		
			if interTaskCounter < CANOPYHEIGHT*2:
				mc.setBlock((int)(taskPos.x),(int)(taskPos.y+interTaskCounter/2),(int)(taskPos.z),block.WOOD)
				mc.setBlock((int)(taskPos.x-1),(int)(taskPos.y+interTaskCounter/2),(int)(taskPos.z),block.WOOD)
				mc.setBlock((int)(taskPos.x+1),(int)(taskPos.y+interTaskCounter/2),(int)(taskPos.z),block.WOOD)
				mc.setBlock((int)(taskPos.x),(int)(taskPos.y+interTaskCounter/2),(int)(taskPos.z-1),block.WOOD)
				mc.setBlock((int)(taskPos.x),(int)(taskPos.y+interTaskCounter/2),(int)(taskPos.z+1),block.WOOD)
			elif interTaskCounter < CANOPYHEIGHT*2+40:
				rx = randint(-5,5)
				rz = randint(-5,5)
				ry = randint(1,5)
				drawLinePI(mc, block.WOOD, 
							((int)(taskPos.x),(int)(taskPos.y+CANOPYHEIGHT),(int)(taskPos.z)),
							((int)(taskPos.x+rx),(int)(taskPos.y+CANOPYHEIGHT+ry),(int)(taskPos.z+rz)))
				for iter in xrange(0,randint(8,15)):
					dx = randint(-1,1)
					dy = randint(0,1)
					dz = randint(-1,1)
					mc.setBlock((int)(taskPos.x+rx+dx),(int)(taskPos.y+CANOPYHEIGHT+ry+dy),(int)(taskPos.z+rz+dz),block.LEAVES)
			elif interTaskCounter < CANOPYHEIGHT*2+45:
				rx = randint(-5,5)
				rz = randint(-5,5)
				ry = randint(1,5)
				sy = randint((int)(CANOPYHEIGHT/2),(int)(CANOPYHEIGHT/3*2))
				drawLinePI(mc, block.WOOD, 
							((int)(taskPos.x),(int)(taskPos.y+sy),(int)(taskPos.z)),
							((int)(taskPos.x+rx),(int)(taskPos.y+sy+ry),(int)(taskPos.z+rz)))
				for iter in xrange(0,randint(8,15)):
					dx = randint(-1,1)
					dy = randint(0,1)
					dz = randint(-1,1)
					mc.setBlock((int)(taskPos.x+rx+dx),(int)(taskPos.y+sy+ry+dy),(int)(taskPos.z+rz+dz),block.LEAVES)


			else:
				mc.postToChat("... big things grow.")
				currentTask = "Available"
		
		
		elif currentTask == "Grow a Pole":
			interTaskCounter = (interTaskCounter + 1) % 4096
			if interTaskCounter < 20:
				for iter in xrange(0,interTaskCounter):
					mc.setBlock((int)(taskPos.x),(int)(taskPos.y+iter/3),(int)(taskPos.z),block.FENCE)
			elif interTaskCounter > 20 :
				mc.postToChat("... big things grow.")
				currentTask = "Available"
			
		elif currentTask == "Planting Flowers":
			if interTaskCounter % 2 == 0:
				print 'Fetching the player position'
				playerPos = mc.player.getPos()
				print 'Player is at %s %s %s' % (playerPos.x, playerPos.y, playerPos.z)
				if (int)(playerPos.x) != (int)(prevPlayerPos.x) or (int)(playerPos.z) != (int)(prevPlayerPos.z):
					theBlock = block.AIR
					dice = randint(1,100)
					if dice < 2:
						currentTask = "Available"
						mc.postToChat("You no longer smell pollen.")
					elif dice < 20:
						theBlock = block.FLOWER_CYAN 
					elif dice < 30:
						theBlock = block.FLOWER_YELLOW
					elif dice < 40:
						theBlock = block.SAPLING
					elif dice < 70:
						theBlock = block.GRASS_TALL
					elif dice < 80:
						theBlock = block.TORCH

					if theBlock != block.AIR:
						dx = randint(-1,1)
						dz = randint(-1,1)
						tgtBlock = mc.getBlockWithData((int)(playerPos.x+dx),(int)(playerPos.y),(int)(playerPos.z+dz))
						tgtBlockBeneath = mc.getBlockWithData((int)(playerPos.x+dx),(int)(playerPos.y-1),(int)(playerPos.z+dz))
						if (tgtBlock == block.AIR or tgtBlock == block.SNOW) and (tgtBlockBeneath != block.AIR and tgtBlockBeneath != block.SNOW):
							mc.setBlock((int)(playerPos.x+dx),(int)(playerPos.y),(int)(playerPos.z+dz),theBlock)
					prevPlayerPos = playerPos
			interTaskCounter = (interTaskCounter + 1) % 4096
		
		time.sleep(0.5)
			
	mc.postToChat("The power wanes.")
	mc.postToChat("You feel... empty.")
	
	log(method, "Ended")
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
			scratchpad.setBlockAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockID)
			scratchpad.setBlockDataAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockData)
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
	
	for cycling in xrange(0, ITERATIONS):
		print '%s: %s Iteration of %s' % (method, cycling, ITERATIONS)
		print '%s: %s Current task is %s' % (method, time.ctime(), currentTask)
		
		if currentTask == "Available":
			if randint(1,100) < 30:
				print 'Fetching the player position'
				playerPos = mc.player.getPos()
				prevPlayerPos = playerPos
				print 'Player is at %s %s %s' % (playerPos.x, playerPos.y, playerPos.z)
				dice = randint(1,100)
				if dice < 10:
					currentTask = "Planting Flowers"
					mc.postToChat("You smell pollen.")
				interTaskCounter = 0
		
		if currentTask == "Planting Flowers":
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
						if tgtBlock == block.AIR or tgtBlock == block.SNOW and tgtBlockBeneath != block.AIR and tgtBlockBeneath != block.SNOW:
							mc.setBlock((int)(playerPos.x+dx),(int)(playerPos.y),(int)(playerPos.z+dz),theBlock)
					prevPlayerPos = playerPos
		interTaskCounter = interTaskCounter + 1
		time.sleep(0.05)
			
	mc.postToChat("The power wanes.")
	mc.postToChat("You feel... empty.")
	
	log(method, "Ended")
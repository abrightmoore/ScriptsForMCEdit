# This filter builds a Voronoi space, based on the blocks in your selection box.
# Suggested by @Nirgalbunny on Twitter.
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("VORONOI", "label"),
	  ("Edges?", False),
	  ("Edge Material", alphaMaterials.BlockofQuartz),
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
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def fix(angle):
	while angle > pi:
		angle = angle - 2 * pi
	while angle < -pi:
		angle = angle + 2 * pi
	return angle

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Voronoi(level, box, options)		
	level.markDirtyBox(box)
	
def Voronoi(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Voronoi"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	DOEDGES = options["Edges?"]
	MATERIALEDGE = (options["Edge Material"].ID,options["Edge Material"].blockData)
	# END CONSTANTS

	Q = []
	# Pass 1 - identify the location and type of each block in the selection box (use sparse regions)
	for iterX in xrange(box.minx, box.maxx):
		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				thisBlock = (level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ))
				if thisBlock != AIR:
					Q.append( (thisBlock, iterX, iterY, iterZ )  )

	# Pass 2 - identify the closest block to each point in space.
	for iterX in xrange(box.minx, box.maxx):
		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				thisBlock = (level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ))
				if thisBlock == AIR:
					# Work out the distance of this block from each of the anchor blocks.
					newBlock = AIR
					lastDistance = 999999999
					for iterQ in xrange(0, len(Q)):
						(controlBlock, x, y, z) = Q[iterQ]
						deltaX = x - iterX
						deltaY = y - iterY
						deltaZ = z - iterZ
						thisDistance = deltaX*deltaX + deltaY*deltaY + deltaZ*deltaZ
						if thisDistance < lastDistance:
							newBlock = controlBlock
							lastDistance = thisDistance # New champion to be beaten
					if newBlock != AIR:
						setBlock(level, newBlock, iterX, iterY, iterZ)
	
	# Optional Pass 3 - identify edges and mark them as the Edge block
	if DOEDGES == True:
		PQ = []
		for iterX in xrange(box.minx, box.maxx):
			print 'Do Edges: %s of %s' % (iterX, box.maxx)
			for iterY in xrange(box.miny, box.maxy):
				for iterZ in xrange(box.minz, box.maxz):
					thisBlock = (level.blockAt(iterX, iterY, iterZ), level.blockDataAt(iterX, iterY, iterZ))	
					if (level.blockAt(iterX+1, iterY, iterZ), level.blockDataAt(iterX+1, iterY, iterZ)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX-1, iterY, iterZ), level.blockDataAt(iterX-1, iterY, iterZ)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX, iterY+1, iterZ), level.blockDataAt(iterX, iterY+1, iterZ)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX, iterY-1, iterZ), level.blockDataAt(iterX, iterY-1, iterZ)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX, iterY, iterZ+1), level.blockDataAt(iterX, iterY, iterZ+1)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
					elif (level.blockAt(iterX, iterY, iterZ-1), level.blockDataAt(iterX, iterY, iterZ-1)) != thisBlock:
						PQ.append( (MATERIALEDGE, iterX, iterY, iterZ) )
		for ( block, x, y, z ) in PQ:
			setBlock(level, block, x, y, z)
					
	print '%s: Ended at %s' % (method, time.ctime())
# This filter is for drawing Spirolaterals and inspired by SourceCoded - http://redd.it/2ojjvd
# abrightmoore@yahoo.com.au
# http://brightmoore.net

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob

# For Reference (see @Texelelf and @CodeWarrior0 examples)
# 	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Mirror the blocks - in memory working read only copy
# 	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
#	setBlock(schematic, (BLOCKID, BLOCKDATA), (int)(centreWidth+xx), (int)(centreHeight+yy), (int)(centreDepth+zz))

# YOUR CODE GOES HERE \/ \/ \/ \/ \/ \/ \/ \/ \/

inputs = (
		("Spirolaterals", "label"),
		("Sequence (Forward, Back, Left, Right, Up, Down)", ("string","value=R")),
		("Degrees to Turn", 144),
		("Line length", 10),
		("Maximum Steps", 6),
		("Material", alphaMaterials.WhiteWool),	
		("Colours", ("string","value=15 0")),	
		("End at the beginning?", True),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Spirolaterals(level, box, options)

	level.markDirtyBox(box)
	

def Spirolaterals(level, box, options):
	method = "SPIROLATERALS"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	TwoPI = 2*pi
	ANGLESTEP = pi/180
	SEQUENCE = options["Sequence (Forward, Back, Left, Right, Up, Down)"]
	SEQUENCELIST = SEQUENCE.split()
	DEGREESTOTURN = options["Degrees to Turn"]
	LINELENGTH = options["Line length"]
	(MATERIALID,MATERIALDATA) = ((options["Material"].ID, options["Material"].blockData))
	COLOURS = options["Colours"].split()
	COLOURSLIST = map(int, COLOURS)
	MAXSTEPS = options["Maximum Steps"]
	ENDATTHEBEGINNING = options["End at the beginning?"]
	
	theta = (float)(0.0)
	phi = (float)(0.0)

	# Start in the middle, follow the rules until we get back where we started or fall outside the box.
	
	stepIter = 0
	cursorPos = 0
	colourPos = 0
	
	curX = (float)(1.0*box.minx+centreWidth)
	curY = (float)(1.0*box.miny+centreHeight)
	curZ = (float)(1.0*box.minz+centreDepth)
	(initX, initY, initZ) = (curX, curY, curZ)
	print '%s %s %s' % (curX, curY, curZ)
	
	while stepIter < MAXSTEPS:
		print 'Step %s of %s' % (stepIter, MAXSTEPS-1)
		command = SEQUENCELIST[cursorPos]
		colour = COLOURSLIST[colourPos]
		(nextX, nextY, nextZ) = (curX,curY,curZ) # initialise!
		if command == 'F' or command == 'f':
			(nextX, nextY, nextZ) = getRelativePolar((curX, curY, curZ), (theta, phi, LINELENGTH))
		elif command == 'B' or command == 'b':
			(nextX, nextY, nextZ) = getRelativePolar((curX, curY, curZ), (theta, phi, -LINELENGTH))
		elif command == 'U' or command == 'u':
			phi = phi +ANGLESTEP*DEGREESTOTURN
			(nextX, nextY, nextZ) = getRelativePolar((curX, curY, curZ), (theta, phi, LINELENGTH))
		elif command == 'D' or command == 'd':
			phi = phi -ANGLESTEP*DEGREESTOTURN
			(nextX, nextY, nextZ) = getRelativePolar((curX, curY, curZ), (theta, phi, LINELENGTH))
		elif command == 'L' or command == 'l':
			theta = theta -ANGLESTEP*DEGREESTOTURN
			(nextX, nextY, nextZ) = getRelativePolar((curX, curY, curZ), (theta, phi, LINELENGTH))
		elif command == 'R' or command == 'r':
			theta = theta +ANGLESTEP*DEGREESTOTURN
			(nextX, nextY, nextZ) = getRelativePolar((curX, curY, curZ), (theta, phi, LINELENGTH))
		else:
			print 'Unrecognised command in sequence: %s - %s' % (command, SEQUENCE)
		
		drawLine(level,(MATERIALID, colour), ((int)(curX), (int)(curY), (int)(curZ)), ((int)(nextX), (int)(nextY), (int)(nextZ)))
		
		curX = nextX
		curY = nextY
		curZ = nextZ
		
		if ENDATTHEBEGINNING == True:
			if (int)(curX) == (int)(initX) and (int)(curY) == (int)(initY) and (int)(curZ) == (int)(initZ):
				print 'Ending - returned to the beginning: %s %s %s' % ((int)(initX), (int)(initY), (int)(initZ))
				stepIter = MAXSTEPS
		
		cursorPos = (cursorPos +1) % len(SEQUENCELIST) # repeat sequence from the end
		colourPos = (colourPos +1) % len(COLOURSLIST)
		stepIter = stepIter +1
	
	print '%s: Ended at %s' % (method, time.ctime())
	
def getRelativePolar((x,y,z), (angleHoriz, angleVert, distance)):
	xDelta = cos(angleHoriz)*cos(angleVert)*distance
	zDelta = sin(angleHoriz)*cos(angleVert)*distance
	yDelta = sin(angleVert)*distance # Elevation
	return (x+xDelta, y+yDelta, z+zDelta)
	
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
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.
			
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

# This filter draws castles
#
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *

inputs = (
  ("Castle component", (
  		    "Round Tower",
  		    "Square Tower",
			"Turret",
  		    "Arch",
  		    "Fill",
			"Round Wall"
  		    )),
  		    
  ("Base Height %", 10.0),
  ("Wall Width %", 75.0),
  ("Wall Thickness %", 5.0),
  ("Top Height %", 30.0),
  ("Top Width %", 100.0),
  ("Number of Angles in a revolution", 90.0),
  ("Main Material:", "blocktype"),
  ("Secondary Material:", "blocktype"),
  ("Highlight Material:", "blocktype"),
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

def RoundTower(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	method = options["Castle component"]
	ANGLESTEPS = options["Number of Angles in a revolution"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	#v = options["Vertical Scale"]
	#h = options["Horizontal Scale"]
	STEPSIZE = (float)(2*pi/ANGLESTEPS) # can this be calculated?


	# Draw a tower from the base of the selection box to the top, with a spire roof, and windows
		
	# Local constants
	stepRadiusWidth = (float)(centreWidth/100.0)
	stepRadiusDepth = (float)(centreDepth/100.0)
	stepHeight = (float)(height/100.0)

	BASEHEIGHT = options["Base Height %"]
	BASERADIUS = options["Wall Width %"]+1
	WALLTHICKNESS = options["Wall Thickness %"]
	WALLRADIUSMIN = options["Wall Width %"]-WALLTHICKNESS
	WALLRADIUSMAX = options["Wall Width %"]
	ROOFHEIGHT = 100-options["Top Height %"] # percent of height
	ROOFRADIUS = options["Top Width %"] # percent of radius
	FLOORHEIGHT = 6
		
	angle = -pi
	while angle <= pi:
		print '%s: %s of %s' % (method, angle, pi)
		for iterRadius in xrange(0,100): # percent of distance from the centre
			for iterHeight in xrange(0, 100): # percent of distance from the base of the selection box
				block = (0, 0) # default to air
				if iterHeight < BASEHEIGHT: # base is thicker and in material 2
					if iterRadius < BASERADIUS:
						block = materialSecondary
				elif iterHeight < ROOFHEIGHT: # Tower is thinner and in material 1
					if iterRadius > WALLRADIUSMIN and iterRadius < WALLRADIUSMAX:
						if randint(0,100) <= 2:
							# block = materialHighlight
							block = materialMain
						elif randint(0,100) <= 4:
							block = materialSecondary
						else:
							block = materialMain
					elif iterRadius < WALLRADIUSMIN: # Inside the tower
						if (int)(iterHeight*stepHeight)%FLOORHEIGHT == 0: # Interior floors
							block = materialHighlight
						
				else: # Roof!
					if iterHeight == ROOFHEIGHT and iterRadius < (100 - (100/(100-ROOFHEIGHT)*(iterHeight-ROOFHEIGHT))): # Attic floor
						block = materialHighlight
					elif iterRadius < (100 - (100/(100-ROOFHEIGHT)*(iterHeight-ROOFHEIGHT))) and iterRadius > ((100-WALLTHICKNESS)-((100-WALLTHICKNESS)/((100-WALLTHICKNESS)-ROOFHEIGHT)*(iterHeight-ROOFHEIGHT))):
						block = materialHighlight
				
					
				# Conditionally, plot the block
				if block <> (0,0): # Maybe add an option for copying air?
					setBlock(level, block,  
						(int)(box.minx+centreWidth+iterRadius*stepRadiusWidth*cos(angle)),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+centreDepth+iterRadius*stepRadiusDepth*sin(angle))
						)
		angle = angle + STEPSIZE
		
	# Windows
	windows = randint(2,8)
	for iterLoop in xrange(0,windows):
		angle = randint(0,4)*pi/2 # centre of window is centre of wall
		TEMPMAXFLOOR = (float)(ROOFHEIGHT*stepHeight-FLOORHEIGHT)/FLOORHEIGHT
		TEMPMINFLOOR = (float)(BASEHEIGHT*stepHeight+FLOORHEIGHT)/FLOORHEIGHT
		if (int)(TEMPMAXFLOOR) > (int)(TEMPMINFLOOR):
			iterHeight = randint((int)(TEMPMINFLOOR), (int)(TEMPMAXFLOOR)) # what floor is this?
			iterHeight = iterHeight *FLOORHEIGHT+FLOORHEIGHT/2
			for iterRadius in xrange((int)(WALLRADIUSMIN), (int)(WALLRADIUSMAX)):
				setBlock(level, (0,0),
					(int)(box.minx+centreWidth+iterRadius*stepRadiusWidth*cos(angle)),
					(int)(box.miny+iterHeight),
					(int)(box.minz+centreDepth+iterRadius*stepRadiusDepth*sin(angle))
					)
				setBlock(level, (0,0),  
					(int)(box.minx+centreWidth+iterRadius*stepRadiusWidth*cos(angle)),
					(int)(box.miny+1+iterHeight),
					(int)(box.minz+centreDepth+iterRadius*stepRadiusDepth*sin(angle))
					)

def SquareTower(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	method = options["Castle component"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2

	# Draw a tower from the base of the selection box to the top, with a crenelated roof and windows
		
	# Local constants
	stepRadiusWidth = (float)(centreWidth/100.0)
	stepRadiusDepth = (float)(centreDepth/100.0)
	stepWidth = (float)(width/100.0)
	stepDepth = (float)(depth/100.0)
	stepHeight = (float)(height/100.0)

	BASEHEIGHT = options["Base Height %"]
	BASERADIUS = options["Wall Width %"]
	WALLTHICKNESS = options["Wall Thickness %"]
	WALLRADIUSMIN = options["Wall Width %"]-WALLTHICKNESS
	WALLRADIUSMAX = options["Wall Width %"]
	ROOFHEIGHT = 100-options["Top Height %"] # percent of height
	ROOFRADIUS = options["Top Width %"] # percent of radius
	FLOORHEIGHT = 6
		
		
	# Base
	for iterHeight in xrange(0,(int)(BASEHEIGHT)):
		print '%s: BASE %s of %s' % (method, iterHeight, BASEHEIGHT)
		for iterX in xrange( (int)((100-BASERADIUS)/2), (int)(BASERADIUS+(100-BASERADIUS)/2) ):
			for iterZ in xrange( (int)((100-BASERADIUS)/2), (int)(BASERADIUS+(100-BASERADIUS)/2) ):
 				block = materialSecondary
 				setBlock(level, block,  
							(int)(box.minx+iterX*stepWidth),
							(int)(box.miny+iterHeight*stepHeight),
							(int)(box.minz+iterZ*stepDepth),
					)
					
					
	# Walls
	for iterHeight in xrange((int)(BASEHEIGHT),(int)(ROOFHEIGHT)):
		print '%s: WALL %s of %s' % (method, iterHeight, ROOFHEIGHT)
		for iterX in xrange( (int)((100-WALLRADIUSMAX)/2),(int)((100-WALLRADIUSMAX)/2+WALLTHICKNESS) ):
			for iterZ in xrange( (int)((100-WALLRADIUSMAX)/2), (int)(WALLRADIUSMAX+(100-WALLRADIUSMAX)/2) ):
				if randint(0,100) <= 2:
					# block = materialHighlight
					block = materialMain
				elif randint(0,100) <= 4:
					block = materialSecondary
				else:
					block = materialMain
	 			setBlock(level, block,  
						(int)(box.minx+iterX*stepWidth),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+iterZ*stepDepth)
					)

		for iterX in xrange( (int)(WALLRADIUSMAX+(100-WALLRADIUSMAX)/2-WALLTHICKNESS),(int)(WALLRADIUSMAX+(100-WALLRADIUSMAX)/2)):
			for iterZ in xrange( (int)((100-WALLRADIUSMAX)/2), (int)(WALLRADIUSMAX+(100-WALLRADIUSMAX)/2) ):
				if randint(0,100) <= 2:
					# block = materialHighlight
					block = materialMain
				elif randint(0,100) <= 4:
					block = materialSecondary
				else:
					block = materialMain
 				setBlock(level, block,  
						(int)(box.minx+iterX*stepWidth),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+iterZ*stepDepth)
					)

		for iterZ in xrange( (int)(WALLRADIUSMAX+(100-WALLRADIUSMAX)/2-WALLTHICKNESS),(int)(WALLRADIUSMAX+(100-WALLRADIUSMAX)/2) ):
			for iterX in xrange( (int)((100-WALLRADIUSMAX)/2), (int)(WALLRADIUSMAX+(100-WALLRADIUSMAX)/2) ):
				if randint(0,100) <= 2:
					# block = materialHighlight
					block = materialMain
				elif randint(0,100) <= 4:
					block = materialSecondary
				else:
					block = materialMain
 				setBlock(level, block,  
						(int)(box.minx+iterX*stepWidth),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+iterZ*stepDepth)
					)

		for iterZ in xrange( (int)((100-WALLRADIUSMAX)/2),(int)((100-WALLRADIUSMAX)/2+WALLTHICKNESS)):
			for iterX in xrange( (int)((100-WALLRADIUSMAX)/2), (int)(WALLRADIUSMAX+(100-WALLRADIUSMAX)/2) ):
				if randint(0,100) <= 2:
					# block = materialHighlight
					block = materialMain
				elif randint(0,100) <= 4:
					block = materialSecondary
				else:
					block = materialMain
 				setBlock(level, block,  
						(int)(box.minx+iterX*stepWidth),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+iterZ*stepDepth)
					)

	# Roof
	for iterHeight in xrange((int)(ROOFHEIGHT),(int)(ROOFHEIGHT+WALLTHICKNESS)):
		print '%s: ROOF EDGE %s of %s' % (method, iterHeight, ROOFHEIGHT+WALLTHICKNESS)
		for iterX in xrange( (int)((100-ROOFRADIUS)/2), (int)(ROOFRADIUS+(100-ROOFRADIUS)/2) ):
			for iterZ in xrange( (int)((100-ROOFRADIUS)/2), (int)(ROOFRADIUS+(100-ROOFRADIUS)/2) ):
 				block = materialSecondary
 				setBlock(level, block,  
							(int)(box.minx+iterX*stepWidth),
							(int)(box.miny+iterHeight*stepHeight),
							(int)(box.minz+iterZ*stepDepth)
					)

	for iterHeight in xrange((int)(ROOFHEIGHT),(int)(ROOFHEIGHT+WALLTHICKNESS)):
		print '%s: ROOF CENTRE %s of %s' % (method, iterHeight, ROOFHEIGHT+WALLTHICKNESS)
		for iterX in xrange( (int)((100-WALLRADIUSMIN)/2), (int)(WALLRADIUSMIN+(100-WALLRADIUSMIN)/2) ):
			for iterZ in xrange( (int)((100-WALLRADIUSMIN)/2), (int)(WALLRADIUSMIN+(100-WALLRADIUSMIN)/2) ):
 				block = materialHighlight
 				setBlock(level, block,  
							(int)(box.minx+iterX*stepWidth),
							(int)(box.miny+iterHeight*stepHeight),
							(int)(box.minz+iterZ*stepDepth)
					)

	# Crenelation
	for iterHeight in xrange((int)(ROOFHEIGHT+WALLTHICKNESS),(int)(100)):
		print '%s: CRENELATION %s of %s' % (method, iterHeight, 100)
		for iterX in xrange( (int)((100-ROOFRADIUS)/2),(int)((100-ROOFRADIUS)/2+WALLTHICKNESS) ):
			for iterZ in xrange( (int)((100-ROOFRADIUS)/2), (int)(ROOFRADIUS+(100-ROOFRADIUS)/2) ):
				block = materialSecondary
				if iterZ%4 == 1 or iterZ%4 == 2:
					block = (0,0)
	 			setBlockIfEmpty(level, block,  
						(int)(box.minx+iterX*stepWidth),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+iterZ*stepDepth)
					)

		for iterX in xrange( (int)(ROOFRADIUS+(100-ROOFRADIUS)/2-WALLTHICKNESS),(int)(ROOFRADIUS+(100-ROOFRADIUS)/2)):
			for iterZ in xrange( (int)((100-ROOFRADIUS)/2), (int)(ROOFRADIUS+(100-ROOFRADIUS)/2) ):
				block = materialSecondary
				if iterZ%4 == 1 or iterZ%4 == 2:
					block = (0,0)
 				setBlockIfEmpty(level, block,  
						(int)(box.minx+iterX*stepWidth),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+iterZ*stepDepth)
					)

		for iterZ in xrange( (int)(ROOFRADIUS+(100-ROOFRADIUS)/2-WALLTHICKNESS),(int)(ROOFRADIUS+(100-ROOFRADIUS)/2) ):
			for iterX in xrange( (int)((100-ROOFRADIUS)/2), (int)(ROOFRADIUS+(100-ROOFRADIUS)/2) ):
				block = materialSecondary
				if iterX%4 == 1 or iterX%4 == 2:
					block = (0,0)
 				setBlockIfEmpty(level, block,  
						(int)(box.minx+iterX*stepWidth),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+iterZ*stepDepth)
					)

		for iterZ in xrange( (int)((100-ROOFRADIUS)/2),(int)((100-ROOFRADIUS)/2+WALLTHICKNESS)):
			for iterX in xrange( (int)((100-ROOFRADIUS)/2), (int)(ROOFRADIUS+(100-ROOFRADIUS)/2) ):
				block = materialSecondary
				if iterX%4 == 1 or iterX%4 == 2:
					block = (0,0)
 				setBlockIfEmpty(level, block,  
						(int)(box.minx+iterX*stepWidth),
						(int)(box.miny+iterHeight*stepHeight),
						(int)(box.minz+iterZ*stepDepth)
					)

	# Floors

	TEMPMAXFLOOR = (float)(ROOFHEIGHT*stepHeight)/FLOORHEIGHT
	TEMPMINFLOOR = (float)(BASEHEIGHT*stepHeight+FLOORHEIGHT)/FLOORHEIGHT
	if (int)(TEMPMAXFLOOR) > (int)(TEMPMINFLOOR):
		for iterHeight in xrange((int)(TEMPMINFLOOR),(int)(TEMPMAXFLOOR)):
			print '%s: FLOOR %s of %s' % (method, iterHeight, (int)(TEMPMAXFLOOR))
			for iterX in xrange( (int)((100-WALLRADIUSMIN)/2), (int)(WALLRADIUSMIN+(100-WALLRADIUSMIN)/2) ):
				for iterZ in xrange( (int)((100-WALLRADIUSMIN)/2), (int)(WALLRADIUSMIN+(100-WALLRADIUSMIN)/2) ):
	 				block = materialHighlight
	 				setBlock(level, block,  
								(int)(box.minx+iterX*stepWidth),
								(int)(box.miny+iterHeight*FLOORHEIGHT),
								(int)(box.minz+iterZ*stepDepth)
						)


	# Windows
	windows = randint(2,8)
	for iterLoop in xrange(0,windows):
		angle = randint(0,4)*pi/2 # centre of window is centre of wall
		TEMPMAXFLOOR = (float)(ROOFHEIGHT*stepHeight-FLOORHEIGHT)/FLOORHEIGHT
		TEMPMINFLOOR = (float)(BASEHEIGHT*stepHeight+FLOORHEIGHT)/FLOORHEIGHT
		if (int)(TEMPMAXFLOOR) > (int)(TEMPMINFLOOR):
			iterHeight = randint((int)(TEMPMINFLOOR), (int)(TEMPMAXFLOOR)) # what floor is this?
			iterHeight = iterHeight *FLOORHEIGHT+FLOORHEIGHT/2
			for iterRadius in xrange((int)(WALLRADIUSMIN), (int)(WALLRADIUSMAX)):
				setBlock(level, (0,0),
					(int)(box.minx+centreWidth+iterRadius*stepRadiusWidth*cos(angle)),
					(int)(box.miny+iterHeight),
					(int)(box.minz+centreDepth+iterRadius*stepRadiusDepth*sin(angle))
					)
				setBlock(level, (0,0),  
					(int)(box.minx+centreWidth+iterRadius*stepRadiusWidth*cos(angle)),
					(int)(box.miny+1+iterHeight),
					(int)(box.minz+centreDepth+iterRadius*stepRadiusDepth*sin(angle))
					)
	
def Arch(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	method = options["Castle component"]
	ANGLESTEPS = options["Number of Angles in a revolution"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = (float)(width / 2)
	centreHeight = height / 2
	centreDepth = (float)(depth / 2)
	#v = options["Vertical Scale"]
	#h = options["Horizontal Scale"]
	STEPSIZE = (float)(2*pi/ANGLESTEPS) # can this be calculated?


	# Draw a tower from the base of the selection box to the top, with a spire roof, and windows
		
	# Local constants
	stepRadiusWidth = (float)(centreWidth/100.0)
	stepRadiusDepth = (float)(centreDepth/100.0)
	stepHeight = (float)(height/100.0)

	BASEHEIGHT = options["Base Height %"]
	BASERADIUS = options["Wall Width %"]+1
	WALLTHICKNESS = options["Wall Thickness %"]
	WALLRADIUSMIN = options["Wall Width %"]-WALLTHICKNESS
	WALLRADIUSMAX = options["Wall Width %"]
	ROOFHEIGHT = 100-options["Top Height %"] # percent of height
	ROOFRADIUS = options["Top Width %"] # percent of radius
	FLOORHEIGHT = 6
	
	# Determine orientation
	orientation = 1 # depth path, 2 is width path
	if level.blockAt(box.minx-1,box.miny+centreHeight,box.minz) == 0:
		orientation = 2 # width path

	if orientation == 1: # depthward arch
		# Bottom half is a vertical space bounded by blocks
		for iterHeight in xrange(0, centreHeight):
			print '%s: ARCHZ1 %s of %s' % (method, iterHeight, centreHeight)
			for iterX in xrange(0,width):
				for iterZ in xrange(0,depth):
					if iterX == 0 or iterX == (width-1):
						setBlock(level, materialMain, box.minx+iterX, box.miny+iterHeight, box.minz+iterZ)
					else:
						setBlock(level, (0,0), box.minx+iterX, box.miny+iterHeight, box.minz+iterZ)
		for iterZ in xrange(0,depth):
			print '%s: ARCHZ2 %s of %s' % (method, iterZ, depth)
			angle = 0
			while angle < pi:
				for iterRadius in xrange(0,100): # percent of distance from the centre
					block = (0,0)
					tempY = (float)(box.miny+centreHeight+iterRadius*stepHeight/2*sin(angle))
					tempX = (float)(box.minx+centreWidth+iterRadius*stepRadiusWidth*cos(angle))
					setBlock(level, block,  
							(int)(tempX),
							(int)(tempY),
							(int)(box.minz+iterZ)
							)
				angle = angle + STEPSIZE
		for iterZ in xrange(0,depth):
			print '%s: ARCHZ3 %s of %s' % (method, iterZ, depth)
			angle = 0
			while angle < pi:
				iterRadius = 99 # percent of distance from the centre
				block = materialSecondary
				tempY = (float)(box.miny+centreHeight+iterRadius*stepHeight/2*sin(angle))
				tempX = (float)(box.minx+centreWidth+iterRadius*stepRadiusWidth*cos(angle))
				setBlock(level, block,  
						(int)(tempX),
						(int)(tempY),
						(int)(box.minz+iterZ)
						)
				angle = angle + STEPSIZE

	else: # widthward arch
		# Bottom half is a vertical space bounded by blocks
		for iterHeight in xrange(0, centreHeight):
			print '%s: ARCHX1 %s of %s' % (method, iterHeight, centreHeight)
			for iterX in xrange(0,width):
				for iterZ in xrange(0,depth):
					if iterZ == 0 or iterZ == (depth-1):
						setBlock(level, materialMain, box.minx+iterX, box.miny+iterHeight, box.minz+iterZ)
					else:
						setBlock(level, (0,0), box.minx+iterX, box.miny+iterHeight, box.minz+iterZ)
		for iterX in xrange(0,width):
			print '%s: ARCHX2 %s of %s' % (method, iterX, width)
			angle = 0
			while angle < pi:
				for iterRadius in xrange(0,100): # percent of distance from the centre
					block = (0,0)
					tempY = (float)(box.miny+centreHeight+iterRadius*stepHeight/2*sin(angle))
					tempZ = (float)(box.minz+centreDepth+iterRadius*stepRadiusDepth*cos(angle))
					setBlock(level, block,  
							(int)(box.minx+iterX),
							(int)(tempY),
							(int)(tempZ)
							)
				angle = angle + STEPSIZE
		for iterX in xrange(0,width):
			print '%s: ARCHX3 %s of %s' % (method, iterX, width)
			angle = 0
			while angle < pi:
				iterRadius = 99 # percent of distance from the centre
				block = materialSecondary
						
				tempY = (float)(box.miny+centreHeight+iterRadius*stepHeight/2*sin(angle))
				tempZ = (float)(box.minz+centreDepth+iterRadius*stepRadiusDepth*cos(angle))
				setBlock(level, block,  
						(int)(box.minx+iterX),
						(int)(tempY),
						(int)(tempZ)
						)
				angle = angle + STEPSIZE

def Fill(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	method = options["Castle component"]
	(width, height, depth) = getBoxSize(box)

	for iterX in xrange(width):
		for iterY in xrange(height):
			for iterZ in xrange(depth):
				if randint(0,100) <= 2:
					# block = materialHighlight
					block = materialMain
				elif randint(0,100) <= 4:
					block = materialSecondary
				else:
					block = materialMain
 				setBlock(level, block,  
						(int)(box.minx+iterX),
						(int)(box.miny+iterY),
						(int)(box.minz+iterZ)
					)				

def RoundWall(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	method = "CastleSymmetric"
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	
	# First, what is the layout for this castle?
	NUMBEROFWALLS = randint(8,8 + (int)(width/8) ) # maximum number of wall sections is influenced by the width of the selection box.
	HEIGHTOFWALLS = (int)( height )
	NUMBEROFWALLSPERQUADRANT = (int)(NUMBEROFWALLS/4) # Optimisation - calculate once, draw four times
	if NUMBEROFWALLSPERQUADRANT == 0:
		NUMBEROFWALLSPERQUADRANT = 1
	DEPTHOFWALLS = randint(3, randint(4,10) ) 
	AIR = (0,0)
	
	# Do the wall. Travel around the circumference of the castle drawing the wall as we go.
	
	WALLANGLE = (float)(pi/2/NUMBEROFWALLSPERQUADRANT) # FIX: radians, not degrees.
	
	continueWalling = True
	while continueWalling == True:
		for wallInstanceNum in xrange(0, NUMBEROFWALLSPERQUADRANT):
			print '%s1: %s of %s' % (method, wallInstanceNum, NUMBEROFWALLSPERQUADRANT)
			# Work out the direction and distance. Calculate in Quadrant 1, apply in all quadrants
			
			STARTANGLE = wallInstanceNum * WALLANGLE
			ENDANGLE = (wallInstanceNum +1) * WALLANGLE

			isaGate = False
			if randint(0,100) < 10:
				isaGate = True

			for wallDepthIter in xrange(0,DEPTHOFWALLS):
				print '%s1a: Rendering wall layer %s of %s' % (method, wallDepthIter, DEPTHOFWALLS)
				
				startX = (int)((centreWidth - wallDepthIter) * cos(STARTANGLE))
				startZ = (int)((centreDepth - wallDepthIter) * sin(STARTANGLE))

				endX = (int)((centreWidth - wallDepthIter) * cos(ENDANGLE))
				endZ = (int)((centreDepth - wallDepthIter) * sin(ENDANGLE))

				dX = endX - startX
				dZ = endZ - startZ
				WALLDIRECTION = (float)(atan2( dZ, dX))

				WALLDISTANCE = (int)( sqrt( dX**2 + dZ**2) ) # This is the number of steps from start of the wall to finish. FIX: +, not *!
				WALLDISTANCE = WALLDISTANCE # adjust for turret.




				for wallIter in xrange(0,WALLDISTANCE+1): # Now, let's go for a walk, adding a layer of wall as we go! We are basically increasing the distance of the vector at each step

					# Calculate the next centre block location.
					offsetX = wallIter * cos(WALLDIRECTION)
					offsetZ = wallIter * sin(WALLDIRECTION)


					for y in xrange(0, HEIGHTOFWALLS-(int)(wallDepthIter/3)):
						if randint(0,100) <= 4:
							block = materialSecondary
						else:				
							if wallDepthIter/3 > 0 and y == (HEIGHTOFWALLS-1-(int)(wallDepthIter/3)):
								block = materialHighlight
							else:
								block = materialMain

						if isaGate == True and (wallIter > (WALLDISTANCE/3 - 2)) and (wallIter < (WALLDISTANCE/2 +3)) and y < 10:
							block = AIR

						setBlock(level, block,  
							(int)(box.minx+centreWidth+(startX+offsetX)),
							(int)(box.miny+y),
							(int)(box.minz+centreDepth+(startZ+offsetZ))
						)

						if randint(0,100) <= 4:
							block = materialSecondary
						else:				
							if wallDepthIter/3 > 0 and y == (HEIGHTOFWALLS-1-(int)(wallDepthIter/3)):
								block = materialHighlight
							else:
								block = materialMain
						if isaGate == True and (wallIter > (WALLDISTANCE/3 - 2)) and (wallIter < (WALLDISTANCE/2 +3)) and y < 10:
							block = AIR

						setBlock(level, block,  
							(int)(box.minx+centreWidth-(startX+offsetX)),
							(int)(box.miny+y),
							(int)(box.minz+centreDepth+(startZ+offsetZ))
						)

						if randint(0,100) <= 4:
							block = materialSecondary
						else:				
							if wallDepthIter/3 > 0 and y == (HEIGHTOFWALLS-1-(int)(wallDepthIter/3)):
								block = materialHighlight
							else:
								block = materialMain
						if isaGate == True and (wallIter > (WALLDISTANCE/3 - 2)) and (wallIter < (WALLDISTANCE/2 +3)) and y < 10:
							block = AIR

						setBlock(level, block,  
							(int)(box.minx+centreWidth-(startX+offsetX)),
							(int)(box.miny+y),
							(int)(box.minz+centreDepth-(startZ+offsetZ))
						)

						if randint(0,100) <= 4:
							block = materialSecondary
						else:				
							if wallDepthIter/3 > 0 and y == (HEIGHTOFWALLS-1-(int)(wallDepthIter/3)):
								block = materialHighlight
							else:
								block = materialMain
						if isaGate == True and (wallIter > (WALLDISTANCE/3 - 2)) and (wallIter < (WALLDISTANCE/2 +3)) and y < 10:
							block = AIR

						setBlock(level, block,  
							(int)(box.minx+centreWidth+(startX+offsetX)),
							(int)(box.miny+y),
							(int)(box.minz+centreDepth-(startZ+offsetZ))
						)
					
		continueWalling = False
			
def Turret(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	AIR = (0,0)
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	method = "CastleSymmetric"
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)

	# Turrets
	TURRETWIDTH = width
	TURRETHEIGHT = height
	TURRETDIAMETER = (int)(pi * TURRETWIDTH)+1 # the number of blocks around the circumference that need to be drawn.
	TURRETRADIUS = (int)(TURRETWIDTH/2)
	TURRETANGLE = (float)(2*pi / TURRETDIAMETER)

	for turretCircumferenceIter in xrange (0,TURRETDIAMETER):
		wallX = (int)(TURRETRADIUS * cos(TURRETANGLE*turretCircumferenceIter))
		wallZ = (int)(TURRETRADIUS * sin(TURRETANGLE*turretCircumferenceIter))
		window = False

		for iterY in xrange(0, TURRETHEIGHT):
			if randint(0,100) <= 4:
				block = materialSecondary
			else:				
				block = materialMain

			if iterY%6 == 2 and randint(0,100) == 1:
				window = True
				block = AIR
			elif window == True:
				block = AIR # AIR
				window = False


			setBlock(level, block,  
				(int)(box.minx+centreWidth+wallX),
				(int)(box.miny+iterY),
				(int)(box.minz+centreDepth+wallZ)
			)
				
	for iterY in xrange(0, TURRETHEIGHT): # Now place flooring
		if (iterY%6) == 0:
			# Drop in a floor
			print 'Placing a floor at %s on Turret' % (iterY)
			for floorRadius in xrange(0, TURRETRADIUS):
				floorCircumference = (int)(2 * floorRadius * pi)+1
				floorAngle = 2*pi/floorCircumference
				for floorIter in xrange(0, floorCircumference):
					floorX = (int)(floorRadius * cos(floorAngle * floorIter))
					floorZ = (int)(floorRadius * sin(floorAngle * floorIter))
					block = materialHighlight
					setBlockIfEmpty(level, block,  
						(int)(box.minx+centreWidth+floorX),
						(int)(box.miny+iterY),
						(int)(box.minz+centreDepth+floorZ)
						)

	
	
def perform(level, box, options):
	''' This script is used to generate components of Castles in Minecraft. Feedback to abrightmoore@yahoo.com.au '''
	method = options["Castle component"]

	# METHODS
	if method == "Round Tower":
		RoundTower(level, box, options)		
	elif method == "Square Tower":
		SquareTower(level, box, options)	
	elif method == "Turret":
		Turret(level, box, options)	
	elif method == "Arch":
		Arch(level, box, options)	
	elif method == "Fill":
		Fill(level, box, options)	
	elif method == "Round Wall":
		RoundWall(level, box, options)
	
	level.markDirtyBox(box)
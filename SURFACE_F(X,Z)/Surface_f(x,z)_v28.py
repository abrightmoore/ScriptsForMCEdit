# This filter draws surfaces based on equations of the style y = f(x, z)
#   Some surface functions are from http://houseof3d.com/pete/applets/graph/index.html
# abrightmoore@yahoo.com.au / http://brightmoore.net
# https://dl.dropbox.com/u/54682869/Minecraft/Filters/Surface_f%28x%2Cz%29_v26.py

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *


inputs = (
  ("Surface Type", (
  		    "Disc-o!",
  		    "Itty Bitty Boxes",
  		    "Dune",
  		    "Sphericalise!",
  		    "Cylindrificate!",
  		    "Rotatiticulator!",
  		    "Razor Wire",
  		    "Clebsch surface",
		    "Spiral",
		    "Sea Shell",
		    "Conic Spiral - Nautilus",
		    "Conic Spiral - Toroid consuming own tail",
		    "Trefoil Knot",
		    "Higher-Order Knot",
			"Higher-Order Knot 16",
			"Higher-Order Knot Param",
		    "Dini's Surface",
		    "Moebius Surface",
		    "Vertical Sheet",
		    "Mushroom",
		    "Deform Landscape - Wave",
		    "Deform Landscape - Rama",
		    "Deform Landscape - Rama II",
  		    "Wave", 
  		    "Parabola", 
  		    "Hyperbolic Paraboloid", 
  		    "Saddle", 
  		    "y=x^2*z^2",
  		    "y=cos(x)+cos(z)", 
  		    "y=(cos(x)+cos(z))^5", 
  		    "y=cos(x^2+z^2)", 
  		    "y=sin(x^2+z^2)^3",
  		    "y=x*z*sin(x)+x*z*sin(z)", 
  		    "y=tan(x)dividedbyz+tan(z)dividedbyx", 
  		    "y=sin(x*z)",
  		    "y=cos(sqrt(x^2+z^2))", 
  		    "y=z*tan(x)", 
  		    "y=x*ln(z^2)", 
  		    "y=x^2 + z^2 - ln(x*z)",
  		    "Cos(x)Sin(y) + Cos(y)Sin(z) + Cos(z)Sin(x) = 0",
  		    "Sombrero", 
  		    "Hyta's function",
  		    "y=floor(x*z)",
  		    "(x2 + (9 div 4)y2 + z2 - 1)3 - x2z3 - (9/80)y2z3 = 0",
		    "Mountain sinc(x)",
		    "Rotatorificationatical!"
  		    )),
  		    
  ("Vertical Scale", 10.0),
  ("Horizontal Scale", 1.0),
  ("Parameter", 5.0),
  ("Cycles", 3.0),
  ("Quick?", False),

  ("Pick a block:", "blocktype"),
  ("Colour?", False)
)

def fix(angle):
 
	while angle > pi:
		angle = angle - 2 * pi
	
	
	while angle < -pi:
		angle = angle + 2 * pi

	return angle


def perform(level, box, options):
	''' This script is used to generate surfaces in Minecraft. Feedback to abrightmoore@yahoo.com.au '''
	
	block = (options["Pick a block:"].ID, options["Pick a block:"].blockData)
	method = options["Surface Type"]

	(width, height, depth) = getBoxSize(box)

	centrewidth = width / 2
	centreheight = height / 2
	centredepth = depth / 2

	scalevert = options["Vertical Scale"]
	h = options["Horizontal Scale"]
	param = options["Parameter"]
	cycles = options["Cycles"]
	quick = options["Quick?"]
	COLOURISE = options["Colour?"]
	colours = "15 7 8 0 6 2 10 11 3 9 13 5 4 1 14 12".split()
	coloursList = map(int, colours)
	
	
	if method == "Cylindrificate!":
		sampleResolution = 720.0		# increase to improve sampling resolution.
		polarDeltaDegree = (float)(2*pi/(sampleResolution)) 	# how many radians to move each map iteration
		polarOriginX = 0 			# centre of the cylinder
		polarOriginY = 127 			# centre of the cylinder
		polarOriginZ = 0 			# centre of the cylinder
		
		cartesianStepSize = (float)(width) / (float)(sampleResolution)	# number of samples - potential optimisation here to improve performance. Don't need to scan a strip already scanned.
		
		iteratorX = 0.0
		polarAngle = 0.0
		while iteratorX < (float)(width):
			print '%s: X %s of %s' % (method, iteratorX, (float)(width))
			
			cartesianIteratorY = height-1
			while cartesianIteratorY >= 0:
				# copy each vertical strip of blocks onto the new polar line
				if h > 0: # bedrock at cylinder surface
					adjust = height-cartesianIteratorY
					polarDestX = polarOriginX + (adjust) * cos(polarAngle)
					polarDestY = polarOriginY + (adjust) * sin(polarAngle) # bedrock at the outer rim, air within
				else: # overworld at cylinder surface, bedrock at core
					polarDestX = polarOriginX + cartesianIteratorY * cos(polarAngle)
					polarDestY = polarOriginY + cartesianIteratorY * sin(polarAngle) # bedrock at the core, surface faces outward
			
				x_1 = (int)(box.minx+iteratorX)
				y_1 = (int)(box.miny+cartesianIteratorY)
				xd_1 = (int)(polarDestX)
				yd_1 = (int)(polarDestY)
			
				iteratorZ = 0
				while iteratorZ < depth:
					tempBlock = level.blockAt(x_1,y_1,(int)(box.minz+iteratorZ))
					if tempBlock != 0:
						polarDestZ = polarOriginZ + iteratorZ 		# for each depth element
						tempBlockTarget = level.blockAt(xd_1, yd_1, (int)(polarDestZ))
					
						if tempBlockTarget == 0: # copy if source is not air. Copy if target is not already a block. Put water and lava here if you want to suppress liquids
							level.setBlockAt(xd_1, yd_1, (int)(polarDestZ), tempBlock ) 
							level.setBlockDataAt(xd_1, yd_1, (int)(polarDestZ), level.blockDataAt(x_1,y_1,(int)(box.minz+iteratorZ)) )
					iteratorZ = iteratorZ +1
				cartesianIteratorY = cartesianIteratorY - 1
			polarAngle = polarAngle + polarDeltaDegree
			iteratorX = iteratorX + cartesianStepSize 

	elif method == "Itty Bitty Boxes": # I love this function. It has SOOOOO much potential.
		for iterX in xrange(0, width):
			print '%s: %s of %s' % (method, iterX, width-1)
			for iterZ in xrange(0, depth):
				for iterY in xrange(0, height):
					if iterX % h == 0 or iterZ % h == 0 or iterY % scalevert == 0:
						setBlock(level, block, (int)(box.minx+iterX), (int)(box.miny+iterY), (int)(box.minz+iterZ))

	elif method == "Mountain sinc(x)":
		iterX = -centrewidth
		while iterX <= centrewidth:
			iterZ = -centredepth
			while iterZ <= centredepth:
				if iterX != 0:
					newY = -scalevert*sin(iterX/h)/iterX*cos(iterZ/h)
				else:
					newY = scalevert*sin(iterX/h)
				setBlockToGround(level, block, (int)(box.minx+centrewidth+iterX), (int)(box.miny+centreheight+newY), (int)(box.minz+centredepth+iterZ), (int)(box.miny))
				iterZ = iterZ+1
			iterX = iterX+1

	elif method == "Disc-o!":
		# draw a disc or cylinder in the horizontal plane
		STEPSIZE = pi/1440 # approx circumference in blocks
		theta = -pi
		while theta <= pi:
			print '%s: %s of %s' % (method, theta, pi)
			for iterX in xrange((int)(h),(int)(h+scalevert)): # Uses scalevert for the width of the disc section. Uses h for the width of the inner opening
				for iterY in xrange(0, height):
					setBlock(level, block, (int)(box.minx+(centrewidth-1)+iterX*cos(theta)), (int)(box.miny+iterY), (int)(box.minz+(centredepth-1)+iterX*sin(theta)))
			theta = theta + STEPSIZE

	elif method == "Razor Wire":

		TWOPI = 2*pi		
		STEPSIZE = pi/180


		iterX = 0.0
		loopPosn = 0.0
		while iterX < width:
			# for each horizontal scale step, perform one loop up and around of the selected block
			newZ = centredepth * cos(loopPosn/h*TWOPI)
			newY = centreheight * sin(loopPosn/h*TWOPI)

			setBlock(level, block, (int)(box.minx+iterX), (int)(box.miny+centreheight+newY), (int)(box.minz+centredepth+newZ))			

			iterX = iterX + STEPSIZE
			loopPosn = loopPosn + STEPSIZE
			if loopPosn >= h:
				loopPosn = 0.0
			
	elif method == "Sphericalise!":
		
		destX = 0.0	# Target origin
		destY = 127.0
		destZ = 0.0
		
		for sx in xrange(0,width):
			print '%s: %s of %s' % (method, sx, width-1)
			theta = (float)(pi *2 * sx / width) # angle around the sphere (latitude) is the ratio of distance traveled in the source blocks to a full revolution.
			
			for sz in xrange(0,depth):
				
				phi = (float)(pi/2 - pi * sz / depth) # longitude is the ratio of distance traveled in the source blocks to a half revolution
			
				polarX = (float)(cos(theta) * cos(phi))
				polarZ = (float)(sin(theta) * cos(phi))
					
				for sy in xrange(0,height):
					
					tempBlockSource = level.blockAt(box.minx+sx,box.miny+sy,box.minz+sz) # What is the source block? Ignore air
					if tempBlockSource <> 0: # Ignore air
						
						dX = (float)(polarX * sy * h + destX)
						dZ = (float)(polarZ * sy * h + destZ)
						dY = (float)(sin(phi) * sy * h + destY)
						
						# print '%s: polarX %s polarZ %s theta %s phi %s' % (method, (float)(polarX), (float)(polarZ),(float)(theta),(float)(phi))

						#We are mapping the source block onto a sphere where the y position is the layer from the core, and x and z are mapped onto the surface in a grid
						
						if level.blockAt((int)(dX), (int)(dY), (int)(dZ)) == 0: #Do nothing if a block already exists at the target location 
							level.setBlockAt((int)(dX), (int)(dY), (int)(dZ), tempBlockSource)
							level.setBlockDataAt((int)(dX), (int)(dY), (int)(dZ), level.blockDataAt(box.minx+sx, box.miny+sy, box.minz+sz))

	elif method == "Dune": # set HORIZ to 2, and scalevert to 1.
		
		theta = -pi/h
		MAXTHETA = pi/h
		MAXPHI =pi/4 # 12.5% of a full revolution
		STEPSIZE = pi / 360
		STEPSIZERADIUS = 1.0 / width
				
		while theta < MAXTHETA:
			print '%s: %s of %s' % (method, theta, MAXTHETA)
			phi= 0.0	
			while phi < MAXPHI:	
				radius = 0.0
				while radius <= 1.0:
					xpos = width*radius*cos(theta)*cos(phi)
					zpos = centredepth+depth*radius/2*sin(theta)*cos(phi)
					newx = (int)(box.minx+xpos)
					newy = (int)(box.miny+(height*radius*sin(phi))*sin(xpos/(width/2))  )
					newz = (int)(box.minz+zpos)
					
					if newy >= (int)(scalevert + box.miny):
						if level.blockAt(newx, newy, newz) == 0: # replace if air
							setBlock(level, block, newx, newy, newz)
			
					radius = radius + STEPSIZERADIUS
				phi = phi + STEPSIZE
			theta = theta + STEPSIZE

	
	elif method == "Rotatorificationatical!":
		# for each block in the selection box, copy to a new location rotated around the origin. Testing BaconnEggs implementation
		# number of copies is in the horizontal scale box
		
		originX = 0.0
		originZ = 0.0
		OFFSET = 0.5
		
		angleDelta = (float)(pi * 2 / h)
		for iterInstances in xrange(1, (int)(h)): # for each copy
			print '%s: %s of %s' % (method, iterInstances, h)
			angleNew = (float)(angleDelta * iterInstances) # change in angle
			# print '%s: angleNew %s' % (method, angleNew)
			for iterX in xrange(0, width): # loop through X
				deltaX = OFFSET + box.minx + iterX - originX
				for iterZ in xrange(0, depth): # ... and Z
					
					deltaZ = OFFSET + box.minz + iterZ - originZ
					distance = (float)(sqrt(deltaX * deltaX + deltaZ * deltaZ))
					scangle = atan2(deltaZ, deltaX)
					
					
					newX = (float)(cos(angleNew+scangle) * distance) # + OFFSET
					newZ = (float)(sin(angleNew+scangle) * distance) # + OFFSET
					# print '%s: newX %s , newZ %s , scangle %s' % (method, newX, newZ, scangle)
					
					for iterY in xrange(0, height): # ... to loop through each vertical line of blocks.
						level.setBlockAt( (int)(originX + newX), (int)(box.miny + iterY), (int)(originZ + newZ), 
									level.blockAt((int)(box.minx + iterX), (int)(box.miny + iterY), (int)(box.minz + iterZ)))
						level.setBlockDataAt( (int)(originX + newX), (int)(box.miny + iterY), (int)(originZ + newZ), 
									level.blockDataAt((int)(box.minx + iterX), (int)(box.miny + iterY), (int)(box.minz + iterZ)))

	elif method == "Rotatiticulator!":
		# for each block in the selection box, copy to a new location rotated the appropriate amount centred about a local origin which is itself rotated around a global origin
		# number of copies is in the horizontal scale box
		
		originX = 0 # change / parameterise
		originZ = 0 # change / parameterise
		
		SAMPLES = 1		
		STEPSIZE = 1.0 / SAMPLES
		OFFSET = 0.0 # If I need to land each scan within a block.
		
		angleDelta = (float)(pi * 2 / h) # the amount of rotation for the blocks 

		majorDeltaX =  OFFSET + box.minx + width / 2 - originX  # find the centre of the box
		majorDeltaZ =  OFFSET + box.minz + depth / 2 - originZ
		majorDistance = (float)(sqrt(majorDeltaX * majorDeltaX + majorDeltaZ * majorDeltaZ))
		
		startAngle = atan2(majorDeltaZ, majorDeltaX)
		
		for iterInstances in xrange(1, (int)(h)): # for each copy
			
			print '%s: %s of %s' % (method, iterInstances, (int)(h-1))
			
			angleNew = fix((float)(startAngle + angleDelta * iterInstances)) # change in angle +startAngle?

			newMajorX = (float)(cos(angleNew) * majorDistance) + originX # new centre of the box
			newMajorZ = (float)(sin(angleNew) * majorDistance) + originZ
			
			level.setBlockAt( (int)(newMajorX), (int)(box.miny), (int)(newMajorZ), 1) # marker for copied objects.
			
			iterX = (float)(0.0)
			while iterX <= (width * SAMPLES):
				scanX = iterX - width / 2 + OFFSET
				
				iterZ = (float)(0.0)
				while iterZ <= (depth * SAMPLES):
					
					scanZ = iterZ - depth / 2 + OFFSET
					
					distance = (float)(sqrt( scanX * scanX + scanZ * scanZ))
					scangle = fix(atan2(scanZ, scanX))
					
					
					newX = (float)(cos(fix(angleNew-startAngle+scangle)) * distance) # + OFFSET
					newZ = (float)(sin(fix(angleNew-startAngle+scangle)) * distance) # + OFFSET
					# print '%s: newX %s , newZ %s , scangle %s' % (method, newX, newZ, scangle)
					
					for iterY in xrange(0, height): # ... to loop through each vertical line of blocks.

						sourceBlock = level.blockAt((int)(box.minx + iterX), (int)(box.miny + iterY), (int)(box.minz + iterZ))
						sourceBlockData = level.blockDataAt((int)(box.minx + iterX), (int)(box.miny + iterY), (int)(box.minz + iterZ))

						targetBlock = level.blockAt((int)(newMajorX + newX), (int)(box.miny + iterY), (int)(newMajorZ + newZ))
						
						if targetBlock == 0 and sourceBlock != 0:
							level.setBlockAt( (int)(newMajorX + newX), (int)(box.miny + iterY), (int)(newMajorZ + newZ), 
									sourceBlock)
							level.setBlockDataAt( (int)(newMajorX + newX), (int)(box.miny + iterY), (int)(newMajorZ + newZ), 
									sourceBlockData)
					iterZ = iterZ + STEPSIZE
				iterX = iterX + STEPSIZE
	
	
	# Surface functions - i.e, parameterised surfaces

	elif method == "Sea Shell": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
		u = 0
		while u <= 13 * pi:
			v = -pi
			while v <= pi:
				(x2, y2, z2) = seashell(u, v)
				setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+height+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
				v = v + pi/360
			u = u + pi/180
			
	elif method == "Conic Spiral - Nautilus": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = 0
			while u <= 3 * pi:
				v = -pi
				while v <= pi:
					(x2, y2, z2) = conicspiral(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + pi/360
				u = u + pi/180

	elif method == "Conic Spiral - Toroid consuming own tail": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = 0
			while u <= 3 * pi:
				v = -pi
				while v <= pi:
					(x2, y2, z2) = conicspiraleattail(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + pi/360
				u = u + pi/540


	elif method == "Spiral": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = -2*pi
			while u <= 2 * pi:
				v = -pi
				while v <= pi:
					(x2, y2, z2) = spiral(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + pi/360
				u = u + pi/720

	elif method == "Trefoil Knot": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = -2*pi
			while u <= 2 * pi:
				v = -pi
				while v <= pi:
					(x2, y2, z2) = trefoilknot(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + pi/360
				u = u + pi/720

	elif method == "Higher-Order Knot": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = -3*pi
			while u <= 3 * pi:
				v = -pi
				while v <= pi:
					(x2, y2, z2) = higherorderkno(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + pi/360
				u = u + pi/1080

	elif method == "Higher-Order Knot 16": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = -3*pi
			while u <= 3 * pi:
				v = -pi
				while v <= pi:
					(x2, y2, z2) = higherorderkno16(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + pi/360
				u = u + pi/1080

	elif method == "Higher-Order Knot Param": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = -cycles*pi
			
			stepv = pi/360
			stepu = pi/1080
			
			if quick == True:
				stepv = stepv*10
				stepu = stepu*10
			
			colourStep = 0
			theBlock = options["Pick a block:"].ID
			
			while u <= cycles * pi:
				print 'Progress: %s of %s' % (u,cycles*pi)
				v = -pi
				while v <= pi:
					(x2, y2, z2) = higherorderknoParam(u, v, param)
					if COLOURISE == True:
						setBlock(level, (theBlock, coloursList[colourStep%16]) , (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))
					else:
						setBlock(level, block , (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))
					v = v + stepv
				u = u + stepu
				colourStep = colourStep + 1

				
	elif method == "Dini's Surface": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = 0
			while u <= 4 * pi:
				v = 0.001
				while v <= 2:
					(x2, y2, z2) = dinisurface(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+height+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + 0.001
				u = u + pi/720

	elif method == "Moebius Surface": # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
			u = 0
			while u <= 2 * pi:
				v = -0.1
				while v <= 0.1:
					(x2, y2, z2) = moebiussurface(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + 0.005
				u = u + pi/360

	elif method == "Vertical Sheet": # AJB
			u = 0
			while u <= 2.75 * pi:
				v = -pi
				while v <= pi:
					(x2, y2, z2) = verticalsheet(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + pi/360
				u = u + pi/360

	elif method == "Mushroom": # AJB
			u = 0
			while u <= 2.5 * pi:
				v = -pi
				while v <= pi:
					(x2, y2, z2) = mushroom(u, v)
					setBlock(level, block, (int)(box.minx+centrewidth+x2*h), (int)(box.miny+centreheight+y2*scalevert), (int)(box.minz+centredepth+z2*h))		
					v = v + pi/360
				u = u + pi/360


			
	else:
		for x in range(-centrewidth,centrewidth):
			for z in range(-centredepth,centredepth):
				x1 = (float)(x * h)
				z1 = (float)(z * h)

				# Surface functions - y = f(x,z)
				if method == "Wave":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f1(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "Parabola":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f2(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "Hyperbolic Paraboloid":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f3(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "Saddle":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f4(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=x^2*z^2":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f5(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=cos(x)+cos(z)":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f6(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=(cos(x)+cos(z))^5":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f7(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=cos(x^2+z^2)":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f8(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=sin(x^2+z^2)^3":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f9(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=x*z*sin(x)+x*z*sin(z)":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f10(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=tan(x)dividedbyz+tan(z)dividedbyx":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f11(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=sin(x*z)":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f12(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=cos(sqrt(x^2+z^2))":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f13(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=z*tan(x)":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f14(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=x*ln(z^2)":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f15(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=x^2 + z^2 - ln(x*z)":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f16(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "Sombrero":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f17(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "Hyta's function":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f18(x1, z1, scalevert), box.minz+centredepth+z)
				elif method == "y=floor(x*z)":
					setBlock(level, block, box.minx+centrewidth+x, centreheight+f19(x1, z1, scalevert), box.minz+centredepth+z)
					
				# Volume functions - result = f(x,y,z). Plot on result.
				elif method == "Clebsch surface":
					for y in range(-centreheight, centreheight):
						r = clebsch(x1, y * scalevert, z1)
						if r == 0:
							setBlock(level, block, box.minx+centrewidth+x, box.miny+centreheight+y, box.minz+centredepth+z)
				elif method == "(x2 + (9 div 4)y2 + z2 - 1)3 - x2z3 - (9/80)y2z3 = 0":
					for y in range(-centreheight, centreheight):
						r = f20(x1, y * scalevert, z1)
						if r == 0.0:
							setBlock(level, block, box.minx+centrewidth+x, box.miny+centreheight+y, box.minz+centredepth+z)
				elif method == "Cos(x)Sin(y) + Cos(y)Sin(z) + Cos(z)Sin(x) = 0":
					for y in range(-centreheight, centreheight):
						r = f21(x1, y * scalevert, z1)
						# print '%s' % r
						if r == 0.0:
							setBlock(level, block, box.minx+centrewidth+x, box.miny+centreheight+y, box.minz+centredepth+z)

				# Deform function
	
				elif method == "Deform Landscape - Wave":
					y1 = box.maxy
					r = (int)(scalevert*(cos(radians(x1))+sin(radians(z1)))) # How high is the deformation right here?
					if r < 1:
						y1 = box.miny # stop checking if this is a depression
					while y1 > box.miny: # search top down
						if level.blockAt((int)(box.minx+centrewidth+x1),(int)(y1),(int)(box.minz+centreheight+z1)) == 0 and level.blockAt((int)(box.minx+centrewidth+x1), (int)(y1-1), (int)(box.minz+centreheight+z1)) != 0: # found the topmost block
							# time to copy everything up!
							while y1 > box.miny:
								level.setBlockAt((int)(box.minx+centrewidth+x1), (int)(y1+r), (int)(box.minz+centreheight+z1), level.blockAt((int)(box.minx+centrewidth+x1),(int)(y1-1),(int)(box.minz+centreheight+z1)) ) # blit one block up
								level.setBlockDataAt((int)(box.minx+centrewidth+x1),(int)(y1+r),(int)(box.minz+centreheight+z1), level.blockDataAt((int)(box.minx+centrewidth+x1), (int)(y1-1), (int)(box.minz+centreheight+z1)) ) # blit one block up
								y1 = y1 - 1
						y1 = y1 - 1

				elif method == "Deform Landscape - Rama":
					y1 = box.maxy
					r = (int)(scalevert*(-cos(radians(x1)))) # How high is the deformation right here?
					if r < 1:
						y1 = box.miny # stop checking if this is a depression
					while y1 > box.miny: # search top down
						if level.blockAt((int)(box.minx+centrewidth+x1),(int)(y1),(int)(box.minz+centreheight+z1)) == 0 and level.blockAt((int)(box.minx+centrewidth+x1), (int)(y1-1), (int)(box.minz+centreheight+z1)) != 0: # found the topmost block
							# time to copy everything up!
							while y1 > box.miny:
								level.setBlockAt((int)(box.minx+centrewidth+x1), (int)(y1+r), (int)(box.minz+centreheight+z1), level.blockAt((int)(box.minx+centrewidth+x1),(int)(y1-1),(int)(box.minz+centreheight+z1)) ) # blit one block up
								level.setBlockDataAt((int)(box.minx+centrewidth+x1),(int)(y1+r),(int)(box.minz+centreheight+z1), level.blockDataAt((int)(box.minx+centrewidth+x1), (int)(y1-1), (int)(box.minz+centreheight+z1)) ) # blit one block up
								level.setBlockAt((int)(box.minx+centrewidth+x1),(int)(y1-1),(int)(box.minz+centreheight+z1), 0 ) # Destroy the copied block.
								y1 = y1 - 1
						y1 = y1 - 1

				elif method == "Deform Landscape - Rama II":
					y1 = box.maxy
					r = y1+(int)(scalevert*(-cos(radians(x1)))) # How high is the deformation right here?
					
					while y1 > box.miny: # search top down
						if level.blockAt((int)(box.minx+centrewidth+x1),(int)(y1),(int)(box.minz+centreheight+z1)) == 0 and level.blockAt((int)(box.minx+centrewidth+x1), (int)(y1-1), (int)(box.minz+centreheight+z1)) != 0: # found the topmost block
							# time to copy everything up!
							while y1 > box.miny:
								level.setBlockAt((int)(box.minx+centrewidth+x1), (int)(y1+r), (int)(box.minz+centreheight+z1), level.blockAt((int)(box.minx+centrewidth+x1),(int)(y1-1),(int)(box.minz+centreheight+z1)) ) # blit one block up
								level.setBlockDataAt((int)(box.minx+centrewidth+x1),(int)(y1+r),(int)(box.minz+centreheight+z1), level.blockDataAt((int)(box.minx+centrewidth+x1), (int)(y1-1), (int)(box.minz+centreheight+z1)) ) # blit one block up
								level.setBlockAt((int)(box.minx+centrewidth+x1),(int)(y1-1),(int)(box.minz+centreheight+z1), 0 ) # Destroy the copied block.
								y1 = y1 - 1
						y1 = y1 - 1			
				
				
    
  	level.markDirtyBox(box)

def mushroom(u, v):
	return ( (10-u*cos(u))*sin(v), 
	         3*u*sin(u),
	         (10-u*cos(u))*cos(v)
	         )

#	return ( (10-u*cos(u))*sin(v), 
#	         3*u*sin(u),
#	         1
#	         )


#	return ( (10-u*cos(u))*sin(v), 
#	         3*u*sin(u),
#	         (10-u*sin(u))*cos(v)
#	         )


#	return ( (10+u*cos(u))*sin(v), 
#	         3*u*sin(u),
#	         10*cos(v)
#	         )


# Surfboard
#	return ( u*cos(u)*sin(v), 
#	         3*u*sin(u),
#	         cos(v)
#	         )


#	return ( u*cos(u)*sin(v), 
#	         3*u*sin(u),
#	         sin(v)
#	         )


def verticalsheet(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/ [0:13*pi][-pi:pi] u*cos(u)*(cos(v)+1), u*sin(u)*(cos(v)+1), u*sin(v) - ((u+3)/8*pi)**2 - 20
	return ( u*cos(u), 
	         2*u*sin(v),
	         u*sin(u)
	         )

def seashell(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/ [0:13*pi][-pi:pi] u*cos(u)*(cos(v)+1), u*sin(u)*(cos(v)+1), u*sin(v) - ((u+3)/8*pi)**2 - 20
	return ( u*cos(u)*(cos(v)+1), 
	         u*sin(v) - ((u+3)/8*pi)*((u+3)/8*pi) - 20,
	         u*sin(u)*(cos(v)+1)
	         )

def spiral(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( cos(u)*(cos(v)+3), 
	         sin(v)+u,
	         sin(u)*(cos(v)+3)
	         )


def conicspiral(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( u*cos(u)*(cos(v)+1), 
	         u*sin(v),
	         u*sin(u)*(cos(v)+1)
	         )

def conicspiraleattail(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( cos(u)*(u/(3*pi)*cos(v)+2), 
	         u*sin(v)/(3*pi),
	         sin(u)*(u/(3*pi)*cos(v)+2)
	         )



def trefoilknot(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( cos(u)*cos(v)+3*cos(u)*(1.5+sin(1.5*u)/2),
	         sin(v)+2*cos(1.5*u),
	         sin(u)*cos(v)+3*sin(u)*(1.5+sin(1.5*u)/2)
	         )

def higherorderkno(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( cos(u)*cos(v)+3*cos(u)*(1.5+sin(u*5/3)/2), 
	         sin(v)+2*cos(u*5/3),
	         sin(u)*cos(v)+3*sin(u)*(1.5+sin(u*5/3)/2)
	         )

def higherorderkno16(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( cos(u)*cos(v)+3*cos(u)*(1.5+sin(u*16/3)/2), 
	         sin(v)+2*cos(u*16/3),
	         sin(u)*cos(v)+3*sin(u)*(1.5+sin(u*16/3)/2)
	         )

def higherorderknoParam(u, v, param): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( cos(u)*cos(v)+3*cos(u)*(1.5+sin(u*param/3)/2), 
	         sin(v)+2*cos(u*param/3),
	         sin(u)*cos(v)+3*sin(u)*(1.5+sin(u*param/3)/2)
	         )
			 
def dinisurface(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( cos(u)*sin(v), 
	         cos(v)+log(tan(v/2))+0.2*u-4,
	         sin(u)*sin(v)
	         )

def moebiussurface(u, v): # /u/a_contact_juggler  http://soukoreff.com/gnuplot/
	return ( cos(u)+v*cos(u/2)*cos(u), 
	         v*sin(u/2),
	         sin(u)+v*cos(u/2)*sin(u)
	         )


def clebsch(x, y, z): # : /u/fesenjoon  http://redd.it/139d5s  http://imgur.com/a/dujAz
	x2 = x*x
	y2 = y*y
	z2 = z*z
	x3 = x*x*x
	y3 = y*y*y
	z3 = z*z*z

	term1 = x3 + y3 + z3
	term2 = x2 * y + x2 * z + y2 * x + y2 * z + z2 * x + z2 * y
	term3 = x * y + x * z + y * z
	term4 = x2 + y2 + z2
	term5 = x + y + z

	r = 81 * term1 
	r = r - 189 * term2 
	r = r + 54 * x * y * z 
	r = r + 126 * term3 
	r = r - 9 * term4 
	r = r - 9 * term5 + 1

	return (int)(r)

def f21(x, y, z): # : /u/Tbone139  http://www.reddit.com/r/math/comments/139d5s/i_have_been_plotting_surfaces_in_the_3d_space_of/c7294oo
	
	return cos(x)*sin(z)+cos(z)*sin(y)+cos(y)*sin(x)

def f20(x, y, z): # : /u/listix  http://redd.it/139d5s
	
	term1 = (x*x+(9/4)*y*y+z*z-1)
	
	return term1*term1*term1-x*x*z*z*z-(9/80)*y*y*z*z*z


def f19(x, z, v): # : /u/listix  http://redd.it/139d5s
	return (int)(v*floor(x*z))

def f18(x, z, v): # : /u/Hyta
	if x ==0 and z == 0:
		return 0
	return (int)(v*sin(16*x/sqrt(x*x+z*z))+sin(0.5*sqrt(x*x+z*z)))



def f17(x, z, v): # Sombrero function: /u/ConstipatedNinja http://redd.it/139d5s
	if x ==0 and z == 0:
		return 0
		
	return (int)(v*sin(sqrt(x*x+z*z))/sqrt(x*x+z*z))


def f16(x, z, v): # y=x^2 + z^2 - ln(x*z): /u/CrimsonTideAOC http://redd.it/139d5s
	if x*z <= 0:
		return 0
	else:
		return (int)(v*(x*x + z*z - log(x*z)))


def f15(x, z, v): # y=x*ln(z^2): /u/CrimsonTideAOC http://redd.it/139d5s
	if z == 0:
		return 0
	
	return (int)(v*x*log(z*z))


def f14(x, z, v): # y=z*tan(x): /u/ANiceChap http://redd.it/139d5s
	return (int)(v*z*tan(x))


def f13(x, z, v): # y=cos(sqrt(x^2+z^2)): /u/NoCdm http://redd.it/139d5s
	return (int)(v*cos(sqrt(x*x+z*z)))


def f12(x, z, v): # y=sin(x*z): /u/Jon-Targaryen http://redd.it/139d5s
	return (int)(v*sin(x*z))


def f11(x, z, v): # y=tan(x)/z+tan(z)/x: /u/Jon-Targaryen http://redd.it/139d5s
	if z <> 0 and x <> 0:
		return (int)(v*(tan(x)/z+tan(z)/x))
	else:
		return 0

def f10(x, z, v): # y=x*z*sin(x)+x*z*sin(z): /u/Jon-Targaryen http://redd.it/139d5s
	return (int)(v*(x*z*sin(x)+x*z*sin(z)))

def f1(x, z, v): # Wave 1: a slanty arcy surface
	return (int)(v*(cos(radians(x))+sin(radians(z))))
	
def f2(x, z, v): # Parabola 1: a surface with a central depression
	return (int)(v*sqrt(x*x+z*z))
	
def f3(x, z, v): # Hyperbolic Paraboloid
	return (int)(v*(x*x-z*z))
	
def f4(x, z, v): # Saddle
	return (int)(v*(x*z))

def f5(x, z, v): # y=x^2*z^2 . v = 0.00001
	return (int)(v*(x*x*z*z))

def f6(x, z, v): # y=cos(x)+cos(z) . v = 5
	return (int)(v*(cos(x)+cos(z)))

def f7(x, z, v): # y=(cos(x)+cos(z))^5
	t = (cos(x)+cos(z))
	return (int)(v*t*t*t*t*t)

def f8(x, z, v): # y=cos(x^2+z^2)
	return (int)(v*(cos((x)*(x)+(z)*(z))))

def f9(x, z, v): # y=sin(x^2+z^2)^3
	t = sin(x*x+z*z)
	return (int)(v*t*t*t)
	
	
# Utility methods

def setBlock(level, (block, data), x, y, z):
    level.setBlockAt(x, y, z, block)
    level.setBlockDataAt(x, y, z, data)

def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, y):
    	level.setBlockAt(x, iterY, z, block)
    	level.setBlockDataAt(x, iterY, z, data)




def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	
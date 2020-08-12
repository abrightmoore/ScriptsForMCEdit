# @TheWorldFoundry
# Map a selection to a hemisphere - per Cold Fusion Gaming
from random import randint
from math import pi,atan2,sin,cos,sqrt
from pymclevel import alphaMaterials
import PROCGEN_TOOLS
from PROCGEN_TOOLS import getBlock,setBlock,getBlockFromOptions

inputs = (
		("Hemisphere", "label"),
		("Select a plane of material", "label"),
		("Raise the selection to the desired radius", "label"),
		("Fraction of sphere to render",0.5),
		("adrian@TheWorldFoundry.net", "label"),
		("http://TheWorldFoundry.com", "label"),
)


def perform(level, box, options):
	hemisphere(level,box,options)
	level.markDirtyBox(box)
	
def hemisphere(level,box,options):
	''' Plot all the pixels to the surface above the selection, which is a hemisphere
		The lowest layer of the selection is the selection of blocks to be translated into the hemisphere
	'''
	fraction = options["Fraction of sphere to render"]
	radius = float(box.maxy-box.miny)*fraction*2.0 # This is the radius of the hemisphere
	cx = (box.minx+box.maxx)>>1 # Mid point along width of selection
	cz = (box.minz+box.maxz)>>1 # Mid point along depth of selection
	
	# Traverse each layer of the selection
	# If the voxel is in the surface of the hemisphere, find what block it should be

	
	
	y = box.maxy-1
	halfcirc = pi*radius
	while y > box.miny:
		if y % 10 == 0: print y
		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				dx = x-cx
				dz = z-cz
				dy = y-box.miny
				hdistsq = dx**2+dz**2
				if int(radius) == int(sqrt(hdistsq+dy**2)):
					# This block position is on the hemisphere
					# Calculate the distance from the top of the dome around the circumference (longitudinal) and the angle (latitude)
					
					# 2*pi*r = pi*d = circumference
					
					hangle = atan2(dz,dx)
					vangle = atan2(dy,sqrt(hdistsq))
					distratio = (pi/2-vangle)/(fraction*2.0*pi)
					dist = distratio*halfcirc
					#print dist
					# Lookup the block that is at the appropriate angle and distance in the lowest layer
					theBlock = getBlock(level,cx+dist*cos(hangle),box.miny,cz+dist*sin(hangle))
					setBlock(level,x,y,z,theBlock)
				
		y -= 1 # Move down one layer

	print "Done!"
	
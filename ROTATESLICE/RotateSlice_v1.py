# @TheWorldFoundry
# Map a selection to a Cylinder
from random import randint
from math import pi,atan2,sin,cos,sqrt
from pymclevel import alphaMaterials,BoundingBox
import PROCGEN_TOOLS
from PROCGEN_TOOLS import getBlock,setBlock,getBlockFromOptions

inputs = (
		("RotateSlice", "label"),
		("Select a plane of material", "label"),
		("adrian@TheWorldFoundry.com", "label"),
		("http://TheWorldFoundry.com", "label"),
)

def perform(level, box, options):
	rotateslice(level,box,options)
	level.markDirtyBox(box)
	
def rotateslice(level,box,options):
	''' Given a width-wise selection, rotate it 360
	'''
	
	width = (box.maxx-box.minx)<<1
	height = (box.maxy-box.miny)
	depth = width
	
	for y in xrange(box.miny,box.maxy): # Scan the target space
		if y%10: print y
		for z in xrange(box.maxz, box.minz+(width>>1)): # Start one step out from the selection
			for x in xrange(box.minx, box.maxx):
#				if x < box.minx or z != box.minz: # Don't try to map over the source blocks
				dx = x-box.minx # distance from centre
				dz = z-box.minz
				
				rHere = sqrt(dx**2+dz**2)
				
				# Find the block that needs to be mapped in here
				theBlock = getBlock(level,box.minx+int(rHere),y,box.minz)
				if theBlock != (0,0):
					setBlock(level,x,y,z,theBlock) # Quadrant1
					setBlock(level,box.minx-dx,y,z,theBlock) # Quadrant2
					setBlock(level,x,y,box.minz-dz,theBlock) # Quadrant3
					setBlock(level,box.minx-dx,y,box.minz-dz,theBlock) # Quadrant4
		z= box.minz
		for x in xrange(box.minx, box.maxx):
			theBlock = getBlock(level,x,y,z)
			if theBlock != (0,0):
				setBlock(level,box.minx-(x-box.minx),y,z,theBlock) # Quadrant1
			
	level.markDirtyBox(BoundingBox((box.minx-(width>>1),box.miny,box.minz-(width>>1)),(width,height,width)))
	print "Done!"
	
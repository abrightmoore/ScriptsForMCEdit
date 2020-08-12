# @TheWorldFoundry
import numpy as np
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
 
def perform(level, box, options):
	dumpChunk(level, box, options)
		
def dumpChunk(level, box, options):

	for (chunk, _, _) in level.getChunkSlices(box):
		print "Entities:"
		for e in chunk.Entities:
			print e
		print "TileEntities:"
		for e in chunk.TileEntities:
			print e["x"],e["y"],e["z"],e["Command"]

					
		
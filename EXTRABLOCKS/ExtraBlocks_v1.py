# @TheWorldFoundry
import numpy as np
from pymclevel import alphaMaterials

inputs = (
		("EXTRABLOCKS", "label"),
		("Block:", alphaMaterials.Water),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

def perform(level, box, options):
	fullChunkExtraBlocks(level,box,options)

def fullChunkExtraBlocks(level,box,options):
	materialID = options["Block:"].ID
	materialData = options["Block:"].blockData
	for (chunk, _, _) in level.getChunkSlices(box):
		for subchunk in xrange(0,16):
			for layer in xrange(0,16):
				for block in xrange(0,256):
					chunk.extra_blocks[subchunk][layer][block] = materialID
					chunk.extra_blocks_data[subchunk][layer][block] = materialData
		chunk.dirty = True
	print "Done!"
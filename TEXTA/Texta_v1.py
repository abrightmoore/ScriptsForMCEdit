# @TheWorldFoundry
# Set all the text tags within the selection box to be the supplied file content
# Use for Minecraft Education Edition Slate.
# Suggested by Timur

import os
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long

inputs = (
		("TEXTA", "label"),
		("Set the Text tag in the selection", "label"),
		("to be the content of the file", "label"),
		("File path", ("string","value=")),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

def perform(level, box, options):
	# Read in the supplied text from the nominated file
	filename = options["File path"]
	text = loadTextFromFile(filename)
	
	for (chunk, _, _) in level.getChunkSlices(box):
		print "TileEntities:"
		for e in chunk.TileEntities:
			print e
			#if e["id"].value == "ChalkboardBlock":
			if "Text" in e:
				e["Text"] = TAG_String(text)	
				chunk.dirty = True
	
	
def loadTextFromFile(filename):
	f = open(filename, 'r+')
	text = f.read()
	f.close()
	return text

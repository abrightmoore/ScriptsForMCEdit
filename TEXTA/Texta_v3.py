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
		("Tag to replace", ("string","value=Text")),
		("Tag type", ("TAG_String", "TAG_Byte", "TAG_Int", "TAG_Short", "TAG_Long", "TAG_Float", "TAG_Double" )),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

def perform(level, box, options):
	# Read in the supplied text from the nominated file
	filename = options["File path"]
	text = loadTextFromFile(filename)
	tagName = options["Tag to replace"]
	tagType = options["Tag type"]
	
	for (chunk, _, _) in level.getChunkSlices(box):
		print "TileEntities:"
		for e in chunk.TileEntities:
			print e
			#if e["id"].value == "ChalkboardBlock":
			if tagName in e:
				if tagType == "TAG_String" and type(e[tagName]) is TAG_String:
					e[tagName] = TAG_String(text)
					chunk.dirty = True
				elif tagType == "TAG_Byte" and type(e[tagName]) is TAG_Byte:
					e[tagName] = TAG_Byte(int(text))
					chunk.dirty = True
				elif tagType == "TAG_Int" and type(e[tagName]) is TAG_Int:
					e[tagName] = TAG_Int(int(text))
					chunk.dirty = True
				elif tagType == "TAG_Short" and type(e[tagName]) is TAG_Short:
					e[tagName] = TAG_Short(int(text))
					chunk.dirty = True
				elif tagType == "TAG_Long" and type(e[tagName]) is TAG_Long:
					e[tagName] = TAG_Long(int(text))
					chunk.dirty = True
				elif tagType == "TAG_Float" and type(e[tagName]) is TAG_Float:
					e[tagName] = TAG_Float(float(text))
					chunk.dirty = True
				elif tagType == "TAG_Double" and type(e[tagName]) is TAG_Double:
					e[tagName] = TAG_Double(float(text))
					chunk.dirty = True
				else:
					print "Tag",tagName,"of type",tagType,"is a",type(e[tagName])

	
	
def loadTextFromFile(filename):
	f = open(filename, 'r+')
	text = f.read()
	f.close()
	return text

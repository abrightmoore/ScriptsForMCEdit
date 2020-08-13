# This filter is for Onnowhere's awesome machine
# abrightmoore@yahoo.com.au
# http://brightmoore.net

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0
import inspect # @Texelelf
from PIL import Image
import png

# GLOBAL
CHUNKSIZE = 16

ALPHABET = [
	[35,0," "],
	[35,1,"A"],
	[35,2,"B"],
	[35,3,"C"],
	[35,4,"D"],
	[35,5,"E"],
	[35,6,"F"],
	[35,7,"G"],
	[35,8,"H"],
	[35,9,"I"],
	[35,10,"J"],
	[35,11,"K"],
	[35,12,"L"],
	[35,13,"M"],
	[35,14,"N"],
	[35,15,"O"],
	[159,0,"P"],
	[159,1,"Q"],
	[159,2,"R"],
	[159,3,"S"],
	[159,4,"T"],
	[159,5,"U"],
	[159,6,"V"],
	[159,7,"W"],
	[159,8,"X"],
	[159,9,"Y"],
	[159,10,"Z"],
	[159,11,","],
	[159,12,"'"],
	[159,13,"."],
	[159,14,"!"],
	[159,15,"?"],
	[7,0,""]
	]

inputs = (
		("ALBERT HELPER", "label"),
		("Operation", (
			"Read","Write"
  		    )),
		("File name:", ("string","value=Chat")),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
		)


def perform(level, box, options):
	if options["Operation"] == "Read":
		chat = Read(level,box,options)
		file = open(options["File name:"]+".txt","w")
		for line in chat:
			file.write(line)
			file.write("\n")
		file.close()
	if options["Operation"] == "Write":
		with open(options["File name:"]+".txt","r") as file:
			chat = file.readlines()
			Write(level,box,options,chat)
			file.close()
			
def Write(level, box, options,chat):
	
	index = 0
	for y in xrange(box.miny,box.maxy):
		for x in xrange(box.minx,box.maxx):
			line = chat[index]
			i = 0
			for z in xrange(box.minz,box.maxz):
				if i < len(line)-1:
					char = line[i]
					i += 1
					for (b,d,c) in ALPHABET:
						if c == char:
							setBlock(level, (b,d), x,y,z)
				else:
					setBlock(level, (7,0), x,y,z)
			index += 1

			
def Read(level, box, options):
	chat = []
	print '------------------------------------------'
	for y in xrange(box.miny,box.maxy):
		for x in xrange(box.minx,box.maxx):
			msg = ''
			for z in xrange(box.minz,box.maxz):
				(theBlock,theData) = getBlock(level,x,y,z)
				for (b,d,c) in ALPHABET:
					if theBlock == b and theData == d:
							msg = msg+c
			print msg
			chat.append(msg)
	print '------------------------------------------'
	return chat







#				text = ""
#				chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
#		
#				for t in chunka.TileEntities:
#					x1 = t["x"].value
#					y1 = t["y"].value
#					z1 = t["z"].value
#					# print t["id"].value
#					#print t
#					if x == x1 and y == y1-1 and z == z1 and t["id"].value == "Sign":
#						text = t["Text1"].value #.split()
#						#text = text1["text"]
#
#				print '[%s,%s,"%s"],' % (theBlock,theData,text)	
						

				
				
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))
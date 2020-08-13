# This filter identifies which Command Blocks target which cells in the world, relabels the co-ordinates with a sign holding an Alias.
# Then, after things are moved around, the filter will re-calculate the target block co-ordinates (replacing the Alias).
# Suggested by Jigarbov
# This filter: abrightmoore@yahoo.com.au (http://brightmoore.net)
# This filter builds on the prior work of: @texelelf


import time # for timing
import re # for Regular Expressions per http://stackoverflow.com/questions/5319922/python-check-if-word-is-in-a-string
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf


# These imports by @SethBling (http://youtube.com/SethBling)
from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Float
from pymclevel import TAG_Double
from pymclevel import TAG_String

inputs = (
	  ("AAA_LINKCHECKER", "label"),
	  # ("Command", ("setblock","testforblock","summon")),
	  ("Alias Prefix:", ("string","value=AJBLBL_")),
	  ("Alias Suffix:", 1000000),
	  ("Overwrite target blocks?", False),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
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

def createCmdBlock(level, x, y, z, command): #abrightmoore - convenience method.
	COMMANDBLOCK = 137
	CHUNKSIZE = 16

	level.setBlockAt(x, y, z, COMMANDBLOCK)
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command)
	control["SuccessCount"] = TAG_Int(0)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	chunka.TileEntities.append(control)
	chunka.dirty = True
	
def createSign(level, x, y, z, text): #abrightmoore - convenience method.
	COMMANDBLOCK = 137
	CHUNKSIZE = 16
	STANDING_SIGN = 63
	
	setBlock(level, (STANDING_SIGN,8), x, y, z)
	control = TAG_Compound()
	control["id"] = TAG_String("Sign")
	control["Text1"] = TAG_String(text[0])
	control["Text2"] = TAG_String(text[1])
	control["Text3"] = TAG_String(text[2])
	control["Text4"] = TAG_String(text[3])
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	chunka.TileEntities.append(control)
	chunka.dirty = True

def appendToSign(level, x, y, z, text): # I want to collapse the sign access later
	CHUNKSIZE = 16
	
	chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
	for t in chunka.TileEntities:
		x1 = t["x"].value
		y1 = t["y"].value
		z1 = t["z"].value
		if x == x1 and y == y1 and z == z1 and t["id"].value == "Sign": # Update this command block
			print 'Updating text %s %s %s with %s' % (x1,y1,z1,text)
			if t["Text1"].value == '':
				t["Text1"].value = text
			elif t["Text2"].value == '':
				t["Text2"].value = text
			elif t["Text3"].value == '':
				t["Text3"].value = text
			elif t["Text4"].value == '':
				t["Text4"].value = text
			else: # Error
				print 'WARNING: Unable to add an alias to a sign at %s %s %s. No free slots? Please review.' % ((int)(x), (int)(y), (int)(z))
			chunka.dirty = True
			return True # Success
	return False # Fail
	
def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	LinkChecker(level, box, options)		
	level.markDirtyBox(box)
	
def LinkChecker(level, box, options):
	method = "LINKCHECKER"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	CBCOMMAND = "setblock"
	CBCOMMAND2 = "testforblock"
	ALIASPREFIX = options["Alias Prefix:"]
	ALIASSUFFIX = options["Alias Suffix:"]
	OVERWRITE = options["Overwrite target blocks?"]
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	SPONGE = (19,0)
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16
	STANDING_SIGN = 63
	# Process all the qualifying Command Blocks
	
	# First scan, it's either a cmd block with an alias asigned or not.
	# Sign block 63 - freestanding, or 68 Wall
	
	
	# Pseudocode
	# Search through space. If I find:
	# 1. A command block with the command of interest and co-ordinates then: # DONE
	#    Check the block at the co-ordinates is air #DONE
	#	 	Place a standing sign with a new Alias.  # DONE
	#		Add this sign to a list because we don't want to resolve it back to co-ordinates if we find it later. # DONE
	#		Replace the command block command with the alias # DONE
	#		Continue hunting #DONE
	#	 If it isn't air and is a sign then or overwrite is enabled  #DONE
	#		Add another Alias row unless there's no room then sound the alarm (check the console) - we're not in Kansas any more and manual intervention is required.
	#    If it isn't air then:
	#		Optionally sound the alarm
	# 2. A command block with the command of interest and an alias then: # DONE
	#	 This needs to be resolved back to the co-ordinates of a corresponding sign. Add it to a list for later processing. Scan needs to finish #DONE
	# 3. A sign with an Alias on it: #DONE
	#	 Was this sign created in this run of the filter? If it was, do nothing. #MAY NOT BE REQUIRED
	#	 This needs to be resolved back to the command block that references it. Add it to a list for later processing. Scan needs to finish #DONE
	#		
	
	signNewQueue = []	# To be ignored
	cmdBlockAliasQueue = [] # To be resolved back to co-ordinates
	signAliasQueue = [] # To provide the co-ordinates for the cmdBlocks on the cmdBlockAliasQueue
	aliasSuffix = ALIASSUFFIX # One meelion alias's.
	
	for (chunk, slices, point) in level.getChunkSlices(box): # @Texelelf
		
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if t["id"].value == "Control":
					command = t["Command"].value # convenience
					print("Command At: " +str(x)+"(x)"+" "+str(y)+"(y)"+" "+str(z)+ "(z)" + " " +"is: " + command) # @wiresegal, @TheDestruc7i0n
					#if re.compile(r'\b({0})\b'.format(CBCOMMAND), flags=re.IGNORECASE).search == True or re.compile(r'\b({0})\b'.format("/"+CBCOMMAND), flags=re.IGNORECASE).search == True:  # Handle slash format
					if command.find(CBCOMMAND) != -1 or command.find(CBCOMMAND2) != -1: # after @Texelelf
						print 'Found the command %s' % (CBCOMMAND+' or '+CBCOMMAND2)
						#ignore minecraft:air. These are probably not of interest as they simply toggle/clear
						if True: # command.find("minecraft:air") == -1: # @Texelelf
							#if re.compile(r'\b({0})\b'.format(ALIASPREFIX), flags=re.IGNORECASE).search == False:   # Check for Alias. No alias? It's co-ordinates
							if command.find(ALIASPREFIX) == -1: # @Texelelf
								# Mojang have the format setblock <x> <y> <z> and it's split by single spaces
								print 'Co-ordinates'
								cmdParts = command.split() # http://stackoverflow.com/questions/8113782/split-string-on-whitespace-in-python
								thisAlias = ALIASPREFIX + str(aliasSuffix) # Convenience
								aliasSuffix = aliasSuffix + 1 # prepare for the next one
								newCmd = cmdParts[0] + ' ' + thisAlias # Temporary
								for i in xrange(4,len(cmdParts)): # skip the co-ordinates. They are an Alias now!
									newCmd = newCmd + ' ' + cmdParts[i]

								# Make relative absolute
								if cmdParts[1][0] == '~':
									#print 'Tilda 1'
									tempVal = cmdParts[1][1:]
									if tempVal == '':
										tempVal = '0'
									#print '%s' % (tempVal)
									cmdParts[1] = str(float(tempVal)+x)
								if cmdParts[2][0] == '~':
									#print 'Tilda 2'
									tempVal = cmdParts[2][1:]
									if tempVal == '':
										tempVal = '0'
									cmdParts[2] = str(float(tempVal)+y)
								if cmdParts[3][0] == '~':
									#print 'Tilda 3'
									tempVal = cmdParts[3][1:]
									if tempVal == '':
										tempVal = '0'
									cmdParts[3] = str(float(tempVal)+z)
									
								tx = float(cmdParts[1]) # Convenience - need to handle relative?
								ty = float(cmdParts[2]) # Convenience - need to handle relative?
								tz = float(cmdParts[3]) # Convenience - need to handle relative?
								
								destBlock = (level.blockAt( (int)(tx), (int)(ty), (int)(tz) ),level.blockDataAt( (int)(tx), (int)(ty), (int)(tz)))
								if destBlock == AIR or (destBlock != AIR and OVERWRITE == True and destBlock != (STANDING_SIGN,8)): # OK to create a sign marker and update the command block
									text = []
									# text.append('(LINKCHECKER)')
									# text.append('CB: '+str((int)(x))+' '+str((int)(y))+' '+str((int)(z))) # Original CMD Block
									# text.append('TG: '+str((int)(tx))+' '+str((int)(ty))+' '+str((int)(tz))) # Original marker location
									text.append(thisAlias) # Marker
									text.append('') # stubby
									text.append('') # stubby
									text.append('') # stubby
									createSign(level, (int)(tx), (int)(ty), (int)(tz), text)
									blob = (thisAlias, (int)(tx), (int)(ty), (int)(tz)) # save for later - this is an ignore list
									signNewQueue.append(blob) # save for later - this is an ignore list
									t["Command"].value = newCmd
									chunk.dirty = True
								elif destBlock == (STANDING_SIGN,8):
									# We found a sign that has (probably) already been generated, so I need to append this current alias to it. If there's no room, alarm! (to the console. Manual intervention required.
									print 'Appending %s to existing sign at %s %s %s' % (thisAlias,(int)(tx), (int)(ty), (int)(tz))
									s = appendToSign(level, (int)(tx), (int)(ty), (int)(tz), thisAlias)
									if s == False:
										print 'WARNING: Unable to append and Alias to the sign at %s %s %s. We may be out of sync. Please review.' % ((int)(tx), (int)(ty), (int)(tz))
									else:
										t["Command"].value = newCmd
										chunk.dirty = True
								else:
									print 'WARNING: Unable to create a marker at %s %s %s. Is it air? Please review.' % ((int)(tx), (int)(ty), (int)(tz))
							else: # We found an alias Command Block
								# Add this CB to a scan list of CB labels and locations
								cmdParts = command.split()
								blob = (cmdParts[1],x,y,z,command) # key off the alias
								cmdBlockAliasQueue.append(blob) # This should be a dictionary to improve performance later
				elif t["id"].value == "Sign":
					text = []
					text.append(t["Text1"].value)
					text.append(t["Text2"].value)
					text.append(t["Text3"].value)
					text.append(t["Text4"].value)
					for Text4 in text:
						print 'Found a sign with alias %s %s %s %s' % (Text4,x,y,z)
						if Text4.find(ALIASPREFIX) != -1: # Just a normal sign, ignore
						# This is an alias sign. Ignore if this is newly created.
							found = False
							for (alias, x, y, z) in signNewQueue: # Do this as a dictionary for speed
								if Text4 == alias:
									found = True
							if found == False:
								blob = (Text4,x,y,z)
								signAliasQueue.append(blob)
	
	# if this was the first run, we are done. All references are now to aliases.
	# If this is a second run we now have a scan list of all the signs with aliases and command blocks with aliases and replace the command block alias with the corresponding sign coords. Kapische?
	
	for (SignAlias, x, y, z) in signAliasQueue:
		print 'Checking Sign %s %s %s %s' % (SignAlias,x,y,z)
		# Find a corresponding Command Block
		for (CmdAlias, xc, yc, zc, cmd) in cmdBlockAliasQueue:
			if SignAlias == CmdAlias: # We have a match
				print 'Found a matching Alias pair %s' % (SignAlias)
				# Replace the Alias in the Cmd with the Sign co-ordinates x,y,z
				cmdParts = cmd.split()
				newCmd = cmdParts[0]
				newCmd = newCmd + ' ' + str(x) + ' ' + str(y) + ' ' + str(z)
				for i in xrange(2,len(cmdParts)): # skip the co-ordinates. They are an Alias now!
					newCmd = newCmd + ' ' + cmdParts[i]
					
				chunka = level.getChunk((int)(xc/CHUNKSIZE), (int)(zc/CHUNKSIZE))
				for t in chunka.TileEntities:
					x1 = t["x"].value
					y1 = t["y"].value
					z1 = t["z"].value
					if xc == x1 and yc == y1 and zc == z1 and t["id"].value == "Control": # Update this command block
						print 'Updating Command %s %s %s Block to %s' % (x1,y1,z1,newCmd)
						t["Command"].value = newCmd
						chunka.dirty = True
						setBlock(level, AIR, int(x), int(y), int(z)) # Purge the sign
						
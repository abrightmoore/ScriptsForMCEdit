# coding=UTF-8
# @TheWorldFoundry
# via @Jigarbov

from pymclevel import TAG_Long,TAG_String
import sys
reload(sys)
sys.setdefaultencoding('utf8')

inputs = (
	("TRANSLATABLE", "label"),
	("Input Language File",("string","value=RP\\texts\\en_US.lang")),
	("Output Language File",("string","value=RP\\texts\\en_US_translate.lang")),
	("Namespace",("string","value=jig.mymap")),
	("adrian@TheWorldFoundry.com", "label"),
	("http://TheWorldFoundry.com", "label"),
)

def handleBookPages(e,t,namespace,lines,slot):
	namespace_obj = "book"
	sep = "_"

	posx = e["x"].value
	posy = e["y"].value
	posz = e["z"].value
	
	p = t["pages"]
	counter = 0
	for p1 in p:
		# print "Iterating on",p1
		if "photoname" in p1:
			print "photoname found"
			#p1["photoname"] = TAG_String("Map_-8589934582")
			#print "Updated"
		if "text" in p1:
			print "Text found:",p1["text"]
			text = p1["text"].value
			if text != "":
				if "\"translate\"" not in text: # If this is already calling out to a translatable component, ignore it
					counter += 1
					key = namespace + "." + namespace_obj +sep+ str(posx) +sep+ str(posy) +sep+ str(posz)+sep+"slot_"+str(slot)+".page"+str(counter)
					
					values = text.split("\n")
					counterLine = 0 # Start at 1 because... simpler for map maker readability
					newText = "{\"rawtext\": [ " # This is the text to replace on the sign. We build it now
					found = False
					for v in values:
						counterLine += 1
						if v != "":
							found = True
							newKey = key+"."+"line"+str(counterLine)
							lines.append(newKey+"="+v) # Add this new key to the language file copy in memory
							if counterLine > 1 and counterLine <= len(values):
								newText = newText+",{\"text\":\"\n\"},"
							newText = newText + "{\"translate\":\""+newKey+"\"}"
					newText = newText + " ]}" # Close it out
					
					if found == True:
						print newText
						p1["text"] = TAG_String(newText)
				else:
					print "Ignored the "+namespace_obj+" because it is already referring to a translation: "+text
					print "Note that the word TRANSLATE can confuse me if it is not a translation"
			else:
				print "Ignored the "+namespace_obj+" because it has no text and is probably cosmetic."


def handleCommand(e,namespace,lines):
	namespace_obj = "command"
	sep = "_"

	posx = e["x"].value
	posy = e["y"].value
	posz = e["z"].value
	text = e["Command"].value
	if "\"translate\"" not in text: # If this is already calling out to a translatable component, ignore it
		key = namespace + "." + namespace_obj +sep+ str(posx) +sep+ str(posy) +sep+ str(posz)
		found = False
		for l in lines:
			if key in l:
				found = True
		if found == False:
			posn = text.find("say")
			if posn >= 0:
				customname = e["CustomName"].value
				v = text[(posn+4):] # Tail past the say part
				if customname != "":
					v = "["+customname+"] "+v
				newText = "tellraw @a {\"rawtext\": [ {\"translate\":\""+key+"\"}]}" # This is the text to replace on the command. We build it now
				lines.append(key+"="+v) # Add this new key to the language file copy in memory
				print newText
				e["Command"] = TAG_String(newText)
			else:
				posn = text.find(" title") # Looking for the SECOND title
				if posn >= 0:
					v = text[(posn+7):] # Tail past the title part
					spaceposn = text.find(" ")
					newText = "titleraw"+text[spaceposn:(posn+7)]+"{\"rawtext\": [ {\"translate\":\""+key+"\"}]}" # This is the text to replace on the command. We build it now
					lines.append(key+"="+v) # Add this new key to the language file copy in memory
					print newText
					e["Command"] = TAG_String(newText)
				
		else:
			print "Ignored the "+namespace_obj+" because it is already referring to a translation in the language file: "+key
	else:
		print "Ignored the "+namespace_obj+" because it is already referring to a translation: "+text
		print "Note that the word TRANSLATE can confuse me if it is not a translation"


def handleSign(e,namespace,lines):
	namespace_obj = "sign"
	sep = "_"

	posx = e["x"].value
	posy = e["y"].value
	posz = e["z"].value
	text = e["Text"].value
	if text != "":	
		if "\"translate\"" not in text: # If this is already calling out to a translatable component, ignore it
			key = namespace + "." + namespace_obj +sep+ str(posx) +sep+ str(posy) +sep+ str(posz)
			found = False
			for l in lines:
				if key in l:
					found = True
			if found == False:
				# Split it on new lines
				values = text.split("\n")
				counter = 0 # Start at 1 because... simpler for map maker readability
				newText = "{\"rawtext\": [ " # This is the text to replace on the sign. We build it now
				if len(values) < 4: # Add dummy lines if there are less than 4 lines on this sign
					for i in xrange(0,4-len(values)):
						values.append("") # Force a line
				found = False
				for v in values:
					counter += 1				
					if v != "":
						found = True
						newKey = key+"."+"line"+str(counter)
						lines.append(newKey+"="+v) # Add this new key to the language file copy in memory
						if counter > 1 and counter <= len(values):
							newText = newText+",{\"text\":\"\n\"},"
						newText = newText + "{\"translate\":\""+newKey+"\"}"
				newText = newText + " ]}" # Close it out
				if found == True:
					print newText
					e["Text"] = TAG_String(newText)
			else:
				print "Ignored the "+namespace_obj+" because it is already referring to a translation in the language file: "+key
		else:
			print "Ignored the "+namespace_obj+" because it is already referring to a translation: "+text
			print "Note that the word TRANSLATE can confuse me if it is not a translation"

def addStringToFile(filename,theString):
	theFile = open(filename, 'a+')
	theFile.write(str(theString))
	theFile.close()
		
def loadLinesFromFile(fileName):
	fileOfStatements = open(fileName, 'r+')
	lines = fileOfStatements.read().split("\n")
	fileOfStatements.close()
	return lines
	
def perform(level,box,options):
#	dumpNBT(level,box,options)
	
	index = 0
	# Read in the current file to work out where we're up to
	
	SIGNS = []
	
	BOOKS = []
	namespace_book = "book"
	COMMANDS = []
	namespace_command = "command"
	
	# Read and parse the current lang file.
	lines = loadLinesFromFile(options["Input Language File"])
	print lines
	namespace_global = options["Namespace"]
	
	# Find all the candidate objects within the selection box
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			# print e
			if "Command" in e: # Command block
				print "Command block at "+str(e["x"].value)+","+str(e["y"].value)+","+str(e["z"].value)
				print e["Command"]
				posx = e["x"].value
				posy = e["y"].value
				posz = e["z"].value
				if (posx,posy,posz) in box.positions: # Make sure the tile is within the selection box
					handleCommand(e,namespace_global,lines)
				
				
				
			if "Items" in e: # Container - is there a book?
				print "found a container with Items"
				for i in e["Items"]:
					print "Checking",i
					if "Name" in i:
						print "found a name, checking if it is a book",i["Name"].value
						if i["Name"].value == "minecraft:writable_book" or i["Name"].value == "minecraft:book":
							print "It is a book!"
							slot = -1
							if "Slot" in i:
								slot = i["Slot"].value
							if "tag" in i:
								print "tag found"
								t = i["tag"]
								if "pages" in t:
									print "pages found"
									posx = e["x"].value
									posy = e["y"].value
									posz = e["z"].value
									if (posx,posy,posz) in box.positions: # Make sure the tile is within the selection box
										handleBookPages(e,t,namespace_global,lines,slot)
								
			if "Text" in e: # Sign?
				print "Sign at "+str(e["x"].value)+","+str(e["y"].value)+","+str(e["z"].value)
				print e["Text"]
				posx = e["x"].value
				posy = e["y"].value
				posz = e["z"].value
				if (posx,posy,posz) in box.positions: # Make sure the tile is within the selection box
					handleSign(e,namespace_global,lines)
			
	print "Result:"
	print lines
	print "Writing output file!"
	outFilename = options["Output Language File"]
	counter = 0
	for l in lines:
		counter += 1
		if l != "" and l != "\n":
			if counter < len(lines):
				l = l+"\n"
			addStringToFile(outFilename,l)
		
	# For each object, invoke a parser that understands the NBT of that object and parse the translatable components
	
	level.markDirtyBox(box)	

	

def dumpNBT(level,box,options):
	for (chunk, _, _) in level.getChunkSlices(box):
		print dir(chunk)
		print "Entities:"
		for e in chunk.Entities:
			print e
		print "TileEntities:"
		for e in chunk.TileEntities:
			print e	
	

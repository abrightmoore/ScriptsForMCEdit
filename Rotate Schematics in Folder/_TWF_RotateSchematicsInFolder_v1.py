# @TheWorldFoundry
# Rotate all the schematics in the folders
from numpy import zeros
from random import randint
from os import listdir
from os.path import isfile, join
import glob
import pygame
from pymclevel import alphaMaterials,MCSchematic,BoundingBox
import PROCGEN_TOOLS

inputs = (
		("ROTATE SCHEMATICS", "label"),
		("Folder",("string","temp")),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
		)
def perform(level, box, options):
	rotateSchematicsInFolder(options["Folder"])

def rotateSchematicsInFolder(folder):
	# Get files in folder
	# Read schematic

	SCHEMATICS = PROCGEN_TOOLS.loadSchematicsFromDirectory(folder) # tuple of schematic and name
	print "Read",len(SCHEMATICS),"Schematics."

	# Rotate and save	

	for (schema,fn) in SCHEMATICS:
		print "Rotating",fn
		schema.rotateLeft()
		schema.saveToFile(fn+"_1")
		schema.rotateLeft()
		schema.saveToFile(fn+"_2")
		schema.rotateLeft()
		schema.saveToFile(fn+"_3")
		schema.rotateLeft()
		schema.saveToFile(fn+"_4")
		
	print "Schematic rotation complete"
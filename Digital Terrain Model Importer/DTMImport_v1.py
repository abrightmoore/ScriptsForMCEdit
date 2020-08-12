# DTM import

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from random import * # @Codewarrior0

import csv

inputs = (
	("DTM Import", "label"),
	("Material Top", alphaMaterials.Grass),	
	("Material Soil", alphaMaterials.Dirt),	
	("Material Ground", alphaMaterials.Stone),
	("Depth Soil", 3),
	("Depth Base", 0),
	("Scale Vert", 1.0),
	("DTM ASC File", ("string","value=")),
)

def perform(level,box,options):
	# Questions/comments - abrightmoore@yahoo.com.au
	doDTM(level,box,options)
	print "Marking changes..."
	level.markDirtyBox(box)	
	print "Finished!"
	
def doDTM(level,box,options):
	print "Reading file..."
	P = DTMImport(options)
	print "Placing blocks..."
	renderHeightMap(level,box,options,P)

def renderHeightMap(level,box,options,P):
	Pw,Ph = P.shape
	
	MAT_TOP = getBlockFromOptions(options, "Material Top" )
	MAT_SOIL = getBlockFromOptions(options, "Material Soil" )
	MAT_GROUND = getBlockFromOptions(options, "Material Ground" )
	DEPTHBASE = int(options["Depth Base"])
	DEPTHSOIL = int(options["Depth Soil"])
	SCALEVERT = float(options["Scale Vert"])
	
	readCursorRow = 0

	for writeCursorRow in xrange(box.minz, box.maxz):
		if writeCursorRow%10 == 0:
			print writeCursorRow-box.minz
		if writeCursorRow - box.minz < Ph: # Don't go past the row limit in source data
			readCursorCol = 0
			for writeCursorCol in xrange(box.minx, box.maxx):
				if writeCursorCol - box.minx < Pw: # Don't go past the column limit in source data
					heightHere = box.miny+int(SCALEVERT*P[readCursorRow][readCursorCol])+DEPTHBASE
					#if writeCursorCol%100 == 0:
					#	print heightHere
					for y in xrange(box.miny,heightHere):
						if y < heightHere-DEPTHSOIL:
							setBlockForced(level,MAT_GROUND,writeCursorCol,y,writeCursorRow)
						elif y < heightHere-1:
							setBlockForced(level,MAT_SOIL,writeCursorCol,y,writeCursorRow)
						else:
							setBlockForced(level,MAT_TOP,writeCursorCol,y,writeCursorRow)
				readCursorCol += 1
		readCursorRow += 1
	
def DTMImport(options):
	filename = options["DTM ASC File"]
	filename = filename.strip()
	if filename == "":
		filename = askOpenFile("Select a Top image...", False)	

	reader = csv.reader(open(filename), delimiter=" ")

	count = 1000000
	ncols = 1000
	nrows = 1000
	xllcorner = 0
	yllcorner = 0
	cellsize = 1
	NODATA_value = -9999
	P = zeros((ncols,nrows)) # Stub
	posCol = 0
	posRow = 0
	MIN = 99999999999999
	MAX = -MIN
	for row in reader:
		# print posRow
		if len(row) > 0:
			if row[0] == "ncols":
				ncols = int(row[len(row)-1])
				P = zeros((ncols,nrows)) # Resize
				posCol = 0
				posRow = 0
				print "Number of columns found as "+str(ncols)+" and map resized"
			elif row[0] == "nrows":
				nrows = int(row[len(row)-1])
				P = zeros((ncols,nrows)) # Resize
				posCol = 0
				posRow = 0
				print "Number of rows found as "+str(nrows)+" and map resized"
			elif row[0] == "xllcorner":
				xllcorner = int(row[len(row)-1])			
				print "xllcorner found as "+str(xllcorner)
			elif row[0] == "yllcorner":
				yllcorner = int(row[len(row)-1])
				print "yllcorner found as "+str(yllcorner)
			elif row[0] == "cellsize":
				cellsize = int(row[len(row)-1])
				print "Cell size found as "+str(cellsize)
			elif row[0] == "NODATA_value":
				NODATA_value = float(row[len(row)-1])
				print "NoData marker found as "+str(NODATA_value)				
			elif len(row) == ncols: # Data set, append
				for posCol in xrange(0,len(row)): # Copy data
					if P[posRow][posCol] != NODATA_value:
						P[posRow][posCol] = float(row[posCol])
						if float(row[posCol]) < MIN:
							MIN = float(row[posCol])
						if float(row[posCol]) > MAX:
							MAX = float(row[posCol])
				posRow += 1
			
		count = count-1
		if count == 0:
			break
	print "Min = "+str(MIN)+", Max = "+str(MAX)
	return P

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

def setBlock(level, (block, data), x, y, z):
	if getBlock(level, x,y,z) == (0,0): # AIR
		level.setBlockAt(int(x), int(y), int(z), block)
		level.setBlockDataAt(int(x), int(y), int(z), data)

def setBlockForced(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)
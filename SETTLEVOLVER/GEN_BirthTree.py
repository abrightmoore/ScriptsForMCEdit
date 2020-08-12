# @TheWorldFoundry

import Settlevolver_v1 as Settlevolver
from pymclevel import BoundingBox

from random import randint, random

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	print "Building a",generatorName,"at", box," by ",str(agent)
	cx = (box.minx+box.maxx)>>1
	cz = (box.minz+box.maxz)>>1
	
	Settlevolver.createBirthTree(level, box, cx, box.miny, cz, agent)
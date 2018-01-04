###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Assigns information for each level
# 
###############################################################################
import spec
import ai
import astar
import generateMaze
import drawMaze
import pygame
import dijkstra

def levelOne(data):
	spec.difficulty = 18
	spec.mazeType = "Binary"

	spec.level = 1

	#features
	spec.ammoOn = False
	spec.speedOn = True
	spec.pointPilesOn = False
	spec.singles = False

	#AI
	spec.AI = False
	data.myAI = None
	data.otherAI = None

	prepareNewMaze(data)

def levelTwo(data):
	spec.difficulty = 18
	spec.mazeType = "RecursiveDivision"

	spec.level = 2

	#features
	spec.ammoOn = False
	spec.speedOn = True
	spec.pointPilesOn = True
	spec.singles = False
	
	#AI
	spec.AI = True
	data.myAI = ai.AIPlayer()
	data.otherAI = ai.AIPlayer()
	data.otherAI.tag = "opponent"

	prepareNewMaze(data)

def levelThree(data):
	spec.difficulty = 18
	spec.mazeType = "Sidewinder"

	spec.level = 3

	#features
	spec.ammoOn = True
	spec.speedOn = True
	spec.pointPilesOn = True
	spec.singles = False
	
	#AI
	spec.AI = True
	data.myAI = dijkstra.AIThree()
	data.otherAI = dijkstra.AIThree()
	data.otherAI.tag = "opponent"

	prepareNewMaze(data)

def levelFour(data):
	spec.difficulty = 18
	spec.mazeType = "Eller"

	spec.level = 4

	#features
	spec.ammoOn = True
	spec.speedOn = True
	spec.pointPilesOn = True
	spec.singles = True
	
	#AI
	spec.AI = True
	data.myAI = dijkstra.AIThree()
	data.otherAI = dijkstra.AIThree()
	data.otherAI.tag = "opponent"

	prepareNewMaze(data)

def levelFive(data):
	spec.difficulty = 22
	spec.mazeType = "HuntAndKill"

	spec.level = 0

	#features
	spec.ammoOn = True
	spec.speedOn = True
	spec.pointPilesOn = True
	spec.singles = True

	#AI
	spec.AI = True
	data.myAI = astar.AIFour()
	data.otherAI = astar.AIFour()
	data.otherAI.tag = "opponent"

	prepareNewMaze(data)

def prepareNewMaze(data):
	#reset for drawings
	spec.cellWidth = spec.gameWidth/spec.difficulty
	spec.cellHeight = spec.gameHeight/spec.difficulty
	spec.wallThickness = spec.cellHeight//10
	#clear all existing sprites
	spec.walls.empty()
	spec.borders.empty()
	spec.points.empty()
	spec.points.empty()
	spec.staticPoints.empty()
	spec.ammos.empty()
	spec.staticAmmos.empty()
	spec.pause.empty()
	spec.threeTimes.empty()
	spec.ghost.empty()

	#generate new maze + wall sprites
	spec.maze = generateMaze.createMaze()
	drawMaze.border()
	drawMaze.cellWalls()

	data.me.renderMe()
	data.opponent.renderMe()
	spec.computerPlayers = pygame.sprite.Group()

	if data.myAI != None: spec.computerPlayers.add(data.myAI)
	if data.otherAI != None: spec.computerPlayers.add(data.otherAI)

	if data.myAI != None: data.myAI.renderMe()
	if data.otherAI != None: data.otherAI.renderMe()
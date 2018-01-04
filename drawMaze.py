###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Draws maze walls 
# 
###############################################################################
import pygame #graphics

from random import * #randomized numbers

import spec #game specifications
import generateMaze #creates randomized mazes
import pointPieces #creates points in maze

class Wall(pygame.sprite.Sprite):

	def __init__(self, x, y, width, height, tag = "Walls"):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)

		#walls are defined by their coordinates and size
		self.image = pygame.Surface([width, height])
		self.image.fill(spec.wallColor)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		#add walls to sprite group
		if tag == "Walls": spec.walls.add(self)
		elif tag == "Borders": spec.borders.add(self)

#create borders of game
def border():
	#horizontal borders
	top = Wall(0, 0, spec.screenWidth, spec.vPad, "Borders")
	bottom = Wall(0, spec.vPad + spec.gameHeight, spec.screenWidth, spec.vPad, "Borders")
	#vertical borders
	left = Wall(0, spec.vPad, spec.hPad, spec.gameHeight, "Borders")
	right = Wall(spec.hPad + spec.gameWidth, spec.vPad, spec.hPad, spec.gameHeight, "Borders")

def cellWalls():
	maze = spec.maze
	for row in range(len(maze)):

		for col in range(len(maze)):
			pointPieces.createPoints(row, col)
			cell = maze[row][col]
			if "Right" not in cell: #create vertical line dividing cell and cell to its right
				Wall(spec.hPad + spec.cellWidth*(col+1) - spec.wallThickness/2, 
					spec.vPad + spec.cellHeight*(row), spec.wallThickness, spec.cellHeight)

			if "Down" not in cell: #create horizontal line dividing cell and cell below it
				Wall(spec.hPad + spec.cellWidth*(col), 
					spec.vPad + spec.cellHeight*(row+1) - spec.wallThickness/2, 
					spec.cellWidth, spec.wallThickness)

###############################################################################
#
# Testing drawMaze (includes generateMaze)
#
###############################################################################

class testDrawMaze(object):
	def init(data):
		spec.difficulty = 10 #number of rows/cols in maze determines difficulty

		#allow access of game specifications to all docs
		spec.gameDisplay = pygame.display.set_mode((data.width, data.height))
		spec.screenWidth = data.width
		spec.screenHeight = data.height
		spec.gameWidth = (2/3)*spec.screenWidth
		spec.gameHeight = (3/4)*spec.screenHeight

		#change when difficulty changes
		spec.cellWidth = spec.gameWidth/spec.difficulty
		spec.cellHeight = spec.gameHeight/spec.difficulty
		spec.wallThickness = spec.cellHeight//10
		spec.vPad = (spec.screenHeight-spec.gameHeight)/2
		spec.hPad = (spec.screenWidth-spec.gameWidth)/2

		spec.maze = generateMaze.testRandomMaze(spec.difficulty)
		border()
		cellWalls()

	def mousePressed(data, x, y): pass

	def mouseReleased(data, x, y): pass

	def mouseMotion(data, x, y): pass 

	def mouseDrag(data, x, y): pass

	def keyPressed(data, keyCode, modifier): 
		#control q to quit game
		if keyCode == pygame.K_LCTRL: spec.keys["Control"] = True
		if keyCode == pygame.K_q: spec.keys["q"] = True

		#change maze 
		if keyCode == pygame.K_SPACE:
			# *** NOTE: USE CODE LATER WHEN IMPLEMENTING LEVELS
			spec.difficulty += 1 
			#reset for drawings
			spec.cellWidth = spec.gameWidth/spec.difficulty
			spec.cellHeight = spec.gameHeight/spec.difficulty
			spec.wallThickness = spec.cellHeight//10
			#clear all existing sprites
			spec.walls.empty()
			#generate new maze + wall sprites
			spec.maze = generateMaze.testRandomMaze(spec.difficulty)
			cellWalls()
			border()

	def keyReleased(data, keyCode, modifier):
		#control q to quit game
		if keyCode == pygame.K_LCTRL: spec.keys["Control"] = False
		if keyCode == pygame.K_q: spec.keys["w"] = False

	def timerFired(data, dt):
		#control q to quit game
		if "q" in spec.keys and "Control" in spec.keys and spec.keys["q"] and spec.keys["Control"]:
			pygame.quit()
			quit()

	def redrawAll(data, screen):
		spec.walls.draw(screen)
		spec.borders.draw(screen)

	def isKeyPressed(data, key): return data._keys.get(key, False) #keys being held down

	def __init__(data, width=1080, height=720, fps=50, title="maze"):
		data.width = width
		data.height = height
		data.fps = fps
		data.title = title
		data.bgColor = (255, 255, 255)
		pygame.init()

	def run(data, serverMsg = None, server = None):

		clock = pygame.time.Clock()
		screen = pygame.display.set_mode((data.width, data.height))
		# set the title of the window
		pygame.display.set_caption(data.title)

		# stores all the keys currently being held down
		data._keys = dict()

		data.serverMsg = serverMsg
		data.server = server

		# call game-specific initialization
		data.init()
		playing = True

		while playing:
			time = clock.tick(data.fps)
			data.timerFired(time)
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					data.mousePressed(*(event.pos))
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					data.mouseReleased(*(event.pos))
				elif (event.type == pygame.MOUSEMOTION and
					  event.buttons == (0, 0, 0)):
					data.mouseMotion(*(event.pos))
				elif (event.type == pygame.MOUSEMOTION and
					  event.buttons[0] == 1):
					data.mouseDrag(*(event.pos))
				elif event.type == pygame.KEYDOWN:
					data._keys[event.key] = True
					data.keyPressed(event.key, event.mod)
				elif event.type == pygame.KEYUP:
					data._keys[event.key] = False
					data.keyReleased(event.key, event.mod)
				elif event.type == pygame.QUIT:
					playing = False
			screen.fill(data.bgColor)
			data.redrawAll(screen)
			pygame.display.flip()

		pygame.quit()


def main():
	game = testDrawMaze()
	game.run()

#main()
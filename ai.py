###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# ai Players: Levels 1 and 2 of "intelligence"
# Basic framework for backtracking algorithm (findMoves()): https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#mazeSolving
# All code implementations completely by Andrea Estrada
#
###############################################################################
import pygame #graphics
import math
from random import * #randomly place player
import spec
import copy
import player

class AIPlayer(player.GenericCharacter):

	@staticmethod
	def almostEqual(num1, num2, proximity = 0.06):
		return abs(num1-num2) < proximity

	@staticmethod
	def roundHalfUp(num):
		if num%1 >= 0.5: return math.ceil(num)
		else: return int(num)

	def __init__(self, tag = "me", dDistance = 2):
		self.moves = ["Reset"]
		self.checkX = 0
		self.checkY = 0
		self.tag = tag

		self.currentMoveTime = 0
		self.currentMoveTimeMax = 30

		#set appearance
		self.imgs = spec.aiImages

		super().__init__()

		self.dDistance = dDistance

		self.dX, self.dY = 0, 0

		spec.computerPlayers.add(self)
		self.chooseMovement()

		self.routeNow = []

	#backup in case mid-detection is missed
	def collide(self):
		if pygame.sprite.spritecollide(self, spec.walls, False): 
			self.dX *= -1
			self.dY *= -1
		if pygame.sprite.spritecollide(self, spec.borders, False): 
			self.dX *= -1
			self.dY *= -1

	#carries out move, communicates via server
	def carryOut(self):
		self.rect.x += self.dX
		self.rect.y += self.dY

	#direction currently moving
	def currentMovement(self):
		if self.dX == self.dDistance: return "Right"
		if self.dX == -self.dDistance: return "Left"
		if self.dY == self.dDistance: return "Down"
		if self.dY == -self.dDistance: return "Up"

	@staticmethod 
	def oppositeMovement(movement):
		if movement == "Right": return "Left"
		if movement == "Left": return "Right"
		if movement == "Down": return "Up"
		if movement == "Up": return "Down"

	#destructively modifies moves
	def edgeCases(self):
		if self.checkX == 0 and "Left" in self.moves: self.moves.remove("Left")
		elif self.checkX == len(spec.maze[0]) - 1 and "Right" in self.moves: self.moves.remove("Right")
		if self.checkY == 0 and "Up" in self.moves: self.moves.remove("Up")
		elif self.checkY == len(spec.maze) - 1 and "Down" in self.moves: self.moves.remove("Down")

	#randomly changes direction, avoiding edge cases and backtracking
	def chooseMovement(self):
		#don't backtrack steps!
		oppMove = AIPlayer.oppositeMovement(self.currentMovement())
		if oppMove in self.moves: self.moves.remove(oppMove)

		#choose new direction
		goTo = choice(self.moves)
		operationX, operationY = self.translateMove(goTo)
		self.dX = self.dDistance * operationX
		self.dY = self.dDistance * operationY

	#from directions --> values
	def translateMove(self, goTo): #return x, y
		if goTo == "Right": return 1, 0
		elif goTo == "Left": return -1, 0
		elif goTo == "Up": return 0, -1
		elif goTo == "Down": return 0, 1
		else: return 0, 0

	#checks whether ai is in the center of a square
	def getMazeSpot(self):
		x = self.rect.centerx
		y = self.rect.centery

		alignX = (x - spec.hPad)/spec.cellWidth - 0.5
		self.checkX = AIPlayer.roundHalfUp(alignX)

		alignY = (y - spec.vPad)/spec.cellHeight - 0.5
		self.checkY = AIPlayer.roundHalfUp(alignY)

		return AIPlayer.almostEqual(alignX, self.checkX) and AIPlayer.almostEqual(alignY, self.checkY)

	#generic AI player makes choices regardless of player's location
	def move(self):
		self.currentMoveTime += 1
		if self.getMazeSpot(): #in the center of a square
			self.moves = copy.deepcopy(spec.maze[self.checkY][self.checkX])
			self.edgeCases()
			#continue along current path
			if self.currentMovement() in self.moves and self.currentMoveTime < self.currentMoveTimeMax: self.currentMoveTime += 1
			else: 
				self.currentMoveTime = 0 
				self.chooseMovement()
		self.collide()
		if self.tag == "me":
			self.carryOut()
			msg = "AIat %d %d\n" % (self.rect.centerx, self.rect.centery)
			if spec.server != None: spec.server.send(msg.encode())

class AITwo(AIPlayer):

	#level two AI player completes backtracking based on player's location 
	def move(self):
		if self.getMazeSpot(): #in the center of a square
			if len(self.routeNow) < 1: self.routeNow = self.findPathToPlayer()
			if len(self.routeNow) >= 1: 
				goTo = self.routeNow[0]
				operationX, operationY = self.translateMove(goTo)
				self.dX = self.dDistance * operationX
				self.dY = self.dDistance * operationY
				self.routeNow.pop(0)
		self.collide()
		self.carryOut()

	#uses backtracking to direct AI towards player's location
	#does not optimize path distance, as loops exist in the map making multiple solutions valid 
	def findPathToPlayer(self):
		aiX, aiY = self.currentSlot()
		if self.tag == "me": endX, endY = spec.me.currentSlot() #my AI
		elif self.tag == "opponent": endX, endY = spec.opponent.currentSlot() #other AI
		solution = []
		directions = []

		def findMoves(currY, currX, targetY, targetX):
			nonlocal solution
			nonlocal directions
			if (currY, currX) in solution: return False #already visited this spot in maze
			solution += [(currY, currX)]
			if (currY, currX) == (targetY, targetX): return True #got to destination
			else:
				for move in spec.maze[currY][currX]:
					directions.append(move)
					if move == "Right": dX, dY = 1, 0
					elif move == "Left": dX, dY = -1, 0
					elif move == "Up": dX, dY = 0, -1
					elif move == "Down": dX, dY = 0, 1
					try:
						if findMoves(currY + dY, currX + dX, targetY, targetX): return True
					except IndexError: pass
					directions.pop()
				solution.pop()
				return False

		if findMoves(aiY, aiX, endY, endX): 
			return directions
		else: return None



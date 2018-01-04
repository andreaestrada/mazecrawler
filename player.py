###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Draws characters
# 
###############################################################################
import pygame #graphics
from random import * #randomly place player

import spec #game specifications
import generateMaze #creates randomized mazes
import drawMaze #draws randomized mazes


class GenericCharacter(pygame.sprite.Sprite):

	def __init__(self):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)
		self.renderMe()

	def renderMe(self): #change size
		self.gridX, self.gridY = randint(0, len(spec.maze)-1), randint(0, len(spec.maze)-1)
		self.currentCoordinates()

		#players must be square
		width = spec.cellHeight*2/3
		height = spec.cellHeight*2/3

		self.width, self.height = int(width), int(height)
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)

		self.currImage = 0

		#set up how it should be displayed
		self.image = pygame.transform.scale(self.imgs[self.currImage], (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.x = self.x - width/2
		self.rect.y = self.y - height/2

		self.sendMessageMax = 1
		self.sendMessage = 0

	def changeImage(self):
		self.currImage += 1
		self.image = pygame.transform.scale(self.imgs[self.currImage%len(self.imgs)], 
			(self.width, self.height))

	def currentSlot(self):
		x = self.rect.centerx - spec.hPad
		y = self.rect.centery - spec.vPad
		indexX = int(x//spec.cellWidth)
		indexY = int(y //spec.cellHeight)
		return indexX, indexY

	def currentCoordinates(self):
		#find coordinates first from index in grid --> coordinates from middle
		self.x = spec.hPad + spec.cellWidth*(self.gridX+0.5)
		self.y = spec.vPad + spec.cellHeight*(self.gridY+0.5)

	def draw(self):
		spec.gameDisplay.blit(self.image, (self.rect.x, self.rect.y))


class Character(GenericCharacter):

	def __init__(self, num):
		#set appearance
		if num == 1: self.imgs = spec.player1Images
		else: self.imgs = spec.player2Images

		super().__init__()

		#initialize
		self.score = 0
		self.powerupsCollected = 0
		self.ammoShot = 0

		self.ammoOwned = 0
		self.speed = spec.maxSpeed/2

		#powerups
		self.hasPowerup = False #can only have one powerup at a time
		self.bonus = False #triple points
		self.ghost = False #go through walls
		self.aiPause = False
		spec.aiPause = False #opponent is paused
		self.powerupEnd = 0 #powerups last 5 seconds

		self.pause = False
		self.pauseTimer = 0

	def move(self, dX, dY):
		if not self.pause:
			#complete legal moves
			self.rect.x += dX
			while self.isNotLegal(): #fully undo move (while loop necessary for pygame bug associated with variable speeds)
				if dX > 0: self.rect.x -= 1 
				else: self.rect.x +=1
			self.rect.y += dY
			while(self.isNotLegal()): #fully undo move (while loop necessary for pygame bug associated with variable speeds)
				if dY > 0: self.rect.y -= 1 
				else: self.rect.y +=1
			self.collectFeatures()

	def isNotLegal(self):
		if self.ghost: return pygame.sprite.spritecollide(self, spec.borders, False)
		else: return pygame.sprite.spritecollide(self, spec.walls, False) \
			or pygame.sprite.spritecollide(self, spec.borders, False)

	def collectFeatures(self):
		#collect power ups and ammunition
		if pygame.sprite.spritecollide(self, spec.points, True):
			if self.bonus: self.score += 3
			else: self.score += 1
		ammoCollected = pygame.sprite.spritecollide(self, spec.staticAmmos, True)
		for ammoReceived in ammoCollected:
			if self.bonus: self.score += 3*ammoReceived.amount
			else: self.ammoOwned += ammoReceived.amount
		pointsCollected = pygame.sprite.spritecollide(self, spec.staticPoints, True)
		for pointsReceived in pointsCollected:
			self.score += pointsReceived.amount
		self.collectSingles()

	def aiCollide(self):
		hitBy = pygame.sprite.spritecollide(self, spec.computerPlayers, False)
		if hitBy:
			self.pause = True
			self.pauseTimer = spec.currTimer + 1.5
			for ai in hitBy:
				if ai.tag == "me":
					ai.gridX, ai.gridY = randint(0, len(spec.maze)-1), randint(0, len(spec.maze)-1)
					ai.currentCoordinates()
					ai.rect.centerx = ai.x
					ai.rect.centery = ai.y
					msg = "AIat %d %d\n" % (ai.rect.centerx, ai.rect.centery)
					spec.server.send(msg.encode())

		if spec.currTimer > self.pauseTimer: 
			self.pause = False
			self.pauseTimer = 0

	def collectSingles(self):
		if not self.hasPowerup:
			if pygame.sprite.spritecollide(self, spec.pause, True): spec.aiPause, self.aiPause = True, True
			elif pygame.sprite.spritecollide(self, spec.threeTimes, True): self.bonus = True
			elif pygame.sprite.spritecollide(self, spec.ghost, True): self.ghost = True
			else: return None #no powerup collected
			self.powerupEnd = spec.currTimer + 3 #each powerup lasts 3 seconds
			self.hasPowerup = True
			self.powerupsCollected += 1
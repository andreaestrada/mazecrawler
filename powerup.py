###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Generic powerup appearances
# 
###############################################################################
import pygame
import spec
from random import *

class PowerupGeneric(pygame.sprite.Sprite):
	def __init__(self, centerX, centerY, images, group, size):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)
		self.imgs = images

		self.width = int(size)
		self.height = int(size)

		self.currImage = randint(0, len(self.imgs)-1)
		#set up how it should be displayed
		self.image = pygame.transform.scale(self.imgs[self.currImage], (self.width, self.height))

		self.rect = self.image.get_rect()
		self.rect.centerx = centerX
		self.rect.centery = centerY
		group.add(self)

	def changeImage(self):
		self.currImage += 1
		self.image = pygame.transform.scale(self.imgs[self.currImage%len(self.imgs)], 
			(self.width, self.height))

	@staticmethod
	def generateNewPowerupLocation():
		#random place to be generated
		x, y = randint(0, len(spec.maze)-1), randint(0, len(spec.maze)-1)
		centerX = spec.hPad + spec.cellWidth*(x+0.5)
		centerY = spec.vPad + spec.cellHeight*(y+0.5)
		return centerX, centerY
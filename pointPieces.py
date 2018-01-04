###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Creates points
# 
###############################################################################
import pygame #graphics

from random import * #randomized numbers

import spec #game specifications

def createPoints(row, col):
	#specifications for each point piece
	powX = spec.hPad + spec.cellWidth*(col+0.5)
	powY = spec.vPad + spec.cellHeight*(row+0.5)
	width = max(spec.cellHeight/7, 5)
	height = max(spec.cellHeight/7, 5)
	Point(powX, powY, width, height)

class Point(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height):
		self.width, self.height = int(width), int(height)
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)

		self.currImage = randint(0, len(spec.pointImages)-1)

		#set up how it should be displayed
		self.image = pygame.transform.scale(spec.pointImages[self.currImage], (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.x = x - width/2
		self.rect.y = y - height/2

		#add point to sprite group
		spec.points.add(self)

	def changeImage(self):
		self.currImage += 1
		self.image = pygame.transform.scale(spec.pointImages[self.currImage%len(spec.pointImages)], 
			(self.width, self.height))


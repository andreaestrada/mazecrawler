###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Create generic powerup piles
# 
###############################################################################
import pygame
from random import *

import spec
import powerup

class Piles(powerup.PowerupGeneric):

	def __init__(self, centerX, centerY, amount, images, group, size):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)
		super().__init__(centerX, centerY, images, group, size)

		self.amount = amount

	@staticmethod
	def generateNewPowerup(data, typeAdded):
		centerX, centerY = powerup.PowerupGeneric.generateNewPowerupLocation()
		amount = randint(3,7)
		msg = "%s %d %d %d\n" % (typeAdded, centerX, centerY, amount)
		data.server.send(msg.encode())
		if typeAdded == "AmmoAdded": AmmoPile(centerX, centerY, amount)
		elif typeAdded == "PointsAdded": PointPile(centerX, centerY, amount)

class AmmoPile(Piles):
	def __init__(self, centerX, centerY, amount):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)
		super().__init__(centerX, centerY, amount, spec.ammoPileImages, spec.staticAmmos, spec.cellWidth/3)

class PointPile(Piles):
	def __init__(self, centerX, centerY, amount):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)
		super().__init__(centerX, centerY, amount, spec.pointPileImages, spec.staticPoints, spec.cellWidth/3)


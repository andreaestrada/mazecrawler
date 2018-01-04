###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Create single powerups
# 
###############################################################################
import pygame

import spec
import powerup

class Single(powerup.PowerupGeneric):

	@staticmethod
	def generateNewPowerup(data, typeAdded):
		centerX, centerY = powerup.PowerupGeneric.generateNewPowerupLocation()
		msg = "%s %d %d\n" % (typeAdded, centerX, centerY)
		if data.server != None: data.server.send(msg.encode())
		if typeAdded == "GhostAdded": Ghost(centerX, centerY)
		elif typeAdded == "ThreeAdded": Three(centerX, centerY)
		elif typeAdded == "PauseAdded": Pause(centerX, centerY)

class Ghost(Single):
	def __init__(self, centerX, centerY):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)
		super().__init__(centerX, centerY, spec.ghostImages, spec.ghost, spec.cellWidth/2)

class Three(Single):
	def __init__(self, centerX, centerY):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)
		super().__init__(centerX, centerY, spec.threeTimesImages, spec.threeTimes, spec.cellWidth/2)

class Pause(Single):
	def __init__(self, centerX, centerY):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)
		super().__init__(centerX, centerY, spec.pauseImages, spec.pause, spec.cellWidth/2)

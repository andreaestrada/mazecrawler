###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# AI ammunition to track opponent
# 
###############################################################################
import spec
import pygame
from random import *
import pygame.mixer

class Ammunition(pygame.sprite.Sprite):

	def __init__(self, owner):
		#call Sprite class constructor
		pygame.sprite.Sprite.__init__(self)

		self.owner = owner

		if self.owner == "Me": 
			self.ammoStart = spec.me
			self.ammoEnd = spec.opponent
			spec.me.ammoShot += 1 
		else: 
			self.ammoStart = spec.opponent
			self.ammoEnd = spec.me
			spec.opponent.ammoShot += 1

		self.dX, self.dY = self.findMovement()

		self.image = pygame.transform.scale(spec.ammoImage, (7,7))
		self.rect = self.image.get_rect()
		self.rect.centerx = self.ammoStart.rect.centerx
		self.rect.centery = self.ammoStart.rect.centery

		if spec.volume != 0: spec.shotFired.play()

		spec.ammos.add(self)

	def findMovement(self): #AI tracks opponent for easy, smart shooting
		moveX = self.ammoEnd.rect.centerx - self.ammoStart.rect.centerx 
		moveY = self.ammoEnd.rect.centery - self.ammoStart.rect.centery
		distance = (moveX**2 + moveY**2)**0.5

		return moveX/abs(distance/10), moveY/abs(distance/10)

	def move(self): #move ammunition, check to see if it hits a wall or an opponent
		self.rect.centerx += self.dX
		self.rect.centery += self.dY
		if self.owner == "Me" and pygame.sprite.collide_rect(spec.opponent, self):
			if spec.volume != 0: spec.playerHit.play()
			added = 0
			while spec.opponent.score > 0 and added < 5: #steal up to 5 points from opponent 
				spec.opponent.score -= 1
				spec.me.score += 1
				added += 1
			self.kill()
		elif self.owner == "Opponent" and pygame.sprite.collide_rect(spec.me, self):
			if spec.volume != 0: spec.playerHit.play()
			added = 0
			while spec.me.score > 0 and added < 5: #steal up to 5 points from opponent 
				spec.me.score -= 1
				spec.opponent.score += 1
				added += 1
			self.kill()
		if pygame.sprite.spritecollide(self, spec.borders, False): self.kill()
		if pygame.sprite.spritecollide(self, spec.walls, False): self.kill()

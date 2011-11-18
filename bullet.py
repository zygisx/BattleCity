__author__ = 'zee'

from pygame.sprite import Sprite
import pygame

class Bullet(Sprite):
	def __init__(self, screen, speed, pos, mode):
		Sprite.__init__(self)
		self.screen = screen
		self.speed = speed
		self.pos = pos
		self.mode = mode
		#print self.pos
		self.base_bullet = pygame.image.load("bullet.png").convert_alpha()

		self.bullet = self.base_bullet.get_rect()

	def update(self, millis):

		if self.mode == 0:
			self.pos[1] -= self.speed
		elif self.mode == 1:
			self.pos[0] += self.speed
		elif self.mode == 2:
			self.pos[1] += self.speed
		else:
			self.pos[0] -= self.speed

		#draw.rect(self.screen, (0, 0, 0), self.bullet, 0)
		self.screen.blit(self.base_bullet, self.pos)

	#END

__author__ = 'zee'

from pygame.sprite import Sprite
import pygame

class Bullet(Sprite):
    def __init__(self, screen, speed, pos, mode):
        Sprite.__init__(self)
        self.screen = screen
        self.area = screen.get_rect()
        self.speed = speed

        self.mode = mode
        self.image = pygame.image.load("bullet.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, millis):

        if self.mode == 0:
            self.rect.centery -= self.speed
        elif self.mode == 1:
            self.rect.centerx += self.speed
        elif self.mode == 2:
            self.rect.centery += self.speed
        else:
            self.rect.centerx -= self.speed

        if self.rect.centerx  < 0 or \
                self.rect.centerx > self.area.right or \
                self.rect.centery  < 0 or \
                self.rect.centery > self.area.bottom:
            self.kill();

    #END

import pygame

__author__ = 'zee'

import pygame
import abc
from pygame import transform
from bullet import Bullet
from pygame.sprite import Sprite

class Tank(Sprite):
    __metaclass__ = abc.ABCMeta
    def __init__(self, screen, img_filename, speed, pos):
        Sprite.__init__(self)
        self.screen = screen
        self.speed = speed
        self.pos = pos
        self.base_tank = pygame.image.load(img_filename).convert_alpha()
        self.tank = self.base_tank.get_rect()
        self.bullets = []
        self.bullet_time = 0;
        self.mode  = 1;
    #END




    def bullets_update(self, millis):
        """ update all bullets of current tank """
        for bullet in self.bullets:
            bullet.update(0);
        self.bullet_time -= millis
    #END

    #--- Private access ---

    def _rotate (self, code):		# code 0, 1, 2, 3
        """
        rotate tank by code:
        0 - 0 deg, 1 - 90 deg, 2 - 180, 3 - 270;
        """
        if self.mode != code:
            self.base_tank = transform.rotate(self.base_tank, (self.mode - code)*90)
            self.mode = code
    #END

    #--- Abstract methods ---

    @abc.abstractmethod
    def update(self, millis, move):
        """ update tank position """
        raise NotImplemented("Please Implement this method")

    @abc.abstractmethod
    def shot (self, millis):
        """ make a shot """
        raise NotImplemented("Please Implement this method")



class PlayerTank(Tank):
    """

    """
    def __init__(self, screen, img_filename, speed ):
        Tank.__init__(self, screen, img_filename, speed, [10.0,10.0])

        self.area = screen.get_rect()
        self.__rotate(0)

    #END

    def update(self, millis, move):

        self.pos[0] += move[0]*self.speed
        self.pos[1] += move[1]*self.speed

        # check for tank going outside window
        if self.pos[0]  < 0 or  self.pos[0] + self.tank.width > self.area.right:
            self.pos[0] -= move[0]*self.speed
        if self.pos[1]  < 0 or  self.pos[1] + self.tank.height > self.area.bottom:
            self.pos[1] -= move[1]*self.speed

        #rotate tank
        if move[0] > 0:
            self.__rotate(1)
        elif move[0] < 0:
            self.__rotate(3)
        elif move[1] > 0:
            self.__rotate(2)
        elif move[1] < 0:
            self.__rotate(0)

        self.screen.blit(self.base_tank, self.pos)
    #END

    def shot (self, millis):
        if self.bullet_time > 0: return
        else: self.bullet_time = 500

        pos = []
        if self.mode == 0:
            pos.append( self.pos[0] + self.tank.centerx - 2)
            pos.append( self.pos[1] - 4 )
        elif self.mode == 1:
            pos.append( self.pos[0] + self.tank.right + 2)
            pos.append( self.pos[1] + self.tank.centery - 2)
        elif self.mode == 2:
            pos.append( self.pos[0] + self.tank.centerx - 3)
            pos.append( self.pos[1] + self.tank.bottom + 4)
        else:
            pos.append( self.pos[0] - 4 )
            pos.append( self.pos[1] + self.tank.centery - 2)
        print pos
        self.bullets.append(Bullet(self.screen,self.speed + 1, pos, self.mode))


    def __rotate (self, code):		# code 0, 1, 2, 3
        if self.mode != code:
            self.base_tank = transform.rotate(self.base_tank, (self.mode - code)*90)
            self.mode = code

    #END
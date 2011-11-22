__author__ = 'zee'

import pygame
import abc
from pygame import transform
from bullet import Bullet
from pygame.sprite import Sprite
from random import randrange

class Tank(Sprite):
    __metaclass__ = abc.ABCMeta
    def __init__(self, screen, img_filename, speed, pos):
        Sprite.__init__(self)
        self.screen = screen
        self.speed = speed

        self.image = pygame.image.load(img_filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.bullets = pygame.sprite.Group();
        self.bullet_time = 0;
        self.mode  = 0;
        self.alive = True
    #END

    def shot (self, millis):
        """ make a shot """
        pos = []
        if self.mode == 0:
            pos.append( self.rect.centerx)
            pos.append( self.rect.centery - self.rect.height/2 )
        elif self.mode == 1:
            pos.append( self.rect.centerx + self.rect.width/2)
            pos.append( self.rect.centery)
        elif self.mode == 2:
            pos.append( self.rect.centerx)
            pos.append( self.rect.centery + self.rect.height/2)
        else:
            pos.append( self.rect.centerx - self.rect.width/2)
            pos.append( self.rect.centery)
        self.bullets.add(Bullet(self.screen,self.speed +1, pos, self.mode))

    #END

    def collision_detect(self, sprite):
        return pygame.sprite.collide_rect(self, sprite)

    #--- Private access ---

    def _rotate (self, code):		# code 0, 1, 2, 3
        """
        rotate tank by code:
        0 - 0 deg, 1 - 90 deg, 2 - 180, 3 - 270;
        """
        if self.mode != code:
            self.image = transform.rotate(self.image, (self.mode - code)*90)
            self.mode = code
    #END

     #--- Abstract methods ---

    @abc.abstractmethod
    def update(self, move, millis):
        """ update tank position """
        raise NotImplemented("Please Implement this method")

class PlayerTank(Tank):
    """

    """
    def __init__(self, screen, img_filename, speed ):
        Tank.__init__(self, screen, img_filename, speed, [20.0,20.0])

        self.area = screen.get_rect()
        #self.__rotate(0)

    #END


    def update(self, millis, move, enem):

        # move sprite
        self.rect.centerx += move[0]*self.speed
        self.rect.centery += move[1]*self.speed

        #collisions
        if pygame.sprite.spritecollideany(self, enem):
            self.rect.centerx -= move[0]*self.speed
            self.rect.centery -= move[1]*self.speed

        # check for tank going outside window
        if self.rect.left  < 0 or  self.rect.right > self.area.right:
            self.rect.centerx -= move[0]*self.speed
        if self.rect.top  < 0 or  self.rect.bottom > self.area.bottom:
            self.rect.centery -= move[1]*self.speed

        #rotate tank
        if move[0] > 0:
            self.__rotate(1)
        elif move[0] < 0:
            self.__rotate(3)
        elif move[1] > 0:
            self.__rotate(2)
        elif move[1] < 0:
            self.__rotate(0)

        # bullets
        self.bullet_time -= millis
        self.bullets.update(millis)
        self.bullets.draw(self.screen)
    #END

    def __rotate (self, code):		# code 0, 1, 2, 3
        if self.mode != code:
            self.image = transform.rotate(self.image, (self.mode - code)*90)
            self.mode = code
    #END

    def shot(self, millis):
        if self.bullet_time > 0: return
        else: self.bullet_time = 400

        Tank.shot(self, millis)
    #END




class EnemyTank(Tank):
    """ Enemy tank.
    """

    def __init__(self, screen, img_filename, speed, pos):
        Tank.__init__(self, screen ,img_filename, speed, pos)
        self.area = screen.get_rect()
        self.distance = 0

    def update(self, millis, tanks):
        """

        """
        # check is distance complete
        if self.distance <= 0:
            self.distance = randrange(200)
            self._rotate(randrange(4))
        else: self.distance -= self.speed

        # ---
        move = [0, 0]
        if self.mode == 0:
           move[1] -= 1
        elif self.mode == 1:
            move[0] += 1
        elif self.mode == 2:
            move[1] += 1
        else:
            move[0] -= 1

        # make move
        self.rect.centerx += self.speed * move[0]
        self.rect.centery += self.speed * move[1]

        # Collisions
        tanks.remove(self)
        if pygame.sprite.spritecollideany(self, tanks):
            self.rect.centerx -= move[0]*self.speed
            self.rect.centery -= move[1]*self.speed
        tanks.add(self)

        # screen out
        if self.rect.left  < 0 or  self.rect.right > self.area.right:
            self.rect.centerx -= move[0]*self.speed
            self.distance = 0
        if self.rect.top  < 0 or  self.rect.bottom > self.area.bottom:
            self.rect.centery -= move[1]*self.speed
            self.distance = 0
            
        #bullets update
        self.bullet_time -= millis
        self.bullets.update(millis)
        self.bullets.draw(self.screen)

        # shot
        self.shot(millis)
    #END

    def shot(self, millis):
        if self.bullet_time > 0: return
        else: self.bullet_time = randrange(200, 2000)

        Tank.shot(self, millis)
    #END

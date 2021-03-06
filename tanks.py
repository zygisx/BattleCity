__author__ = 'zee'

import pygame
import abc
from pygame import transform
from bullet import Bullet
from pygame.sprite import Sprite
from random import randrange

#SHOT_SOUND_FILE = "shot2.wma"

class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Tank(Sprite):
    __metaclass__ = abc.ABCMeta



    def __init__(self, screen, img_filename, speed, pos):
        Sprite.__init__(self)
        self.screen = screen
        self.speed = speed

        self.image = pygame.image.load(img_filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.bullets = pygame.sprite.Group()
        self.bullet_time = 0
        self.direction  = Direction.UP
        self.alive = True
    #END

    def shot (self, millis, speed):
        """ make a shot """
        pos = []
        if self.direction == Direction.UP:
            pos.append( self.rect.centerx)
            pos.append( self.rect.centery - self.rect.height/2 )
        elif self.direction == Direction.RIGHT:
            pos.append( self.rect.centerx + self.rect.width/2)
            pos.append( self.rect.centery)
        elif self.direction == Direction.DOWN:
            pos.append( self.rect.centerx)
            pos.append( self.rect.centery + self.rect.height/2)
        else:
            pos.append( self.rect.centerx - self.rect.width/2)
            pos.append( self.rect.centery)
        self.bullets.add(Bullet(self.screen,speed, pos, self.direction))

    #END

    def collision_detect(self, sprite):
        return pygame.sprite.collide_rect(self, sprite)

    #--- Private access ---

    def _rotate (self, direct):		# code 0, 1, 2, 3
        """
        rotate tank by code:
        0 - 0 deg, 1 - 90 deg, 2 - 180, 3 - 270;
        """
        if self.direction != direct:
            self.image = transform.rotate(self.image, (self.direction - direct)*90)
            self.direction = direct
    #END

     #--- Abstract methods ---

    @abc.abstractmethod
    def update(self, move, millis):
        """ update tank position """
        raise NotImplemented("Please Implement this method")

class PlayerTank(Tank):
    """

    """

    INIT_COORDINATES = [20.0, 580.0]

    def __init__(self, screen, img_filename, speed, shot_sound ):
        Tank.__init__(self, screen, img_filename, speed, PlayerTank.INIT_COORDINATES)

        self.shot_sound = shot_sound
        self.area = screen.get_rect()
        #self.__rotate(0)
    #END


    def update(self, millis, move, enem, map):

        # move sprite
        self.rect.centerx += move[0]*self.speed
        self.rect.centery += move[1]*self.speed

        #enemy collisions
        if pygame.sprite.spritecollideany(self, enem):
            self.rect.centerx -= move[0]*self.speed
            self.rect.centery -= move[1]*self.speed

        #map collisions
        if map.isCollideWithMap(self.rect):
            self.rect.centerx -= move[0]*self.speed
            self.rect.centery -= move[1]*self.speed

        # check for tank going outside window
        if self.rect.left  < 0 or  self.rect.right > self.area.right:
            self.rect.centerx -= move[0]*self.speed
        if self.rect.top  < 0 or  self.rect.bottom > self.area.bottom:
            self.rect.centery -= move[1]*self.speed

        #rotate tank
        if move[0] > 0:
            self.__rotate(Direction.RIGHT)
        elif move[0] < 0:
            self.__rotate(Direction.LEFT)
        elif move[1] > 0:
            self.__rotate(Direction.DOWN)
        elif move[1] < 0:
            self.__rotate(Direction.UP)

        # bullets
        self.bullet_time -= millis
        self.bullets.update(millis)
        self.bullets.draw(self.screen)
    #END

    def __rotate (self, direction):
        if self.direction != direction:
            self.image = transform.rotate(self.image, (self.direction - direction)*90)
            self.direction = direction
    #END

    def shot(self, millis):
        if self.bullet_time > 0: return
        else: self.bullet_time = 200

        self.shot_sound.play()
        Tank.shot(self, millis, self.speed + 10)
    #END




class EnemyTank(Tank):
    """ Enemy tank.
    """

    def __init__(self, screen, img_filename, speed, pos):
        Tank.__init__(self, screen ,img_filename, speed, pos)
        self.area = screen.get_rect()
        self.distance = 0

    def update(self, millis, tanks, map):
        """

        """
        # check is distance complete
        if self.distance <= 0:
            self.distance = randrange(200)
            self._rotate(randrange(4))
        else: self.distance -= self.speed

        # ---
        move = [0, 0]
        if self.direction == Direction.UP:
           move[1] -= 1
        elif self.direction == Direction.RIGHT:
            move[0] += 1
        elif self.direction == Direction.DOWN:
            move[1] += 1
        else:
            move[0] -= 1

        # make move
        self.rect.centerx += self.speed * move[0]
        self.rect.centery += self.speed * move[1]

        #other tanks Collisions
        tanks.remove(self)
        if pygame.sprite.spritecollideany(self, tanks):
            self.rect.centerx -= move[0]*self.speed
            self.rect.centery -= move[1]*self.speed
            self.distance = 0
        tanks.add(self)

        #map collision
        if map.isCollideWithMap(self.rect):
            self.rect.centerx -= move[0]*self.speed
            self.rect.centery -= move[1]*self.speed
            self.distance = 0

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

        Tank.shot(self, millis, self.speed + 1)
    #END

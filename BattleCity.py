__author__ = 'zee'

from time import time

from tanks import *
import pygame, sys
from pygame.locals import *
from random import randrange


SCREEN_RESOLUTION = 600, 600
BG_COLOR = (255, 255, 255)
TANK_FILE = "tank.png"
ENEMY_FILE = "enemy_tank.png"


def main():

    pygame.init();
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)

    clock = pygame.time.Clock()

    #groups
    tanks =  pygame.sprite.Group()
    player =  pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    sprite = PlayerTank(screen, TANK_FILE, 2.0)
    sprite.add(tanks, player)

    i=0
    while i <= 20:
        enemy = (EnemyTank(screen, ENEMY_FILE, 2.0,  \
			[60 + randrange(300), 60 + randrange(300)]))
        if not pygame.sprite.spritecollideany(enemy, tanks):
            enemy.add(tanks, enemies)
            i+=1

    while 1:

        time_passed = clock.tick(50)
        screen.fill(BG_COLOR); print time_passed

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        keyPresses = pygame.key.get_pressed()
        if keyPresses[K_SPACE]:
            sprite.shot(time_passed)
        if keyPresses[K_UP]:
            sprite.update(time_passed, (0, -1), enemies)
        elif keyPresses[K_DOWN]:
            sprite.update(time_passed, (0, 1), enemies)
        elif keyPresses[K_LEFT]:
            sprite.update(time_passed, (-1, 0), enemies)
        elif keyPresses[K_RIGHT]:
            sprite.update(time_passed, (1, 0), enemies)
        elif keyPresses[K_ESCAPE]:
            sys.exit()
        else:
            sprite.update(time_passed, (0, 0), enemies)

        # TODO bullets_update wia group not itterating enemies sprites
        for enemy in enemies.sprites():
            enemy.bullets_update(time_passed)

        enemies.update(time_passed, tanks)
        sprite.bullets_update(time_passed)

        tanks.draw(screen)

        pygame.display.flip()

    return 0

if __name__ == '__main__':
	main()

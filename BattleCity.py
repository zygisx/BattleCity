#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zee'

from time import time
from explosion import Explosion, FINAL_EXPLOSION
from tanks import *
import pygame, sys
from pygame.locals import *
from random import randrange
from level import Map

ENEMIES = 5
SCREEN_RESOLUTION = 800, 600
BG_COLOR = (255, 255, 255)
TANK_FILE = r"resources\images\tank.png"
ENEMY_FILE = "resources/images/enemy_tank.png"
EXPLOSION = "resources/images/explosion.png"
EXPLOSION2 = "resources/images/exp2.png"
EXPLOSION_SOUND = "resources/sounds/explosion.ogg"
FINAL_EXPLOSION_SOUND = "resources/sounds/final_explosion.ogg"
SHOT_SOUND_FILE = "resources/sounds/shot.ogg"
TILES_FILE_NAME = "resources/images/tiles.png"
TESTING = True

def main():
    pygame.init();
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)

    clock = pygame.time.Clock()

    #groups
    tanks =  pygame.sprite.Group()
    player =  pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    killed =  pygame.sprite.Group()

    #sound
    shot_sound  = pygame.mixer.Sound(SHOT_SOUND_FILE)
    explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND)

    #map
    map = Map(TILES_FILE_NAME);
    map.loadMap("1.map")

    sprite = PlayerTank(screen, TANK_FILE, 2.0, shot_sound)
    sprite.add(tanks, player)

    i=0

    while i < ENEMIES:
        enemy = (EnemyTank(screen, ENEMY_FILE, 2.0,  \
			[20 + randrange(SCREEN_RESOLUTION[0] - 50), 20 + randrange(SCREEN_RESOLUTION[1] - 50)]))
        if not pygame.sprite.spritecollideany(enemy, tanks):
            enemy.add(tanks, enemies)
            i+=1

    start = time()
    while (player and enemies) or killed:     #while player group contains any sprite

        time_passed = clock.tick(50)
        screen.fill(BG_COLOR);

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

        for die in pygame.sprite.groupcollide(enemies, sprite.bullets, False, True).keys():
            killed.add(Explosion(EXPLOSION, screen, die.rect, explosion_sound))
            die.kill()

        # works only for one player
        if not TESTING:
            for enemy in enemies.sprites():
                if pygame.sprite.groupcollide(player, enemy.bullets, False, True):
                    killed.add(Explosion(EXPLOSION2,
                                         screen, sprite.rect,
                                         pygame.mixer.Sound(FINAL_EXPLOSION_SOUND),
                                         FINAL_EXPLOSION, 10 ))
                    sprite.kill()

        enemies.update(time_passed, tanks)
        killed.update(time_passed)

        tanks.draw(screen)
        map.drawMap(screen)

        for ex in killed.sprites():
            screen.blit(ex.image, ex.rect, ex.area)
        
        pygame.display.flip()
    #END WHILE

    color = (200,0,0)
    Font = pygame.font.Font(None,30)
    text1 = Font.render('GAME OVER',1,color)
    text2 = Font.render("KILLED: {0}".format(ENEMIES - len(enemies)),1,color)
    text3 = Font.render("TIME {0} SECONDS".format(round(time() - start, 2)),1,color)
    screen.blit(text1,(250,200))
    screen.blit(text2,(260,250))
    screen.blit(text3,(220,300))
    #clock.delay(1000)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            #if event.type == pygame.KEY_DOWN: sys.exit()
        pygame.display.flip()

    return 0

if __name__ == '__main__':
	main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zee'

# sys.path.append(r"d:\ws\python\pygame\tankgame")

from time import time
from explosion import Explosion, FINAL_EXPLOSION
from tanks import *
import pygame, sys
from pygame.locals import *
from random import randrange
from level import *

ENEMIES = 3
SCREEN_RESOLUTION = 800, 600
BG_COLOR = (0, 0, 0)
TANK_FILE = r"resources\images\tank.png"
ENEMY_FILE = "resources/images/enemy_tank.png"
EXPLOSION = "resources/images/explosion.png"
EXPLOSION2 = "resources/images/exp2.png"
EXPLOSION_SOUND = "resources/sounds/explosion.ogg"
FINAL_EXPLOSION_SOUND = "resources/sounds/final_explosion.ogg"
SHOT_SOUND_FILE = "resources/sounds/shot.ogg"
TILES_FILE_NAME = "resources/images/tiles.png"
TESTING = False

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
    level = Level()

    #map = Map(TILES_FILE_NAME);
    #map.loadMap("1.map")

    player_sprite = PlayerTank(screen, TANK_FILE, 2.0, shot_sound)
    player_sprite.add(tanks, player)

    i=0

    while i < ENEMIES:
        enemy = (EnemyTank(screen, ENEMY_FILE, 2.0,  \
			[20 + randrange(SCREEN_RESOLUTION[0] - 50), 20 + randrange(SCREEN_RESOLUTION[1] - 50)]))
        if not pygame.sprite.spritecollideany(enemy, tanks) and not level.map.isCollideWithMap(enemy.rect):
            enemy.add(tanks, enemies)
            i+=1

    start = time()
    while (player and enemies) or killed:     #while player group contains any player_sprite

        time_passed = clock.tick(50)
        screen.fill(BG_COLOR);

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        keyPresses = pygame.key.get_pressed()
        if keyPresses[K_SPACE]:
            player_sprite.shot(time_passed)
        if keyPresses[K_UP]:
            player_sprite.update(time_passed, (0, -1), enemies, level.map)
        elif keyPresses[K_DOWN]:
            player_sprite.update(time_passed, (0, 1), enemies, level.map)
        elif keyPresses[K_LEFT]:
            player_sprite.update(time_passed, (-1, 0), enemies, level.map)
        elif keyPresses[K_RIGHT]:
            player_sprite.update(time_passed, (1, 0), enemies, level.map)
        elif keyPresses[K_ESCAPE]:
            sys.exit()
        else:
            player_sprite.update(time_passed, (0, 0), enemies, level.map)

        for die in pygame.sprite.groupcollide(enemies, player_sprite.bullets, False, True).keys():
            killed.add(Explosion(EXPLOSION, screen, die.rect, explosion_sound))
            die.kill()

        # works only for one player
        if not TESTING:
            for enemy in enemies.sprites():
                if pygame.sprite.groupcollide(player, enemy.bullets, False, True):
                    killed.add(Explosion(EXPLOSION2,
                                         screen, player_sprite.rect,
                                         pygame.mixer.Sound(FINAL_EXPLOSION_SOUND),
                                         FINAL_EXPLOSION, 10 ))
                    player_sprite.kill()

        # is map damaged
        for bullet in player_sprite.bullets.sprites():
            if level.map.isBulletCollideWithMap(bullet.rect):
                bullet.kill()
        for enemy in enemies.sprites():
            for bullet in enemy.bullets.sprites():
                if level.map.isBulletCollideWithMap(bullet.rect):
                    bullet.kill()



        enemies.update(time_passed, tanks, level.map)
        killed.update(time_passed)

        tanks.draw(screen)
        level.map.drawMap(screen)

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

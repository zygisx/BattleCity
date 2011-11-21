__author__ = 'zee'

from time import time

from tanks import *
import pygame, sys
from pygame.locals import *
from random import randrange

ENEMIES = 10
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

    while i < ENEMIES:
        enemy = (EnemyTank(screen, ENEMY_FILE, 2.0,  \
			[60 + randrange(500), 60 + randrange(500)]))
        if not pygame.sprite.spritecollideany(enemy, tanks):
            enemy.add(tanks, enemies)
            i+=1
    game_on = True
    start = time()
    while game_on:     #while player group contains any sprite

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

        pygame.sprite.groupcollide(enemies, sprite.bullets, True, True)
        for enemy in enemies.sprites():
            pygame.sprite.groupcollide(player, enemy.bullets, True, True)

        enemies.update(time_passed, tanks)
        tanks.draw(screen)
        
        pygame.display.flip()

        game_on = len(player) and len(enemies)

    color = (200,0,0)
    Font = pygame.font.Font(None,25)
    text1 = Font.render('GAME OVER',1,color)
    text2 = Font.render("Killed: {0}".format(ENEMIES - len(enemies)),1,color)
    text3 = Font.render("You made this in {0} seconds".format(round(time() - start, 2)),1,color)
    screen.blit(text1,(250,200))
    screen.blit(text2,(260,250))
    screen.blit(text3,(180,300))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        pygame.display.flip()
    print "You made this in: ", time() - start
    print "Killed: ", ENEMIES - len(enemies)

    return 0

if __name__ == '__main__':
	main()

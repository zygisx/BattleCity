__author__ = 'zee'


from tanks import PlayerTank
import pygame, sys
from pygame.locals import *

SCREEN_RESOLIUTION = 400, 450
BG_COLOR = (255, 255, 255)
TANK_FILE = "tank.png"


def main():

	pygame.init();
	screen = pygame.display.set_mode(SCREEN_RESOLIUTION)



	clock = pygame.time.Clock()

	sprite = PlayerTank(screen, TANK_FILE, 2.0)

	while 1:

		time_passed = clock.tick(50)
		screen.fill(BG_COLOR)


		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		keyPresses = pygame.key.get_pressed()
		if keyPresses[K_SPACE]:
			sprite.shot(time_passed)
		if keyPresses[K_UP]:
			sprite.update(time_passed, (0, -1))
		elif keyPresses[K_DOWN]:
			sprite.update(time_passed, (0, 1))
		elif keyPresses[K_LEFT]:
			sprite.update(time_passed, (-1, 0))
		elif keyPresses[K_RIGHT]:
			sprite.update(time_passed, (1, 0))
		elif keyPresses[K_ESCAPE]:
			sys.exit()
		else:
			sprite.update(time_passed, (0, 0))

		sprite.bullets_update(time_passed)

		pygame.display.flip()

	return 0

if __name__ == '__main__':
	main()
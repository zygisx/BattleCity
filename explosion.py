__author__ = 'zee'

import pygame

class Explosion(pygame.sprite.Sprite):
    """

    """
    def __init__(self, image, screen, rect, fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self._frame = 0
        self._delay = 1000/fps
        self._time = 0
        self._areas = (
            (0, 0, 20, 20),
            (20, 0, 20, 20),
            (40, 0, 20, 20),
            (60, 0, 20, 20),
            (80, 0, 20, 20),
            (100, 0, 20, 20),
            (120, 0, 20, 20),
        )
        self.image = pygame.image.load(image).convert_alpha()
        self.area = pygame.rect.Rect(self._areas[self._frame])
        self.rect = pygame.Rect(rect)

    def update(self, millis):
        if (millis + self._time > self._delay):
            self._frame += 1
            if self._frame >= len(self._areas):
                self.kill()
            else:
                self.area = pygame.rect.Rect(self._areas[self._frame])
                self._time = 0
        else: self._time += millis
    #END
        
        
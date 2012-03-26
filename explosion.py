__author__ = 'zee'

import pygame


EXPLOSION = (
    (0, 0, 20, 20),
    (20, 0, 20, 20),
    (40, 0, 20, 20),
    (60, 0, 20, 20),
    (80, 0, 20, 20),
    (100, 0, 20, 20),
    (120, 0, 20, 20),
)

FINAL_EXPLOSION = (
    (0, 0, 62, 62),
    (62, 0, 62, 62),
    (124, 0, 62, 62),
    (186, 0, 62, 62),
    (0, 62, 62, 62),
    (62, 62, 62, 62),
    (124, 62, 62, 62),
    (186, 62, 62, 62),
    (0, 124, 62, 62),
    (62, 124, 62, 62),
    (124, 124, 62, 62),
    (186, 124, 62, 62),
    (0, 186, 62, 62),
    (62, 186, 62, 62),
    (124, 186, 62, 62),
    (186, 186, 62, 62),

)

class Explosion(pygame.sprite.Sprite):
    """
   
    """
    def __init__(self, image, screen, rect, sound, areas = EXPLOSION, fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self._frame = 0
        self._delay = 1000/fps
        self._time = 0
        self._areas = areas
        self.image = pygame.image.load(image).convert_alpha()
        self.area = pygame.rect.Rect(self._areas[self._frame])
        self.rect = pygame.Rect(rect)
        sound.play()
    #END

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
#END

class FinalExplosion(pygame.sprite.Sprite):

    def __init__(self, image, screen, rect, fps = 10):
        self.screen = screen
        self._frame = 0
        self._delay = 1000/fps
        self._time = 0
        self._areas = EXPLOSION
        self.image = pygame.image.load(image).convert_alpha()
        self.area = pygame.rect.Rect(self._areas[self._frame])
        self.rect = pygame.Rect(rect)
    #END
        
        

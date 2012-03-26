#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame


SHOT_SOUND_FILE = "shot2.wma"
__author__ = 'zee'

"""
    Created by PyCharm.
    User: zee
    Date: 12/4/11
    Time: 11:43 PM
"""




pygame.init();

screen = pygame.display.set_mode((100, 100))

pygame.mixer.init()
shot_sound  = pygame.mixer.Sound(SHOT_SOUND_FILE)
shot_sound.play()

for i in range(100):
    shot_sound.play()
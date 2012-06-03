#from argparse import ArgumentParser
#from numpy import tile
#from pytz import _CountryTimezoneDict

__author__ = 'zee'

import pygame
import os
import random

import BattleCity

class Level():

    def __init__(self, level = 1):
        self.__level = level
        from BattleCity import TILES_FILE_NAME
        self.__map = Map(TILES_FILE_NAME)
        self.__map.loadMap(BattleCity.MAPS_DIR + str(level) + ".map")

    """
    Getters
    """
    @property
    def current_level(self):
        return self.__level
    @property
    def map(self):
        return self.__map



class Map():
    (TILE_EMPTY, TILE_BRICK, TILE_STEEL, TILE_WATER, TILE_GRASS, TILE_FROZE) = range(6)

    DESTRUCTABLE = (TILE_BRICK, )
    BULLET_STOPPER = (TILE_BRICK, TILE_STEEL, )
    WALL = (TILE_BRICK, TILE_STEEL, TILE_WATER, )

    TILE_SIZE = 20;



    def __init__(self, tiles_filename):
        #self.map = []

        tiles = pygame.image.load(tiles_filename)

        tile_images = [
            tiles.subsurface(0, 0, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(0, Map.TILE_SIZE, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(Map.TILE_SIZE, Map.TILE_SIZE, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(2*Map.TILE_SIZE, 0, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(3*Map.TILE_SIZE, 0, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(0, 0, 8*2, 8*2),
            tiles.subsurface(0, 0, 8*2, 8*2)
        ]

        self.tile_brick = tile_images[0]
        self.tile_steel = tile_images[1]
        self.tile_grass = tile_images[2]
        self.tile_water = tile_images[3]
        self.tile_water1= tile_images[4]

        self.tile_water2= tile_images[5]

        self.tile_froze = tile_images[6]

        self.tile_rects = []



    def loadMap(self, filename):
        """
        Loads map from file
        """
        if (not os.path.isfile(filename)):
            return False
        f = open(filename, "r")
        data = f.read().split("\n")
        self.map = []
        x, y = 0, 0
        for row in data:
            for col in row:
                if col == "#":
                    self.map.append((Map.TILE_BRICK, pygame.Rect(x, y, Map.TILE_SIZE, Map.TILE_SIZE)))
                elif col == "@":
                    self.map.append((Map.TILE_STEEL, pygame.Rect(x, y, Map.TILE_SIZE, Map.TILE_SIZE)))
                elif col == '%':
                    self.map.append((Map.TILE_GRASS, pygame.Rect(x, y, Map.TILE_SIZE, Map.TILE_SIZE)))
                elif col == '$':
                    self.map.append((Map.TILE_WATER, pygame.Rect(x, y, Map.TILE_SIZE, Map.TILE_SIZE)))

                x += Map.TILE_SIZE

            x = 0
            y += Map.TILE_SIZE
        self.__updateRects()
        return True
    #END

    def drawMap(self, screen):
        """ draw map on specific surface
        """
        water = 0

        for tile in self.map:
            if tile[0] == Map.TILE_BRICK:
                screen.blit(self.tile_brick, tile[1].topleft)
            elif tile[0] == Map.TILE_STEEL:
                screen.blit(self.tile_steel, tile[1].topleft)
            elif tile[0] == Map.TILE_GRASS:
                screen.blit(self.tile_grass, tile[1].topleft)
            elif tile[0] == Map.TILE_WATER:
                if random.randrange(1):
                    screen.blit(self.tile_water, tile[1].topleft)
                else:
                    screen.blit(self.tile_water1, tile[1].topleft)

    #END

    def isCollideWithMap(self, rect):
        for tile in self.map:
            if tile[0] in Map.WALL:
                if tile[1].colliderect(rect):
                    return True
        return False
    #END

    def isBulletCollideWithMap(self, rect):
        index = rect.collidelist(self.tile_rects)
        if index == -1:
            return False
        else:
            if self.map[index][0] == Map.TILE_BRICK:
                self.map.pop(index)
                self.tile_rects.pop(index)
                return True
            elif self.map[index][0] in Map.BULLET_STOPPER:
                return True
        return False



    def __updateRects(self):
        self.tile_rects = []
        for tile in self.map:
            if tile[0] in (self.TILE_BRICK, self.TILE_STEEL, self.TILE_WATER, self.TILE_GRASS):
                self.tile_rects.append(tile[1])
    #END

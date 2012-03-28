from numpy import tile

__author__ = 'zee'

import pygame
import os

class Level():
    pass


class Map():
    (TILE_EMPTY, TILE_BRICK, TILE_STEEL, TILE_WATER, TILE_GRASS, TILE_FROZE) = range(6)

    TILE_SIZE = 20;



    def __init__(self, tiles_filename):
        #self.map = []

        #tiles = pygame.transform.scale(pygame.image.load("images/sprites.gif"), [192, 224])

        tiles = pygame.image.load(tiles_filename)

        tile_images = [
            tiles.subsurface(0, 0, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(0, 0, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(0, 0, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(0, 0, Map.TILE_SIZE, Map.TILE_SIZE),
            tiles.subsurface(0, 0, 8*2, 8*2),
            tiles.subsurface(0, 0, 8*2, 8*2),
            tiles.subsurface(0, 0, 8*2, 8*2)
        ]

        self.tile_brick = tile_images[0]
        self.tile_steel = tile_images[1]
        self.tile_grass = tile_images[3]
        self.tile_water = tile_images[4]
        self.tile_water1= tile_images[4]
        self.tile_water2= tile_images[5]
        self.tile_froze = tile_images[6]



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
                x += Map.TILE_SIZE
            x = 0
            y += Map.TILE_SIZE

        return True
    #END

    def drawMap(self, screen):
        """ draw map on specific surface
        """

        for tile in self.map:
            if tile[0] == Map.TILE_BRICK:
                screen.blit(self.tile_brick, tile[1].topleft)
            elif tile[0] == Map.TILE_STEEL:
                pass
            elif tile[0] == Map.TILE_GRASS:
                pass

    #END
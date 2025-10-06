import pygame
from pygame.locals import *

temp_mosse_dx_illegali=[15,31,47,63,79,95,111]

class Personaggio(pygame.sprite.Sprite):
    def __init__(self, pos, start_cell):
        super().__init__()
        self.pos = pos
        self.cur_cell = start_cell
        self.image = pygame.image.load('background_assets/nanodimerda.png')
        self.rect = self.image.get_rect(topleft = pos)
    def calcola_mosse(self, tiles):
        tiles=list(tiles)
        self.possibili_mosse = []
        ind= tiles.index(self.cur_cell)
        if ind!= 0 and ind%16!=0:
            self.possibili_mosse.append(tiles[ind-1])
        if len(tiles)>ind+1 and ind not in temp_mosse_dx_illegali:
            self.possibili_mosse.append(tiles[ind+1])
        if ind-16 >= 0:
            self.possibili_mosse.append(tiles[ind-16])
        if len(tiles)>=ind+16:
            self.possibili_mosse.append(tiles[ind+16])
        return self.possibili_mosse
    def move(self, tile):
        self.pos = tile.pos
        self.cur_cell.entities = None
        tile.entities = self
        self.cur_cell = tile
        self.rect.x, self.rect.y = self.pos
import pygame
from pygame.locals import *

temp_mosse_dx_illegali=[15,31,47,63,79,95,111]

class Personaggio(pygame.sprite.Sprite):
    def __init__(self, pos, start_cell):
        super().__init__()
        self.pos = pos #posizione in pixel
        self.cur_cell = start_cell #relativa cella in cui è dentro
        self.image = pygame.image.load('background_assets/nanodimerda.png')
        self.rect = self.image.get_rect(topleft = pos)
    def calcola_mosse(self, matrix): #muoversi di 1 casella
        self.possibili_mosse = []
        cur_x = self.cur_cell.x #x e y relativi alla posizione su matrice
        cur_y = self.cur_cell.y
        if cur_x > 0: #se non si trova nella prima colonna
            self.possibili_mosse.append(matrix[cur_y][cur_x-1]) #aggiungi la casella a sx
        if cur_x < len(matrix[0])-1: #se non si trova nell'ultima colonna
            self.possibili_mosse.append(matrix[cur_y][cur_x+1]) #aggiungi la casella a dx
        if cur_y > 0:
            self.possibili_mosse.append(matrix[cur_y-1][cur_x])
        if cur_y < len(matrix)-1:
            self.possibili_mosse.append(matrix[cur_y+1][cur_x])
        return self.possibili_mosse
    def calcola_mosse2(self, matrix): #muoversi di 2 caselle
        self.possibili_mosse = []
        cur_x = self.cur_cell.x 
        cur_y = self.cur_cell.y
        if cur_x > 0: #se non si trova nella prima colonna
            self.possibili_mosse.append(matrix[cur_y][cur_x-1])
            if cur_y > 0:
                self.possibili_mosse.append(matrix[cur_y-1][cur_x-1]) #angolo alto sx
            if cur_y < len(matrix)-1:
                self.possibili_mosse.append(matrix[cur_y+1][cur_x-1]) #angolo basso sx
            if cur_x > 1:
                self.possibili_mosse.append(matrix[cur_y][cur_x-2]) #due a sx
        if cur_x < len(matrix[0])-1: #se non si trova nell'ultima colonna
            self.possibili_mosse.append(matrix[cur_y][cur_x+1])
            if cur_y > 0:
                self.possibili_mosse.append(matrix[cur_y-1][cur_x+1]) #angolo alto dx
            if cur_y < len(matrix)-1:
                self.possibili_mosse.append(matrix[cur_y+1][cur_x+1]) #angolo basso dx
            if cur_x < len(matrix[0])-2:
                self.possibili_mosse.append(matrix[cur_y][cur_x+2]) #due a dx
        if cur_y > 0:
            self.possibili_mosse.append(matrix[cur_y-1][cur_x])
            if cur_y > 1:
                self.possibili_mosse.append(matrix[cur_y-2][cur_x])
        if cur_y < len(matrix)-1:
            self.possibili_mosse.append(matrix[cur_y+1][cur_x])
            if cur_y < len(matrix)-2:
                self.possibili_mosse.append(matrix[cur_y+2][cur_x])

        
        return self.possibili_mosse
    def move(self, tile):
        self.pos = tile.pos
        self.cur_cell.entities = None
        tile.entities = self
        self.cur_cell = tile
        self.rect.x, self.rect.y = self.pos
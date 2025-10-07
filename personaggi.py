import pygame
from pygame.locals import *

class Personaggio(pygame.sprite.Sprite):
    def __init__(self, pos, start_cell):
        super().__init__()
        self.pos = pos #posizione in pixel
        self.cur_cell = start_cell #relativa cella in cui è dentro
        self.image = pygame.image.load('background_assets/nanodimerda.png')
        self.rect = self.image.get_rect(topleft = pos)

    def calcola_mosse(self, matrix, max_dist=5): #utilizzando BFS
        self.possibili_mosse = []
        self.parent = {} #questo servirà per costruire la freccia

        start = self.cur_cell

        rows = len(matrix)
        cols = len(matrix[0])

        #utilizzo BFS, quindi una coda
        queue = [(self.cur_cell, 0)]  # inizializzo la coda con il l'elemento di start, per ogni elemento salvo la distanza (qui 0)
        visited = set([self.cur_cell])
        self.parent[self.cur_cell] = None 
        # direzioni possibili (su, giù, sinistra, destra)
        directions = [(0,1), (0,-1), (1,0), (-1,0)]

        while len(queue) > 0: #finchè la coda non è vuota
            cell_, dist = queue.pop(0) #faccio il dequeue
            x, y = cell_.x, cell_.y

            for dy, dx in directions: #calcolo le celle vicine
                ny = y + dy
                nx = x + dx

                effective_dist = abs(nx - start.x) + abs(ny - start.y)
                if 0 <= ny < rows and 0 <= nx < cols: # controlla che la cella sia dentro la mappa/matrice
                    cell = matrix[ny][nx]
                    if cell not in visited and cell.walkable and (cell_ in self.possibili_mosse or cell_==start): # controlla che la cella sia "valida"
                        visited.add(cell)
                        queue.append((matrix[ny][nx], dist + 1))
                        self.parent[matrix[ny][nx]] = cell_
                        if effective_dist <= max_dist:
                            self.possibili_mosse.append(cell)

        return self.possibili_mosse
    def find_path(self, tile):
        path=[tile]
        cur_tile = tile
        while self.parent[cur_tile]:
            path.append(self.parent[cur_tile])
            cur_tile=self.parent[cur_tile]
        path.append(self.cur_cell) #aggiungo un elemento finale che rappresenta l'inizio della freccia
        return path

    def move(self, tile):
        self.pos = tile.pos
        self.cur_cell.entities = None
        self.cur_cell.walkable = True
        tile.entities = self
        tile.walkable = False
        self.cur_cell = tile
        self.rect.x, self.rect.y = self.pos
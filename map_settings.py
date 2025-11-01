import pygame
from personaggi import Personaggio
from game_settings import *
from random import choices
from movement_holder import add_move, add_shake
grass_img = pygame.transform.scale(pygame.image.load('background_assets/cella.png'), (tile_size, tile_size))
mount_img = pygame.transform.scale(pygame.image.load('background_assets/montagna.png'), (tile_size, tile_size))

map=[
    'X       ',
    '  X     ',
    '      M ',
    '    M   ',
    '   MX   ',
    ' MMM    ',
    '        ',
    '   N    ',
    ' N  NN  ',
    '        ',
]
class Cella(pygame.sprite.Sprite):
    def __init__(self, pos, matrix_pos, ground):
        super().__init__()
        self.pos = pos #posizione in pixel
        self.x,self.y = matrix_pos #posizione sulla matrice
        self.entities = None #se si trova un personaggio sopra quella casella
        self.flagged= False #Bool per controllare se la casella selezionate è questa
        self.walkable = True #Bool per verificare se si può camminare qui
        self.gorund = ground
        match ground:
            case 'grass':
                self.image = grass_img.copy()
                self.name = 'Prato'
                self.desc = 'più vuoto della mia anima!'
            case 'mount':
                self.image = grass_img.copy()
                self.name = 'Montagna'
                self.desc = 'dura come il'
                self.image.blit(mount_img,(0,0))
                self.walkable = False
        self.rect = self.image.get_rect(topleft = pos)
    def shift(self, shift): #shift 1 se scende, -1 se sale
        add_move(self,[(self.pos[0],self.pos[1]+shift*tile_size)])
        #self.pos=(self.pos[0],self.pos[1]+tile_size*shift)
        self.y=self.y+1*shift



matrix=[] #matrice con tutte le tiles trasformate in classe Cella
nani = pygame.sprite.Group()

for n_riga, riga in enumerate(map): #per ogni riga
    matrix_row=[]
    for n_colonna, tile in enumerate(riga): #e ogni colonna (quindi cella) della riga
        y = n_riga * tile_size #pos y cella
        x = n_colonna * tile_size #pos x cella
        if tile=='M':
            cell=Cella((x,y), (n_colonna, n_riga), 'mount')
        else:
            cell=Cella((x,y), (n_colonna, n_riga), 'grass')
        matrix_row.append(cell)
        if tile=='N':
            nano=Personaggio(cell, 0)
            nani.add(nano)
            cell.entities= nano
            cell.walkable = False
        elif tile=='X':
            nano=Personaggio(cell, 1)
            nani.add(nano)
            cell.entities= nano
            cell.walkable = False
    matrix.append(matrix_row)


class Map:
    def __init__(self):
        self.matrix = matrix
        self.tiles = pygame.sprite.LayeredUpdates([x for xs in matrix for x in xs])
    def generate_tile(self): #funzione che spawna una tile in modo random (pesata)
        tile_grounds = ['grass', 'mount']
        weights = [7, 1]
        return choices(tile_grounds, weights=weights)[0]
    def update_map(self, turn):
        new_row=[]
        half = int(len(self.matrix)/2)
        if turn == 0: #ha appena giocato il giocatore sotto
            for cell in self.matrix[half-1]:
                new_row.append(Cella(cell.pos, (cell.x, cell.y), self.generate_tile())) #creo nuove celle nella nuova row usando la funzione random
            new_matrix = self.matrix[:half]
            new_matrix.append(new_row)
            m = self.matrix[half:] # m è la parte di matrice che deve muoversi
            m.append(new_row)
            for row in m:
                for tile in row:
                    tile.shift(1)
            new_matrix.extend(self.matrix[half:-1])
        else:
            for cell in self.matrix[half]:
                new_row.append(Cella(cell.pos, (cell.x, cell.y), self.generate_tile())) #creo nuove celle nella nuova row usando la funzione random
            new_matrix2 = self.matrix[half:]
            m = self.matrix[:half]
            m.append(new_row)
            for row in m:
                for tile in row:
                    tile.shift(-1)
            new_matrix = self.matrix[1:half]
            new_matrix.append(new_row)
            new_matrix.extend(new_matrix2)
        self.tiles.add(new_row, layer= self.tiles.get_bottom_layer()-1)
        self.matrix = new_matrix
        add_shake(self.tiles, 20, 2)
        for n in nani:
            if n.cur_cell not in self.tiles:
                n.kill()
map=Map()




cursore=pygame.Surface((tile_size,tile_size)) #quadratino grigio trasparente
cursore.fill("#585858")
cursore.set_alpha(150)

zona_nemica=pygame.Surface((schermox,len(matrix)/2*tile_size)) #zona rossa trasparente
zona_nemica.fill("#E20E0E")
zona_nemica.set_alpha(50)

tile_opaca = pygame.Surface((tile_size,tile_size))
tile_opaca.fill("#3E0FE6")
tile_opaca.set_alpha(100)

tile_attacchi = pygame.Surface((tile_size,tile_size))
tile_attacchi.fill("#CD0000")
tile_attacchi.set_alpha(100)
import pygame
from personaggi import Personaggio
from game_settings import tile_size, schermox, schermoy
from random import choices
grass_img = pygame.transform.scale(pygame.image.load('background_assets/cella.png'), (tile_size, tile_size))
mount_img = pygame.transform.scale(pygame.image.load('background_assets/montagna.png'), (tile_size, tile_size))

map=[
    'X       ',
    '  X     ',
    '      M ',
    '    M   ',
    '   M    ',
    ' MMM    ',
    '        ',
    '   N    ',
    ' N      ',
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
        match ground:
            case 'grass': self.image = grass_img
            case 'mount':
                self.image = mount_img
                self.walkable = False
        self.rect = self.image.get_rect(topleft = pos)


matrix=[] #matrice con tutte le tiles trasformate in classe Cella
#tiles = pygame.sprite.Group()
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
        if tile=='M':
            cell.image = mount_img
    matrix.append(matrix_row)


class Map:
    def __init__(self):
        self.matrix = matrix
        self.tiles = pygame.sprite.Group([x for xs in matrix for x in xs])
    def generate_tile(self): #funzione che spawna una tile in modo random (pesata)
        tile_grounds = ['grass', 'mount']
        weights = [7, 1]
        return choices(tile_grounds, weights=weights)[0]
    def update_map(self, turn):
        int(len(self.matrix)/2)
        new_row=[]
        half = int(len(self.matrix)/2)
        if turn == 0: #ha appena giocato il giocatore sotto
            for cell in self.matrix[int(len(self.matrix)/2)]:
                new_row.append(Cella(cell.pos, (cell.x, cell.y), self.generate_tile())) #creo nuove celle nella nuova row usando la funzione random
            new_matrix = self.matrix[:half]
            m = self.matrix[half:-1]
            new_matrix.append(new_row)
            new_matrix.extend(m)
        else:
            for cell in self.matrix[int(len(self.matrix)/2)]:
                new_row.append(Cella(cell.pos, (cell.x, cell.y), self.generate_tile())) #creo nuove celle nella nuova row usando la funzione random
            new_matrix = self.matrix[half:]
            m =self. matrix[1:half]
            new_matrix.append(new_row)
            new_matrix.extend(m)
        self.matrix = new_matrix
        self.tiles = pygame.sprite.Group([x for xs in new_matrix for x in xs])
map=Map()




cursore=pygame.Surface((tile_size,tile_size)) #quadratino grigio trasparente
cursore.fill("#585858")
cursore.set_alpha(150)

zona_nemica=pygame.Surface((schermox,schermoy/2)) #zona rossa trasparente
zona_nemica.fill("#E20E0E")
zona_nemica.set_alpha(50)



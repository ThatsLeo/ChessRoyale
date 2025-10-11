import pygame
from personaggi import Personaggio
fps=30
tile_size= 50 #per ora ho messo 50 ma cambiando la dimensione schermo si dovrà modificare
cell_img = pygame.image.load('background_assets/cella.png')
schermox, schermoy = 800,500
map=[                      #layout della mappa (per ora nun ci sta nu cazz, ma gli spazi servono)
    '                ',
    '                ',
    '                ',
    '                ',
    '                ',
    '          N     ',
    '          N     ',
    'M          MN   ',
    ' M              ',
    '  N             ',
]
map2=[
    'M       ',
    '  M     ',
    '        ',
    '        ',
    '        ',
    '        ',
    '        ',
    '   N    ',
    ' N      ',
    '        ',
]
class Cella(pygame.sprite.Sprite):
    def __init__(self, pos, size, matrix_pos):
        super().__init__()
        self.pos = pos #posizione in pixel
        self.x,self.y = matrix_pos #posizione sulla matrice
        self.entities = None #se si trova un personaggio sopra quella casella
        self.image = cell_img
        self.rect = self.image.get_rect(topleft = pos)
        self.flagged= False #Bool per controllare se la casella selezionate è questa
        self.walkable = True #Bool per verificare se si può camminare qui

matrix=[] #matrice con tutte le tiles trasformate in classe Cella
tiles = pygame.sprite.Group()
nani = pygame.sprite.Group()

for n_riga, riga in enumerate(map): #per ogni riga
    matrix_row=[]
    for n_colonna, tile in enumerate(riga): #e ogni colonna (quindi cella) della riga
        y = n_riga * tile_size #pos y cella
        x = n_colonna * tile_size #pos x cella
        cell=Cella((x,y), tile_size, (n_colonna, n_riga))
        tiles.add(cell)
        matrix_row.append(cell)
        if tile=='N':
            nano=Personaggio((x,y), cell, 0)
            nani.add(nano)
            cell.entities= nano
            cell.walkable = False
        if tile=='M':
            nano=Personaggio((x,y), cell, 1)
            nani.add(nano)
            cell.entities= nano
            cell.walkable = False
    matrix.append(matrix_row)





cursore=pygame.Surface((tile_size,tile_size)) #quadratino grigio trasparente
cursore.fill("#585858")
cursore.set_alpha(150)
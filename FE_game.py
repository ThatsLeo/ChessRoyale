import pygame, sys
from pygame.locals import *
from personaggi import Personaggio
fps=30
fpsclock=pygame.time.Clock()
pygame.init()
infoObject = pygame.display.Info()
#schermox, schermoy = infoObject.current_w, infoObject.current_h   #per fare schermo intero
schermox, schermoy = 800,500
screen=pygame.display.set_mode((schermox,schermoy))
map=[                      #layout della mappa (per ora nun ci sta nu cazz, ma gli spazi servono)
    '                ',
    '                ',
    '                ',
    '                ',
    '                ',
    '          N     ',
    '                ',
    '                ',
    '                ',
    '                ',
]
tile_size= 50 #per ora ho messo 50 ma cambiando la dimensione schermo si dovrà modificare

class Cella(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = pos
        self.entities = None
        self.image = pygame.image.load('background_assets/cella.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.flagged= False

cursore=pygame.Surface((tile_size,tile_size))
cursore.fill("#585858")
cursore.set_alpha(150)
        

tiles = pygame.sprite.Group()
nani = pygame.sprite.Group()

for n_riga, riga in enumerate(map): #per ogni riga
    for n_colonna, tile in enumerate(riga): #e ogni colonna (quindi cella) della riga
        y = n_riga * tile_size #pos y cella
        x = n_colonna * tile_size
        cella=Cella((x,y),tile_size)
        tiles.add(cella)
        if tile=='N':
            nano=Personaggio((x,y), cella)
            nani.add(nano)
            cella.entities= nano



possibili_mosse=None
while True:
    key_input=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos()
    for tile in tiles:
        if tile.rect.collidepoint(mouse):
            cella_attuale=tile
    tiles.draw(screen)
    nani.draw(screen)
    screen.blit(cursore,cella_attuale.pos)
    if possibili_mosse:
        for mossa in possibili_mosse:
            tile_opaca = pygame.Surface((tile_size,tile_size))
            tile_opaca.fill("#3E0FE6")
            tile_opaca.set_alpha(150)
            screen.blit(tile_opaca, mossa.pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cella_attuale.flagged:
                possibili_mosse = None
                cella_attuale.flagged = False
                flagged_cell= None
            else:
                if possibili_mosse and cella_attuale in possibili_mosse:
                    flagged_cell.entities.move(cella_attuale)
                    possibili_mosse = None
                    cella_attuale.flagged = False
                    flagged_cell= None
                elif cella_attuale.entities:
                    possibili_mosse=cella_attuale.entities.calcola_mosse(tiles)
                    cella_attuale.flagged = True
                    flagged_cell= cella_attuale
    pygame.display.update()
    fpsclock.tick(fps)
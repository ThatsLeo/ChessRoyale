import pygame, sys
from pygame.locals import *
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
    '                ',
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
        self.image = pygame.image.load('background_assets/cella.png')
        self.rect = self.image.get_rect(topleft = pos)

cursore=pygame.Surface((tile_size,tile_size))
cursore.fill("#585858")
cursore.set_alpha(150)
cursore_pos = (0,0)
def update_cursor(cursor, pos):
    pass
        

tiles = pygame.sprite.Group()

for n_riga, riga in enumerate(map): #per ogni riga
    for n_colonna, tile in enumerate(riga): #e ogni colonna (quindi cella) della riga
        y = n_riga * tile_size #pos y cella
        x = n_colonna * tile_size
        tiles.add(Cella((x,y),tile_size))




#'''
while True:
    key_input=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos()
    for tile in tiles:
        if tile.rect.collidepoint(mouse):
            cella_attuale=tile

    tiles.draw(screen)
    screen.blit(cursore,cella_attuale.pos)
    pygame.display.update()
    fpsclock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
#'''
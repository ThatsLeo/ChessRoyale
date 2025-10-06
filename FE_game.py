import pygame, sys
from pygame.locals import *
from personaggi import Personaggio
fps=30
tile_size= 50 #per ora ho messo 50 ma cambiando la dimensione schermo si dovrà modificare
fpsclock=pygame.time.Clock()
cell_img = pygame.image.load('background_assets/cella.png')
arrow_point=pygame.transform.scale(pygame.image.load('background_assets/arrow/arrowpoint.png'),(tile_size,tile_size))
arrow_line=pygame.transform.scale(pygame.image.load('background_assets/arrow/arrowline.png'),(tile_size,tile_size))
arrow_curve=pygame.transform.scale(pygame.image.load('background_assets/arrow/arrowcurve.png'),(tile_size,tile_size))
arrow_img=[arrow_line, arrow_curve,arrow_point]

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
    'N               ',
    ' N              ',
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

cursore=pygame.Surface((tile_size,tile_size)) #quadratino grigio trasparente
cursore.fill("#585858")
cursore.set_alpha(150)
        
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
            nano=Personaggio((x,y), cell)
            nani.add(nano)
            cell.entities= nano
            cell.walkable = False
    matrix.append(matrix_row)



possibili_mosse=None #Inizializziamo vuota
while True:
    key_input=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos() #posizione mouse
    for tile in tiles:
        if tile.rect.collidepoint(mouse):
            cella_attuale=tile #individuiamo quale cella stiamo guardando
    tiles.draw(screen)
    nani.draw(screen)
    screen.blit(cursore,cella_attuale.pos) #per disegnare le cose opache usiamo blit
    if possibili_mosse: #tiles colorate blu
        for mossa in possibili_mosse:
            tile_opaca = pygame.Surface((tile_size,tile_size))
            tile_opaca.fill("#3E0FE6")
            tile_opaca.set_alpha(100)
            screen.blit(tile_opaca, mossa.pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cella_attuale.flagged: #se clicchi di nuovo la stessa cella, rimuove gli attributi e torna a non averla selezionata
                possibili_mosse = None
                cella_attuale.flagged = False
                flagged_cell= None
            else:
                if possibili_mosse and cella_attuale in possibili_mosse: #se clicchi in uno dei "quadrati blu"
                    flagged_cell.entities.move(cella_attuale) #muove la pedina in quel quadrato
                    flagged_cell.flagged = False #e rimuove i dovuti attributi
                    possibili_mosse = None
                    cella_attuale.flagged = False
                    flagged_cell= None
                elif cella_attuale.entities: #se clicchi su una cella che ha un personaggio
                    possibili_mosse=cella_attuale.entities.calcola_mosse(matrix) #evidenzia le celle in cui esso può muoversi
                    cella_attuale.flagged = True
                    flagged_cell= cella_attuale
    pygame.display.update()
    fpsclock.tick(fps)
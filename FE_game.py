import pygame, sys
from pygame.locals import *
from arrow_settings import arrowing
from map_settings import *
fpsclock=pygame.time.Clock()

pygame.init()
infoObject = pygame.display.Info()
#schermox, schermoy = infoObject.current_w, infoObject.current_h   #per fare schermo intero
screen=pygame.display.set_mode((schermox,schermoy))
        




possibili_mosse=None #Inizializziamo vuota
cella_attuale=None
while True:
    key_input=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos() #posizione mouse
    for tile in tiles:
        if tile.rect.collidepoint(mouse):
            if cella_attuale!=tile:
                cambio_cella = True
            cella_attuale=tile #individuiamo quale cella stiamo guardando
    tiles.draw(screen)
    nani.draw(screen)
    screen.blit(cursore,cella_attuale.pos) #per disegnare le cose opache usiamo blit
    if possibili_mosse:
        for mossa in possibili_mosse: #tiles colorate blu
            tile_opaca = pygame.Surface((tile_size,tile_size))
            tile_opaca.fill("#3E0FE6")
            tile_opaca.set_alpha(100)
            screen.blit(tile_opaca, mossa.pos)
        if cambio_cella and cella_attuale in possibili_mosse: # calcolo la freccia solo quando il cursore si sposta di casella
            path = flagged_cell.entities.find_path(cella_attuale)
            arrows, arrow_path = arrowing(path)
            cambio_cella = False
        if cella_attuale in possibili_mosse:
            for arrow in arrows:
                screen.blit(arrow.image, arrow.tile.pos)

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
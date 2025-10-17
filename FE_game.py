import pygame, sys
from arrow_settings import arrowing
from map_settings import *
from game_settings import *
from movement_holder import check_movement, moving_objects
fpsclock=pygame.time.Clock()

pygame.init()
infoObject = pygame.display.Info()
#schermox, schermoy = infoObject.current_w, infoObject.current_h   #per fare schermo intero
screen=pygame.display.set_mode((schermox,schermoy))
possibili_mosse=None #Inizializziamo vuota
cella_attuale=None




turno = 0
fine_turno = False
while True:
    key_input=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos() #posizione mouse
    for tile in map.tiles:
        if tile.rect.collidepoint(mouse):
            if cella_attuale!=tile:
                cambio_cella = True
            cella_attuale=tile #individuiamo quale cella stiamo guardando
    map.tiles.draw(screen)
    nani.draw(screen)
    nani.update()
    if not moving_objects:
        screen.blit(cursore,cella_attuale.pos) #per disegnare le cose opache usiamo blit
    screen.blit(zona_nemica,(0,0))

    if not moving_objects and fine_turno: #check per la fine del turno
        map.update_map(turno)
        turno = abs(turno-1) 
        fine_turno=False

    if possibili_mosse:
        for mossa in possibili_mosse: #tiles colorate blu
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
            if not moving_objects: #se si sta muovendo qualcosa blocca tutto 
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

                        # per ora il turno finisce quando muovi una pedina:
                        fine_turno=True

                    elif cella_attuale.entities: #se clicchi su una cella che ha un personaggio
                        if turno == cella_attuale.entities.team: # puoi cliccare solo le pedine della squadra a cui tocca
                            possibili_mosse=cella_attuale.entities.calcola_mosse(map.matrix) #evidenzia le celle in cui esso può muoversi
                            cella_attuale.flagged = True
                            flagged_cell= cella_attuale
    check_movement()
    pygame.display.update()
    fpsclock.tick(fps)
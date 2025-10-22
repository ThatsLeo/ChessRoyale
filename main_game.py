import pygame, sys
from arrow_settings import arrowing
from map_settings import *
from game_settings import *
from movement_holder import check_movement, moving_objects
from info_menu import *
fpsclock=pygame.time.Clock()

pygame.init()
screen=pygame.display.set_mode((schermox,schermoy))
game_field = pygame.Surface((schermox,schermoy-info_section_height))

possibili_mosse=None #Inizializziamo vuota
cella_attuale=None


turno = 0
fine_turno = False
while True:
    screen.blit(game_field, (0,0))
    key_input=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos() #posizione mouse
    for tile in map.tiles:
        if tile.rect.collidepoint(mouse):
            if cella_attuale!=tile:
                cambio_cella = True
            cella_attuale=tile #individuiamo quale cella stiamo guardando
            info_section.update_info_menu(cella_attuale)

    moving = check_movement()
    if not moving_objects and fine_turno: #check per la fine del turno
        map.update_map(turno)
        turno = abs(turno-1) 
        fine_turno=False
        
    map.tiles.draw(game_field)
    nani.draw(game_field)
    nani.update()
    if not moving and cella_attuale:
        game_field.blit(cursore,cella_attuale.pos)
    game_field.blit(zona_nemica,(0,0))
    info_section.draw(screen)

    if possibili_mosse:
        for mossa in possibili_attacchi: #tiles colorate blu
            if mossa in flagged_cell.entities.possibili_mosse:
                game_field.blit(tile_opaca, mossa.pos)
            else:
                game_field.blit(tile_attacchi, mossa.pos)
        if cambio_cella and cella_attuale in possibili_mosse: # calcolo la freccia solo quando il cursore si sposta di casella
            path = flagged_cell.entities.find_path(cella_attuale)
            arrows, arrow_path = arrowing(path)
            cambio_cella = False
        if cella_attuale in possibili_mosse:
            for arrow in arrows:
                game_field.blit(arrow.image, arrow.tile.pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not moving: #se si sta muovendo qualcosa blocca tutto 
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

                    elif cella_attuale.entities and game_field.get_rect(topleft= (0,0)).collidepoint(mouse): #se clicchi su una cella che ha un personaggio
                        if turno == cella_attuale.entities.team: # puoi cliccare solo le pedine della squadra a cui tocca
                            possibili_mosse, possibili_attacchi=cella_attuale.entities.calcola_mosse(map.matrix) #evidenzia le celle in cui esso può muoversi
                            cella_attuale.flagged = True
                            flagged_cell= cella_attuale
    pygame.display.update()
    fpsclock.tick(fps)
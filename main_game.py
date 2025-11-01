import pygame, sys
from arrow_settings import arrowing
from map_settings import *
from game_settings import *
from movement_holder import check_movement, moving_objects
from info_menu import *
from buttons import *
fpsclock=pygame.time.Clock()

pygame.init()
screen=pygame.display.set_mode((schermox,schermoy))
game_field = pygame.Surface((schermox,schermoy-info_section_height))

possibili_mosse=None #Inizializziamo vuota
cella_attuale=None


while True:
    screen.blit(game_field, (0,0))
    map.tiles.draw(game_field)
    key_input=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos() #posizione mouse
    for tile in map.tiles:
        if tile.rect.collidepoint(mouse):
            if cella_attuale!=tile:
                cambio_cella = True
            cella_attuale=tile #individuiamo quale cella stiamo guardando
            info_section.update_info_menu(cella_attuale)

    moving = check_movement()
    if not moving and game.used_movement:
        celle_attaccabili= flagged_cell.entities.calcola_attacchi(map.matrix)
        if len(celle_attaccabili)==0:
            game.fine_turno=True
        for mossa in celle_attaccabili:
            game_field.blit(tile_attacchi, mossa.pos)
    if not moving and game.fine_turno: #check per la fine del turno
        end_turn()
        
    
    nani.draw(game_field)
    nani.update()
    if not moving and cella_attuale:
        game_field.blit(cursore,cella_attuale.pos)
    game_field.blit(zona_nemica,(0,0))
    info_section.draw(screen)

    if possibili_mosse:
        for mossa in possibili_attacchi: #tiles colorate blu e rosse
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
            info_section.check_tasti_click(mouse)
            if not moving: #se si sta muovendo qualcosa blocca tutto 
                if not game.used_movement:
                    if possibili_mosse and cella_attuale in possibili_mosse: #se clicchi in uno dei "quadrati blu"
                        flagged_cell.entities.move(cella_attuale) #muove la pedina in quel quadrato
                        flagged_cell.flagged = False #e rimuove i dovuti attributi
                        possibili_mosse = None
                        cella_attuale.flagged = True
                        flagged_cell= cella_attuale
                        game.used_movement=True

                    elif cella_attuale.entities and game_field.get_rect(topleft= (0,0)).collidepoint(mouse): #se clicchi su una cella che ha un personaggio
                        if game.turno == cella_attuale.entities.team: # puoi cliccare solo le pedine della squadra a cui tocca
                            possibili_mosse, possibili_attacchi=cella_attuale.entities.calcola_mosse(map.matrix) #evidenzia le celle in cui esso può muoversi
                            cella_attuale.flagged = True
                            flagged_cell= cella_attuale
    pygame.display.update()
    fpsclock.tick(fps)
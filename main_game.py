import pygame, sys
from arrow_settings import arrowing
from map_settings import *
from game_settings import *
from movement_holder import check_movement
from info_menu import *
from buttons import *
fpsclock=pygame.time.Clock()

pygame.init()
screen=pygame.display.set_mode((schermox,schermoy))
game_field = pygame.Surface((schermox,schermoy-info_section_height))
game_field_rect=game_field.get_rect(topleft= (0,0))

possibili_mosse=None #Inizializziamo vuota
celle_attaccabili = None
cella_attuale=None

while True:
    key_input=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos() #posizione mouse
    if not game.moving:
        for tile in map.tiles:
            if tile.rect.collidepoint(mouse):
                if cella_attuale!=tile:
                    cambio_cella = True
                cella_attuale=tile #individuiamo quale cella stiamo guardando
                info_section.update_info_menu(cella_attuale)
    else: cella_attuale = None

    game.moving = check_movement()
    if game.fine_turno: #check per la fine del turno
        end_turn()
        
    screen.blit(game_field, (0,0))
    map.tiles.draw(game_field)
    nani.draw(game_field)
    nani.update()
    if not game.moving and cella_attuale:
        game_field.blit(cursore,cella_attuale.pos)
    game_field.blit(zona_nemica,(0,0))
    info_section.draw(screen)

    if possibili_mosse:
        for mossa in possibili_attacchi: #tiles colorate blu e rosse
            if mossa in possibili_mosse:
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
    elif celle_attaccabili and not game.moving:
        for mossa in celle_attaccabili:
            game_field.blit(tile_attacchi, mossa.pos)
    elif game.used_movement and (game.used_attack or not celle_attaccabili):
        game.fine_turno = True




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            info_section.check_tasti_click(mouse)
            if not game.moving: #se si sta muovendo qualcosa blocca tutto 
                if not game.used_movement: #se hai già usato il movimento questo turno, non puoi farlo di nuovo
                    if possibili_mosse and cella_attuale in possibili_mosse: #se clicchi in uno dei "quadrati blu"
                        flagged_cell.entities.move(cella_attuale) #muove la pedina in quel quadrato
                        flagged_cell.flagged = False #e rimuove i dovuti attributi
                        possibili_mosse = None
                        cella_attuale.flagged = True
                        flagged_cell= cella_attuale
                        game.used_movement=True
                        celle_attaccabili= flagged_cell.entities.calcola_attacchi(map.matrix)

                    elif cella_attuale.entities and game_field_rect.collidepoint(mouse): #se clicchi su una cella che ha un personaggio
                        if game.turno == cella_attuale.entities.team: # puoi cliccare solo le pedine della squadra a cui tocca
                            possibili_mosse, possibili_attacchi=cella_attuale.entities.calcola_mosse(map.matrix) #evidenzia le celle in cui esso può muoversi
                            cella_attuale.flagged = True
                            flagged_cell= cella_attuale
                    else: #se clicchi una cella "inutile", rimuove gli attributi e torna a non averla selezionata
                        possibili_mosse = None
                        cella_attuale.flagged = False
                        flagged_cell= None
                elif not game.used_attack:
                    if cella_attuale in celle_attaccabili:
                        flagged_cell.entities.attack(cella_attuale)
                        celle_attaccabili = None
                        game.used_attack = True
                        cella_attuale.flagged = False
                        flagged_cell= None
    pygame.display.update()
    fpsclock.tick(fps)
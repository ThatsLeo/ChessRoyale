import pygame
from game_settings import tile_size

arrow_point=pygame.transform.scale(pygame.image.load('background_assets/arrow/arrowpoint.png'),(tile_size,tile_size))
arrow_line=pygame.transform.scale(pygame.image.load('background_assets/arrow/arrowline.png'),(tile_size,tile_size))
arrow_curve=pygame.transform.scale(pygame.image.load('background_assets/arrow/arrowcurve.png'),(tile_size,tile_size))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, tile, img):
        super().__init__()
        self.tile = tile 
        self.image = img


def get_relative_pos(tile1,tile2):
    return (tile2.x-tile1.x,tile2.y-tile1.y) #se il primo elemento è negativo allora tile2 è sopra, se il secondo è negativo allora tile2 è a sinistra

def arrowing(path):
    arrows=[]
    arrow_path=[]
    if len(set(path))==1: return [],[] # caso in cui partenza e destinazione sono la stessa, la freccia non esiste
    for tile in range(len(path)):
        if path[tile]==path[0]: #caso della punta
            arrow = Arrow(path[tile], arrow_point)
            x, y = get_relative_pos(path[tile],path[tile+1]) #guardo la casella successiva nel path
            if x!=0:
                if x<0: arrow.image=pygame.transform.rotate(arrow.image, 180) #se è a sinistra
            else:
                if y>0: arrow.image=pygame.transform.rotate(arrow.image, 270) # se è in alto
                else: arrow.image=pygame.transform.rotate(arrow.image, 90) #se è in basso
            arrows.append(arrow)
            arrow_path.append(path[tile])
        else:
            if tile+1<len(path):
                w, z = get_relative_pos(path[tile-1],path[tile+1])
                if w!=0 and z!=0: #caso di curva
                    arrow = Arrow(path[tile], arrow_curve)
                    if w<0:
                        if z<0: #caso in alto a sx
                            if path[tile].x == path[tile-1].x: 
                                arrow.image=pygame.transform.flip(arrow.image, 1, 1)
                        else: #caso in basso a sx
                            if path[tile].x == path[tile-1].x:
                                arrow.image=pygame.transform.flip(arrow.image, 1,0)
                            else: #o da quella a destra
                                arrow.image=pygame.transform.flip(arrow.image, 0,1)
                    else:
                        if z<0: #caso in alto a dx
                            if path[tile].y == path[tile-1].y:
                                arrow.image=pygame.transform.flip(arrow.image, 1,0)
                            else: #o quella in basso
                                arrow.image=pygame.transform.flip(arrow.image, 0,1)
                        else: #caso in basso a dx
                            if path[tile].y == path[tile-1].y:
                                arrow.image=pygame.transform.flip(arrow.image, 1,1)
                    arrows.append(arrow)
                    arrow_path.append(path[tile])
                else: #caso di linea
                    arrow = Arrow(path[tile], arrow_line)
                    x, y = get_relative_pos(path[tile],path[tile+1])
                    if y!=0:
                        arrow.image=pygame.transform.rotate(arrow.image, 270) #se è verticale
                    arrows.append(arrow)
                    arrow_path.append(path[tile])
    return arrows[:-1], arrow_path[:-1] #levo l'ultimo perchè è la casella del personaggio
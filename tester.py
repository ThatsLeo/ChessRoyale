import pygame, sys

pygame.init()
schermox, schermoy = 800,500
screen=pygame.display.set_mode((schermox,schermoy))
clock = pygame.time.Clock()

class Cella(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos #posizione in pixel
        self.info = {}
        self.image = pygame.Surface((50,50))
        self.image.fill('White')
        self.rect = self.image.get_rect(topleft = pos)

class OggettoInfo(dict):
    def __init__(self, oggetto, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._oggetto = oggetto


test1 = Cella((0,0))
test2 = Cella((0,200))
moving={'test1': {'obj': test1, 'start': (test1.pos[0],test1.pos[1]), 'target': [(200,0),(200,200),(400,200),(400,400)], 'time': 0},
        'test2': {'obj': test2, 'start': (test2.pos[0],test2.pos[1]), 'target': [(200,200),(200,400)], 'time': 0}}
moving_time = 2 #secondi per giungere ogni destinazione

while True:
    t = clock.tick(30)/1000
    screen.fill("Black")

    if moving:
        for tile in moving.copy():
            obj= tile
            tile = moving[tile]
            tile['time']+=t

            time_ratio=tile['time']/moving_time
            if time_ratio>1:
                x=tile['target'][0][0]
                y=tile['target'][0][1]
                tile['target'].pop(0)
                if tile['target']:
                    tile['start']=(tile['obj'].pos[0],tile['obj'].pos[1])
                    tile['time'] = 0
                else:
                    moving.pop(obj)
                    continue
            else:
                new_x=tile['start'][0]+(tile['target'][0][0]-tile['start'][0])*time_ratio
                new_y=tile['start'][1]+(tile['target'][0][1]-tile['start'][1])*time_ratio
                tile['obj'].pos=(new_x,new_y)



    screen.blit(test1.image, test1.pos)
    screen.blit(test2.image, test2.pos)

    key_input=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
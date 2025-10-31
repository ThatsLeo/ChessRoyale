from game_settings import game
from map_settings import map
import pygame
pygame.font.init()

class Tasto(pygame.sprite.Sprite):
    def __init__(self, dim, pos, name, function, color="#ffffffff"):
        super().__init__()
        self.color = color
        self.name = name
        self.activate = function
        self.resize(dim, pos)
    def resize(self, new_dim, new_pos):
        self.dim = new_dim
        self.image = pygame.Surface(self.dim)
        self.image.fill(self.color)
        self.pos = new_pos
        self.rect = self.image.get_rect(topleft = self.pos)

        #parte per il text
        self.font_size = int(self.rect.height//2)
        self.font = pygame.font.SysFont('maiandragd', self.font_size)
        parts_names = self.name.split()
        parts=[self.font.render(part, True, (255, 255, 255)) for part in parts_names]
        
        if len(parts)==1:
            size = self.font.size(self.name)
            text_pos = ((self.dim[0]-size[0])/2, (self.dim[1]-size[1])/2)
            self.image.blit(parts[0], text_pos)
        else:
            part=parts_names[0]
            size1 = self.font.size(part)
            padding=size1[1]/3
            text_pos1 = ((self.dim[0]-size1[0])/2, (self.dim[1]-size1[1])/2-padding)
            self.image.blit(parts[0], text_pos1)

            part=parts_names[1]
            size2 = self.font.size(part)
            text_pos2 = ((self.dim[0]-size2[0])/2, (self.dim[1]-size2[1])/2+padding)
            self.image.blit(parts[1], text_pos2)

def end_turn():
    map.update_map(game.turno)
    game.turno = abs(game.turno-1) 
    game.fine_turno=False
    game.used_movement=False

def test_fun():
    print('diomerda')

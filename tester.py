import pygame
from game_settings import tile_size
mount_img = pygame.transform.scale(pygame.image.load('background_assets/montagna.png'), (tile_size, tile_size))
nails_img = pygame.transform.scale(pygame.image.load('background_assets/nails.png'), (tile_size, tile_size))
obstacles = pygame.sprite.Group()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, cur_cell, type):
        super().__init__()
        self.cur_cell = cur_cell
        match type:
            case 'mount':
                self.image = mount_img
                self.walkable = False
                self.hp = 10000
                self.dmg = 0
            case 'nails':
                self.image = nails_img
                self.walkable = True
                self.hp = 5
                self.dmg = 2
        self.rect = self.image.get_rect(topleft = cur_cell.pos)
    def update(self):
        self.rect.topleft=self.cur_cell.rect.topleft
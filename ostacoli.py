import pygame
from game_settings import tile_size
from movement_holder import is_shaking, add_shake

bomba_img = pygame.image.load('background_assets/bomba.png')
class Ostacolo(pygame.sprite.Sprite):
    def __init__(self, start_cell):
        super().__init__()
        self.pos = start_cell.pos #posizione in pixel
        self.cur_cell = start_cell #relativa cella in cui è dentro
        self.image = bomba_img
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft = self.pos)
        self.team = 2 #non fa parte nè del team 0 nè del team 1
        self.name = 'Bomba'
        self.desc = 'esplode'
        self.dmg = 1
        self.range = 1
        self.hp = 3
    def update(self):
        #self.check_attack()
        self.check_alive()
        self.rect = self.image.get_rect(topleft = self.pos)

    def get_damaged_animation(self):
        add_shake([self], 20, 0.7)
    
    def get_damaged(self, damage):
        self.get_damaged_animation()
        self.hp-=damage

    def check_alive(self): #se non ha più vita e non è in animazione di shake, viene rimosso
        if self.hp <=0 and not is_shaking(self):
            self.die()

    def die(self):
        self.kill()
        self.cur_cell.entities = None
        self.cur_cell.walkable = True
import pygame
from game_settings import tile_size
from movement_holder import is_shaking, add_shake

bomba_img = pygame.image.load('background_assets/bomba.png')

expl = pygame.Surface((tile_size,tile_size))
expl.fill("#CD5200")
expl.set_alpha(200)


class Ostacolo(pygame.sprite.Sprite):
    def __init__(self, start_cell):
        super().__init__()
        self.pos = start_cell.pos #posizione in pixel
        self.cur_cell = start_cell #relativa cella in cui è dentro
        self.image = bomba_img
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft = self.pos)
        self.team = 2 #non fa parte nè del team 0 nè del team 1
        self.name = 'Blank'
        self.desc = 'Blank'
        self.dmg = 0
        self.range = 0
        self.hp = 0
        self.dead = False

    def update(self, *args, **kwargs):
        self.rect = self.image.get_rect(topleft = self.pos)
        self.check_alive()
        self.check_die_animation(*args, **kwargs)

    def get_damaged_animation(self):
        add_shake([self], 20, 0.7)
    
    def get_damaged(self, damage):
        self.get_damaged_animation()
        self.hp-=damage
        self.on_damage()

    def check_alive(self): #se non ha più vita e non è in animazione di shake, viene rimosso
        if self.hp <=0 and not is_shaking(self) and not self.dead:
            self.dead = True
            self.start_death()
        if self.dead and not is_shaking(self):
            self.death_effect()
            self.die()

    def die(self):
        self.kill()
        self.cur_cell.entities = None
        self.cur_cell.walkable = True

    def death_effect(self): #se un ostacolo ha un effetto alla morte
        pass
    def start_death(self): #se un oggetto ha una animazione di morte
        pass
    def check_die_animation(self, *args, **kwargs):
        pass
    def on_damage(self): #se un ostacolo ha un effetto al danno
        pass

class Bomba(Ostacolo):
    def __init__(self, start_cell):
        super().__init__(start_cell)
        self.name = 'Bomba'
        self.desc = 'esplode'
        self.dmg = 1
        self.range = 1
        self.hp = 1
        self.exploding_cells=[]

    def explode(self, matrix, rows=8, cols=10):
        self.exploding_cells = []
        x, y = self.cur_cell.x, self.cur_cell.y

        for riga in range(-self.range, self.range + 1):
            for colonna in range(-self.range, self.range + 1):
                if riga == 0 and colonna == 0:
                    continue  # esclude la cella stessa della bomba
                r_tile, c_tile = x + riga, y + colonna
                if 0 <= r_tile < rows and 0 <= c_tile < cols:
                    self.exploding_cells.append(matrix[c_tile][r_tile])
        return self.exploding_cells
    
    def start_death(self):
        self.matrix = self._update_args["matrix"]
        self.explode(self.matrix)
        add_shake([self], 15, 1)
    
    def check_die_animation(self, *args, **kwargs):
        self._update_args = kwargs

        if self.dead:
            self.board = self._update_args["board"]
            for c in self.exploding_cells:
                self.board.blit(expl, c.pos)

    def death_effect(self):
        for c in self.exploding_cells:
            if c.entities and not getattr(c.entities, 'dead', False):
                c.entities.hp-=self.dmg
                c.entities.check_alive()
    

        
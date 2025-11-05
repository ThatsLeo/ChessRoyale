import pygame
from game_settings import tile_size
from movement_holder import add_move, add_shake, is_shaking

# direzioni possibili (su, giù, sinistra, destra)
directions = [(0,1), (0,-1), (1,0), (-1,0)]

class Personaggio(pygame.sprite.Sprite):
    def __init__(self, start_cell, team):
        super().__init__()
        self.pos = start_cell.pos #posizione in pixel
        self.cur_cell = start_cell #relativa cella in cui è dentro
        self.image = pygame.image.load('background_assets/nanodimerda.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft = self.pos)
        self.name = 'Nano di Merda'
        self.desc = 'è proprio un nano di merda!'
        self.dmg = 2
        self.hp = 5
        self.range = 2 #range di attacco
        self.team = team
        if self.team==1:
            self.image=pygame.transform.rotate(self.image, 180)
        self.attacking_enemy = False
        self.attacked_enemy = None

    def update(self):
        self.check_attack()
        self.check_alive()
        #self.pos = self.cur_cell.rect.topleft
        self.rect = self.image.get_rect(topleft = self.pos)

    def check_alive(self): #se non ha più vita e non è in animazione di shake, viene rimosso
        if self.hp <=0 and not is_shaking(self):
            self.die()

    def calcola_mosse(self, matrix, max_dist=3): #utilizzando BFS
        start = self.cur_cell

        self.possibili_mosse = [start]
        self.mosse_totali = []
        self.possibili_attacchi = set()
        self.parent = {} #questo servirà per costruire la freccia

        rows = len(matrix)
        cols = len(matrix[0])

        #utilizzo BFS, quindi una coda
        queue = [(start, 0)]  # inizializzo la coda con il l'elemento di start, per ogni elemento salvo la distanza (qui 0)
        visited = set([start])
        self.parent[start] = None 

        while len(queue) > 0: #finchè la coda non è vuota
            cell_, dist = queue.pop(0) #faccio il dequeue
            if dist >= max_dist:
                continue

            x, y = cell_.x, cell_.y

            for dy, dx in directions: #calcolo le celle vicine
                ny = y + dy
                nx = x + dx

                #effective_dist = abs(nx - start.x) + abs(ny - start.y) 
                if 0 <= ny < rows and 0 <= nx < cols: # controlla che la cella sia dentro la mappa/matrice
                    cell = matrix[ny][nx]
                    is_ally = getattr(cell.entities, "team", None)==self.team #verifica se una pedina è dello stesso team
                    if cell not in visited and (cell.walkable or is_ally) and (cell_ in self.mosse_totali or cell_==start): # controlla che la cella sia "valida"
                        visited.add(cell)
                        queue.append((matrix[ny][nx], dist + 1))
                        self.parent[matrix[ny][nx]] = cell_
                        if getattr(cell.entities, "team", None)!=self.team:
                            self.possibili_mosse.append(cell)
                        self.mosse_totali.append(cell) # mosse totali include le pedine alleate

        #BFS per calcolare gli attacchi
        queue = [(cell, 0) for cell in (self.possibili_mosse)]
        visited_attack = set(self.possibili_mosse)

        while len(queue) > 0:
            cell_, dist = queue.pop(0)
            if dist >= self.range:
                continue

            x, y = cell_.x, cell_.y

            for dy, dx in directions:
                ny = y + dy
                nx = x + dx
                if 0 <= ny < rows and 0 <= nx < cols:
                    cell = matrix[ny][nx]
                    if cell not in visited_attack:
                        visited_attack.add(cell)
                        queue.append((cell, dist + 1))
                        if cell!=start:
                            self.possibili_attacchi.add(cell)

        self.possibili_attacchi.update(self.possibili_mosse) #ggiungo le celle di movimento che sono sempre anche di attacco

        return self.possibili_mosse, self.possibili_attacchi
    
    def calcola_attacchi(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        queue = [(self.cur_cell, 0)]
        visited_attack = set([self.cur_cell])
        self.nemici_attaccabili = []

        while len(queue) > 0:
            cell_, dist = queue.pop(0)
            if dist >= self.range:
                continue

            x, y = cell_.x, cell_.y

            for dy, dx in directions:
                ny = y + dy
                nx = x + dx
                if 0 <= ny < rows and 0 <= nx < cols:
                    cell = matrix[ny][nx]
                    if cell not in visited_attack:
                        visited_attack.add(cell)
                        queue.append((cell, dist + 1))
                        if getattr(cell.entities,'team',self.team)!=self.team:
                            self.nemici_attaccabili.append(cell)
        return self.nemici_attaccabili

    def find_path(self, tile):
        self.path=[tile]
        cur_tile = tile
        while self.parent[cur_tile]:
            self.path.append(self.parent[cur_tile])
            cur_tile=self.parent[cur_tile]
        self.path.append(self.cur_cell) #aggiungo un elemento finale che rappresenta l'inizio della freccia
        return self.path

    def move(self, tile):
        targets = [x.pos for x in reversed(self.path[:-2])]
        add_move(self, targets, moving_time=0.5) #alto moving time = più lento
        self.pos = tile.pos
        self.cur_cell.entities = None
        self.cur_cell.walkable = True
        tile.entities = self
        tile.walkable = False
        self.cur_cell = tile

    def attack(self, enemy):
        enemy_target_pos= ((enemy.pos[0]+self.cur_cell.pos[0])/2, (enemy.pos[1]+self.cur_cell.pos[1])/2)
        add_move(self, [enemy_target_pos, self.cur_cell.pos], moving_time=0.2)
        self.attacking_enemy = True
        self.attacked_enemy = (enemy.entities, enemy_target_pos)

    def check_attack(self):
        if self.attacking_enemy: #se sta facendo l'animazione di attacco
            if self.pos == self.attacked_enemy[1]:
                self.attacked_enemy[0].get_damaged(self.dmg)
                self.attacking_enemy=False
                self.attacked_enemy = None

    def get_damaged_animation(self):
        add_shake([self], 20, 0.7)
    
    def get_damaged(self, damage):
        self.get_damaged_animation()
        self.hp-=damage

    def die(self):
        self.kill()
        self.cur_cell.entities = None
        
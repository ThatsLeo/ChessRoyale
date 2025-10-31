import pygame
from game_settings import tile_size
from movement_holder import add_move

# direzioni possibili (su, giù, sinistra, destra)
directions = [(0,1), (0,-1), (1,0), (-1,0)]

class Personaggio(pygame.sprite.Sprite):
    def __init__(self, start_cell, team):
        super().__init__()
        self.pos = start_cell.pos #posizione in pixel
        self.cur_cell = start_cell #relativa cella in cui è dentro
        self.image = pygame.image.load('background_assets/nanodimerda.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.name = 'Nano di Merda'
        self.desc = 'è proprio un nano di merda!'
        self.range = 2 #range di attacco
        self.rect = self.image.get_rect(topleft = self.pos)
        self.team = team
        if self.team==1:
            self.image=pygame.transform.rotate(self.image, 180)
    def update(self):
        self.pos = self.cur_cell.rect.topleft
        self.rect = self.image.get_rect(topleft = self.pos)
    def calcola_mosse(self, matrix, max_dist=3): #utilizzando BFS
        #max_dist-=1 #levo 1 pk sennò ne conta una in più...
        self.possibili_mosse = []
        self.mosse_totali = []
        self.possibili_attacchi = set()
        self.parent = {} #questo servirà per costruire la freccia

        start = self.cur_cell

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
        add_move(self, reversed(self.path[:-2]), moving_time=0.5) #alto moving time = più lento
        self.pos = tile.pos
        self.cur_cell.entities = None
        self.cur_cell.walkable = True
        tile.entities = self
        tile.walkable = False
        self.cur_cell = tile
        
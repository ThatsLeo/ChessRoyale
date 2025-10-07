import pygame, sys
import time

pygame.init()

fps = 12
schermox, schermoy = 800,500
screen=pygame.display.set_mode((schermox,schermoy))

class RunningPoint:
    def __init__(self, screen_width, screen_height, time: float):
        self.xpos = 1
        self.ypos = 1
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.time = time

    def update(self):
        """Aggiorna la posizione del punto per un frame"""
        self.xpos += 1
        if self.xpos >= self.screen_width:
            self.xpos = 1
            self.ypos += 1
        if self.ypos > self.screen_height:
            self.ypos = 1
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, self.xpos, self.ypos))

class Menu:
    def __init__(self, screen: pygame.display, width: int, height: int, borderWidth: int, color=(int, int, int)):
        self.screen = screen
        if color is None:
            color = (255, 255, 255)
        else: 
            self.color = color
        
        self.screenWidth, self.screenHeight = screen.get_size()
        
        if height > self.screenHeight or width > self.screenWidth:
            raise ValueError("Menu dimensions exceed screen dimensions")
        
        self.x = (self.screenWidth - width) // 2
        self.y = (self.screenHeight - height) // 2

        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.borderWidth = borderWidth
        self.active = False
    
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
    
    def window_state(self):
        return self.active

    def draw(self):
        if self.active:
            pygame.draw.rect(self.screen, self.color, self.rect, self.borderWidth)

# Inizializzazione
menu = Menu(screen, 400, 300, 5, color=(200, 200, 200))
running_point = RunningPoint(schermox, schermoy, 0.01)
clock = pygame.time.Clock()

last_update_time = time.time()
last_running_point_update = time.time()

# Game loop principale
while True:
    current_time = time.time()
    
    # Gestione eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if menu.window_state():
                    menu.deactivate()
                else:
                    menu.activate()

    # Ogni running_point.time secondi vengono aggiornate le coordinate del punto
    if current_time - last_running_point_update >= running_point.time:
        last_running_point_update = current_time
        running_point.update()
    
    # REFRESH DELLO SCHERMO: solo ogni 1/fps secondi
    if current_time - last_update_time >= float(1/fps):
        last_update_time = current_time
        
        # Pulisce lo schermo
        screen.fill((0, 0, 0))
        
        # Disegna tutto
        running_point.draw(screen)
        menu.draw()
        
        # Mostra le modifiche
        pygame.display.flip()
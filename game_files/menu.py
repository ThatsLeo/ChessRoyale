import pygame, sys
import time

pygame.init()

fps = 60
schermox, schermoy = 1820,1000
screen=pygame.display.set_mode((schermox,schermoy), pygame.RESIZABLE)

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

class Menu(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.display, width: int, height: int, borderWidth: int, color=(int, int, int)):
        super().__init__()

        self.highlighted_option = 0
        self.selected_option = -1

        self.box_size = [width, height]
        self.screen = screen
        self.options = []
        self.screenWidth, self.screenHeight = screen.get_size()
        self.ratio = width / height

        if color is None:
            color = (255, 255, 255)
        else: 
            self.color = color
        
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

    # Disegna il menu con le relative opzioni con un paddding centrato verticalmente nel box
    def draw(self):
        if self.active:
            pygame.draw.rect(self.screen, self.color, self.rect, self.borderWidth) 
            
            option_size = [None, None] 
            
            option_size[0] = int(self.box_size[0] / 3)
            option_size[1] = int(self.box_size[1] / 6)
            paddingY = self.screenHeight * 0.02

            xPos = self.x + (self.box_size[0] / 2) - (option_size[0] / 2)
            yPos = self.y + (self.box_size[1] / 2) - (option_size[1] / 2) * len(self.options) - paddingY
            for option in range(len(self.options)):
                if option == self.highlighted_option:
                    pygame.draw.rect(self.screen, (255, 0, 0), (xPos, yPos, option_size[0], option_size[1]), self.borderWidth)
                else:
                    pygame.draw.rect(self.screen, self.color, (xPos, yPos, option_size[0], option_size[1]), self.borderWidth)
                yPos += option_size[1] + paddingY

    # Gestione dei keypress da tastiera, solo se il menu è attivo(non ancora gestisce il mouse)
    def handle_event(self, event):
        match event.key:
            case pygame.K_SPACE:
                if self.window_state():
                    self.deactivate()
                else:
                    self.activate()
            case pygame.K_UP:
                if self.window_state():
                    self.highlighted_option -= 1
            case pygame.K_DOWN:
                if self.window_state():
                    self.highlighted_option += 1
            case _:
                pass
        if self.highlighted_option < 0: 
            self.highlighted_option = len(self.options) - 1
        elif self.highlighted_option >= len(self.options): 
            self.highlighted_option = 0

    # Resize del menu in base alla nuova dimensione della finestra
    def resize(self, new_width, new_height):
        if new_width > self.screenWidth:
            self.box_size[0] += (new_width - self.screenWidth) / 2
            self.box_size[1] += (new_width - self.screenWidth) * (self.ratio / 2)
        
        elif new_width < self.screenWidth:
            self.box_size[0] -= (self.screenWidth - new_width) / 2
            self.box_size[1] -= (self.screenWidth - new_width) * (self.ratio / 2)


        if new_height > self.screenHeight:
            self.box_size[1] += (new_height - self.screenHeight) / 2
            self.box_size[0] += (new_height - self.screenHeight) * (self.ratio / 2)

        elif new_height < self.screenHeight:
            self.box_size[1] -= (self.screenHeight - new_height) / 2
            self.box_size[0] -= (self.screenHeight - new_height) * (self.ratio / 2)

        self.screenWidth, self.screenHeight = new_width, new_height
        self.x = (self.screenWidth - self.box_size[0]) // 2
        self.y = (self.screenHeight - self.box_size[1]) // 2
        self.rect = pygame.Rect(self.x, self.y, self.box_size[0], self.box_size[1])
        


            

    def set_options(self,lista: list[str] ):
        for opzione in lista:
            self.options.append(opzione)


# Inizializzazione
menu = Menu(screen, 400, 300, 3, color=(200, 200, 200))
menu.set_options(["Start Game", "Options", "Exit"])
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
            menu.handle_event(event)
        elif event.type == pygame.VIDEORESIZE:
            menu.resize(event.w, event.h)
            

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
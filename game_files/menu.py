import window_handler
import pygame, sys
import time

pygame.init()

fps = 60
schermox, schermoy = 1280,720
finestra = window_handler.window(schermox, schermoy, fps)

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

        self.options = [" "]
        self.highlighted_option = self.options[0]
        self.selected_option = 0

        self.box_size = [width, height]
        self.screen = screen
        
        self.screenWidth, self.screenHeight = screen.get_size()
        self.ratio = width / height
        self.original_size = (width, height)
        self.original_screen_size = (self.screenWidth, self.screenHeight)

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
            paddingX = self.screenWidth * 0.04

            max_options_in_column = int((self.box_size[1] - paddingY) / (option_size[1] + paddingY))
            max_options_in_column = max(1, max_options_in_column) 
            n_columns = (len(self.options) + max_options_in_column - 1) // max_options_in_column
            
            options_per_column = len(self.options) / n_columns
            if options_per_column > int(options_per_column): options_per_column = int(options_per_column) + 1 
            else: options_per_column = int(options_per_column)

            if n_columns > int(n_columns):
                n_columns = int(n_columns) + 1

            total_columns_width = (option_size[0] * n_columns) + (paddingX * (n_columns - 1))
            xPos = self.x + (self.box_size[0] - total_columns_width) / 2
            
            yPos = self.y + (self.box_size[1] / 2) - (option_size[1] / 2) * options_per_column - paddingY

            pygame.draw.rect(self.screen, self.color,(self.x + self.box_size[0]/2 - 4, self.y, 8, self.box_size[1]))

            counter = 0     
            for option in self.options:
                if option == self.highlighted_option:
                    pygame.draw.rect(self.screen, (255, 0, 0), (xPos, yPos, option_size[0], option_size[1]), self.borderWidth)
                else:
                    pygame.draw.rect(self.screen, self.color, (xPos, yPos, option_size[0], option_size[1]), self.borderWidth)
                yPos += option_size[1] + paddingY
                    
                counter += 1
                    
                if counter >= options_per_column: 
                    counter = 0
                    xPos += option_size[0] + paddingX
                    yPos = self.y + (self.box_size[1] / 2) - (option_size[1] / 2) * options_per_column - paddingY

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
                    self.selected_option -= 1
            
            case pygame.K_DOWN:
                if self.window_state():
                    self.selected_option += 1
                          
            case _:
                pass
        
        if self.selected_option < 0:
            self.selected_option = len(self.options) - 1 
            self.highlighted_option = self.options[len(self.options) - 1]
        
        elif self.selected_option >= len(self.options): 
            self.selected_option = 0
            self.highlighted_option = self.options[0]
        else:
            self.highlighted_option = self.options[self.selected_option]

    # Resize del menu in base alla nuova dimensione della finestra
    def resize(self):
        new_width, new_height = self.screen.get_size()
        if new_width != self.screenWidth or new_height != self.screenHeight:
            self.box_size[0] = (new_width * self.original_size[0]) // self.original_screen_size[0]
            self.box_size[1] = (self.box_size[0] * self.original_size[1]) // self.original_size[0]

        self.screenWidth, self.screenHeight = new_width, new_height
        self.x = (self.screenWidth - self.box_size[0]) // 2
        self.y = (self.screenHeight - self.box_size[1]) // 2
        self.rect = pygame.Rect(self.x, self.y, self.box_size[0], self.box_size[1])
        
            

    def set_options(self,lista: list[str] ):
        for opzione in lista:
            self.options.append(opzione)


# Inizializzazione
menu = Menu(finestra.screen, 400, 300, 3, color=(200, 200, 200))
menu.set_options(["Start Game", "Options", "Palle", "Pene", "Exit", "Altro"])
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
            finestra.resize(event.w, event.h)
            menu.screen = finestra.screen
            menu.resize()


    # Ogni running_point.time secondi vengono aggiornate le coordinate del punto
    if current_time - last_running_point_update >= running_point.time:
        last_running_point_update = current_time
        running_point.update()
    
    # REFRESH DELLO SCHERMO: solo ogni 1/fps secondi
    if current_time - last_update_time >= float(1/fps):
        last_update_time = current_time
        
        # Pulisce lo schermo
        finestra.screen.fill((0, 0, 0))
        
        # Disegna tutto
        running_point.draw(finestra.screen)
        menu.draw()
        
        # Mostra le modifiche
        pygame.display.flip()
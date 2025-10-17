import enum
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

class Position():
    CENTER = 0
    TOP = 1
    BOTTOM = 2
    class Padding():
        CENTER = 0
        LEFT = 1
        RIGHT = 2


class Menu(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.display, width: int, height: int, borderWidth: int,
                  position: Position = Position.CENTER, padding: Position.Padding = Position.Padding.CENTER, color=(int, int, int)):
        super().__init__()

        self.options = [" "]
        self.highlighted_option = self.options[0]
        self.selected_option = 0
        self.options_per_col = None
        self.position = position
        self.padding = padding

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
        
        self.update_position()

        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.borderWidth = borderWidth
        self.active = False

    def update_position(self):
        match self.position:
            case Position.CENTER:
                self.y = (self.screenHeight - self.box_size[1]) // 2
            case Position.TOP:
                self.y = self.screenHeight - (self.screenHeight * 99/100) 
            case Position.BOTTOM:
                self.y = self.screenHeight - (self.screenHeight * 1/100) - self.box_size[1]
        match self.padding:
            case Position.Padding.CENTER:
                self.x = (self.screenWidth - self.box_size[0]) // 2
            case Position.Padding.LEFT:
                self.x = self.screenWidth * 0.01
            case Position.Padding.RIGHT:
                self.x = self.screenWidth - (self.screenWidth * 0.01) - self.box_size[0] 

    def window_state(self):
        return self.active
    
    def toggle(self):
        self.active = not self.active

    # Disegna il menu con le relative opzioni con un paddding centrato verticalmente nel box
    def draw(self):
        if self.active:

            pygame.font.init() 
            my_font = pygame.font.SysFont('Arial MS', 30)
            
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

            self.options_per_col = options_per_column

            if n_columns > int(n_columns):
                n_columns = int(n_columns) + 1

            total_columns_width = (option_size[0] * n_columns) + (paddingX * (n_columns - 1))
            total_options_height = (option_size[1] * options_per_column) + (paddingY * (options_per_column - 1))

            while total_columns_width > self.box_size[0]:
                if paddingX <= 10: break
                paddingX -= 1
                total_columns_width = (option_size[0] * n_columns) + (paddingX * (n_columns - 1))

            
            xPos = self.x + (self.box_size[0] - total_columns_width) / 2
            yPos = self.y + (self.box_size[1] - total_options_height) / 2

            counter = 0
            for option in self.options:
                text_surface = my_font.render(option, False, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(xPos + option_size[0] / 2, yPos + option_size[1] / 2))
                self.screen.blit(text_surface, text_rect)

                if option == self.highlighted_option:
                    pygame.draw.rect(self.screen, (255, 0, 0), (xPos, yPos, option_size[0], option_size[1]), self.borderWidth)
                else:
                    pygame.draw.rect(self.screen, self.color, (xPos, yPos, option_size[0], option_size[1]), self.borderWidth)
                yPos += option_size[1] + paddingY
                    
                counter += 1
                    
                if counter >= options_per_column: 
                    counter = 0
                    xPos += option_size[0] + paddingX
                    yPos = self.y + (self.box_size[1] - total_options_height) / 2

    # Gestione dei keypress da tastiera, solo se il menu è attivo(non ancora gestisce il mouse)
    def handle_event(self, event):
        
        if event.key == pygame.K_SPACE:
            self.toggle()

        if self.window_state():
            
            match event.key:
                case pygame.K_UP:
                    self.selected_option -= 1
                
                case pygame.K_DOWN:
                    self.selected_option += 1
                
                case pygame.K_LEFT:
                    self.selected_option -= self.options_per_col
                    if self.selected_option < 0:
                        self.selected_option += self.options_per_col * 2 
                
                case pygame.K_RIGHT:
                    self.selected_option += self.options_per_col
                    if self.selected_option >= len(self.options):
                        self.selected_option -= self.options_per_col * 2

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
        
        self.update_position()
        self.rect = pygame.Rect(self.x, self.y, self.box_size[0], self.box_size[1])
        
            

    def set_options(self,lista: list[str] ):
        self.options = lista


# Inizializzazione
menu = Menu(finestra.screen, 400, 300, 3, Position.BOTTOM, Position.Padding.RIGHT, color=(200, 200, 200))
menu.set_options(["Start Game", "Options", "Palle", "Pene", "Exit", "Altro", "Opzione 7", "Opzione 8"])
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
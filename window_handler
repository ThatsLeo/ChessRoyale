import pygame, sys

class window():
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps

    def resize(self, width, height):
        self.width = width
        self.height = height

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.fps

pygame.init()

screen_info = window(300, 300, 30)

htiles = 16
wtiles = 10

tile_size = 48

screen = pygame.display.set_mode((screen_info.width, screen_info.height), pygame.RESIZABLE)


def check_tile_size():
    global tile_size
    step = 2
    min_size = 16

    while (screen_info.width < wtiles * tile_size) or (screen_info.height < htiles * tile_size):
        tile_size -= step
        if tile_size < min_size:
            tile_size = min_size
            break

    while (screen_info.width >= wtiles * (tile_size + step)) and (screen_info.height >= htiles * (tile_size + step)):
        tile_size += step

image = pygame.image.load('background_assets/cella.png')
nanodimerda = pygame.image.load('background_assets/nanodimerda.png')
def draw_grid():
    center_x = screen_info.width / 2
    center_y = screen_info.height / 2

    total_w = wtiles * tile_size
    total_h = htiles * tile_size

    start_x = int(center_x - total_w / 2)
    start_y = int(center_y - total_h / 2)
    scaled_image = pygame.transform.scale(image, (tile_size, tile_size))
    scaled_nano = pygame.transform.scale(nanodimerda, (tile_size, tile_size))

    for row in range(htiles):
        for col in range(wtiles):
            x = start_x + col * tile_size
            y = start_y + row * tile_size
            screen.blit(scaled_image, (x, y))
            screen.blit(scaled_nano, (x, y))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, tile_size, tile_size), 1)
            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            screen_info.resize(event.w, event.h)
            screen = pygame.display.set_mode((screen_info.width, screen_info.height), pygame.RESIZABLE)
            check_tile_size()

    screen.fill((0, 0, 0))
    draw_grid()
    pygame.display.flip()
    pygame.time.Clock().tick(screen_info.get_fps())
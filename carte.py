import pygame, sys
from pygame.locals import *

pygame.init()
schermox, schermoy = 800,500
screen=pygame.display.set_mode((schermox,schermoy))
clock = pygame.time.Clock()

class Menu_Carte_Aperto:
    def __init__(self, carte):
        self.carte = carte
        self.n_carte = len(carte)
        self.show = False
    def calcola_pos(self):
        len_carta = self.carte[0].dim[0] #lunghezza carta in x
        sep=round(schermox/50)
        if sep%2 == 1: sep+=1 # in caso non fosse pari
        for n, c in enumerate(self.carte):
            shift=-1*(self.n_carte-1)*(len_carta+sep)/2+(len_carta+sep)*n
            c.rect = c.image.get_rect(center = (schermox/2+shift, schermoy/2))
    def draw(self, display):
        for c in self.carte:
            display.blit(c.image, c.rect.topleft)
    def toggle(self):
        self.show = not self.show

class Menu_Carte(pygame.sprite.Sprite):
    def __init__(self, n_carte):
        super().__init__()
        self.n_carte = n_carte
        self.dim = (schermox/2, schermoy/8)
        self.image = pygame.Surface(self.dim)
        self.image.fill('White')
        self.rect = self.image.get_rect(midbottom = (schermox/2, schermoy))
        self.show = True
    def toggle(self):
        self.show = not self.show

class Carta(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dim = (schermox/6, schermoy/2.5)
        self.image = pygame.Surface(self.dim)
        self.image.fill('White')
        self.rect = self.image.get_rect(center = (200, schermoy/2))
        
menu_carte= Menu_Carte(3)
menu_carte_group = pygame.sprite.GroupSingle(menu_carte)
c=[]
for i in range(5): c.append(Carta())
carte = Menu_Carte_Aperto(c)



card_clicked = False
while True:
    screen.fill("Black")
    key_input=pygame.key.get_pressed()
    if menu_carte.show:
        menu_carte_group.draw(screen)
    else:
        carte.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if carte.show:
                for card in carte.carte:
                    if card.rect.collidepoint(mouse_pos):
                        card_clicked = True
                        pass # usa quella carta
                if not card_clicked: #se non clicchi una carta, esci dal menu
                    menu_carte.toggle()
                    carte.toggle()
            if menu_carte.show and menu_carte.rect.collidepoint(mouse_pos):
                carte.calcola_pos()
                menu_carte.toggle()
                carte.toggle()
                

    pygame.display.update()
    clock.tick(30)
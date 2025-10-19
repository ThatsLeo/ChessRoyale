import pygame
from game_settings import *
info_section = pygame.Surface((schermox,info_section_height))
info_section.fill("#1F1152")
img_padding=info_section_height/5
img_dim = info_section_height*3/5
grass_img = pygame.transform.scale(pygame.image.load('background_assets/cella.png'), (img_dim, img_dim))
img_x, img_y = img_padding*2, img_padding

cornice_dim= img_dim*1.2
cornice_padding = img_dim*0.2/2
cornice_img = pygame.transform.scale(pygame.image.load('background_assets/cornice.png'), (cornice_dim, cornice_dim))
cornice_x, cornice_y = img_x-cornice_padding, img_y-cornice_padding

info_section.blit(grass_img, (img_x,img_y))
info_section.blit(cornice_img, (cornice_x,cornice_y))
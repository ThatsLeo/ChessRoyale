import pygame
from game_settings import *
from buttons import Tasto, test_fun, end_turn
pygame.font.init()
class InfoSection:
    def __init__(self, info_section_height):
        self.image = pygame.Surface((schermox,info_section_height))
        self.cell_name = ''
        self.cell_desc = ''
        self.turn = Tasto((10,10), (0,0), 'FINE TURNO', end_turn, color="#0a27e7ff")
        self.shop = Tasto((10,10), (0,0), 'SHOP', test_fun, color="#1aed06ff")
        self.tasti = pygame.sprite.Group(self.turn, self.shop)
        self.resize(info_section_height)
    def resize(self, info_section_height):
        self.info_section_height = info_section_height
        self.image= pygame.transform.scale(self.image, (schermox,info_section_height))
        img_padding=info_section_height/5
        self.img_dim = info_section_height*3/5
        self.img_x, self.img_y = img_padding*2, img_padding
        self.cur_img = pygame.transform.scale(pygame.image.load('background_assets/cella.png'), (self.img_dim, self.img_dim))

        cornice_dim= self.img_dim*1.2
        self.cornice_img = pygame.transform.scale(pygame.image.load('background_assets/cornice.png'), (cornice_dim, cornice_dim))
        cornice_padding = self.img_dim*0.2/2
        self.cornice_x, self.cornice_y = self.img_x-cornice_padding, self.img_y-cornice_padding

        name_font_size = int(self.img_dim//2.5)
        self.name_font = pygame.font.SysFont('maiandragd', name_font_size)
        self.name_x, self.name_y = img_padding*4+self.img_x, img_padding-cornice_padding

        desc_font_size = int(name_font_size*2//3)
        self.desc_font = pygame.font.SysFont('maiandragd', desc_font_size)
        self.desc_x, self.desc_y = self.name_x, self.name_y*3.5

        stats_font_size = int(name_font_size*2//3)
        self.stats_font = pygame.font.SysFont('maiandragd', stats_font_size)
        stats_text_height = self.stats_font.size('render')[1]
        stats_text_padding = stats_text_height/4
        self.stats_dmg_pos = (self.name_x*2.9, self.info_section_height/2-stats_text_padding-1.5*stats_text_height)
        self.stats_range_pos = (self.name_x*2.9, (self.info_section_height-stats_text_height)/2)
        self.stats_hp_pos = (self.name_x*2.9, self.info_section_height/2+stats_text_padding+stats_text_height/2)

        tasti_dim_x, tasti_dim_y = schermox/6,info_section_height/3
        tasti_padding = tasti_dim_y/3
        turn_pos = (schermox-tasti_dim_x-tasti_padding, tasti_padding)
        shop_pos = (schermox-tasti_dim_x-tasti_padding, tasti_padding*2+tasti_dim_y)
        self.turn.resize((tasti_dim_x, tasti_dim_y), turn_pos)
        self.shop.resize((tasti_dim_x, tasti_dim_y), shop_pos)
        
    def draw(self, display):
        display.blit(self.image,(0,tile_size*10))
        self.image.fill("#1F1152")
        self.image.blit(self.cur_img, (self.img_x,self.img_y))
        self.image.blit(self.cornice_img, (self.cornice_x,self.cornice_y))
        
        self.image.blit(self.name_surface, (self.name_x, self.name_y))
        self.image.blit(self.desc_surface, (self.desc_x, self.desc_y))

        if self.cur_cell.entities:
            self.image.blit(self.stats_atk_surface, self.stats_dmg_pos)
            self.image.blit(self.stats_range_surface, self.stats_range_pos)
            self.image.blit(self.stats_hp_surface, self.stats_hp_pos)

        self.tasti.draw(self.image)
        

    def update_info_menu(self, cell):
        self.cur_cell=cell
        self.cur_img = pygame.transform.scale(cell.image.copy(), (self.img_dim, self.img_dim))

        self.name_surface = self.name_font.render(self.cell_name, True, (255, 255, 255))
        self.desc_surface = self.desc_font.render(self.cell_desc, True, (255, 255, 255))

        if self.cur_cell.entities:
            pg = self.cur_cell.entities
            self.stats_atk_surface = self.stats_font.render(f'danno: {pg.dmg}', True, (255, 255, 255))
            self.stats_range_surface = self.stats_font.render(f'range: {pg.range}', True, (255, 255, 255))
            self.stats_hp_surface = self.stats_font.render(f'vita: {pg.hp}', True, (255, 255, 255))

        if cell.entities: #se c'è un personaggio sopra lo integra e usa le sue descrizioni
            self.cur_img.blit(pygame.transform.scale(cell.entities.image.copy(), (self.img_dim, self.img_dim)),(0,0))
            self.cell_name = cell.entities.name
            self.cell_desc = cell.entities.desc
        else:
            self.cell_name = cell.name
            self.cell_desc = cell.desc
    def check_tasti_click(self, mouse):
        for tasto in self.tasti:
            if tasto.image.get_rect(topleft=(tasto.pos[0],tasto.pos[1]+tile_size*10)).collidepoint(mouse):
                tasto.activate()
        

info_section = InfoSection(info_section_height)
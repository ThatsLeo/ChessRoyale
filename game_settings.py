fps = 30
tile_size = 64
info_section_height = tile_size*1.5
schermox, schermoy = tile_size*8,tile_size*10+info_section_height


class Game_state:
    def __init__(self):
        self.turno= 0
        self.fine_turno = False
        self.used_movement = False
        self.used_attack = False
        self.moving = None
game = Game_state()
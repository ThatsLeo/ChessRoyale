fps = 30
tile_size = 64
info_section_height = tile_size*1.5
schermox, schermoy = tile_size*8,tile_size*10+info_section_height


class Game_state:
    def __init__(self, turno, fine_turno, used_movement):
        self.turno= turno
        self.fine_turno = fine_turno
        self.used_movement = used_movement
game = Game_state(0, False, False)
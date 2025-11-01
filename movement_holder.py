from game_settings import fps
from random import randint

moving_objects={}

def add_move(obj, targets, moving_time = 2):
    moving_objects[str(id(obj))] = {'obj': obj, 'start': (obj.pos[0],obj.pos[1]), 'target': targets, 'time': 0, 'moving_time': moving_time}

#obj: oggetto in questione
#start: punto di inizio del movimento (si resetta ogni casella)
#target: insieme di caselle da raggiungere (come fossero delle tappe)
#time: variabile che si resetta in automatico per capire se ha giunto destinazione
#moving_time: secondi per passare alla cella successiva (quindi se è alto è più lento)

shaking_objects={}

def add_shake(tiles, intensity, duration):
    moving_time = 0.07
    shake_offsets=[]
    for _ in range(int(duration//moving_time/2)-1): #duration cambia la lunghezza della lista target
        shake_offsets.append(randint(0,intensity)) #intensity varia quanti pixel si muove di shake
        shake_offsets.append(randint(-intensity,0))
    shake_offsets.append(0)
    for tile in tiles:
        shaking_objects[str(id(tile))] = {'obj': tile, 'default': tile.pos[0], 'offsets': shake_offsets.copy(), 'time': 0, 'moving_time': moving_time}


t=1/fps
def check_movement():
    if not moving_objects and not shaking_objects:
        return False
    if moving_objects: 
        for tile in moving_objects.copy():
            obj = tile
            tile = moving_objects[tile]
            if not tile['target']: #caso in cui la pedina non si muove di alcuna casella
                moving_objects.pop(obj)
                continue 
            tile['time']+=t

            time_ratio=tile['time']/tile['moving_time']
            if time_ratio>1: #ha raggiunto il primo target
                tile['obj'].pos = tile['target'][0]
                if getattr(tile['obj'], 'entities', None):
                    tile['obj'].entities.pos = tile['target'][0]
                tile['obj'].rect.x=tile['target'][0][0]
                tile['obj'].rect.y=tile['target'][0][1]
                tile['target'].pop(0)
                if tile['target']:
                    tile['start']=(tile['obj'].rect.x,tile['obj'].rect.y)
                    tile['time'] = 0
                else:
                    moving_objects.pop(obj)
                    if getattr(tile['obj'], 'y', 5)>9 or getattr(tile['obj'], 'y', 5)<0: #se una cella va sotto o sopra lo schermo lo rimuove
                        tile['obj'].kill()
            else:
                x = tile['start'][0]+(tile['target'][0][0]-tile['start'][0])*time_ratio
                y = tile['start'][1]+(tile['target'][0][1]-tile['start'][1])*time_ratio
                tile['obj'].pos = (x,y)
                if getattr(tile['obj'], 'entities', None):
                    tile['obj'].entities.pos = (x,y)
                tile['obj'].rect.x = x
                tile['obj'].rect.y = y

    if shaking_objects: 
        for tile in shaking_objects.copy():
            obj = tile
            tile = shaking_objects[tile]
            tile['time']+=t
            time_ratio=tile['time']/tile['moving_time']
            if time_ratio>1:
                tile['obj'].rect.x=tile['default']+tile['offsets'][0]
                tile['offsets'].pop(0)
                if tile['offsets']:
                    tile['time'] = 0
                else:
                    shaking_objects.pop(obj)
            else:
                tile['obj'].rect.x=tile['default']+tile['offsets'][0]*time_ratio
                if getattr(tile['obj'], 'entities', None): #se c'è una pedina in una casella che scuote, scuote anche essa
                    tile['obj'].entities.pos = (tile['default']+tile['offsets'][0]*time_ratio,tile['obj'].entities.pos[1])
    return True

def check_shaking(obj):
    return True if str(id(obj)) in shaking_objects else False 
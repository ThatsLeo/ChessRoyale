from game_settings import fps

moving_objects={}

def add_move(obj, targets, moving_time = 2):
    if hasattr(obj, 'team'): #controlla se è una pedina 
        temp=[]
        for cell in targets:
            temp.append(cell.pos) 
        targets=temp
    moving_objects[str(id(obj))] = {'obj': obj, 'start': (obj.pos[0],obj.pos[1]), 'target': targets, 'time': 0, 'moving_time': moving_time}

#obj: oggetto in questione
#start: punto di inizio del movimento (si resetta ogni casella)
#target: insieme di caselle da raggiungere (come fossero delle tappe)
#time: variabile che si resetta in automatico per capire se ha giunto destinazione
#moving_time: secondi per passare alla cella successiva (quindi se è alto è più lento)



def check_movement():
    if moving_objects:
        t=fps/1000 
        for tile in moving_objects.copy():
            obj= tile
            tile = moving_objects[tile]
            tile['time']+=t

            time_ratio=tile['time']/tile['moving_time']
            if time_ratio>1:
                tile['obj'].rect.x=tile['target'][0][0]
                tile['obj'].rect.y=tile['target'][0][1]
                tile['target'].pop(0)
                if tile['target']:
                    tile['start']=(tile['obj'].rect.x,tile['obj'].rect.y)
                    tile['time'] = 0
                else:
                    moving_objects.pop(obj)
                    if getattr(obj, 'y', 5)>9 or getattr(obj, 'y', 5)<0: #se una cella va sotto o sopra lo schermo lo rimuove
                        obj.kill()
            else:
                tile['obj'].rect.x=tile['start'][0]+(tile['target'][0][0]-tile['start'][0])*time_ratio
                tile['obj'].rect.y=tile['start'][1]+(tile['target'][0][1]-tile['start'][1])*time_ratio

            


# world[0] : 백그라운드 객체들
# world[1] : foreground 객체들
from grass import Grass
world = [[],[]]

def add_object(o, depth):
    world[depth].append(o)

def create_world():
    grass1 = Grass(400,50)
    add_object(grass1, 0)

    grass2 = Grass(400, 30)
    add_object(grass2, 0)

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    print(f'CRITICAL : 존재하지않는 객체{o}를 지우려고 합니다.')
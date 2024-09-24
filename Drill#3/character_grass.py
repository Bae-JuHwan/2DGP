from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
boy = load_image('character.png')

def run_circle():
    r, cx, cy = 300, 800 // 2, 600 // 2

    for degree in range(0, 360, 3):
        theta = math.radians(degree)
        x = r * math.cos(theta) + cx
        y = r * math.sin(theta) + cy
        
        clear_canvas_now()
        boy.draw_now(x,y)
        delay(0.1)
def run_rectangle():
    run_top()
    run_right()
    run_bottom()
    run_left()

def run_top():
    pass
def run_right():
    pass
def run_bottom():
    pass
def run_top():
    pass

while True:
    run_circle()
    run_rectangle()
    delay(0.01)

close_canvas()


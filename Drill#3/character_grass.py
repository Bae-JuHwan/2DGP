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
        grass.draw_now(400,30)
        boy.draw_now(x,y)
        delay(0.01)
def run_rectangle():
    run_top()
    run_right()
    run_bottom()
    run_left()

def run_top():
    print('TOP')
def run_right():
    print('RIGHT')
def run_bottom():
    print('BOTTOM')
def run_left():
    print('LEFT')

while True:
    #run_circle()
    run_rectangle()
    break


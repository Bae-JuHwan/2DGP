from pico2d import *

open_canvas()

grass = load_image('grass.png')
boy = load_image('character.png')

def draw_boy(x,y):
    clear_canvas()
    grass.draw_now(400, 30)
    boy.draw(x,y)
    update_canvas()
    delay(0.01)

def run_circle():
    r, cx, cy = 300, 800 // 2, 600 // 2

    for degree in range(0, 360, 3):
        theta = math.radians(degree)
        x = r * math.cos(theta) + cx
        y = r * math.sin(theta) + cy
        
        draw_boy(x,y)
        
def run_rectangle():
    run_top()
    run_right()
    run_bottom()
    run_left()

def run_triangle():
    run_bottom()
    run_left()
    run_diagonal()

def run_top():
    for x in range(20, 780, 10):
        draw_boy(x, 550)
        
def run_right():
    for y in range(550, 90, -10):
        draw_boy(780,y)
        
def run_bottom():
    for x in range(780, 20, -10):
        draw_boy(x, 90)
        
def run_left():
    for y in range(90, 550, 10):
        draw_boy(20, y)

def run_diagonal():
    x1, y1 = 0, 600
    x2, y2 = 800, 90
    for i in range(0, 100 + 1, 4):
        t = i / 100
        x = (1-t)*x1 + t*x2
        y = (1-t)*y1 + t*y2
        draw_boy(x,y)

while True:
    run_circle()
    run_rectangle()
    run_triangle()

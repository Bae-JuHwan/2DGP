from pico2d import *

open_canvas()

grass = load_image('grass.png')
boy = load_image('character.png')

def draw_boy(x,y):
    clear_canvas_now()
    grass.draw_now(400, 30)
    boy.draw_now(x,y)
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
    run_diagonalLeft()
    run_diagonalRight()

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

def run_diagonalLeft():
    for r in range(0, 600, 10):
        cx, cy = 20, 90
        theta = 70
        x = r * math.cos(theta) + cx
        y = r * math.sin(theta) + cy
        draw_boy(x,y)

def run_diagonalRight():
    for r in range(10, 600, 10):
        cx, cy = 390,550
        theta = 200
        x = r * math.cos(theta) + cx
        y = r * math.sin(theta) + cy
        draw_boy(x,y)

while True:
    run_circle()
    run_rectangle()
    run_triangle()
    break


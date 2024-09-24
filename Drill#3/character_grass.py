from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

x = 400
y = 90
center_x = 400
center_y = 300
radius = 200
angle = 0

is_square_motion = True

while(True):
    clear_canvas_now()
    grass.draw_now(400,30)

    if is_square_motion:
        character.draw_now(x, y)

        if y == 90 and x < 790:
            x += 2
        elif x == 790 and y < 570:
            y += 2
        elif y == 570 and x > 10:
            x -= 2
        elif x == 10 and y > 90:
            y -= 2

        if x == 400 and y == 90:
            is_square_motion = False
            angle = 0

    else:
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        character.draw_now(x, y)

        angle += 0.05

        if angle >= 2 * math.pi:
            is_square_motion = True
            x = 400
            y = 90

    delay(0.01)

close_canvas()

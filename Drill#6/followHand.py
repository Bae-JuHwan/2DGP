from pico2d import *
import random
import math

TUK_WIDTH, TUK_HEIGHT = 800, 600
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand = load_image('hand_arrow.png')

running = True
frame = 0

char_x, char_y = TUK_WIDTH // 2, TUK_HEIGHT // 2
hand_x, hand_y = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)

speed = 0.01
t = 0.0
dir = 1

p1_x, p1_y = char_x, char_y
p2_x, p2_y = hand_x, hand_y

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    if t <= 1:
        char_x = (1 - t) * p1_x + t * p2_x
        char_y = (1 - t) * p1_y + t * p2_y
        t += speed

        if p2_x > p1_x:
            dir = 1
        else:
            dir = -1
    else:
        p1_x, p1_y = p2_x, p2_y
        p2_x, p2_y = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)
        t = 0.0

    hand.draw(p2_x, p2_y)

    if dir == 1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, char_x, char_y)
    else:
        character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', char_x, char_y, 100, 100)

    update_canvas()
    frame = (frame + 1) % 8

    delay(0.01)

close_canvas()

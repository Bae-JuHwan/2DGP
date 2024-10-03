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

speed = 3

dir = 1

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    dx, dy = hand_x - char_x, hand_y - char_y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance > speed:
        char_x += speed * (dx / distance)
        char_y += speed * (dy / distance)

        if dx > 0 :
            dir = 1
        else:
            dir = -1
    else:
        hand_x, hand_y = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)

    hand.draw(hand_x, hand_y)

    if dir == 1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, char_x, char_y)
    else:
        character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', char_x, char_y, 100, 100)
    
    update_canvas()
    frame = (frame + 1) % 8

    delay(0.01)

close_canvas()

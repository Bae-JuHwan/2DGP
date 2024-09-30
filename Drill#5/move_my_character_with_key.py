from pico2d import *

open_canvas()
background = load_image('TUK_GROUND.png')
character = load_image('character_wasd.png')

def handle_events():
    global running, dir_x, dir_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_w:
                dir_y += 1
            elif event.key == SDLK_s:
                dir_y -= 1
            elif event.key == SDLK_a:
                dir_x -= 1
            elif event.key == SDLK_d:
                dir_x += 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w:
                dir_y -= 1
            elif event.key == SDLK_s:
                dir_y += 1
            elif event.key == SDLK_a:
                dir_x += 1
            elif event.key == SDLK_d:
                dir_x -= 1

running = True
x, y = 800 // 2, 600 // 2
frame = 0
dir_x, dir_y = 0, 0

frame_width = character.w // 8
frame_height = character.h // 4

row = 0 

while running:
    clear_canvas()
    background.draw(400, 300)

    if dir_y > 0:
        row = 0
    elif dir_y < 0:
        row = 3
    elif dir_x > 0:
        row = 1
    elif dir_x < 0:
        row = 2

    character.clip_draw(frame * frame_width, row * frame_height, frame_width, frame_height, x, y)

    update_canvas()
    handle_events()

    frame = (frame + 1) % 8
    x += dir_x * 10
    y += dir_y * 10

    if x < 10:
        x = 10
    elif x > 780:
        x = 780

    if y < 20:
        y = 20
    elif y > 580:
        y = 580
    delay(0.05)

close_canvas()

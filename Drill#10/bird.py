# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
FLY_SPEED_KMPH = 20.0
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

class Idle:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.action = 3
            bird.face_dir = 1
        elif right_down(e) or left_up(e):
            bird.action = 2
            bird.face_dir = -1
        elif left_down(e) or right_up(e):
            bird.action = 3
            bird.face_dir = 1

        bird.frame = 0
        bird.wait_time = get_time()

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        if get_time() - bird.wait_time > 2:
            bird.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(bird):
        total_frames = 14
        frames_per_row = 5
        frame_width = 183.6  # 가로 프레임 크기
        frame_height = 168.6  # 세로 프레임 크기
        current_row = int(bird.frame // frames_per_row)  # 현재 줄(행) 계산
        current_column = int(bird.frame % frames_per_row)  # 현재 열(가로) 프레임 계산

        if bird.face_dir == 1:
            bird.image.clip_composite_draw(int(current_column * frame_width), int((2 - current_row) * frame_height),
                                           int(frame_width), int(frame_height),
                                           0, '', bird.x, bird.y, frame_width, frame_height)
        else:
            bird.image.clip_composite_draw(int(current_column * frame_width), int((2 - current_row) * frame_height),
                                           int(frame_width), int(frame_height),
                                           0, 'h', bird.x, bird.y, frame_width, frame_height)

class Sleep:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.face_dir = 1
            bird.action = 3
        bird.frame = 0

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14

    @staticmethod
    def draw(bird):
        total_frames = 14
        frames_per_row = 5
        frame_width = 183.6  # 가로 프레임 크기
        frame_height = 168.6  # 세로 프레임 크기
        current_row = int(bird.frame // frames_per_row)  # 현재 줄(행) 계산
        current_column = int(bird.frame % frames_per_row)  # 현재 열(가로) 프레임 계산

        if bird.face_dir == 1:
            bird.image.clip_composite_draw(int(current_column * frame_width), int((2 - current_row) * frame_height), int(frame_width), int(frame_height),
                                          0, '', bird.x, bird.y, frame_width, frame_height)
        else:
            bird.image.clip_composite_draw(int(current_column * frame_width), int((2 - current_row) * frame_height), int(frame_width), int(frame_height),
                                          0, 'h', bird.x, bird.y, frame_width, frame_height)

class Fly:
    @staticmethod
    def enter(bird, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = -1, -1, 0

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.dir * FLY_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(bird):
        total_frames = 14
        frames_per_row = 5
        frame_width = 183.6  # 가로 프레임 크기
        frame_height = 168.6  # 세로 프레임 크기
        current_row = int(bird.frame // frames_per_row)  # 현재 줄(행) 계산
        current_column = int(bird.frame % frames_per_row)  # 현재 열(가로) 프레임 계산

        if bird.face_dir == 1:
            bird.image.clip_composite_draw(int(current_column * frame_width), int((2 - current_row) * frame_height),
                                           int(frame_width), int(frame_height),
                                           0, '', bird.x, bird.y, frame_width, frame_height)
        else:
            bird.image.clip_composite_draw(int(current_column * frame_width), int((2 - current_row) * frame_height),
                                           int(frame_width), int(frame_height),
                                           0, 'h', bird.x, bird.y, frame_width, frame_height)

class Bird:

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Fly, left_down: Fly, left_up: Fly, right_up: Fly, time_out: Sleep, space_down: Idle},
                Fly: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Fly},
                Sleep: {right_down: Fly, left_down: Fly, right_up: Fly, left_up: Fly, space_down: Idle}
            }
        )
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 60, self.y + 50, f'(Time: {get_time():.2f})', (255,255,0))

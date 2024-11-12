# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font, \
    draw_rectangle

from ball import newBall
import game_world
import game_framework
from state_machine import start_event, right_down, left_up, left_down, right_up, space_down, StateMachine, time_out

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif right_down(e) or left_up(e):
            boy.action = 2
            boy.face_dir = -1
        elif left_down(e) or right_up(e):
            boy.action = 3
            boy.face_dir = 1

        boy.frame = 0
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8
        # boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.wait_time > 2:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.face_dir = 1
            boy.action = 3
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8


    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 300, 100, 100,
                                          3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 200, 100, 100,
                                          -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, -1, 0

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()


    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8

        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Boy:

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.ball_count = 10
        self.font = load_font('ENCR10B.TTF', 16)
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        # 소년의 충돌 영역 그려보기
        draw_rectangle(*self.get_bb())

    def fire_ball(self):
        if self.ball_count > 0:
            self.ball_count -= 1
            new_ball = newBall(self.x, self.y, self.face_dir * 10)
            game_world.add_object(new_ball)
            game_world.add_collision_pair('newBall:zombie', new_ball, None)

    def get_bb(self): # bounding box 충돌 처리하기 위한 단계
        # fill here
        # 네 개의 값을 리턴하는데, 사실은 한개의 튜플을 리턴하는 것이기 때문에 draw_rectangle로 가져올때 *를 붙여야함. 이때 *은 튜플 해제
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50
        # 소년이 누웠을때의 상태도 get_bb로 만들어줘야 함.
        pass

    def handle_collision(self, group, other):
        # fill here
        if group == 'boy:ball':
            self.ball_count += 1

        elif group == 'boy:zombie':
            game_world.remove_object(self)
from pico2d import load_image, get_time
from sdl2 import SDLK_a

from State_machine import StateMachine, time_out, space_down, right_down, left_down, right_up, left_up, start_event


def is_key_pressed(SDLK_a):
    pass

class Idle:
    @staticmethod
    # @ is decorator grammer
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1

        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1

        elif is_key_pressed(e):
            if boy.dir == 1:
                boy.action = 1
                boy.dir = 1

            elif boy.dir == -1:
                boy.action = 0
                boy.dir = -1

        boy.frame = 0
        boy.dir = 0

        # 시작 시간을 기록.
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 1:
            # 이벤트를 발생
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100,100, 3.141592 / 2, '', # 좌우상하 반전 x
            boy.x - 25, boy.y - 25, 100,100 )

        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100, -3.141592 / 2, '',  # 좌우상하 반전 x
            boy.x + 25, boy.y - 25, 100, 100)

        # 함수 호출을 먼저하고 나중에 정의

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1

        elif left_down(e) or right_up(e):
            boy.action = 0
            boy.dir = -1

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 3
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100,100, boy.x, boy.y
        )
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있음
        self.state_machine.start(Idle) # 객체를 생성한게 아니고 직접 Idle이라는 클래스를 사용함
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : input event
        # state machine event : (이벤트종류, 값)
        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw()

# Sleep 상태에서는 무적모드 안해도 됨.
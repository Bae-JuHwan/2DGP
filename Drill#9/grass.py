from pico2d import load_image

class Grass:
    def __init__(self, x=400, y=30):
        self.image = load_image('grass.png')
        self.x = x
        self.y = y

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

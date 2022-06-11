# Matrix_mark01

# Sic mundus creatus est.
# Hinc erunt adaptationes mirabiles, quarum modus est hic.

import pygame as pg
from camera import *
from projection import *

from Object3D import *


class Renderer:

    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1100, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_obj()
        self.object.rotate_X(180)

    def create_obj(self):
        self.camera = Camera(self, [-0.65646274, 2.00236745, -3.4492734])
        self.projection = Projection(self)
        self.object = self.get_object_from_file("my_potato_face.obj")

    def get_object_from_file(self, filepath):
        vertex, faces = [], []
        with open(filepath) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color("black"))
        self.object.draw()

    def run(self):

        light = pg.image.load('circle.png')

        while True:
            self.draw()
            self.camera.control()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))  # Show fps on top bar
            pg.display.flip()
            self.clock.tick(self.FPS)
            print(self.camera.pos)


if __name__ == '__main__':
    matrix = Renderer()
    matrix.run()

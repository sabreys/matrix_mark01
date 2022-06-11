import numpy as np
from matrix_functions import *
import pygame as pg

from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))  # fps improvement


class Object3D:
    def __init__(self, render, vertexes, faces):
        self.render = render
        self.vertexes = np.array([np.array(v) for v in vertexes])

        self.faces = np.array([np.array(face) for face in faces])
        self.draw_vertexes = False

    def draw(self):
        self.screen_projection()
        self.rotate_Y(0.1)
        self.rotate_Z(0.1)

    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.project_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0  # higher is better for getting near to objects
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for face in self.faces:
            polygon = vertexes[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, pg.Color('orange'), polygon, 1)

        # for vertex in vertexes:
        #     if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
        #         pg.draw.circle(self.render.screen, pg.Color("white"), vertex, 2)

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, n):
        self.vertexes = self.vertexes @ scale(n)

    def rotate_X(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    def rotate_Y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    def rotate_Z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)

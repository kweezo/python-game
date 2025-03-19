import pygame

from camera import *
from copy import *

from random import *
from physics.rect_collider import *

class Stage:
    def __init__(self, screen):
        self._WIDTH = 2000
        self._HEIGHT = 2000

        self._floor_image = pygame.image.load("res/floorboards.jpg").convert()
        self._floor_image = pygame.transform.scale(self._floor_image, (100, 100))

        self._bush_image = pygame.image.load("res/bush.png").convert_alpha()
        self._bush_image = pygame.transform.scale(self._bush_image, (200, 200))

        self._bushes = list()
        self.__spawn_bushes()

        self._border_colliders = list()
        self.__create_border_colliders()
    
        self._screen = screen

    def __create_border_colliders(self):
        self._border_colliders = [
            RectCollider(Vector2(-self._WIDTH, -self._HEIGHT / 2 - 500), Vector2(self._WIDTH * 2.5, 1000), 0, True),  # Top
            RectCollider(Vector2(-self._WIDTH - 500, self._HEIGHT / 2 - 500), Vector2(self._WIDTH * 2.5, 1000), 0, True),   # Bottom
            RectCollider(Vector2(-self._WIDTH / 2 - 750, -self._HEIGHT), Vector2(1000, self._HEIGHT * 2.5), 0, True),  # Left
            RectCollider(Vector2(self._WIDTH / 2 - 200, -self._HEIGHT), Vector2(500, self._HEIGHT * 2.5), 0, True),  # Right
        ]
    
    def __spawn_bushes(self):
        for x in range(15):
            self._bushes.append(
                RectCollider(Vector2(
                         randint(int(-self._WIDTH / 2), int(self._HEIGHT / 2)),
                         randint(int(-self._WIDTH / 2), int(self._HEIGHT / 2)),
                        ),
                            Vector2(100, 100), 0, True)
            )

    def __draw_floor(self):
        image = copy(self._floor_image)
        image.fill(Camera.get_color_rgb(), special_flags=pygame.BLEND_RGB_MULT)
        for x in range(-int(self._WIDTH/2), int(self._WIDTH / 2), 100):
            for y in range(-int(self._HEIGHT / 2), int(self._HEIGHT / 2), 100):
                self._screen.blit(image, (Vector2(x, y) + Camera.get_pos()).tuple)
        
    def __draw_bushes(self):
        for bush in self._bushes:
            self._screen.blit(self._bush_image, (bush.get_pos + Camera.get_pos() - bush.get_size / 2).tuple)
        
    def check_border_collision(self, other):
        for border in self._border_colliders:
            other.handle_collision(border)

    def check_environment_collision(self, other):
        for bush in self._bushes:
            other.handle_collision(bush)

    def draw(self):
        self.__draw_floor()

        for border in self._border_colliders:
            border.draw(self._screen)

    def draw_on_top(self):
        self.__draw_bushes()

    @property
    def get_environment_colliders(self):
        return self._bushes

    @property
    def get_size(self):
        return Vector2(self._WIDTH, self._HEIGHT)
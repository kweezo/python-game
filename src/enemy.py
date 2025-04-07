from vec import * 
from copy import *
from camera import *

import pygame

from physics.circle_collider import *
from physics.rect_collider import *


class Enemy(RectCollider):

    def __init__(self, window, pos, size, speed, max_speed, hp, image, worth, dmg) -> None:
        super().__init__(pos, size, 10, False, 0)

        self._speed = speed
        self._max_speed = max_speed
        self._hp = hp
        self._screen = window
        self._worth = worth
        self._dmg = dmg

        self._hit_time = 0

        self._image = pygame.transform.scale(image, self._size.tuple)

    def draw(self, player_pos):
        image = copy(self._image)
        if pygame.time.get_ticks() - self._hit_time < 100:
            image.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
        image.fill(Camera.get_color_rgb(), special_flags=pygame.BLEND_RGB_MULT)

        angle = atan2(self._pos.x - player_pos.x, self._pos.y - player_pos.y)

        image = pygame.transform.rotate(image, angle * 180 / 3.14159)

        self._screen.blit(image, (self._pos + Camera.get_pos()).tuple)

    def __handle_movement(self, dt, player_pos):

        dir_vec = ~(self._pos - player_pos)

        self._vel = dir_vec * dt * -self._speed

    def __turn_towards_player(self, player_pos):
        c = (self._pos - player_pos).size
        b = abs(self._pos.y - player_pos.y)

        self._orientation = cos(b/c)

    def update(self, dt, player_pos):
        self.__turn_towards_player(player_pos) # oriented bounding boxes sigma sigma??
        self.__handle_movement(dt, player_pos)

        self._physics_update(dt)


    def deal_dmg(self, dmg, dmg_dir):
        self._hp -= dmg
        self._hit_time = pygame.time.get_ticks()

        self.apply_force(-self._vel)
        self.apply_force(dmg_dir * self._speed)    
    
    def should_destroy(self):
        return self._hp <= 0

    def get_worth(self):
        return self._worth

    def get_dmg(self):
        return self._dmg
    

class BasicEnemy(Enemy):
    def __init__(self, screen, pos):
        super().__init__(screen, pos, Vector2(80, 80), 260, 60, 100, pygame.image.load("res/basic_zombie.png").convert_alpha(), 10, 15)
class TurtleEnemy(Enemy):
    def __init__(self, screen, pos):
        super().__init__(screen, pos, Vector2(90, 90), 100, 50, 200, pygame.image.load("res/turtle.png").convert_alpha(), 30, 50)
class ChildEnemy(Enemy):
    def __init__(self, screen, pos):
        super().__init__(screen, pos, Vector2(70, 70), 80, 30, 50, pygame.image.load("res/child.png").convert_alpha(), 30, 50)
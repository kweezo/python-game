from vec import * 
from copy import *
from camera import *

import pygame

from physics.circle_collider import *
from physics.rect_collider import *

from random import *


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

    def _handle_movement(self, dt, player_pos):

        dir_vec = ~(self._pos - player_pos)

        self._vel = dir_vec * dt * -self._speed

    def _turn_towards_player(self, player_pos):
        c = (self._pos - player_pos).size
        b = abs(self._pos.y - player_pos.y)

        self._orientation = cos(b/c)

    def update(self, dt, player_pos):
        self._turn_towards_player(player_pos) # oriented bounding boxes sigma sigma??
        self._handle_movement(dt, player_pos)

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

class RangedEnemy(Enemy):
    def __init__(self, screen, pos):
        super().__init__(screen, pos, Vector2(150, 150), 260, 60, 100, pygame.image.load("res/ranged_enemy.png").convert_alpha(), 10, 1)

        self._laser_pos = Vector2(0, 0)
        self._hit_player = False
        self._since_last_shot = 0
        self._laser_offset = Vector2(20, 5)

    def _obstacle_in_path(self, player, colliders):
        player_dist = (self._pos - player.get_pos).size_pow
        laser_dir = ~(self._pos - player.get_pos) * 10
        self._laser_pos = copy(self._pos)

        hit = False
        hit_player_in_frame = False #ugly as hell but it's 11 pm and I can't be arsed
        
        for i in range(100):
            for col in colliders:
                if (col.get_pos - self._pos).size_pow > player_dist:
                    continue 

                if col.colliding_with_point(self._laser_pos):
                    hit = True
                    break


            if hit:
                break
            self._laser_pos -= laser_dir
            
            if player.colliding_with_point(self._laser_pos + player.get_size / 2):
                if not self._hit_player:
                    self._since_last_shot = pygame.time.get_ticks()
                self._laser_pos -= laser_dir * 1.3

                hit_player_in_frame = True
                break
        
        self._hit_player = hit_player_in_frame


    def _dmg_player(self, player):
        if not self._hit_player or pygame.time.get_ticks() - self._since_last_shot < 3000:
            return

        self._since_last_shot = pygame.time.get_ticks()

        player.deal_dmg(self._dmg, Vector2(0, 0))
        
        Camera.offset_pos(Vector2(randrange(-50, 50), randrange(-50, 50)))
            

    def update(self, player, colliders, dt):
        self._turn_towards_player(player.get_pos) # oriented bounding boxes sigma sigma??

        self._obstacle_in_path(player, colliders)
        if (self._pos - player.get_pos).size_pow > 300000:
            self._handle_movement(dt, player.get_pos)
        else:
            self._dmg_player(player)


        self._physics_update(dt)

    def draw_laser(self):
        start_pos = self.get_pos + Camera.get_pos() + self._laser_offset * Vector2(cos(self._orientation), sin(self._orientation))
        final_pos = self._laser_pos + Camera.get_pos()


        pygame.draw.line(self._screen, (0, 255, 255), start_pos.tuple, final_pos.tuple, 2)


    def draw(self, player_pos):
        image = copy(self._image)
        if pygame.time.get_ticks() - self._hit_time < 100:
            image.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
        image.fill(Camera.get_color_rgb(), special_flags=pygame.BLEND_RGB_MULT)

        angle = atan2(self._pos.x - player_pos.x, self._pos.y - player_pos.y) + 1.57

        image = pygame.transform.rotate(image, angle * 180 / 3.14159) 

        self._screen.blit(image, (self._pos + Camera.get_pos() - Vector2(image.get_width(), image.get_height()) / 2).tuple)


    

class BasicEnemy(Enemy):
    def __init__(self, screen, pos):
        super().__init__(screen, pos, Vector2(80, 80), 260, 60, 100, pygame.image.load("res/basic_zombie.png").convert_alpha(), 10, 15)
class TurtleEnemy(Enemy):
    def __init__(self, screen, pos):
        super().__init__(screen, pos, Vector2(90, 90), 100, 50, 200, pygame.image.load("res/turtle.png").convert_alpha(), 30, 50)
class ChildEnemy(Enemy):
    def __init__(self, screen, pos):
        super().__init__(screen, pos, Vector2(70, 70), 80, 30, 50, pygame.image.load("res/child.png").convert_alpha(), 30, 50)
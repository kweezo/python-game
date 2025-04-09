from vec import * 
import pygame
from copy import *
from camera import *
from random import *


class Weapon:

    def __init__(self, screen, damage, image, size, radius_offset, shoot_sound, is_automatic, laser_color, fire_rate) -> None:

        self._damage = damage
        self._size = size
        self._screen = screen
        self._rotation = 0
        self._radius_offset = radius_offset
        self._shoot_sound = shoot_sound
        self._last_press = False
        self._fire_time = 0
        self._dir_vec = Vector2(0, 0)
        self._is_automatic = is_automatic
        self._fire_rate = fire_rate
        self._laser_color = laser_color
        self._hit_sound = pygame.mixer.Sound("res/sfx/hit.wav")
        
        self._object_in_path = False
        self._enemy_in_path_pos = Vector2(0, 0)
        self._enemy = None

        self._image = pygame.transform.scale(image, (self._size.get_x, self._size.get_x))

########
    def draw_laser(self, player_pos):
   
        player_pos += Camera.get_pos()
        final_pos = player_pos + self._dir_vec * 1500

        if self._object_in_path:
            final_pos = self._enemy_in_path_pos + Camera.get_pos()

        pygame.draw.line(self._screen, self._laser_color, player_pos.tuple, final_pos.tuple, 2)

    def draw(self, player_pos, rotate=True):
        image = None
        if rotate:
            image = pygame.transform.rotate(self._image, self._rotation * 180 / 3.14159)
        else: 
            image = copy(self._image)
        image.fill(Camera.get_color_rgb(), special_flags=pygame.BLEND_RGB_MULT)

        pos = Vector2(player_pos.x - image.get_width() / 2, player_pos.y - image.get_height() / 2) + self._dir_vec * self._radius_offset

        self.draw_laser(player_pos)
        self._screen.blit(image, (pos + Camera.get_pos()).tuple)
########


    def __handle_rotation(self, player_pos):
        mouse = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) - Camera.get_pos()

        self._rotation = atan2(player_pos.y - mouse.y, mouse.x - player_pos.x)

        self._dir_vec = Vector2(cos(self._rotation), -sin(self._rotation))

    def __fire(self):
        self._fire_time = pygame.time.get_ticks()
        self._shoot_sound.play()

        if self._enemy is None:
            return

        self._enemy.deal_dmg(self._damage, self._dir_vec)
        self._hit_sound.play()

    def __manual_fire(self):

        buttons = pygame.mouse.get_pressed()

        if not buttons[0] or pygame.time.get_ticks() - self._fire_rate < self._fire_time or self._last_press:
            self._last_press = buttons[0]
            return

        self._last_press = buttons[0]

        self.__fire()
        self._fire_time = pygame.time.get_ticks()

    def __auto_fire(self):
        buttons = pygame.mouse.get_pressed()

        if not buttons[0] or pygame.time.get_ticks() - self._fire_rate < self._fire_time:
            return

        self.__fire()


        self._fire_time = pygame.time.get_ticks()


    def __handle_shooting(self):
        if self._is_automatic:
            self.__auto_fire()
        else:
            self.__manual_fire()

    def __get_enemy_in_path(self, player_pos, enemies, environment):
        self._object_in_path = False
        self._enemy = None

        for i in range(0, 1500, 10): #just shitty raycasting also a lot of temp variables cause I am scared of computing this twice
            offset_pos = player_pos + self._dir_vec * i 

            for env_obj in environment:
                if env_obj.colliding_with_point(offset_pos):
                    self._object_in_path = True
                    self._enemy_in_path_pos = offset_pos
                    self._enemy = None
                    return

            for enemy in enemies:
                if enemy.colliding_with_point(offset_pos):
                    self._object_in_path = True
                    self._enemy = enemy
                    self._enemy_in_path_pos = offset_pos
                    break

            if self._object_in_path:
               break 

    def update(self, player_pos, enemies, environment):
        self.__handle_rotation(player_pos)
        self.__get_enemy_in_path(player_pos, enemies, environment)
        self.__handle_shooting()

        if pygame.time.get_ticks() - self._fire_time < 100:
            time_multiplier = min((1 - (pygame.time.get_ticks() - self._fire_time) / 100) + 0.3, 1)

            Camera.set_color((1 * time_multiplier, 1 * time_multiplier, 1 * time_multiplier)) 
            Camera.offset_pos(Vector2(randrange(-5, 5), randrange(-5, 5)))



    
    
import pygame

from vec import *
from camera import * 

from copy import *
from random import *

class Grenade:
    def __init__(self, screen):
        self._image = pygame.image.load("res/grenade.png").convert_alpha()
        self._image = pygame.transform.scale(self._image, (30, 30))
        self._sound = pygame.mixer.Sound("res/sfx/grenade_explosion.mp3")

        self._use_time = -150000
        self._cooldown = 1000
        self._max_range = 600
        self._detonation_time = 250
        self._detonation_range = 300

        self._screen = screen

        self._is_thrown = False
        self._pos = Vector2(0, 0)
        self._target_pos = Vector2(0, 0)
        self._smoke_rects = list()
        self._exploded = False

    
    def draw(self):
        if not self._is_thrown:
            return



        if self._exploded:
            self.__draw_explosion()
        else:
            self.__draw_grenade()

    def __draw_grenade(self):
        image = copy(self._image)
        image.fill(Camera.get_color_rgb(), special_flags=pygame.BLEND_RGB_MULT)
        self._screen.blit(self._image, (self._pos + Camera.get_pos()).tuple)
    
    def __draw_explosion(self):
        for rect in self._smoke_rects:
            pygame.draw.rect(self._screen, (127, 127, 127), (rect[0].get_x + Camera.get_pos().get_x, rect[0].get_y + Camera.get_pos().get_y, rect[1].get_x, rect[1].get_y))


    ####
        
    def __handle_throw(self, player_pos):
        buttons = pygame.mouse.get_pressed()
        if not buttons[2] or pygame.time.get_ticks() - self._use_time < self._cooldown:
            return False

        self._target_pos = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) - Camera.get_pos()

        self._use_time = pygame.time.get_ticks()
        self._pos = player_pos
        self._is_thrown = True


        if (self._target_pos - self._pos).size_pow > self._max_range ** 2:
            self._target_pos = ~(self._pos - self._target_pos) * -self._max_range + self._pos

    def on_explode(self, enemies):
        Camera.offset_pos(Vector2(randrange(-200, 200), randrange(-200, 200)))

        for i in range(250):
            rect = ( 
                Vector2(self._pos.get_x + randrange(-self._detonation_range, self._detonation_range),
                self._pos.get_y + randrange(-self._detonation_range, self._detonation_range)),
                Vector2(randrange(5, 10), randrange(5, 10)))

            if ((self._pos - rect[0]).size_pow > self._detonation_range ** 2):
                continue
            
            self._smoke_rects.append(rect)

        for enemy in enemies:
            if (enemy.get_pos + enemy.get_size / 2 - self._pos).size_pow <= self._detonation_range ** 2:
                enemy.deal_dmg(1000, (self._pos - enemy.get_pos))

        self._sound.play()

    def update(self, player_pos, enemies, dt):
        self.__handle_throw(player_pos)

        if pygame.time.get_ticks() - self._use_time > self._cooldown:
            self._is_thrown = False
            self._exploded = False
            self._smoke_rects.clear()
            return

        if not self._is_thrown:
            return 


        self._pos.lerp(self._target_pos, 1 * dt)  

        for rect in self._smoke_rects:
            rect[0].y -= 1 * dt

        if pygame.time.get_ticks() - self._use_time > self._detonation_time and not self._exploded:
            self.on_explode(enemies)
            self._exploded =  True



    
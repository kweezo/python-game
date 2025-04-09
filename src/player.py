import pygame

from vec import *
from constants import *
from copy import copy

from physics.circle_collider import *
from physics.rect_collider import *

from camera import * 
from weapons.weapon import *
from weapons.grenade import * 
from dog import *

class Player(RectCollider):
    def __init__(self, screen, font) -> None:
        super().__init__(Vector2(200, 200), Vector2(50, 50), 40, False) 

        self._speed = 50
        self._screen = screen
        self._max_speed = 60
        self._last_dash = 0
        self._dash_force = 150
        self._weapon = Weapon(screen, 10, pygame.image.load("res/glock.png").convert_alpha(), Vector2(50, 10), 20, pygame.mixer.Sound("res/sfx/shoot_glock.mp3"), False, (255, 255, 255), 500)
        self._since_last_hit = 0
        self._dog = None
        #
        self._grenade = Grenade(screen)
        self._max_hp = 100
        self._hp = self._max_hp
        self._currency = 999
        self._font = font


    def draw_on_top(self):
        currency_surface = self._font.render("cekinarji: " + str(self._currency), False, (255, 255, 0))
        health_surface = self._font.render("zdravje: " + str(self._hp), False, (255, 255, 0))

        self._screen.blit(health_surface, (0, 0))
        self._screen.blit(currency_surface, (0, 60))

    def draw(self):
        final_pos = (self._pos + Camera.get_pos()).tuple
        rect = pygame.Rect(final_pos[0], final_pos[1], self._size.x, self._size.y)


        pygame.draw.rect(self._screen, Camera.get_color_rgb(), rect)

        self._weapon.draw(self._pos + self._size / 2)
        self._grenade.draw()


        if self._dog is not None:
            self._dog.draw()

    def __handle_movement(self, dt):
        if self._vel.size > self._max_speed:
            return

        keys = pygame.key.get_pressed()

        dir_vec = Vector2(0, 0)

        if keys[pygame.K_w]:
            dir_vec.y -= 1
        if keys[pygame.K_s]:
            dir_vec.y += 1
        if keys[pygame.K_a]:
            dir_vec.x -= 1
        if keys[pygame.K_d]:
            dir_vec.x += 1
        if keys[pygame.K_LSHIFT] and pygame.time.get_ticks() - self._last_dash > 1000:
            self.apply_force(-self._vel)
            self.apply_force(~dir_vec * self._dash_force)
            self._last_dash = pygame.time.get_ticks()


        self.apply_force(~dir_vec * self._speed * dt)

    def update(self, enemies, environment, dt):
        self._weapon.update(self._pos + self._size / 2, enemies, environment)
        self._grenade.update(self._pos + self._size / 2, enemies, dt)

        self.__handle_movement(dt)

        self._physics_update(dt)
        
        if self._dog is not None:
            self._dog.update(enemies, dt)

    def deal_dmg(self, dmg, dmg_dir):
        if pygame.time.get_ticks() - self._since_last_hit < 1000:
            return

        self._since_last_hit = pygame.time.get_ticks()

        self._hp -= dmg
        self._hit_time = pygame.time.get_ticks()

        self.apply_force(-self._vel)
        self.apply_force(dmg_dir * 150)

    def reset_hp(self):
        self._hp = self._max_hp
    
    def add_currency(self, amount):        
        self._currency += amount

        if self._currency < 0:
            self._currency -= amount
            return False

        return True

    def set_weapon(self, weapon):
        self._weapon = weapon

    def enable_dog(self):
       self._dog = Dog(self._screen, self) 


    @property 
    def get_pos(self):
        return copy(self._pos)

import pygame

from physics.rect_collider import *
from physics.collider import *

from camera import *

class BuyPad(RectCollider):
    def __init__(self, screen, pos, price, weapon):
        self._size = Vector2(100, 100)
        super().__init__(pos, self._size, 0, 0)

        self._screen = screen
        self._price = price
        self._weapon = weapon
        self._used = False  
        self._image = pygame.image.load("res/buy_pad.png").convert()
        self._image = pygame.transform.scale(self._image, self._size.tuple)

    def draw(self):
        self._screen.blit(self._image, (self._pos + Camera.get_pos()).tuple)

        if self._weapon is not None:
            self._weapon.draw(self._pos + self._size / 2)

    def update(self, player):
        if self._get_overlap(player) == None or self._used:
            return

        keys = pygame.key.get_pressed()

        if not keys[pygame.K_SPACE]:
            return

        self._used = True
        player.add_currency(-self._price)
        player.set_weapon(self._weapon)

        self._weapon = None
            

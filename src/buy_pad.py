import pygame

from physics.rect_collider import *
from physics.collider import *

from camera import *

from abc import ABC, abstractmethod

class BuyPad(RectCollider, ABC):
    def __init__(self, screen, pos, price, image, font):
        self._size = Vector2(100, 100)
        super().__init__(pos, self._size, 0, 0)

        self._screen = screen
        self._price = price
        self._used = False  
        self._image = image
        self._image = pygame.transform.scale(self._image, self._size.tuple)
        self._price_surface = font.render("price: " + str(self._price), False, (255, 255, 0))
        self._colliding_with_player = False

    def draw(self):
        image = copy(self._image)
        image.fill(Camera.get_color_rgb(), special_flags=pygame.BLEND_RGB_MULT)

        self._screen.blit(image, (self._pos + Camera.get_pos()).tuple)

        if self._item is not None:
            self._item.draw(self._pos + self._size / 2)

    def draw_on_top(self):
        if self._colliding_with_player is not None:
            self._screen.blit(self._price_surface, (self._pos + Camera.get_pos() - Vector2(25, 50)).tuple)

    def _darken(self):
        self._image.fill((127, 127, 127), special_flags=pygame.BLEND_RGB_MULT)

    @abstractmethod
    def _on_buy(self):
        pass

    def update(self, player):
        self._colliding_with_player = self._get_overlap(player)

        if self._colliding_with_player == None or self._used:
            return

        keys = pygame.key.get_pressed()

        if not keys[pygame.K_SPACE]:
            return

        if not player.add_currency(-self._price):
            return

        self._used = True
        self._on_buy()

class WeaponBuyPad(BuyPad):
    def __init__(self, screen, pos, price, weapon, player, font):
        super().__init__(screen, pos, price, pygame.image.load("res/buy_pad.png").convert(), font)
        self._item = weapon
        self._player = player


    def _on_buy(self):
        self._player.set_weapon(self._item)
        self._item = None
        self._darken()

class DogBuyPad(BuyPad):
    def __init__(self, screen, pos, price, player, font):
        super().__init__(screen, pos, price, pygame.image.load("res/dog_pad.png").convert(), font)
        self._player = player
        self._item = None


    def _on_buy(self):
        self._player.enable_dog()
        self._item = None
        self._darken()

class CureBuyPad(BuyPad):
    def __init__(self, screen, pos, price, player, font):
        super().__init__(screen, pos, price, pygame.image.load("res/cure_pad.png").convert(), font)
        self._item = None
        self._player = player

    def _on_buy(self):
        pass

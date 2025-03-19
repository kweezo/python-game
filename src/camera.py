
from vec import *
from copy import * 
from constants import * 

class Camera:
    _color = (0.4, 0.4, 0.4)
    _pos = Vector2(0, 0) 
    _limits = (Vector2(0, 0), Vector2(0, 0))
    _offset = Vector2(0, 0)

    @staticmethod
    def set_limits(min, max):
        offset = Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) / 2
        Camera._limits = (min - offset, max - offset)
    @staticmethod
    def update(player_pos, dt):
        Camera._pos.lerp(player_pos  - Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 0.5 * dt)
        Camera._pos.clamp(Camera._limits[0], Camera._limits[1])
        Camera._pos += Camera._offset
        Camera._offset = Vector2(0, 0)

    @staticmethod
    def get_pos():
        return -Camera._pos

    @staticmethod
    def get_color_float():
        return Camera._color

    @staticmethod
    def get_color_rgb():
        return (255 * Camera._color[0], 255 * Camera._color[1], 255 * Camera._color[2])

    @staticmethod
    def set_color(color):
        Camera._color = color

    @staticmethod
    def offset_pos(offset):
        Camera._offset += offset

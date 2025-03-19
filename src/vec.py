from math import *

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lerp(self, other, t):
        self.x = self.x + t * (other.x - self.x)
        self.y = self.y + t * (other.y - self.y)
    
    def clamp(self, min, max):
        if self.x < min.x:
            self.x = min.x
        if self.y < min.y:
            self.y = min.y

        if self.x > max.x:
            self.x = max.x
        if self.y > max.y:
            self.y = max.y

    @property
    def abs(self):
        return Vector2(abs(self.x), abs(self.y))

    @property
    def size(self):
        return sqrt(self.x * self.x + self.y * self.y)

    @property
    def size_pow(self):
        return self.x * self.x + self.y * self.y

    @property
    def tuple(self):
        return (self.x, self.y)

    @property
    def get_x(self):
        return self.x

    @property
    def get_y(self):
        return self.y
    
    def __add__(self, other):
        return Vector2(self.get_x + other.get_x, self.get_y + other.get_y)

    def __mul__(self, other):
        if type(other) is Vector2:
            return Vector2(self.get_x * other.get_x, self.get_y * other.get_y)
        return Vector2(self.get_x * other, self.get_y * other)

    def __truediv__(self, other):
        if type(other) is Vector2:
            return Vector2(self.get_x / other.get_x, self.get_y / other.get_y)
        return Vector2(self.get_x / other, self.get_y / other)

    def __sub__(self, other):
        return Vector2(self.get_x - other.get_x, self.get_y - other.get_y)

    def __invert__(self):
        scalar = self.size

        if scalar == 0:
            return Vector2(0, 0)

        return Vector2(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f"x: {self.x}, y: {self.y}"

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mod__(self, other):
        return self.x * other.x + self.y * other.y

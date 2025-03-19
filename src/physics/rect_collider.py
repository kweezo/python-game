from physics.collider import *
from vec import *
from copy import copy

class RectCollider(Collider):
    def __init__(self, pos, size, mass, is_static, orientation=0):
        super().__init__(ColliderType.RECT, pos, size, mass, is_static, orientation)
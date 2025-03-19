from physics.collider import *
from vec import *
from copy import copy

class CircleCollider(Collider):
    def __init__(self, pos, size, mass):
        super().__init__(ColliderType.CIRCLE, pos, size, mass)
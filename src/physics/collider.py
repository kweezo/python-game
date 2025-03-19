from abc import abstractmethod
from enum import Enum
from math import *
from vec import *
from copy import copy
from camera import *
import pygame

DRAG_COEFFICIENT = 0.7

class ColliderType(Enum):
    CIRCLE = 0,
    RECT = 1

class Collider:
    def __init__(self, collider_type, pos, size, mass, is_static, orientation=0):
        self.collider_type = collider_type
        self._pos = pos
        self._size = size
        self._vel = Vector2(0, 0)
        self._mass = mass
        self._orientation = orientation
        self._is_static = is_static

### COLLISION DETECTION THINGAMAJIG also ne ni chatgpt spisu sam ugotovu sem da se mi ne lubi circle collisiona se delat do konca
    def __rect_rect_collision(self, other):
        #broad phase because muh frames

        if (self._pos - other._pos).size_pow > (self._size + other._size).size_pow:
            return

        all_perps = list(set(self.__get_perpendiculars + other.__get_perpendiculars))

        self_edges = self.__get_edges
        other_edges = other.__get_edges

        overlaps = list()

        for i in range(len(all_perps)):
            a_max = None
            a_min = None
    
            b_max = None
            b_min = None


            for j in range(len(self_edges)):
                dot = self_edges[j] % all_perps[i]

                if a_max == None or dot > a_max:
                    a_max = dot
                if a_min == None or dot < a_min:
                    a_min = dot

            for j in range(len(other_edges)):
                dot = other_edges[j] % all_perps[i]

                if b_max == None or dot > b_max:
                    b_max = dot
                if b_min == None or dot < b_min:
                    b_min = dot

            if a_max < b_min or b_max < a_min:
                return None

### shoutout to deepseek for this snippet
            self_mid = (a_min + a_max) / 2
            other_mid = (b_min + b_max) / 2
            direction = -1 if other_mid > self_mid else 1
            mtv_axis = all_perps[i] * direction 
####
            overlaps.append((abs(min(a_max, b_max) - max(a_min, b_min)), mtv_axis))

        return min(overlaps, key=lambda x: x[0])




    def __circle_circle_collision(self, other):
        if (self._pos.get_x - other.get_pos.get_x) ** 2 + (self._pos.get_y - other.get_pos.get_y) ** 2 < (self._size + other._size) ** 2:
              return True

        return False

    def _get_overlap(self, other):
        if self.collider_type != other.collider_type or self.collider_type == ColliderType.RECT:
            return self.__rect_rect_collision(other)

        return self.__circle_circle_collision(other)

    def colliding_with_point(self, point):
        if point.x > self._pos.x and point.x < self._pos.x + self._size.x and \
           point.y > self._pos.y and point.y < self._pos.y + self._size.y:
           return True
        return False

    def draw(self, screen):
        edges = self.__get_edges
        for i in range(len(edges)):
            pygame.draw.line(screen, (0, 255, 0), (edges[i] + Camera.get_pos()).tuple, (edges[(i + 1) % len(edges)] + Camera.get_pos()).tuple) # doesnt work at all lmfao
            

    def handle_collision(self, other): 
        if self._is_static and other._is_static:
            print("warning, checking collision against two static objects")
            return False

        overlap = self._get_overlap(other)
        
        if overlap == None:
            return False

        if not self._is_static and not other._is_static:
            self._pos += overlap[1] * overlap[0] * 0.5
            other._pos -= overlap[1] * overlap[0] * 0.5
        else: 
            self._pos += overlap[1] * overlap[0]

#        while self._is_colliding(other):
#            dist = ~(self._pos - other._pos)
#
#            if abs(dist.x) > abs(dist.y):
#                self._pos.x += dist.x
#
#                if dist.x < 0:
#                    self._vel.x = min(self._vel.x, 0)                
#                else:
#                    self._vel.x = max(self._vel.x, 0)                
#            else: 
#                self._pos.y += dist.y
#                self._vel.y = 0
#
#                if dist.y < 0:
#                    self._vel.y = min(self._vel.y, 0)                
#                else:
#                    self._vel.y = max(self._vel.y, 0)                
            
        return True

########

    def __handle_drag(self, dt):
        self._vel -= ~self._vel * DRAG_COEFFICIENT * self._mass * dt

    def _physics_update(self, dt):
        self._pos += self._vel * dt

        self.__handle_drag(dt)

        if self._vel.size < 2:
            self._vel = Vector2(0, 0)

        


###### setters and getters (kinda)

    def apply_force(self, f):
        self._vel += f

    @property
    def get_type(self):
        return self.collider_type

    @property
    def get_pos(self):
        return copy(self._pos)

    @property
    def get_size(self):
        return copy(self._size)

    @property
    def get_vel(self):
        return copy(self._vel)

    @property
    def __get_perpendiculars(self):

        edge_vecs = list()
        edges = self.__get_edges

        import pygame
        for i in range(len(self.__get_edges)):
            edge_vecs.append(edges[i] - edges[( i + 1 ) % len(edges)])

        edge_vecs
        perpendiculars = []
        for edge in edge_vecs:
            perpendiculars.append(
                ~Vector2(-edge.y, edge.x)
            )

        return perpendiculars


    @property
    def __get_edges(self):
        scalar = self._size 
        pos = self._pos + scalar / 2
        rad = self._orientation #* 3.14 / 180
        return [
            pos + Vector2(cos(0.7853981634 + rad), sin(0.7853981634 + rad)) * scalar + pos,
            pos + Vector2(cos(5.4977871438 + rad), sin(5.4977871438 + rad)) * -scalar + pos,
            pos + Vector2(cos(0.7853981634 + rad), sin(0.7853981634 + rad)) * -scalar + pos,
            pos + Vector2(cos(5.4977871438 + rad), sin(5.4977871438 + rad)) * scalar + pos,
        ]




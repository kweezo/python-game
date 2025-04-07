from vec import * 
from physics.rect_collider import *
from enum import Enum
from camera import *
from random import *

class DogState(Enum):
    IDLE = 0,
    AGGRESSIVE = 1

class Dog(RectCollider):
    def __init__(self, screen, player):
        super().__init__(player.get_pos, Vector2(50, 100), 40, False)

        self._screen = screen
        self._player = player
        self._image = pygame.image.load("res/dog.png")
        self._image = pygame.transform.scale(self._image, (100, 100))
        self._pos = player.get_pos
        self._since_last_state_update = 0
        self._target_pos = Vector2(0, 0)
        self._state = DogState.IDLE
        self._dmg = 5
        
    def _idle_update(self, dt):


        if (self._pos - self._target_pos).size_pow > 100:
            self.apply_force(-self._vel)
            self.apply_force(~(self._pos - self._target_pos) * 80 * -dt)

        if pygame.time.get_ticks() - self._since_last_state_update < 2000:
            return

        self._target_pos = self._player.get_pos + Vector2(randint(-200, 200), randint(-200, 200))
        self._since_last_state_update = pygame.time.get_ticks()

        self._orientation = atan2(self._target_pos.y - self._pos.y, self._target_pos.x - self._pos.x) - 3.14
        

    def _aggressive_update(self, enemies, dt):
        if pygame.time.get_ticks() - self._since_last_state_update < 500:
            return

        closest_target = None
        closest_target_dist = None

        for enemy in enemies:
            dist = (self._pos - enemy.get_pos).size_pow
            if dist > 200000:
                continue

            if self.handle_collision(enemy):
                self.apply_force(-self._vel)
                self.apply_force(~(self._pos - enemy._pos) * 150)
                enemy.deal_dmg(self._dmg, Vector2(0, 0))

            if closest_target_dist is None or closest_target_dist > dist:
                closest_target_dist = dist
                closest_target = enemy.get_pos                    
        


            self._state = DogState.AGGRESSIVE

        self._target_pos = closest_target

        if self._target_pos is not None:
            self._orientation = atan2(self._target_pos.y - self._pos.y, self._target_pos.x - self._pos.x)
            self.apply_force(~(self._pos - self._target_pos) * 40 * -dt)

    def update(self, enemies, dt):
        for enemy in enemies:
            if (self._pos - enemy.get_pos).size_pow < 200000: # todo, adjust
                self._state = DogState.AGGRESSIVE
                break
        else:
            self._state = DogState.IDLE


        if self._state == DogState.IDLE:
            self._idle_update(dt)
        elif self._state == DogState.AGGRESSIVE:
            self._aggressive_update(enemies, dt)

        self._physics_update(dt)


    def draw(self, pos = None):
        if pos is not None:
            self._screen.blit(self._image, (pos + Camera.get_pos()).tuple)
            return
        
        image = pygame.transform.rotate(self._image, self._orientation * 180 / 3.14159)
        pos = self._pos - Vector2(image.get_width(), image.get_height()) / 2
        self._screen.blit(image, (pos + Camera.get_pos()).tuple)
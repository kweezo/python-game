from enemy import *
from math import *
from random import *

class EnemySpawner:
    def __init__(self, screen, stage, font):
        self._stage_size = stage.get_size
        self._curr_round = 0
        self._screen = screen
        self._cooldown_time = 10000
        self._since_round_start = 0
        self._round_start_sound = pygame.mixer.Sound("res/sfx/vine.mp3")
        self._last_round_start = -1
        self._font = font

    def __get_enemy_spawn_chance(self, deviation, mean_round):
        return int(10 - min(abs(self._curr_round - mean_round) / deviation, 10)) # distribution curve halal inshallah approves

    def __get_enemy_count(self):
        base_enemy_count = 3
        round_multiplier = 3
        round_enemy_multiplier = 1.4
        enemy_cap = 50

        return min(ceil((self._curr_round * round_multiplier + base_enemy_count) * round_enemy_multiplier), enemy_cap)

    def __biased_random(self, weights):
        choices = list()
        for i in range(len(weights)):
            choices += [*( [i] * weights[i] )]

        return choice(choices) # a bit confusing but its the rand function thingy


    def __spawn_enemies(self):
        count = self.__get_enemy_count()
        enemies = list()

        exclusion_min = -self._stage_size / 2
        exclusion_max = self._stage_size / 2

        base_enemy_spawn_chance = self.__get_enemy_spawn_chance(6, 3)
        turtle_enemy_spawn_chance = self.__get_enemy_spawn_chance(1, 6)
        child_enemy_spawn_chance = self.__get_enemy_spawn_chance(5, 1)

        weights = [base_enemy_spawn_chance, turtle_enemy_spawn_chance, child_enemy_spawn_chance]

        for i in range(count):

            enemy_choice = self.__biased_random(weights)

            pos = Vector2(
                randint(-self._stage_size.x, self._stage_size.x),
                randint(-self._stage_size.y, self._stage_size.y)
            )

            while (pos.x > exclusion_min.x and pos.x < exclusion_max.x) or (pos.y > exclusion_min.y and pos.y < exclusion_max.y):
                pos = Vector2(
                    randint(-self._stage_size.x, self._stage_size.x),
                    randint(-self._stage_size.y, self._stage_size.y)
                )

            enemy = None

            match enemy_choice:
                case 0:
                    enemy = BasicEnemy(self._screen, pos)
                case 1:
                    enemy = TurtleEnemy(self._screen, pos)
                case 2:
                    enemy = ChildEnemy(self._screen, pos)

            enemies.append(
                enemy
            )

        return enemies

    def update(self):
        if self.__can_advance_round() and self._last_round_start != self._curr_round:
            return self.__advance_round()

        return list()

    def draw(self):
        if pygame.time.get_ticks() - self._since_round_start > 3000:
            return

        round_surface = self._font.render("ROUND: " + str(self._curr_round), False, (255, 0, 0))

        self._screen.blit(round_surface, (640, 320))

    #scuffed as hell lmao
    def __can_advance_round(self):
        return pygame.time.get_ticks() - self._since_round_start > self._cooldown_time

    def to_next_round(self):
        if self._last_round_start != self._curr_round:
            return

        self._round_start_sound.play()

        self._since_round_start = pygame.time.get_ticks()
        self._curr_round += 1

    def __advance_round(self):
        enemies = self.__spawn_enemies()

        self._last_round_start += 1

        return enemies



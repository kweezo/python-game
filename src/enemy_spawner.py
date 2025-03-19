from enemy import *
from math import *
from random import *

class EnemySpawner:
    def __init__(self, screen, stage):
        self._stage_size = stage.get_size
        self._curr_round = 0
        self._screen = screen

    def __get_enemy_spawn_chance(self, deviation, mean_round):
        return int(10 - min(abs(self._curr_round - mean_round) / deviation, 10)) # distribution curve halal inshallah approves

    def __get_enemy_count(self):
        base_enemy_count = 2
        round_multiplier = 2
        round_enemy_multiplier = 1.2
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

        base_enemy_spawn_chance = self.__get_enemy_spawn_chance(5, 3)
        turtle_enemy_spawn_chance = self.__get_enemy_spawn_chance(2, 6)

        weights = [base_enemy_spawn_chance, turtle_enemy_spawn_chance]

        for i in range(count):

            enemy_choice = self.__biased_random(weights)
            print(enemy_choice)

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

            enemies.append(
                enemy
            )

        return enemies
    
    def advance_round(self):
        enemies = self.__spawn_enemies()

        self._curr_round += 1

        return enemies



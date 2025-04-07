# Example file showing a basic pygame "game loop"
import pygame
from player import *
from enemy import *
from weapons.weapon import *
from constants import *
from stage import *
from buy_pad import *
from enemy_spawner import *
from dog import *

# pygame setup
pygame.init()
pygame.mixer.init()
pygame.font.init()

pygame.mixer.set_num_channels(128) # more than enough-ish

font = pygame.font.SysFont("res/font.ttf", 50)
font_big = pygame.font.SysFont("res/font.ttf", 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

dt = 0

player = Player(screen, font)

stage = Stage(screen)
buy_pad = WeaponBuyPad(screen, Vector2(500, 500), 69, Weapon(screen, 10, pygame.image.load("res/ak.png").convert_alpha(), Vector2(60, 50), 20, pygame.mixer.Sound("res/sfx/shoot_ak.mp3"), True, (255, 0, 0), 100), player)
dog_pad = DogBuyPad(screen, Vector2(500, 350), 10, player)

enemy_spawner = EnemySpawner(screen, stage, font_big)

Camera.set_limits(Vector2(-200, -200), Vector2(200, 200))

enemies = enemy_spawner.update()

def add_enemy(pos):
    enemies.append(
        Enemy(screen, pos, Vector2(70, 70), 260, 60, 100, pygame.image.load("res/basic_zombie.png").convert_alpha(), 10, 15)
    )

for i in range(0):
    add_enemy(Vector2(randrange(-500, 500), randrange(-500, 500)))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(enemies, stage.get_environment_colliders, dt)
    stage.check_environment_collision(player)
    stage.check_border_collision(player)

    for enemy in enemies:
        stage.check_environment_collision(enemy)
        enemy.update(dt, player.get_pos)
        if enemy.handle_collision(player):
            player.deal_dmg(enemy.get_dmg(), ~(player.get_pos - enemy.get_pos))



    for i in range(len(enemies)):
        if enemies[i].should_destroy():
            player.add_currency(enemies[i].get_worth())
            enemies.pop(i)
            break

        for y in range(i+1, len(enemies)):
            enemies[i].handle_collision(enemies[y])


    buy_pad.update(player)
    dog_pad.update(player)

    if len(enemies) == 0:
        enemy_spawner.to_next_round()
        enemies = enemy_spawner.update()
        player.reset_hp()


    # fill the screen with a color to wipe away anything from last frame
    screen.fill((255 * Camera.get_color_float()[0], 0 * Camera.get_color_float()[1], 255 * Camera.get_color_float()[2]))

    # RENDER YOUR GAME HERE

    Camera.update(player.get_pos + player.get_size / 2, dt)


    stage.draw()

    buy_pad.draw()
    dog_pad.draw()

    player.draw()

    for enemy in enemies:
        enemy.draw(player.get_pos + player.get_size / 2)
    
    stage.draw_on_top()
    enemy_spawner.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()   


    dt = clock.tick(60) / 100  # limits FPS to 60

pygame.quit()
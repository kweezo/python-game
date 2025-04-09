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
ak_pad = WeaponBuyPad(screen, Vector2(500, 500), 69, Weapon(screen, 10, pygame.image.load("res/ak.png").convert_alpha(), Vector2(60, 50), 20, pygame.mixer.Sound("res/sfx/shoot_ak.mp3"), True, (255, 0, 0), 100), player, font)
sniper_pad = WeaponBuyPad(screen, Vector2(350, 500), 100, Weapon(screen, 100, pygame.image.load("res/sniper.png").convert_alpha(), Vector2(100, 50), 20, pygame.mixer.Sound("res/sfx/sniper.wav"), False, (255, 255, 0), 2000), player, font)
dog_pad = DogBuyPad(screen, Vector2(500, 350), 10, player, font)
cure_pad = CureBuyPad(screen, Vector2(350, 350), 1000, player, font)

enemy_spawner = EnemySpawner(screen, stage, font_big)
enemies = enemy_spawner.update()

Camera.set_limits(Vector2(-200, -200), Vector2(200, 200))

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
            stage.check_border_collision(player)



    for i in range(len(enemies)):
        if enemies[i].should_destroy():
            player.add_currency(enemies[i].get_worth())
            enemies.pop(i)
            break

        for y in range(i+1, len(enemies)):
            enemies[i].handle_collision(enemies[y])


    ak_pad.update(player)
    dog_pad.update(player)
    sniper_pad.update(player)
    cure_pad.update(player)

    if len(enemies) == 0:
        enemy_spawner.to_next_round()
        enemies = enemy_spawner.update()
        player.reset_hp()


    screen.fill((255 * Camera.get_color_float()[0], 0 * Camera.get_color_float()[1], 255 * Camera.get_color_float()[2]))


    Camera.update(player.get_pos + player.get_size / 2, dt)


    stage.draw()

    ak_pad.draw()
    sniper_pad.draw()
    cure_pad.draw()
    dog_pad.draw()

    player.draw()

    for enemy in enemies:
        enemy.draw(player.get_pos + player.get_size / 2)
    
    stage.draw_on_top()
    player.draw_on_top()
    ak_pad.draw_on_top()
    sniper_pad.draw_on_top()
    cure_pad.draw_on_top()
    dog_pad.draw_on_top()


    enemy_spawner.draw()

    pygame.display.flip()   


    dt = clock.tick(60) / 100  # it just do be like that

pygame.quit()
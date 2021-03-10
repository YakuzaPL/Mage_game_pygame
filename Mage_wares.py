import math
import random
import pygame
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

# background sound
mixer.music.load("sounds/background.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.3)

score = 0

font = pygame.font.Font("assets/AkayaTelivigala-Regular.ttf", 32)
text_x = 10
text_y = 10


def show_score(x, y):
    score_text = font.render("Wynik: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (x, y))


# screen size setting
screen = pygame.display.set_mode((800, 600))

# game title
pygame.display.set_caption('Wizzard Wars')

# game icon

icon = pygame.image.load("assets/magic-wand.png")
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load("assets/wizard.png").convert_alpha()
player_x = 368
player_y = 480
speed_x = 0
speed_y = 0
move_speed = 7

# evil wizard
enemy_img = []
enemy_x = []
enemy_y = []
enemy_speed_x = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("assets/fortune-teller.png").convert_alpha())
    enemy_x.append(random.randint(1, 735))
    enemy_y.append(0)
    enemy_speed_x.append(random.choice([-4, -3, -2, 2, 3, 4]))

# spell cast

spell_img = pygame.image.load("assets/flash.png").convert_alpha()
spell_x = -50
spell_y = -50
spell_speed_y = 15
spell_state = "ready"  # ready / throw

# end game
over_font = pygame.font.Font("assets/AkayaTelivigala-Regular.ttf", 70)
game_state = "play"  # play / over


def game_over():
    global game_state, num_of_enemies, enemy_y, player_y
    for j in range(num_of_enemies):
        enemy_y[j] = 2000
    player_y = 2000
    game_state = "over"
    over_text = over_font.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def new_game():
    global game_state, score, player_x, player_y
    game_state = "play"
    score = 0
    player_x = 368
    player_y = 480
    for i in range(num_of_enemies):
        gen_enemy(i)


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def throw_spear(x, y):
    global spell_state
    spell_state = "throw"
    screen.blit(spell_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, spear_x, spear_y, d):
    distance = math.sqrt((math.pow(enemy_x - spear_x, 2) + (math.pow(enemy_y - spear_y, 2))))
    if distance < d:
        return True
    else:
        return False


def gen_enemy(i):
    global enemy_x, enemy_y, enemy_speed_x
    enemy_x[i] = random.randint(1, 735)
    enemy_y[i] = random.randint(0, 80)
    enemy_speed_x[i] = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])


running = True

while running:
    # background colour
    screen.fill((102, 102, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "play":
                if event.key == pygame.K_SPACE:
                    if spell_state == "ready":
                        throw_sound = mixer.Sound("sounds/spell_sound.wav")
                        throw_sound.play()
                        spell_y = player_y
                        spell_x = player_x
                        throw_spear(spell_x, spell_y)
            if game_state == "over":
                if event.key == pygame.K_r:
                    new_game()

    # player movement
    keys = pygame.key.get_pressed()
    speed_x = 0
    speed_y = 0
    if game_state == "play":
        if keys[pygame.K_LEFT]:
            speed_x = - move_speed
        elif keys[pygame.K_RIGHT]:
            speed_x = move_speed

        if keys[pygame.K_UP]:
            speed_y = - move_speed
        elif keys[pygame.K_DOWN]:
            speed_y = move_speed

    player_x += speed_x
    player_y += speed_y

    # game field restrictions
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    if player_y <= 0:
        player_y = 0
    elif player_y >= 536:
        player_y = 536

    # opponent movement restriction
    for i in range(num_of_enemies):

        if enemy_y[i] > 536:
            game_over()
            break
        if enemy_x[i] <= 0:
            enemy_speed_x[i] *= -1
            enemy_y[i] += 32
        elif enemy_x[i] >= 736:
            enemy_speed_x[i] *= -1
            enemy_y[i] += 32

        # collision
        collision = is_collision(enemy_x[i], enemy_y[i], spell_x, spell_y, 25)
        if collision:
            throw_sound = mixer.Sound("sounds/death.wav")
            throw_sound.play()
            spell_state = "ready"
            spell_y = -50
            score += 1
            gen_enemy(i)

        player_collision = is_collision(enemy_x[i], enemy_y[i], player_x, player_y, 50)
        if player_collision:
            game_over()

        enemy(enemy_x[i], enemy_y[i], i)

        enemy_x[i] += enemy_speed_x[i]

    if spell_y <= -32:
        spell_y = -50
        spell_state = "ready"

    # thrown spell
    if spell_state == "throw":
        throw_spear(spell_x, spell_y)
        spell_y -= spell_speed_y

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
    clock.tick(60)

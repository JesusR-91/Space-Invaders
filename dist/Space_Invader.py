#IMPORTS
import random
import pygame
import math
from pygame import mixer
import io

#Font transformatio to bytes

def font_bytes(font):
    with open(font, "rb") as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)

# Inicializate pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1000, 800))

class Background(pygame.sprite.Sprite):
    def __init__(self, img, location):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = location

bg_img = pygame.image.load("screenplay2.jpg")
bg_img = pygame.transform.scale(bg_img, (1000, 800))
bg = Background(bg_img, [0, 0])

# Control variable
execute = True

# Title and Img
icon = pygame.image.load("icons8-alien-monster-emoji-48.png")

pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)

# Music
mixer.music.load("level1.mp3")
mixer.music.set_volume(0.01)
mixer.music.play(-1)

# score
score = 0
font_as_bytes = font_bytes("Agdasima-Bold.ttf")
font = pygame.font.Font(font_as_bytes, 32)
score_text_x = 10
score_text_y = 10

# Game over

game_over_text = pygame.font.Font(font_as_bytes, 70)

def game_ove():
    final_text = game_over_text.render("Game Over", True, (255, 255, 255))
    screen.blit(final_text, (375, 320))

# Player
img_player = pygame.image.load("spaceship1.png")
img_player = pygame.transform.scale(img_player, (75, 100))
player_x = 462
player_y = 620
x_movement = 0


def player(x, y):
    screen.blit(img_player, (x, y))


def show_score(x, y):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))


# Bullet

bullets = []

bullet_img = pygame.image.load("bala.png")
bullet_x = 462 + 24
bullet_y = 630


class Bullet():
    def __init__(self, x, y):
        self.img = bullet_img
        self.x = x
        self.y = y
        self.speed = -1


def bullet_collition(x_1, y_1, x_2, y_2):
    collition = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))

    if collition <= 45:
        return True
    else:
        return False

# Enemy

enemy_img = []
enemy_x = []
enemy_y = []
enemy_movement_x = []
enemy_movement_y = []
num_of_enemies = 0

ene_img = pygame.image.load("enemy3.png")
ene_img = pygame.transform.scale(ene_img, (80, 100))


def enemy_spawn():
    for en in range(8):
        enemy_img.append(ene_img)
        enemy_x.append((50 + (en * 110)))
        enemy_y.append(0)
        enemy_movement_x.append(0.3)
        enemy_movement_y.append(80)
        global num_of_enemies
        num_of_enemies += 1

    for en in range(8):
        enemy_img.append(ene_img)
        enemy_x.append((50 + (en * 110)))
        enemy_y.append(160)
        enemy_movement_x.append(0.3)
        enemy_movement_y.append(80)
        num_of_enemies += 1


def enemy(x, y, en):
    screen.blit(enemy_img[en], (x, y))


# Game loop
while execute:

    # Screen
    screen.blit(bg.img, bg.rect)

    # Enemy Spawn
    if num_of_enemies < 16:
        enemy_spawn()

    # Events
    for event in pygame.event.get():

        # Close game event
        if event.type == pygame.QUIT:
            execute = False

        # Key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_movement = -0.5
            if event.key == pygame.K_RIGHT:
                x_movement = 0.5
            if event.key == pygame.K_SPACE:

                if len(bullets) < 2:
                    # Sound
                    shoot_sound = mixer.Sound("shoot.mp3")
                    shoot_sound.set_volume(0.01)
                    shoot_sound.play()

                    # Img
                    bullet_x = player_x + 24
                    new_bullet = Bullet(bullet_x, bullet_y)
                    bullets.append(new_bullet)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_movement = 0

    # Movement player
    player_x += x_movement

    # Bullet movement
    for element in bullets:
        for bull in bullets:
            bull.y += bull.speed
            screen.blit(bull.img, (bull.x, bull.y))
            if bull.y <= 0:
                bullets.remove(element)

    # Enemy movement

    for e in range(num_of_enemies):

        # Game Over condition
        if enemy_y[e] >= 620:
            for k in range(num_of_enemies):
                enemy_y[k] = 2000
                score_text_x = 450
                score_text_y = 400
            game_ove()
            break

        enemy_x[e] = enemy_x[e] + enemy_movement_x[e]
        # Borders enemy
        # x
        if enemy_x[e] <= -30:
            enemy_movement_x[e] = 0.3
            enemy_y[e] += enemy_movement_y[e]
        elif enemy_x[e] > 950:
            enemy_movement_x[e] = -0.3
            enemy_y[e] += enemy_movement_y[e]

        for bullet in bullets:
            # Collition
            checkin_collition = bullet_collition(enemy_x[e], enemy_y[e], bullet.x, bullet.y)

            if checkin_collition:

                # Remove the bullet from the list
                bullets.remove(bullet)

                # Sound
                collition_sound = mixer.Sound("explosion.mp3")
                collition_sound.set_volume(0.01)
                collition_sound.play()

                # Score
                score += 5

                # New enemy
                enemy_x[e] = 50
                enemy_y[e] = 0
                enemy_movement_x[e] = 0.3
                break

        # Drawing enemies
        enemy(enemy_x[e], enemy_y[e], e)

    # Borders player
    if player_x <= -30:
        player_x = -30
    elif player_x > 950:
        player_x = 950

    # Drawing the player
    player(player_x, player_y)

    # Score
    show_score(score_text_x, score_text_y)

    # Update
    pygame.display.update()

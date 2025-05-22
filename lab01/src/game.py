import pygame
import math
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Constants
GENERAL_SCALE = 4
BULLET_SIZE = 5 * GENERAL_SCALE
PLAYER_SIZE = 25 * GENERAL_SCALE
ENEMY_SIZE = 16 * GENERAL_SCALE
SCREEN_WIDTH = 200 * GENERAL_SCALE
SCREEN_HEIGHT = 150 * GENERAL_SCALE
ANIMATION_SPEED = 0.05  # Lower = slower animation, Higher = faster animation

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load('background.jpg')

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
icon = pygame.transform.scale(icon, (ENEMY_SIZE, ENEMY_SIZE))
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (PLAYER_SIZE, PLAYER_SIZE))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_animation = []  # Track animation state for each enemy
enemy_animation_frame = []  # Track animation frame for each enemy
num_of_enemies = 6

# Load and scale enemy image once
enemy_temp = pygame.image.load('enemy.png')
enemy_temp = pygame.transform.scale(enemy_temp, (ENEMY_SIZE, ENEMY_SIZE))

for i in range(num_of_enemies):
    enemyImg.append(enemy_temp)
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(20)
    enemy_animation.append(False)  # False = no animation, True = animating
    enemy_animation_frame.append(0)  # 0-15 for animation frames

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (BULLET_SIZE, BULLET_SIZE))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score
score_value = 0
total_score = 0
level = 1
points_to_next_level = 10 + (10 * level)
font = pygame.font.Font('freesansbold.ttf', 22)

textX = 10
textY = 10

# Game Over

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 255, 0))
    total = font.render("Total : " + str(total_score), True, (0, 255, 0))
    level_text = font.render("Level : " + str(level), True, (0, 255, 0))
    next_level = font.render("Next: " + str(points_to_next_level), True, (0, 255, 0))
    screen.blit(score, (x, y))
    screen.blit(total, (x, y + 40))
    screen.blit(level_text, (x, y + 80))
    screen.blit(next_level, (x, y + 120))

def game_over_text():
  over_text = font.render("GAME OVER", True, (0, 255, 0))
  screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 40, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def check_level_up():
    global level, points_to_next_level, score_value, total_score
    if score_value >= points_to_next_level:
        total_score += score_value  # Add current score to total before resetting
        level += 1
        score_value = 0  # Reset level score
        points_to_next_level = 10 + (10 * level)
        return True
    return False

def animate_enemy(i):
    if enemy_animation[i]:
        if enemy_animation_frame[i] < 8:  # First 8 frames: grow
            scale = 1 + (0.0375 * (enemy_animation_frame[i] + 1) * ANIMATION_SPEED)  # Apply animation speed
            scaled_img = pygame.transform.scale(enemy_temp, (int(ENEMY_SIZE * scale), int(ENEMY_SIZE * scale)))
            screen.blit(scaled_img, (enemyX[i] - (ENEMY_SIZE * (scale-1)/2), enemyY[i] - (ENEMY_SIZE * (scale-1)/2)))
        elif enemy_animation_frame[i] < 16:  # Last 8 frames: shrink
            scale = 1.3 - (0.0375 * (enemy_animation_frame[i] - 7) * ANIMATION_SPEED)  # Apply animation speed
            scaled_img = pygame.transform.scale(enemy_temp, (int(ENEMY_SIZE * scale), int(ENEMY_SIZE * scale)))
            screen.blit(scaled_img, (enemyX[i] - (ENEMY_SIZE * (scale-1)/2), enemyY[i] - (ENEMY_SIZE * (scale-1)/2)))
        
        enemy_animation_frame[i] += ANIMATION_SPEED  # Apply animation speed to frame progression
        if enemy_animation_frame[i] >= 16:  # Animation complete
            enemy_animation[i] = False
            enemy_animation_frame[i] = 0
            return True  # Animation finished
    return False  # Animation still in progress

# Game Loop
running = True
while running:
  #RGB
  screen.fill((0, 0, 0))
  # Background Image
  screen.blit(background, (0, 0))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    #if keystroke is pressed check whether its right or left
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        playerX_change = -1
      if event.key == pygame.K_RIGHT:
        playerX_change = 1
      if event.key == pygame.K_SPACE:
        if bullet_state is "ready":
          bulletX = playerX
          fire_bullet(bulletX, bulletY)
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        playerX_change = 0

  # Player Movement
  playerX += playerX_change
  if playerX <= 0:
    playerX = 0
  elif playerX >= 736:
    playerX = 736

  # Enemy Movement
  for i in range(num_of_enemies):
    # Game Over
    if enemyY[i] > 440:
      for j in range(num_of_enemies):
        enemyY[j] = 2000
      game_over_text()
      break

    enemyX[i] += enemyX_change[i]
    if enemyX[i] <= 0:
      enemyX_change[i] = 0.5
      enemyY[i] += enemyY_change[i]
    elif enemyX[i] >= 736:
      enemyX_change[i] = -0.5
      enemyY[i] += enemyY_change[i]

    # Collision
    collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
    if collision:
      bulletY = 480
      bullet_state = "ready"
      score_value += 1
      total_score += 1  # Also increment total score
      check_level_up()
      if not enemy_animation[i]:
          enemy_animation[i] = True
          enemy_animation_frame[i] = 0
      else:
          enemyX[i] = random.randint(0, 735)
          enemyY[i] = random.randint(50, 150)

    # Draw enemy or animation
    if enemy_animation[i]:
        if animate_enemy(i):  # If animation finished
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
    else:
        enemy(enemyX[i], enemyY[i], i)

  # Bullet Movement
  if bulletY <= 0:
    bulletY = 480
    bullet_state = "ready"
  if bullet_state is "fire":
    fire_bullet(bulletX, bulletY)
    bulletY -= bulletY_change

  # Player
  player(playerX, playerY)
  show_score(textX, textY)
  pygame.display.update()

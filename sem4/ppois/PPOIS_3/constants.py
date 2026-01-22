import copy
from board import boards, board_2
import pygame
import math
import random
import json
import os

# Путь к файлу с таблицей лидеров
LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    """Загружает таблицу лидеров из файла или возвращает стандартную, если файла нет."""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return [
        {"name": "Player1", "score": 10000},
        {"name": "Player2", "score": 8000},
        {"name": "Player3", "score": 5000},
        {"name": "Player4", "score": 3000},
        {"name": "Player5", "score": 1000}
    ]

def save_leaderboard(leaderboard):
    """Сохраняет таблицу лидеров в файл."""
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f)

# Инициализация таблицы лидеров
leaderboard = load_leaderboard()

pygame.init()
# Звуковые эффекты
pygame.mixer.init()
click_sound = pygame.mixer.Sound('sounds/knopka-schelchok-korotkii-zvonkii-blizkii-suhoi1.mp3')
uhh_sound = pygame.mixer.Sound('sounds/uuff-roblox.mp3')
death_sound = pygame.mixer.Sound('sounds/zvuk-smerti-v-igre.mp3')
reverse_movement = pygame.mixer.Sound('sounds/eeee-kak-rulit.mp3')
victory_sound = pygame.mixer.Sound('sounds/pobednaya-melodiya.mp3')
powerup_sounds = [
    pygame.mixer.Sound('sounds/ox-poidet-shhas-voznia-futazi-s-mellstroem-zvukm_YOGyA0Kc.mp3'),
    pygame.mixer.Sound('sounds/ам-ам-ам-мелстрой-мем-оригинал-(256-kbps)-made-with-Voicemod.mp3'),  
    pygame.mixer.Sound('sounds/ооо-чиназес-сюда-сюда-made-with-Voicemod.mp3')
]
available_powerup_sounds = powerup_sounds.copy()

ghost_eat_sound = pygame.mixer.Sound('sounds/brue.mp3')
start_sound = pygame.mixer.Sound('sounds/1-track-1.mp3')

# Функция для получения случайного неповторяющегося звука powerup
def get_random_powerup_sound():
    global available_powerup_sounds
    
    if not available_powerup_sounds:
        available_powerup_sounds = powerup_sounds.copy()
    
    sound = random.choice(available_powerup_sounds)
    available_powerup_sounds.remove(sound)
    
    return sound

# Фоновая музыка
pygame.mixer.music.load('sounds/Parry Gripp - Nom Nom Nom Nom Nom Nom Nom.mp3')
pygame.mixer.music.set_volume(0.2)

# Цвета для меню
MENU_COLOR = (33, 33, 255)
HOVER_COLOR = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)
current_board = boards 

MAP_BUTTON_COLOR = (0, 255, 0)  # Зеленый цвет по умолчанию
CORAL_COLOR = (255, 127, 80)    # Коралловый цвет для второй карты

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(current_board)
color = 'blue'
PI = math.pi
pacman_img = pygame.image.load("images/pacman/default/walk.png").convert_alpha()
blinky_img = pygame.image.load("images/ghost/blinky/walk.png").convert_alpha()
clyde_img = pygame.image.load("images/ghost/clyde/walk.png").convert_alpha()
inky_img = pygame.image.load("images/ghost/inky/walk.png").convert_alpha()
pinky_img = pygame.image.load("images/ghost/pinky/walk.png").convert_alpha()
dead_packman = pygame.image.load("images/pacman/default/dead.png").convert_alpha()
eaten_ghost = pygame.image.load("images/ghost/eaten.png").convert_alpha()
frozen_ghost = pygame.image.load("images/ghost/frightened_1.png").convert_alpha()
frozen_ghost_2 = pygame.image.load("images/ghost/frightened_2.png").convert_alpha()
packman_width = pacman_img.get_width() // 4
packman_height = pacman_img.get_height() // 4
ghost_width = blinky_img.get_width() // 2
ghost_height = blinky_img.get_height() // 4

dead_packman_width = dead_packman.get_width() // 12

def get_images(img, width, height, start, end, amount):
    ghost_images = []
    for i in range(amount):
        frame = img.subsurface((i * start * width, i * end * height, width, height))
        ghost_images.append(pygame.transform.scale(frame, (45,45)))
    return ghost_images


blinky_images = get_images(blinky_img, ghost_width, ghost_height, 0 ,1, 4)
clyde_images = get_images(clyde_img, ghost_width, ghost_height, 0 ,1, 4)
inky_images = get_images(inky_img, ghost_width, ghost_height, 0 ,1, 4)
pinky_images = get_images(pinky_img, ghost_width, ghost_height, 0 , 1, 4)

dead_packman_images = get_images(dead_packman, dead_packman_width, packman_height, 1, 0, 12)
eaten_ghost_images = get_images(eaten_ghost, eaten_ghost.get_width(), eaten_ghost.get_height() // 4, 0 ,1, 4)
#frozen_ghost_images = get_images(frozen_ghost, frozen_ghost.get_width() // 2, frozen_ghost.get_height(), 1, 0, 1)
frozen_ghost_images = get_images(frozen_ghost_2, frozen_ghost_2.get_width() // 4, frozen_ghost_2.get_height(), 1, 0, 3)



RIGHT = 1
LEFT = 0
UP = 3
border = 3
DOWN = 2
DOOR = 9 
small_dot = 1
big_dot = 2
displacement_100 = 100
score_modifier = 100

player_images = []
player_images = get_images(pacman_img, packman_width, packman_height, 1, 0, 4)
# blinky_img = blinky_images[0]
# pinky_img = pinky_images[0]
# inky_img = inky_images[0]
# clyde_img = clyde_images[0]
# spooked_img = frozen_ghost_images[0]
# dead_img = dead_packman_images[0]
player_x = 450
player_y = 663
direction = 0
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 380
clyde_y = 438
clyde_direction = 2
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 0
game_over = False
game_won = False
death_animation = False
death_counter = 0
controls_reversed = False
controls_reversed_counter = 0
ghosts_frozen = False
ghosts_frozen_counter = 0
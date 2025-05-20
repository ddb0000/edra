import pygame

# --- Tamanho do tile e tela ---
TILE_SIZE = 16
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Paths (ajuste conforme seu sistema) ---
TILESET_PATH = "assets/maps/Tilesets/Floors_Tiles.png"
PLAYER_ANIM_PATH = "assets/characters/Body_A/Animations"

# --- Teclas de controle ---
KEY_MOVE_UP    = pygame.K_w
KEY_MOVE_DOWN  = pygame.K_s
KEY_MOVE_LEFT  = pygame.K_a
KEY_MOVE_RIGHT = pygame.K_d
KEY_INTERACT   = pygame.K_e
KEY_ATTACK     = pygame.K_x

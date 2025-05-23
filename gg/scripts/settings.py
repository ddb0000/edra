import os
import pygame

# ─── Tela e FPS ────────────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60

# ─── Dimensão do tile (seu tileset é 16×16) ───────────────────
TILE_SIZE = 16

# ─── Estrutura de pastas de assets ────────────────────────────
# Prefixo relativo à raiz do projeto
ASSETS_DIR   = "assets"

# Tilesets (mapas)
TILESETS_DIR = os.path.join(ASSETS_DIR, "maps", "Tilesets")
TILESET_PATH = os.path.join(TILESETS_DIR, "Floors_Tiles.png")

# Animações do jogador
CHAR_DIR         = os.path.join(ASSETS_DIR, "characters", "Body_A", "Animations")
PLAYER_ANIM_PATH = CHAR_DIR

# ─── Teclas de controle ───────────────────────────────────────
KEY_MOVE_UP    = pygame.K_w
KEY_MOVE_DOWN  = pygame.K_s
KEY_MOVE_LEFT  = pygame.K_a
KEY_MOVE_RIGHT = pygame.K_d

KEY_INTERACT   = pygame.K_e
KEY_ATTACK     = pygame.K_x

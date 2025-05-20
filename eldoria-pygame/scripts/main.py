# scripts/main.py

import pygame
from tilemap import load_tileset, TileMap
from player import Player
from ui import UIManager
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    TILESET_PATH
)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Eldoria War RPG")
    clock = pygame.time.Clock()

    tiles = load_tileset(TILESET_PATH)
    map_layout = [[0] * 50 for _ in range(30)]
    game_map = TileMap(map_layout, tiles)
    player = Player(x=100, y=100)
    ui = UIManager(screen)
    obstacles = []
    cam = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    show_dialog_once = True

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(dt, obstacles)

        if show_dialog_once:
            ui.show_text("Teste de diálogo! Aperte E para continuar.")
            show_dialog_once = False

        cam.x = player.rect.centerx - (SCREEN_WIDTH // 2)
        cam.y = player.rect.centery  - (SCREEN_HEIGHT // 2)
        cam.x = max(0, min(cam.x, game_map.width  - SCREEN_WIDTH))
        cam.y = max(0, min(cam.y, game_map.height - SCREEN_HEIGHT))

        screen.fill((0, 0, 0))
        game_map.draw(screen, cam)
        screen.blit(player.image, (player.rect.x - cam.x, player.rect.y - cam.y))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

import os
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    TILESET_PATH, KEY_INTERACT
)
from tilemap import load_tileset, TileMap
from player  import Player
from ui      import UIManager

def main():
    # ─── Inicialização ──────────────────────────────────────────
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Eldoria War RPG")
    clock = pygame.time.Clock()

    # ─── Carregamento do Tileset e Mapa ─────────────────────────
    # Garante que o caminho é relativo à raiz do projeto
    base = os.getcwd()
    tileset_file = os.path.join(base, TILESET_PATH)
    tiles = load_tileset(tileset_file)

    # Layout de exemplo 50×30, tudo índice 0 (chão)
    map_layout = [[0] * 50 for _ in range(30)]
    game_map   = TileMap(map_layout, tiles)

    # ─── Criação dos objetos ────────────────────────────────────
    player = Player(x=100, y=100)
    ui     = UIManager(screen)

    # no futuro, coloque aqui seus blockers:
    obstacles = []

    # câmera
    cam = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    # flag para diálogo de teste apenas uma vez
    first_dialog = True

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # delta em segundos

        # ─── Eventos ─────────────────────────────────────────────
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # ─── Atualização ─────────────────────────────────────────
        player.update(dt, obstacles)

        # ─── Diálogo de teste ───────────────────────────────────
        if first_dialog:
            ui.show_text("Teste de diálogo! Aperte E para continuar.")
            first_dialog = False

        # ─── Ajuste da câmera ────────────────────────────────────
        cam.center = player.hitbox.center
        cam.x = max(0, min(cam.x, game_map.width  - SCREEN_WIDTH))
        cam.y = max(0, min(cam.y, game_map.height - SCREEN_HEIGHT))

        # ─── Desenho ────────────────────────────────────────────
        screen.fill((0, 0, 0))
        game_map.draw(screen, cam)

        # desenha o player relativo à câmera
        screen.blit(
            player.image,
            (player.rect.x - cam.x,
             player.rect.y - cam.y)
        )

        # desenha eventuais diálogos ativos
        ui.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

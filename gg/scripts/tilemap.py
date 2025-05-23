import pygame
from settings import TILE_SIZE

def load_tileset(path):
    """
    Carrega uma imagem de tileset e recorta em blocos TILE_SIZE × TILE_SIZE.
    Retorna uma lista de pygame.Surface.
    """
    sheet = pygame.image.load(path).convert_alpha()
    sheet_w, sheet_h = sheet.get_size()
    tiles = []
    for y in range(0, sheet_h, TILE_SIZE):
        for x in range(0, sheet_w, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            tiles.append(sheet.subsurface(rect).copy())
    return tiles

class TileMap:
    """
    Representa um mapa de tiles com um layout (matriz de índices).
    """
    def __init__(self, layout, tiles):
        """
        :param layout: lista de listas de índices, e.g. [[0,1,0], [2,0,1], ...]
        :param tiles: lista de pygame.Surface carregadas em load_tileset()
        """
        self.layout = layout
        self.tiles  = tiles

        # dimensões totais do mapa em pixels
        self.width  = len(layout[0]) * TILE_SIZE
        self.height = len(layout) * TILE_SIZE

    def draw(self, surface, cam_rect):
        """
        Desenha apenas as tiles visíveis dentro da câmera (cam_rect).
        :param surface: a Surface principal onde desenhar
        :param cam_rect: pygame.Rect definindo a região de mundo a exibir
        """
        sw, sh = surface.get_size()

        for row_idx, row in enumerate(self.layout):
            for col_idx, tile_idx in enumerate(row):
                world_x = col_idx * TILE_SIZE
                world_y = row_idx * TILE_SIZE

                # converte para coordenadas de tela subtraindo a câmera
                screen_x = world_x - cam_rect.x
                screen_y = world_y - cam_rect.y

                # se dentro da viewport, desenha
                if 0 <= screen_x < sw and 0 <= screen_y < sh:
                    surface.blit(self.tiles[tile_idx], (screen_x, screen_y))

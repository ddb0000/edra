import pygame
from settings import TILE_SIZE

def load_tileset(path):
    """
    Carrega uma imagem de tileset e recorta em blocos TILE_SIZE × TILE_SIZE.
    Retorna uma lista de Surfaces.
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
    def __init__(self, layout, tiles):
        """
        layout: lista de listas de índices em 'tiles'
        tiles: lista de pygame.Surface
        """
        self.layout = layout
        self.tiles  = tiles
        # Dimensão total do mapa em pixels:
        self.width  = len(layout[0]) * TILE_SIZE
        self.height = len(layout) * TILE_SIZE

    def draw(self, surface, cam_rect):
        """
        Desenha só a região visível pela câmera (cam_rect).
        """
        for row_index, row in enumerate(self.layout):
            for col_index, tile_index in enumerate(row):
                world_x = col_index * TILE_SIZE
                world_y = row_index * TILE_SIZE
                screen_x = world_x - cam_rect.x
                screen_y = world_y - cam_rect.y

                # Só desenha se estiver visível na tela
                if (0 <= screen_x < surface.get_width() and
                    0 <= screen_y < surface.get_height()):
                    surface.blit(self.tiles[tile_index], (screen_x, screen_y))

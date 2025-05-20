import pygame, os

class TileMap:
    def __init__(self, tileset_filename, tw, th):
        path = os.path.join('assets','maps','tilesets', tileset_filename)
        sheet = pygame.image.load(path).convert_alpha()
        sw, sh = sheet.get_size()
        cols, rows = sw // tw, sh // th

        self.tile_w, self.tile_h = tw, th
        self.tiles = [
            sheet.subsurface(pygame.Rect(x*tw, y*th, tw, th)).copy()
            for y in range(rows) for x in range(cols)
        ]

        # Exemplo simples de layout (0 = piso, 1 = outro piso, -1 = vazio)
        self.map_data = [
            [0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,0],
            [0,1,-1,-1,-1,-1,1,0],
            [0,1,-1,2,2,-1,1,0],
            [0,1,-1,-1,-1,-1,1,0],
            [0,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0],
        ]
        self.width  = len(self.map_data[0]) * tw
        self.height = len(self.map_data)    * th

    def draw(self, surface, camera):
        for y, row in enumerate(self.map_data):
            for x, idx in enumerate(row):
                if idx >= 0 and idx < len(self.tiles):
                    px = x*self.tile_w - camera.offset.x
                    py = y*self.tile_h - camera.offset.y
                    surface.blit(self.tiles[idx], (px, py))

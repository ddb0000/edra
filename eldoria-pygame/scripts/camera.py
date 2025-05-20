import pygame

class Camera:
    def __init__(self, map_width, map_height, screen_width, screen_height):
        # limites do mundo (pixel)
        self.map_w, self.map_h = map_width, map_height
        # tamanho da janela
        self.screen_w, self.screen_h = screen_width, screen_height
        # retângulo de deslocamento
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_rect):
        # centraliza a câmera na posição do target
        x = target_rect.centerx - self.screen_w // 2
        y = target_rect.centery - self.screen_h // 2
        # clampa para não sair do mapa
        x = max(0, min(x, self.map_w - self.screen_w))
        y = max(0, min(y, self.map_h - self.screen_h))
        self.offset.update(x, y)

    def apply(self, rect):
        # desloca qualquer rect para a coordenada de tela
        return rect.move(-self.offset.x, -self.offset.y)

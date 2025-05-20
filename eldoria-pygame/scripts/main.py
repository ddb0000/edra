import pygame, sys
from character import Player
from map import TileMap
from camera import Camera

def main():
    pygame.init()
    SW, SH = 800, 600
    screen = pygame.display.set_mode((SW, SH))
    clock = pygame.time.Clock()

    # agora usamos o tileset de chão, tamanho 32×32
    tilemap = TileMap('Floors_Tiles.png', 32, 32)
    cam = Camera(tilemap.width, tilemap.height, SW, SH)

    player = Player(100, 100)
    player_group = pygame.sprite.GroupSingle(player)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player_group.update()
        cam.update(player.rect)

        screen.fill((0,0,0))
        tilemap.draw(screen, cam)
        for spr in player_group:
            screen.blit(spr.image, cam.apply(spr.rect))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

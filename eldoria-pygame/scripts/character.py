import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Armazenará todas as animações por key: Idle_Down, Walk_Side, etc.
        self.animations = {}
        self.frame_index = 0
        self.animation_speed = 0.15

        # Estado de direção atual (Down, Up, Side) e se está virado para a esquerda
        self.direction_status = 'Down'
        self.facing_left = False

        # Carrega todas as animações ao iniciar
        self.load_animations()

        # Estado inicial: idle olhando para baixo
        self.status = f'Idle_{self.direction_status}'
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = pygame.math.Vector2(0, 0)

    def load_animations(self):
        base_path = os.path.join('assets', 'characters', 'Body_A', 'Animations')
        for anim_folder in os.listdir(base_path):
            folder_path = os.path.join(base_path, anim_folder)
            if not os.path.isdir(folder_path):
                continue

            # Cada sheet PNG tem o nome: <Action>_<Dir>-Sheet.png (ex: Walk_Down-Sheet.png)
            for fname in sorted(os.listdir(folder_path)):
                if fname.endswith('-Sheet.png'):
                    key = fname.replace('-Sheet.png', '')      # ex: "Walk_Down"
                    sheet = pygame.image.load(os.path.join(folder_path, fname)).convert_alpha()
                    w, h = sheet.get_size()
                    cols = w // h                              # número de frames
                    frames = []
                    for i in range(cols):
                        rect = pygame.Rect(i*h, 0, h, h)
                        frames.append(sheet.subsurface(rect).copy())
                    self.animations[key] = frames

    def update(self):
        self.animate()
        self.move()

    def animate(self):
        frames = self.animations[self.status]
        self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
        frame = frames[int(self.frame_index)]
        # Se é animação lateral e estiver virado pra esquerda, flip
        if 'Side' in self.status and self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    def move(self):
        self.rect.x += self.direction.x * 3
        self.rect.y += self.direction.y * 3

    def handle_input(self, keys):
        # Reseta direção
        self.direction.x = 0
        self.direction.y = 0

        # Movimentação e mudança de estado
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.direction_status = 'Side'
            self.facing_left = True
            self.status = 'Walk_Side'
            self.frame_index = 0

        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.direction_status = 'Side'
            self.facing_left = False
            self.status = 'Walk_Side'
            self.frame_index = 0

        elif keys[pygame.K_UP]:
            self.direction.y = -1
            self.direction_status = 'Up'
            self.facing_left = False
            self.status = 'Walk_Up'
            self.frame_index = 0

        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.direction_status = 'Down'
            self.facing_left = False
            self.status = 'Walk_Down'
            self.frame_index = 0

        else:
            # sem tecla, volta para idle na última direção
            self.status = f'Idle_{self.direction_status}'
            self.frame_index = 0

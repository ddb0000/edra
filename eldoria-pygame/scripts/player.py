# scripts/player.py

import pygame
import os
from settings import (
    KEY_MOVE_UP, KEY_MOVE_DOWN,
    KEY_MOVE_LEFT, KEY_MOVE_RIGHT,
    PLAYER_ANIM_PATH
)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carrega animações no formato { "Walk_Down": [...], "Idle_Side": [...], ... }
        self.animations = self.load_player_frames(PLAYER_ANIM_PATH)

        # Estado inicial (olhando para baixo parado)
        self.status    = "Idle_Down"
        self.frame_idx = 0
        self.image     = self.animations[self.status][0]
        self.rect      = self.image.get_rect(topleft=(x, y))

        # Vetor de direção e velocidade
        self.direction = pygame.Vector2(0, 0)
        self.speed     = 100  # pixels por segundo

        # Para saber qual direção usar no idle
        self.last_dir  = pygame.Vector2(0, 1)
        # Para flipar horizontalmente as animações de lado
        self.flip_h    = False

    def load_player_frames(self, base_path):
        """
        Procura recursivamente por arquivos '*-Sheet.png' e gera uma lista de frames
        para cada nome base (ex: 'Walk_Down', 'Idle_Side', ...).
        """
        animations = {}
        # caminha por todas as subpastas
        for root, _, files in os.walk(base_path):
            for fname in files:
                if not fname.endswith("-Sheet.png"):
                    continue
                key = fname[:-len("-Sheet.png")]  # ex: 'Walk_Down'
                full_path = os.path.join(root, fname)
                sheet = pygame.image.load(full_path).convert_alpha()
                w, h = sheet.get_size()
                count = w // h  # número de quadros na largura
                frames = []
                for i in range(count):
                    rect = pygame.Rect(i*h, 0, h, h)
                    frames.append(sheet.subsurface(rect).copy())
                animations[key] = frames

        # Verificação básica
        expected = [
            "Idle_Down","Idle_Up","Idle_Side",
            "Walk_Down","Walk_Up","Walk_Side"
        ]
        for e in expected:
            if e not in animations:
                raise Exception(f"Animação faltando: {e} em {base_path}")
        return animations

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = keys[KEY_MOVE_RIGHT] - keys[KEY_MOVE_LEFT]
        dy = keys[KEY_MOVE_DOWN]  - keys[KEY_MOVE_UP]
        self.direction.x = dx
        self.direction.y = dy

        if dx == 0 and dy == 0:
            # parado: escolhe Idle_* com base em last_dir
            if abs(self.last_dir.x) > abs(self.last_dir.y):
                self.status = "Idle_Side"
                self.flip_h = self.last_dir.x < 0
            else:
                if self.last_dir.y < 0:
                    self.status = "Idle_Up"
                else:
                    self.status = "Idle_Down"
        else:
            # andando: escolhe Walk_* e armazena last_dir
            if abs(dx) > abs(dy):
                self.status = "Walk_Side"
                self.flip_h = dx < 0
                self.last_dir = pygame.Vector2(dx, 0)
            else:
                if dy < 0:
                    self.status = "Walk_Up"
                else:
                    self.status = "Walk_Down"
                self.last_dir = pygame.Vector2(0, dy)

    def move_and_collide(self, dt, obstacles):
        vel = (self.direction.normalize() * self.speed * dt
               if self.direction.length() else pygame.Vector2(0, 0))

        # movimento em X
        self.rect.x += vel.x
        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                if vel.x > 0: self.rect.right = obj.rect.left
                if vel.x < 0: self.rect.left  = obj.rect.right

        # movimento em Y
        self.rect.y += vel.y
        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                if vel.y > 0: self.rect.bottom = obj.rect.top
                if vel.y < 0: self.rect.top    = obj.rect.bottom

    def animate(self, dt):
        frames = self.animations[self.status]
        self.frame_idx = (self.frame_idx + 10 * dt) % len(frames)
        frame = frames[int(self.frame_idx)]
        # aplica flip apenas no eixo X quando animação lateral
        self.image = pygame.transform.flip(frame, self.flip_h, False)

    def update(self, dt, obstacles):
        self.handle_input()
        self.move_and_collide(dt, obstacles)
        self.animate(dt)

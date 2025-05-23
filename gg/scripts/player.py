import pygame, os
from settings import (
    KEY_MOVE_UP, KEY_MOVE_DOWN,
    KEY_MOVE_LEFT, KEY_MOVE_RIGHT,
    PLAYER_ANIM_PATH, TILE_SIZE
)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carrega animações (Walk/Idle, Up/Down/Side)
        self.animations = self._load_frames(PLAYER_ANIM_PATH)
        # Estado inicial
        self.status    = "Idle_Down"
        self.frame_idx = 0

        # Imagem e rect para desenhar
        self.image = self.animations[self.status][0]
        self.rect  = self.image.get_rect(topleft=(x, y))

        # Definindo a hitbox (8px de altura apenas nos pés)
        hb_w = self.rect.width - 4
        hb_h = 8
        hb_x = self.rect.x + 2
        hb_y = self.rect.y + (self.rect.height - hb_h)
        self.hitbox = pygame.Rect(hb_x, hb_y, hb_w, hb_h)

        # Offset para sincronizar rect ←→ hitbox
        self._offset = pygame.Vector2(
            self.rect.x - self.hitbox.x,
            self.rect.y - self.hitbox.y
        )

        # Movimento
        self.direction = pygame.Vector2(0, 0)
        self.speed     = 100  # px/s
        # Para manter direção anterior quando parado
        self.last_dir = pygame.Vector2(0, 1)
        # Flip horizontal para animação lateral
        self.flip_h = False

    def _load_frames(self, base_path):
        """
        Varre cada subpasta em base_path e carrega arquivos '*-Sheet.png'
        como animações de 3 quadros. Retorna dicionário:
        { 'Walk_Down': [surf1, surf2, surf3], 'Idle_Side': [...], ... }
        """
        anims = {}
        for fname in os.listdir(base_path):
            dir_full = os.path.join(base_path, fname)
            if not os.path.isdir(dir_full):
                continue
            for file in os.listdir(dir_full):
                if not file.endswith("-Sheet.png"):
                    continue
                key = file[:-len("-Sheet.png")]  # ex: 'Walk_Down'
                sheet = pygame.image.load(os.path.join(dir_full, file)).convert_alpha()
                w, h = sheet.get_size()
                count = w // h
                frames = []
                for i in range(count):
                    rect = pygame.Rect(i*h, 0, h, h)
                    frames.append(sheet.subsurface(rect).copy())
                anims[key] = frames

        # Verificação mínima
        needed = ["Idle_Down","Idle_Up","Idle_Side","Walk_Down","Walk_Up","Walk_Side"]
        for k in needed:
            if k not in anims:
                raise RuntimeError(f"Animação faltando: {k}")
        return anims

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = keys[KEY_MOVE_RIGHT] - keys[KEY_MOVE_LEFT]
        dy = keys[KEY_MOVE_DOWN]  - keys[KEY_MOVE_UP]
        self.direction.x = dx
        self.direction.y = dy

        if dx == 0 and dy == 0:
            # Parado → Idle baseado em last_dir
            if abs(self.last_dir.x) > abs(self.last_dir.y):
                self.status = "Idle_Side"
                self.flip_h = self.last_dir.x < 0
            else:
                if self.last_dir.y < 0:
                    self.status = "Idle_Up"
                else:
                    self.status = "Idle_Down"
        else:
            # Andando → Walk_* e atualiza last_dir
            if abs(dx) > abs(dy):
                self.status = "Walk_Side"
                self.flip_h  = dx < 0
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

        # Move hitbox em X e corrige colisão
        self.hitbox.x += vel.x
        for obs in obstacles:
            if self.hitbox.colliderect(obs.rect):
                if vel.x > 0: self.hitbox.right = obs.rect.left
                if vel.x < 0: self.hitbox.left  = obs.rect.right

        # Move hitbox em Y e corrige colisão
        self.hitbox.y += vel.y
        for obs in obstacles:
            if self.hitbox.colliderect(obs.rect):
                if vel.y > 0: self.hitbox.bottom = obs.rect.top
                if vel.y < 0: self.hitbox.top    = obs.rect.bottom

        # Sincroniza rect para desenhar
        new_tl = pygame.Vector2(self.hitbox.topleft) + self._offset
        self.rect.topleft = (round(new_tl.x), round(new_tl.y))

    def animate(self, dt):
        frames = self.animations[self.status]
        self.frame_idx = (self.frame_idx + 10 * dt) % len(frames)
        frame = frames[int(self.frame_idx)]
        # Aplica flip horizontal se for animação lado
        self.image = pygame.transform.flip(frame, self.flip_h, False)

    def update(self, dt, obstacles):
        self.handle_input()
        self.move_and_collide(dt, obstacles)
        self.animate(dt)

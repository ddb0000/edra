import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, KEY_INTERACT

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.panel = pygame.Surface((SCREEN_WIDTH, 100))
        self.panel.set_alpha(200)
        self.panel.fill((0, 0, 0))

    def show_text(self, text):
        """
        Mostra um painel com texto e espera o jogador apertar KEY_INTERACT para continuar.
        """
        # Quebra linhas se necessário
        lines = self._wrap_text(text, SCREEN_WIDTH - 20)
        for line in lines:
            self.screen.blit(self.panel, (0, SCREEN_HEIGHT - 100))
            txt_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(txt_surf, (10, SCREEN_HEIGHT - 90 + 25 * lines.index(line)))
        pygame.display.flip()

        # Espera o jogador apertar E
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == KEY_INTERACT:
                        waiting = False

    def _wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current = ""
        for w in words:
            test = current + (" " if current else "") + w
            if self.font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

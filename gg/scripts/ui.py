import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, KEY_INTERACT

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        # Fonte padrão tamanho 20
        self.font = pygame.font.Font(None, 20)
        # Painel semi-transparente de diálogo (full width x 100px height)
        self.panel = pygame.Surface((SCREEN_WIDTH, 100))
        self.panel.set_alpha(200)
        self.panel.fill((0, 0, 0))
        # Flag e texto corrente
        self.active = False
        self.queue  = []

    def show_text(self, text):
        """
        Adiciona um texto à fila e bloqueia até o jogador confirmar.
        """
        self.queue.append(text)
        self.active = True
        # Enquanto houver textos na fila, desenha painel e aguarda E
        while self.queue:
            self._draw_panel(self.queue[0])
            pygame.display.flip()
            # Loop de bloqueio até o usuário apertar KEY_INTERACT
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if e.type == pygame.KEYDOWN and e.key == KEY_INTERACT:
                        waiting = False
            # Remove o texto já exibido
            self.queue.pop(0)
        self.active = False

    def _draw_panel(self, text):
        # Desenha o painel
        self.screen.blit(self.panel, (0, SCREEN_HEIGHT - 100))
        # Quebra em linhas
        lines = self._wrap_text(text, SCREEN_WIDTH - 20)
        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(surf, (10, SCREEN_HEIGHT - 90 + i * 25))

    def _wrap_text(self, text, max_width):
        """
        Quebra 'text' em múltiplas linhas para caber no painel.
        """
        words = text.split(' ')
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            if self.font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

    def draw(self):
        """
        Chamado todo frame em main.loop; 
        mantém o panel visível enquanto active=True.
        """
        if self.active and self.queue:
            # desenha o painel com o texto que está no topo da fila
            self._draw_panel(self.queue[0])

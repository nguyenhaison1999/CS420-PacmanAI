import pygame
import sys
from settings import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

########################################### HELPER FUNCTIONS ###########################################
    def draw_text(self, words, screen, position, size, color, font_name, center=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if center:
            position[0] = position[0] - text_size[0]//2
            position[1] = position[1] - text_size[1]//2
        screen.blit(text, position)

########################################### INTRO FUNCTIONS ###########################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('HIGH SCORE', self.screen, [4, 0], START_TEXT_SIZE,
                       (255, 255, 255), START_FONT)
        self.draw_text('PUSH SPACE TO START', self.screen, [WIDTH//2, HEIGHT//2 - 50], START_TEXT_SIZE,
                       (170, 132, 58), START_FONT, center=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2 + 5], START_TEXT_SIZE,
                       (33, 137, 156), START_FONT, center=True)
        self.draw_text('SELECT LEVEL ', self.screen, [WIDTH//2 - 15, HEIGHT//2 + 55], START_TEXT_SIZE,
                       (247, 243, 242), START_FONT, center=True)
        pygame.display.update()

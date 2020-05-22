import pygame
import sys
import random
from settings import *
from player_class import *
from enemy_class import *

pygame.init()
vec = pygame.math.Vector2

pygame.display.set_caption("Pacman - AI project")


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.level = 0
        self.map = 0
        self.wallFile = self.get_wall_file()

        self.walls = []
        self.coins = []
        self.empty_grid = []
        self.empty_grid_score = []
        self.enemies = []

        self.player_pos = None
        self.enemy_pos = []

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'end':
                self.end_events()
                self.end_update()
                self.end_draw()
            else:
                self.running = False
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

    def load(self):
        self.draw_map()

    def get_wall_file(self):
        return "map" + str(self.map) + ".txt"

    def draw_map(self):
        with open(self.wallFile, 'r',) as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    # WALLS
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    # COINS
                    elif char == "2":
                        self.coins.append(vec(xidx, yidx))
                    # PLAYER
                    elif char == "P":
                        self.player_pos = [xidx, yidx]
                        self.empty_grid.append(vec(xidx, yidx))
                    # ENEMY
                    elif char == "3" and self.level != 1:
                        self.enemy_pos.append([xidx, yidx])
                        self.empty_grid.append(vec(xidx, yidx))
                    else:
                        self.empty_grid.append(vec(xidx, yidx))

    def make_enemies(self):
        for idx, position in enumerate(self.enemy_pos):
            self.enemies.append(Enemy(self, vec(position), idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(
                self.screen, GREY, (x*self.cell_width + TOP_BOTTOM_BUFFER//2, 0), (x*self.cell_width + TOP_BOTTOM_BUFFER//2, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(
                self.screen, GREY, (0, x*self.cell_height + TOP_BOTTOM_BUFFER//2), (WIDTH, x*self.cell_height + TOP_BOTTOM_BUFFER//2))
        for wall in self.walls:
            pygame.draw.rect(self.screen, (52, 82, 235), (wall.x*self.cell_width + TOP_BOTTOM_BUFFER//2,
                                                          wall.y*self.cell_height + TOP_BOTTOM_BUFFER//2, self.cell_width, self.cell_height))

    def reset(self):
        # Reset player
        self.player.lives = 1
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0

        # Reset enemy
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        # makes coin from map again
        self.coins = []
        with open(self.wallFile, 'r',) as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '2':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"


########################################### INTRO FUNCTIONS ###########################################


    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.level < 4:
                        self.level += 1
                if event.key == pygame.K_DOWN:
                    if self.level > 0:
                        self.level -= 1
                if event.key == pygame.K_RIGHT:
                    if self.map < 5:
                        self.map += 1
                if event.key == pygame.K_LEFT:
                    if self.map > 0:
                        self.map -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
                self.wallFile = self.get_wall_file()
                self.load()
                self.player = Player(self, vec(self.player_pos))
                self.make_enemies()

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE TO START', self.screen, [WIDTH//2, HEIGHT//2 - 50], START_TEXT_SIZE,
                       (252, 255, 18), START_FONT, center=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE,
                       (33, 137, 156), START_FONT, center=True)
        self.draw_text('SELECT LEVEL: {}'.format(self.level), self.screen, [WIDTH//2, HEIGHT//2 + 50], START_TEXT_SIZE,
                       (255, 43, 18), START_FONT, center=True)

        mapNames = ["No Escape!!!",  "Jenga",
                    "One Pillar pagoda", "Sun temple", "Tartarus", "HCM map"]

        self.draw_text('<< {} >>'.format(mapNames[self.map]), self.screen, [WIDTH//2, HEIGHT//2 + 100], 18,
                       (255, 104, 0), START_FONT, center=True)
        pygame.display.update()

########################################### PLAYING FUNCTIONS ###########################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.level == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.moveHuman(vec(-1, 0))
                    if event.key == pygame.K_RIGHT:
                        self.player.moveHuman(vec(1, 0))
                    if event.key == pygame.K_UP:
                        self.player.moveHuman(vec(0, -1))
                    if event.key == pygame.K_DOWN:
                        self.player.moveHuman(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()
        if not self.coins:
            self.state = "end"

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.draw_coins()
        self.draw_grid()

        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen,
                       [60, 0], 18, WHITE, START_FONT)

        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "end"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0

            # reset enemy position
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        if self.level == 1 or self.level == 2:
            if len(self.coins) > 1:
                coinsTemp = random.choice(self.coins)
                self.coins.clear()
                self.coins.append(coinsTemp)
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7), (int(
                coin.x*self.cell_width) + self.cell_width//2 + TOP_BOTTOM_BUFFER//2, int(coin.y*self.cell_height) + self.cell_height//2 + TOP_BOTTOM_BUFFER//2), 5)

########################################### end FUNCTIONS ###########################################

    def end_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def end_update(self):
        pass

    def end_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press ESC to QUIT"
        again_text = "Press SPACE to PLAY AGAIN"
        score = "Your score: " + str(self.player.current_score)
        if not self.coins:
            self.draw_text('CONGRATULATION!!!', self.screen, [WIDTH//2, 180], 52,
                           YELLOW, "arial", center=True)
            self.draw_text(score, self.screen, [WIDTH//2, HEIGHT//2], 36,
                           (190, 190, 190), "arial", center=True)
        else:
            self.draw_text('GAME OVER ', self.screen, [WIDTH//2, 180], 52,
                           RED, "arial", center=True)
            self.draw_text(again_text, self.screen, [WIDTH//2, HEIGHT//2], 36,
                           (190, 190, 190), "arial", center=True)
        self.draw_text(quit_text, self.screen, [WIDTH//2, HEIGHT//1.5], 36,
                       (190, 190, 190), "arial", center=True)
        pygame.display.update()

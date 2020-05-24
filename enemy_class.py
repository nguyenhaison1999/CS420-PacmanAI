import pygame
import random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.color = self.set_color()
        self.direction = vec(0, 0)  # moving at start
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        # Tracking the enemy position
        self.grid_pos[0] = (
            self.pix_pos[0] - TOP_BOTTOM_BUFFER // 2) // self.app.cell_width
        self.grid_pos[1] = (
            self.pix_pos[1] - TOP_BOTTOM_BUFFER // 2) // self.app.cell_height

    def draw(self):
        pygame.draw.circle(self.app.screen, self.color,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        if self.personality == "speedy":
            speed = 1
        elif self.personality == "slow":
            speed = 0.5
        else:
            speed = 0.75
        return speed

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.app.level == 3:
            if self.personality == "random":
                self.direction = self.get_random_direction()
            if self.personality == "speedy":
                self.direction = self.get_random_direction()
            if self.personality == "slow":
                self.direction = self.get_random_direction()
            if self.personality == "scared":
                self.direction = self.get_path_direction(self.target)
        elif self.app.level == 4 or self.app.level == 0:
            if self.personality == "random":
                self.direction = self.get_random_direction()
            if self.personality == "speedy":
                self.direction = self.get_path_direction(self.target)
            if self.personality == "slow":
                self.direction = self.get_path_direction(self.target)
            if self.personality == "scared":
                self.direction = self.get_path_direction(self.target)

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] < ROWS//2:
                return vec(1, ROWS-2)
            if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(COLS-2, 1)
            else:
                return vec(COLS-2, ROWS-2)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        if next_cell != 0:
            xdir = next_cell[0] - self.grid_pos[0]
            ydir = next_cell[1] - self.grid_pos[1]
            return vec(xdir, ydir)
        else:
            return vec(0, 0)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])
        if path != 0:
            return path[1]
        else:
            return 0

    def BFS(self, start_pos, target_pos):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start_pos]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target_pos:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [
                                neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append(
                                        {"Current":  current, "Next":  next_cell})
        shortest = [target_pos]
        # no solution
        check = [step['Next'] for step in path]
        if target_pos not in check:
            return 0
        # backtracking
        while target_pos != start_pos:
            for step in path:
                if step["Next"] == target_pos:
                    target_pos = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1

            next_position = vec(self.grid_pos.x + x_dir,
                                self.grid_pos.y + y_dir)
            if next_position not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def get_pix_pos(self):
        return (
            vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2 + (self.app.cell_width//2),
                (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2 + (self.app.cell_height//2)))

    def set_color(self):
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (197, 200, 27)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)
        else:
            return (1, 1, 1)

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        if self.number == 1:
            return "slow"
        if self.number == 2:
            return "random"
        else:
            return "scared"

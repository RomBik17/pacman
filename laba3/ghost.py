
import random
import pygame
from metadata import *
from search import *
vec = pygame.math.Vector2

import queue

class Ghost:
    def __init__(self, game, start_position, ghost_type):
        self.type = None
        self.game = game
        self.position = start_position
        self.pix_position = self.get_pix_pos()
        self.path = None
        self.grid_position = start_position
        self.direction = vec(0, 0)
        self.personality = ghost_type
        self.speed = 2

    def draw(self):
        pygame.draw.circle(self.game.screen, RED,
                           (self.pix_position.x, self.pix_position.y),
                           self.game.cell_width // 2 - 2)

    def get_pix_pos(self):
        return vec((self.position[0] * self.game.cell_width) + PADDING // 2 + self.game.cell_width // 2,
                   (self.position[1] * self.game.cell_height) +
                   PADDING // 2 + self.game.cell_height // 2)

    def update(self):
        self.target = (int(self.game.pacman.grid_pos[1]), int(self.game.pacman.grid_pos[0]))
        if self.target != self.grid_position:
            self.pix_position += self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_position[0] = (self.pix_position[0] - PADDING +
                                 self.game.cell_width // 2) // self.game.cell_width + 1
        self.grid_position[1] = (self.pix_position[1] - PADDING +
                                 self.game.cell_height // 2) // self.game.cell_height + 1

    def time_to_move(self):
        if int(self.pix_position.x+PADDING//2) % self.game.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_position.y+PADDING//2) % self.game.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def get_random_direction(self):
        while True:
            rand_int = random.randint(0, 3)
            random_direction = vec(0, 0)
            if rand_int == 0:
                random_direction = vec(-1, 0)
            elif rand_int == 1:
                random_direction = vec(1, 0)
            elif rand_int == 2:
                random_direction = vec(0, 1)
            elif rand_int == 3:
                random_direction = vec(0, -1)
            if vec(self.grid_position + random_direction) not in self.game.walls:
                return random_direction

    def get_a_star_direction(self):
        path = a_star(self.game.grid_map, (int(self.grid_position[1]), int(self.grid_position[0])),
                      (int(self.game.pacman.grid_pos[1]), int(self.game.pacman.grid_pos[0])),
                      euclid_heuristic, 0)
        next_step = (path[1][1], path[1][0])
        direction = vec(int(next_step[0] - self.grid_position[0]), int(next_step[1] - self.grid_position[1]))
        print(direction)
        return direction



    def move(self):
        if self.personality == RANDOM:
            self.direction = self.get_random_direction()
        elif self.personality == DEFAULT:
            self.direction = self.get_a_star_direction()



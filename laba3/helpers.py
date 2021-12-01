import pygame

from metadata import *
vec = pygame.math.Vector2

class GameState:
    def __init__(self, grid_map, coins_positions, pacman_position, ghosts_positions, walls):
        self.grid_map = grid_map
        self.coins_positions = coins_positions
        self.pacman_position = pacman_position
        self.ghosts_positions = ghosts_positions
        self.walls = walls

    def is_lose(self):
        for enemy_position in self.ghosts_positions:
            if self.pacman_position[0] == enemy_position[0] and self.pacman_position[1] == enemy_position[1]:
                return True
        return False

    def is_win(self):
        return len(self.coins_positions) == 0

    def get_score(self):
        distances_to_enemy = []
        for enemy in self.ghosts_positions:
            distances_to_enemy.append(abs(enemy[0] - self.pacman_position[0]) + abs(enemy[1] - self.pacman_position[1]))
        distance_to_enemy = min(distances_to_enemy)
        distances_to_all_coins = []
        if self.coins_positions:
            for coin in self.coins_positions:
                distances_to_all_coins.append((abs(coin[0] - self.pacman_position[0]) + abs(coin[1] - self.pacman_position[1]), coin))
        else:
            return 1
        distance_to_coin, close_coin = min(distances_to_all_coins, key=lambda x: x[0])
        score = -1 / (distance_to_enemy + 0.001) + 1 / (distance_to_coin + 0.1)
        score = 3 * score if distance_to_coin < distance_to_enemy + 2 else score
        return score


    def get_legal_actions(self, mob_type):
        if mob_type == PACMAN:
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)]
            allowed_directions = []
            for direction in directions:
                if (self.pacman_position[0] + direction[0], self.pacman_position[1] + direction[1]) not in self.walls:
                    allowed_directions.append(vec(direction[::-1]))
            return allowed_directions
        elif mob_type == DEFAULT_GHOST:
            ghost_position = (0, 0)
            for ghost in self.ghosts_positions:
                ghost_position = (int(ghost[0]), int(ghost[1]))
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            allowed_directions = []
            for direction in directions:
                if (ghost_position[0] + direction[0], ghost_position[1] + direction[1]) not in self.walls:
                    allowed_directions.append(vec(direction[::-1]))
            return allowed_directions

    def simulate_state(self, direction, mob_type):

        if mob_type == PACMAN:
            player_position = (self.pacman_position[0] + direction[1], self.pacman_position[1] + direction[0])
            return GameState(self.grid_map, self.coins_positions, player_position, self.ghosts_positions, self.walls)

        elif mob_type == DEFAULT_GHOST:
            enemies_positions = []
            for ghost in self.ghosts_positions:
                enemies_positions.append(ghost)
            for i, ghost in enumerate(enemies_positions):
                ghost_position = (ghost[0] + direction[1], ghost[1] + direction[0])
                enemies_positions[i] = ghost_position
                return GameState(self.grid_map, self.coins_positions, self.pacman_position, enemies_positions,
                                 self.walls)

    def get_num_agents(self):
        return len(self.ghosts_positions) + 1

import numpy as np
import pygame
from constants import *
import queue
import time

start_time = time.time()

vec = pygame.math.Vector2


class Ghost:
    def __init__(self, application, start_position):
        self.type = None
        self.application = application
        self.position = start_position
        self.pix_position = self.get_pix_pos()
        self.path = None
        
    def draw(self):
        pygame.draw.circle(self.application.screen, RED,
                           (self.pix_position.x, self.pix_position.y),
                           self.application.cell_width//2-2)

    def get_pix_pos(self):
        return vec((self.position[0]*self.application.cell_width) + PADDING // 2 + self.application.cell_width // 2,
                   (self.position[1]*self.application.cell_height) +
                   PADDING // 2 + self.application.cell_height // 2)

    def BFS(self, start, target):
        start_time = time.time();
        grid = self.load_grid()
        if not self.is_valid_target(target):
            print("your targed is invalid")
            return [start]
        queue = [start]
        path = []
        visited = []
        directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]

        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                for direction in directions:
                    step = current + direction
                    if grid[int(step[1]), int(step[0])] != 1:
                        if step not in visited:
                            queue.append(step)
                            path.append({"Current": current, "Next": step})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])

        finish_time = time.time()
        print("--- %s seconds ---" % (finish_time - start_time))
        return shortest

    def DFS(self, start, target):
        start_time = time.time();
        grid = self.load_grid()
        if not self.is_valid_target(target):
            print("your targed is invalid")
            return [start]

        stack = [start]
        visited = []
        path = []
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        while stack:
            possible_dirs = []
            for direction in directions:
                step = stack[-1] + direction
                if grid[int(step[1]), int(step[0])] != 1 and step not in visited:
                    possible_dirs.append(direction)

            if len(possible_dirs) == 0:
                stack.pop()
                path = stack

            for direction in possible_dirs:
                step2 = stack[-1] + direction
                stack.append(step2)
                visited.append(stack[-1])
                path.append(stack[-1])
                break

            if stack[-1] == target:
                finish_time = time.time()
                print("--- %s seconds ---" % (finish_time - start_time))
                return path

    def UCS(self, start, target):
        start_time = time.time();
        grid = self.load_grid()
        if not self.is_valid_target(target):
            print("your targed is invalid")
            return [start]
        graph = self.grid_to_graph(grid)
        visited = set()
        start = (int(start.y), int(start.x))
        target = (int(target.y), int(target.x))
        path = []
        q = queue.PriorityQueue()
        q.put((0, start))

        while not q.empty():
            cost, node = q.get()
            if node == target:
                path.append(node)
                finish_time = time.time()
                print("--- %s seconds ---" % (finish_time - start_time))
                return path

            for edge in graph[node]:
                if edge not in visited:
                    visited.add(edge)
                    next_node = edge[:2]
                    step_cost = edge[-1]
                    q.put((step_cost + cost, next_node))
            path.append(q.queue[0][1][::-1])

    def grid_to_graph(self, grid):
        cost = 1
        rows, cols = grid.shape
        graph = {}
        for i in range(rows-1):
            for j in range(cols-1):
                if grid[i, j] != 1:
                    adj = []
                    for ele in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                        if grid[ele[0], ele[1]] == 0:
                            adj.append((ele[0], ele[1], cost))
                    graph[(i, j)] = adj
        return graph

    def draw_path(self):
        for step in self.path[1:-1]:
            pygame.draw.rect(self.application.screen, RED, (step[0] * self.application.cell_width + PADDING // 2,
                                                             step[1] * self.application.cell_height + PADDING // 2,
                                                             self.application.cell_width - 1,
                                                             self.application.cell_height - 1))

    def load_grid(self):
        grid = np.zeros((ROWS+1, COLS), dtype=int)
        with open("./Game_data/Map.txt", "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line[:-1]):
                    if char == "W":
                        grid[y, x] = 1
                    else:
                        grid[y, x] = 0
        return grid

    def is_valid_target(self, target):
        grid = self.load_grid()
        if grid[int(target.y), int(target.x)] == 1:
            return False
        else:
            return True


import pygame
from metadata import *
vec = pygame.math.Vector2


class Ghost:
    def __init__(self, application, start_position):
        self.type = None
        self.application = application
        self.position = start_position
        self.pix_position = self.get_pix_pos()

    def draw(self):
        pygame.draw.circle(self.application.screen, RED,
                           (self.pix_position.x, self.pix_position.y),
                           self.application.cell_width//2-2)

    def get_pix_pos(self):
        return vec((self.position[0]*self.application.cell_width) + PADDING // 2 + self.application.cell_width // 2,
                   (self.position[1]*self.application.cell_height) +
                   PADDING // 2 + self.application.cell_height // 2)
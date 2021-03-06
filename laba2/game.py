
import sys
from pacman import *
from ghost import *
from map import *
pygame.init()
vec = pygame.math.Vector2



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MENU
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.coins = []
        self.teleports = []
        self.ghosts = []
        self.e_pos = []
        self.p_pos = (1, 1)
        self.map_generator = Map()
        self.grid_map = None
        self.load_map()
        self.player = Player(self, vec(self.p_pos))


    def start_game(self):
        while self.running:
            if self.state == MENU:
                self.start_events()
                self.start_draw()
            elif self.state == GAMING:
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == GAME_OVER:
                self.game_over_events()
                self.game_over_draw()
            elif self.state == WINNER:
                self.winner_events()
                self.winner_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load_map(self):
        self.background = pygame.image.load('./Game_data/back.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        self.grid_map = self.map_generator.create_labyrinth(ROWS, COLS)
        for y_index in range(ROWS):
            for x_index in range(COLS):
                if self.grid_map[y_index, x_index] == WALL:
                    self.walls.append(vec(x_index, y_index))
                elif self.grid_map[y_index, x_index] == COIN:
                    self.coins.append(vec(x_index, y_index))

    def reset(self):
        self.walls = []
        self.player.lives = PLAYER_LIVES
        self.player.current_score = 0
        self.player.grid_pos = vec((1, 1))
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for ghost in self.ghosts:
            ghost.grid_pos = vec(ghost.position)
            ghost.pix_pos = ghost.get_pix_pos()
        self.load_map()
        self.state = GAMING

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = GAMING

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('Pacman', self.screen, [
                       WIDTH//2, HEIGHT//2-50], START_TEXT_SIZE, RED, START_FONT, centered=True)
        self.draw_text('Press space to play', self.screen, [
                       WIDTH//2, HEIGHT//2], START_TEXT_SIZE, RED, START_FONT, centered=True)
        pygame.display.update()

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.change_direction(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.change_direction(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.change_direction(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.change_direction(vec(0, 1))

    def playing_update(self):
        if len(self.coins) == 0:
            self.state = WINNER
        self.player.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (PADDING // 2, PADDING // 2))
        #self.draw_coins()
        self.draw_walls()
        self.player.draw()
        self.player.draw_path()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1

        if self.player.lives == 0:
            self.state = GAME_OVER
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for ghost in self.ghosts:
                ghost.grid_pos = vec(ghost.position)
                ghost.pix_pos = ghost.get_pix_pos()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, YELLOW,
                               (int(coin.x*self.cell_width) + self.cell_width // 2 + PADDING // 2,
                                int(coin.y*self.cell_height) + self.cell_height // 2 + PADDING // 2), 5)

    def draw_walls(self):
        maze = self.grid_map
        h = maze.shape[0]
        w = maze.shape[1]
        for x in range(w):
            for y in range(h):
                if maze[x, y] == WALL:
                    pygame.draw.rect(self.screen, BLUE, (y * self.cell_width + PADDING // 2,
                                                         x * self.cell_height + PADDING // 2,
                                                         self.cell_width - 1, self.cell_height - 1))
                elif maze[x, y] == GREEN_ZONE:
                    pygame.draw.rect(self.screen, GREEN, (y * self.cell_width + PADDING // 2,
                                                          x * self.cell_height + PADDING // 2,
                                                          self.cell_width - 1, self.cell_height - 1))
                elif maze[x, y] == RED_ZONE:
                    pygame.draw.rect(self.screen, RED, (y * self.cell_width + PADDING // 2,
                                                          x * self.cell_height + PADDING // 2,
                                                          self.cell_width - 1, self.cell_height - 1))
                elif maze[x, y] == ORANGE_ZONE:
                    pygame.draw.rect(self.screen, ORANGE, (y * self.cell_width + PADDING // 2,
                                                          x * self.cell_height + PADDING // 2,
                                                          self.cell_width - 1, self.cell_height - 1))

        pygame.display.update()

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press space to PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100],  52, RED, "Sans Serif MS", centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  36, GREY, "Sans Serif MS", centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  36, GREY, "Sans Serif MS", centered=True)
        pygame.display.update()

    def winner_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                temp_score = self.player.current_score
                self.reset()
                self.player.current_score = temp_score
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.QUIT:
                self.running = False

    def winner_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("You are WINNER!", self.screen, [
            WIDTH // 2, HEIGHT // 2 - 50], 36, START_FONT, "Sans Serif MS", centered=True)
        win_text = "Press space to PLAY AGAIN"
        self.draw_text(win_text, self.screen, [
            WIDTH // 2, HEIGHT // 2], 36, START_FONT, "Sans Serif MS", centered=True)
        pygame.display.update()

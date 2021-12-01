
import time
from pacman import *
from ghost import *
from map import *
from helpers import *
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
        self.enemies = []
        self.e_pos = []
        self.p_pos = (1, 1)
        self.map = Map()
        self.grid_map = None
        self.load_map()
        self.pacman = Pacman(self, vec(self.p_pos))
        self.start_time = time.time()

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
        self.grid_map = self.map.create_labyrinth(ROWS, COLS)
        for y_index in range(ROWS):
            for x_index in range(COLS):
                if self.grid_map[y_index, x_index] == WALL:
                    self.walls.append(vec(x_index, y_index))
                elif self.grid_map[y_index, x_index] == COIN:
                    self.coins.append(vec(x_index, y_index))
                elif self.grid_map[y_index, x_index] == DEFAULT_GHOST:
                    self.enemies.append(Ghost(self, vec(x_index, y_index), DEFAULT))
                elif self.grid_map[y_index, x_index] == RANDOM_GHOST:
                    self.enemies.append(Ghost(self, vec(x_index, y_index), RANDOM))


    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))

    def reset(self):
        self.walls = []
        self.pacman.lives = PACMAN_LIVES
        self.pacman.current_score = 0
        self.pacman.grid_pos = vec((1, 1))
        self.pacman.pix_pos = self.pacman.get_pix_pos()
        self.pacman.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.position)
            enemy.pix_pos = enemy.get_pix_pos()
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
                    self.pacman.change_direction(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.pacman.change_direction(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.pacman.change_direction(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.pacman.change_direction(vec(0, 1))

    def playing_update(self):
        if len(self.coins) == 0:
            play_time = time.time() - self.start_time
            with open("results.csv", "a") as file:
                file.write(f"{self.pacman.algo},{self.pacman.current_score},{play_time},win\n")

            self.state = WINNER
        self.pacman.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (PADDING // 2, PADDING // 2))
        self.draw_coins()
        self.draw_walls()
        self.draw_text(f'CURRENT SCORE: {self.pacman.current_score}',
                       self.screen, [60, 0], 36, WHITE, START_FONT)
        self.pacman.draw()
        # self.player.draw_path()
        for enemy in self.enemies:
            enemy.update()
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.pacman.lives -= 1

        if self.pacman.lives == 0:
            with open("results.csv", "a") as file:
                play_time = time.time() - self.start_time
                file.write(f"{self.pacman.algo},{self.pacman.current_score},{play_time},lose\n")
            if self.pacman.current_score > self.high_score:
                self.high_score = self.pacman.current_score
            self.write_score(self.pacman.current_score)
            self.state = GAME_OVER
        else:
            self.pacman.grid_pos = vec(self.pacman.starting_pos)
            self.pacman.pix_pos = self.pacman.get_pix_pos()
            self.pacman.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.position)
                enemy.pix_pos = enemy.get_pix_pos()

    def draw_coins(self):
        for coin in self.coins:
            if self.pacman.target_coin is not None and coin[1] == self.pacman.target_coin[0] and coin[0] == self.pacman.target_coin[1]:
                pygame.draw.circle(self.screen, RED,
                                   (int(coin.x*self.cell_width) + self.cell_width // 2 + PADDING // 2,
                                    int(coin.y*self.cell_height) + self.cell_height // 2 + PADDING // 2), 5)
            else:

                pygame.draw.circle(self.screen, YELLOW,
                                   (int(coin.x * self.cell_width) + self.cell_width // 2 + PADDING // 2,
                                    int(coin.y * self.cell_height) + self.cell_height // 2 + PADDING // 2), 5)

    def draw_walls(self):
        maze = self.grid_map
        h = maze.shape[0]
        w = maze.shape[1]
        for x in range(h):
            for y in range(w):
                if maze[x, y] == WALL:
                    pygame.draw.rect(self.screen, BLUE, (y * self.cell_width + PADDING // 2,
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
                temp_score = self.pacman.current_score
                self.reset()
                self.pacman.current_score = temp_score
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.QUIT:
                self.running = False

    def winner_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("You are WINNER!", self.screen, [
            WIDTH // 2, HEIGHT // 2 - 50], 36, GREEN, "Sans Serif MS", centered=True)
        win_text = "Press space to PLAY AGAIN"
        self.draw_text(win_text, self.screen, [
            WIDTH // 2, HEIGHT // 2], 36, GREEN, "Sans Serif MS", centered=True)
        pygame.display.update()

    def get_state(self) -> GameState:
        grid = self.grid_map
        enemy_positions = []
        coins_positions = []
        walls_positions = []
        player_position = (int(self.pacman.grid_pos[1]), int(self.pacman.grid_pos[0]))
        for enemy in self.enemies:
            enemy_positions.append((int(enemy.position[1]), int(enemy.position[0])))
        for coin in self.coins:
            coins_positions.append((int(coin[1]), int(coin[0])))
        for wall in self.walls:
            walls_positions.append((int(wall[1]), int(wall[0])))
        return GameState(grid, coins_positions, player_position, enemy_positions, walls_positions)



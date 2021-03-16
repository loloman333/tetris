import pygame,sys
from pygame.locals import *

class BaseGame():
    def __init__(self):

        self.block_colors = {
            'clevelandZ': 'red',
            'rhodeIslandZ': 'green',
            'blueRicky': 'blue',
            'smashBoy': 'yellow',
            'orangeRicky': 'orange',
            'teewee': 'purple',
            'hero': 'lightblue'
        }

        self.colors = {
            'white': (255, 255, 255),
            'gray': (185, 185, 185),
            'black': (0, 0, 0),
            'red': (155, 0, 0),
            'green': (0, 155, 0),
            'blue': (0, 0, 255),
            'lightblue': (0, 205, 255),
            'yellow': (255, 247, 0),
            'orange': (255, 137, 0),
            'purple': (213, 0, 255)
        }

        self.accent_colors = {
            'red': (175, 20, 20),
            'green': (20, 175, 20),
            'blue': (77, 83, 255),
            'lightblue': (32, 109, 168),
            'yellow': (167, 179, 53),
            'orange': (179, 145, 53),
            'purple': (114, 52, 149)
        }

        self.block_list = {
            'orangeRicky': [['..x',
                             'xxx'],
                            ['x.',
                             'x.',
                             'xx'],
                            ['xxx',
                             'x..'],
                            ['xx',
                             '.x',
                             '.x']
                            ],
            'blueRicky': [['x..',
                           'xxx'],
                          ['xx',
                           'x.',
                           'x.'],
                          ['xxx',
                           '..x'],
                          ['.x',
                           '.x',
                           'xx']
                          ],
            'clevelandZ': [['xx.',
                            '.xx'],
                           ['.x',
                            'xx',
                            'x.'],
                           ['xx.',
                            '.xx'],
                           ['.x',
                            'xx',
                            'x.']
                           ],
            'rhodeIslandZ': [['.xx',
                              'xx.'],
                             ['x.',
                              'xx',
                              '.x'],
                             ['.xx',
                              'xx.'],
                             ['x.',
                              'xx',
                              '.x']
                             ],
            'hero': [['xxxx'],
                     ['x',
                      'x',
                      'x',
                      'x']
                     ],
            'teewee': [['.x.',
                        'xxx'],
                       ['x.',
                        'xx',
                        'x.'],
                       ['xxx',
                        '.x.'],
                       ['.x',
                        'xx',
                        '.x']
                       ],
            'smashBoy': [['xx',
                          'xx']
                         ]
        }

        self.blank_color = '.'
        self.border_color = self.colors['white']
        self.background = self.colors['black']
        self.text_color = self.colors['white']
        self.window_width = 640
        self.window_height = 480
        self.box_size = 20
        self.board_width = 10
        self.board_height = 18
        self.margin = int((self.window_width - self.board_width * self.box_size) / 2)
        self.top_margin = self.window_height - (self.board_height * self.box_size) - 5
        self.display = 0
        self.clock = 0
        self.speed = 5
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.big_font = pygame.font.Font('freesansbold.ttf', 40)
        self.gameboard = self.get_empty_board()
        self.score = 0

    # Do not modify
    def test_quit_game(self):
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
        for event in pygame.event.get(KEYUP):  # get all the KEYUP events
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            pygame.event.post(event)

    # Do not modify
    def draw_game_board(self):
        pygame.draw.rect(self.display, self.border_color, (
            self.margin - 3, self.top_margin - 7, (self.board_width * self.box_size) + 8,
            (self.board_height * self.box_size) + 8), 5)
        pygame.draw.rect(self.display, self.background,
                         (self.margin, self.top_margin, self.box_size * self.board_width, self.box_size * self.board_height))
        for x in range(self.board_width):
            for y in range(self.board_height):
                self.draw_cell(x, y, self.gameboard[y][x])

    # Do not modify
    def get_empty_board(self):
        board = []
        for i in range(self.board_height):
            board.append([self.blank_color] * self.board_width)
        return board

    # Do not modify
    def convert_coords(self, board_x, board_y):
        return (self.margin + (board_x * self.box_size)), (self.top_margin + (board_y * self.box_size))

    # Do not modify
    def draw_cell(self, x, y, color, next_x=None, next_y=None):
        # nextX and nextY are used for the Next block display!
        if color == self.blank_color:
            return
        if next_x == None and next_y == None:
            next_x, next_y = self.convert_coords(x, y)
        pygame.draw.rect(self.display, self.colors[color], (next_x + 1, next_y + 1, self.box_size, self.box_size))
        pygame.draw.rect(self.display, self.accent_colors[color],
                         (next_x + 1, next_y + 1, self.box_size - 4, self.box_size - 4))

    # Do not modify
    # Draw a Block on Position Px and Py (top-left corner of the block)
    def draw_block(self, block, p_x=None, p_y=None):
        if p_x == None and p_y == None:
            p_x, p_y = self.convert_coords(block.x, block.y)
        for x in range(block.width):
            for y in range(block.height):
                if block.shape[y][x] != self.blank_color:
                    self.draw_cell(None, None, block.color, p_x + (x * self.box_size), p_y + (y * self.box_size))

    # Do not modify
    def draw_next_block(self, block):
        text = self.font.render('Next Block:', True, self.colors['white'])
        rect = text.get_rect()
        rect.topleft = (self.window_width - 120, 80)
        self.display.blit(text, rect)

        self.draw_block(block, p_x=self.window_width - 120, p_y=100)

    # Do not modify
    def draw_score(self):
        score = self.font.render('Score:', True, self.colors['white'])
        rect = score.get_rect()
        rect.topleft = (20, 80)
        self.display.blit(score, rect)
        text = self.font.render('{}'.format(self.score), True, self.colors['white'])
        rect = text.get_rect()
        rect.topleft = (20, 100)
        self.display.blit(text, rect)

    # Do not modify
    def draw_level(self):
        text = self.font.render('Level: {}'.format(self.level), True, self.colors['white'])
        rect = text.get_rect()
        rect.topleft = (20, 140)
        self.display.blit(text, rect)

    # Do not modify
    def check_key_press(self):
        self.test_quit_game()

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None

    # Do not modify
    def show_text(self, msg):
        displ = self.big_font.render(msg, True, self.colors['gray'])
        rect = displ.get_rect()

        rect.center = (int(self.window_width / 2), int(self.window_height / 2))
        self.display.blit(displ, rect)

        displ = self.big_font.render(msg, True, self.colors['white'])
        rect = displ.get_rect()

        rect.center = (int(self.window_width / 2) - 2, int(self.window_height / 2) - 2)
        self.display.blit(displ, rect)

        while self.check_key_press() == None:
            pygame.display.update()
            self.clock.tick()

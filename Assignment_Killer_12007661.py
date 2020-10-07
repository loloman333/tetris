# Tetris - DYOA Advanced at TU Graz WS 2020
# Name: Killer Lorenz
# Student ID: 12007661

import pygame, sys, time, random
from pygame.locals import *
from framework import BaseGame

class Block:
    blocknames = ['clevelandZ', 'rhodeIslandZ', 'blueRicky', 'smashBoy', 'orangeRicky', 'teewee', 'hero']
    def __init__(self, game, block_name):
        self.name = block_name
        self.rotation = random.randint(0, len(game.block_list[block_name]) - 1)
        self.set_shape(game.block_list[self.name][self.rotation])
        self.rotations_list = game.block_list[self.name]
        if block_name == "hero":
            if self.rotation == 0:
                self.rotation_counter = 0
            else:
                self.rotation_counter = 1

        self.x = int(game.board_width / 2) - int(self.width / 2)
        self.y = 0
        self.color = game.block_colors[block_name]

    def set_shape(self, shape):
        self.shape = shape
        self.width = len(shape[0])
        self.height = len(shape)

    def move_right(self):
        self.move(1, 0)

    def move_left(self):
        self.move(-1, 0)

    def move(self, x_diff, y_diff):
        new_x = self.x + x_diff
        if new_x < 0 or new_x + (self.width - 1) > 9:
            return False

        new_y = self.y + y_diff
        if new_y < 0 or new_y + (self.height - 1) > 17:
            return False

        self.x = new_x
        self.y = new_y

    def right_rotation(self, rotation_options):
        self.rotate(1)

        # Adjust positon after rotation for 3x3 blocks
        if max(self.width, self.height) == 3:
            if self.rotation == 0:
                pass
            elif self.rotation == 1:
                self.move(1, 0)
            elif self.rotation == 2:
                self.move(-1, 1)
            elif self.rotation == 3:
                self.move(0, -1)

        # Adjust positon after rotation for hero block
        elif self.name == 'hero':

            print(self.rotation_counter)

            if self.rotation_counter == 0:
                self.move(2, -1)
            elif self.rotation_counter == 1:
                self.move(-2, 2)                
            elif self.rotation_counter == 2:
                self.move(1, -2)
            elif self.rotation_counter == 3:
                self.move(-1, 1)
            
            self.rotation_counter += 1
            if self.rotation_counter == 4:
                self.rotation_counter = 0

    def left_rotation(self, rotation_options):
        self.rotate(-1)

        # Adjust positon after rotation for 3x3 blocks
        if max(self.width, self.height) == 3:
            if self.rotation == 0:
                self.move(-1, 0)
            elif self.rotation == 1:
                self.move(1, -1)
            elif self.rotation == 2:
                self.move(0, 1)
            elif self.rotation == 3:
                pass

        # Adjust positon after rotation for hero block
        elif self.name == 'hero':

            print(self.rotation_counter)

            if self.rotation_counter == 0:
                self.move(1, -1)
            elif self.rotation_counter == 1:
                self.move(-2, 1)
            elif self.rotation_counter == 2:
                self.move(2, -2)
            elif self.rotation_counter == 3:
                self.move(-1, 2)

            self.rotation_counter -= 1
            if self.rotation_counter == -1:
                self.rotation_counter = 3

    
    def rotate(self, direction):

        if self.rotation + direction == len(self.rotations_list):
            self.rotation = 0
        elif self.rotation + direction == -1:
            self.rotation = len(self.rotations_list) - 1
        else:
            self.rotation += direction
        
        self.set_shape(self.rotations_list[self.rotation])
            

class Game(BaseGame):
    def run_game(self):
        self.board = self.get_empty_board()
        fall_time = time.time()

        current_block = self.get_new_block()
        next_block = self.get_new_block()

        # TODO Fill in the score dictionary
        #  Maps "lines removed" to "raw points gained"
        #  0 lines: 0 points; 1 line: 40 points; 2 lines: 100 points; 3 lines: 300 points; 4 lines: 1200 points
        self.score_dictionary = {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }

        # GameLoop
        while True:
            self.test_quit_game()

            key = None
            for event in pygame.event.get([KEYDOWN]):
                key = event.key
            
            if (key == K_RIGHT):
                current_block.move_right()
            elif (key == K_LEFT):
                current_block.move_left()
            elif (key == K_DOWN):
                current_block.move(0,1)
            elif (key == K_UP):
                current_block.move(0,-1)

            elif (key == K_p):
                current_block = next_block
                next_block = self.get_new_block()

            elif (key == K_q):
                current_block.left_rotation(None)
            elif (key == K_e):
                current_block.right_rotation(None)

            # Draw after game logic
            self.display.fill(self.background)
            self.draw_game_board()
            self.draw_score()
            self.draw_next_block(next_block)
            if current_block != None:
                self.draw_block(current_block)
            pygame.display.update()
            self.set_game_speed(self.speed)
            self.clock.tick(self.speed)

    # Check if Coordinate given is on board (returns True/False)
    def is_coordinate_on_board(self, x, y):
        # TODO check if coordinate is on playingboard (in boundary of self.boardWidth and self.boardHeight)
        return False

    # Parameters block, x_change (any movement done in X direction), yChange (movement in Y direction)
    # Returns True if no part of the block is outside the Board or collides with another Block
    def is_block_on_valid_position(self, block, x_change=0, y_change=0):

        

        return False

    # Check if the line on y Coordinate is complete
    # Returns True if the line is complete
    def check_line_complete(self, y_coord):
        # TODO check if line on yCoord is complete and can be removed
        return False

    # Go over all lines and remove those, which are complete
    # Returns Number of complete lines removed
    def remove_complete_line(self):
        # TODO go over all lines and check if one can be removed
        return 0

    # Create a new random block
    # Returns the newly created Block Class
    def get_new_block(self):
        blockname = random.choice(Block.blocknames)
        block = Block(self, blockname)
        return block

    def add_block_to_board(self, block):
        # TODO once block is not falling, place it on the gameboard
        #  add Block to the designated Location on the board once it stopped moving
        pass

    # calculate new Score after a line has been removed
    def calculate_new_score(self, lines_removed, level):
        # TODO calculate new score
        # Points gained: Points per line removed at once times the level modifier!
        # Points per lines removed corresponds to the score_directory
        # The level modifier is 1pyt higher than the current level.
        pass

    # calculate new Level after the score has changed
        # TODO calculate new level
    def calculate_new_level(self, score):
        # The level generally corresponds to the score divided by 300 points.
        # 300 -> level 1; 600 -> level 2; 900 -> level 3
        # TODO increase gamespeed by 1 on level up only
        pass

    # set the current game speed
    def set_game_speed(self, speed):
        # TODO set the correct game speed!
        # It starts as defined in base.py and should increase by 1 after a level up.
        pass

#-------------------------------------------------------------------------------------
# Do not modify the code below, your implementation should be done above
#-------------------------------------------------------------------------------------
def main():
    pygame.init()
    game = Game()

    game.display = pygame.display.set_mode((game.window_width, game.window_height))
    game.clock = pygame.time.Clock()
    pygame.display.set_caption('Tetris')

    game.show_text('Tetris')

    game.run_game()
    game.show_text('Game Over')


if __name__ == '__main__':
    main()

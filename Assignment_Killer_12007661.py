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

        self.game = game

    def set_shape(self, shape):
        self.shape = shape
        self.width = len(shape[0])
        self.height = len(shape)

    def move_right(self):
        self.move(1, 0)

    def move_left(self):
        self.move(-1, 0)

    def move(self, x_diff, y_diff):

        if not self.game.is_block_on_valid_position(self, x_diff, y_diff):
            return False

        self.x = self.x + x_diff
        self.y = self.y + y_diff

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

        if not self.game.is_block_on_valid_position(self):
            self.rotate(-1)

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

        if not self.game.is_block_on_valid_position(self):
            self.rotate(1)
   
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

        self.level = 0

        self.current_block = self.get_new_block()
        self.next_block = self.get_new_block()

        self.score_dictionary = {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }

        self.stop = False
        # GameLoop
        while not self.stop:
            self.test_quit_game()

            self.process_key_events()
            self.gravity()

            # Draw after game logic
            self.display.fill(self.background)
            self.draw_game_board()
            self.draw_score()
            self.draw_level()
            self.draw_next_block(self.next_block)
            if self.current_block != None:
                self.draw_block(self.current_block)
            pygame.display.update()
            self.set_game_speed(self.speed)
            self.clock.tick(self.speed)

    # Check if Coordinate given is on board (returns True/False)
    def is_coordinate_on_board(self, x, y):

        if (x < 0 or x > self.board_width - 1):
            return False
        
        if (y < 0 or y > self.board_height - 1):
            return False
        
        return True

    # Parameters block, x_change (any movement done in X direction), yChange (movement in Y direction)
    # Returns True if no part of the block is outside the Board or collides with another Block
    def is_block_on_valid_position(self, block, x_change=0, y_change=0):

        init_x = block.x + x_change
        init_y = block.y + y_change

        y = init_y
        for row in block.shape:
            
            x = init_x
            for cell in row:

                if (cell == "x"):
                    if (not self.is_coordinate_on_board(x, y) or self.gameboard[y][x] != self.blank_color):
                        return False
                x += 1

            y +=1

        return True

    # Check if the line on y Coordinate is complete
    # Returns True if the line is complete
    def check_line_complete(self, y_coord):

        row = self.gameboard[y_coord]

        complete = True
        for cell in row:
            if cell == self.blank_color:
                complete = False
                break

        return complete

    # Go over all lines and remove those, which are complete
    # Returns Number of complete lines removed
    def remove_complete_line(self):
    
        deleted = 0

        for y_coord in range(self.board_height - 1, 0, -1):
            if self.check_line_complete(y_coord):
                self.gameboard.pop(y_coord)
                deleted += 1    

        self.gameboard = ([[self.blank_color] * self.board_width] * deleted) + self.gameboard

        self.calculate_new_score(deleted, self.level)

        return deleted

    # Create a new random block
    # Returns the newly created Block Class
    def get_new_block(self):
        blockname = random.choice(Block.blocknames)
        block = Block(self, blockname)
        return block

    def add_block_to_board(self, block):
        init_x = block.x
        init_y = block.y

        y = init_y
        for row in block.shape:

            x = init_x
            for cell in row:

                if cell == "x":
                    self.gameboard[y][x] = block.color
                x += 1

            y += 1

    # calculate new Score after a line has been removed
    def calculate_new_score(self, lines_removed, level):
        self.score += self.score_dictionary[lines_removed] * (level + 1)
        self.calculate_new_level(self.score)

    # calculate new Level after the score has changed
    def calculate_new_level(self, score):

        level = 0
        while (score >= 300):
            score -= 300
            level += 1

        if level > self.level:
            self.set_game_speed(self.speed + 1)

        self.level = level        

    # set the current game speed
    def set_game_speed(self, speed):
        self.speed = speed

    def process_key_events(self):
        key = None
        for event in pygame.event.get([KEYDOWN]):
            key = event.key
        
        if (key == K_RIGHT):
            self.current_block.move_right()
        elif (key == K_LEFT):
            self.current_block.move_left()
        elif (key == K_DOWN):
            self.current_block.move(0,2)
        elif (key == K_UP):
            self.current_block.move(0,-1)

        elif (key == K_p):
            self.pause()

        elif (key == K_q):
            self.current_block.left_rotation(None)
        elif (key == K_e):
            self.current_block.right_rotation(None)

    def gravity(self):
        if (self.is_block_on_valid_position(self.current_block, 0, 1)):
            self.current_block.move(0, 1)
        else:
            self.add_block_to_board(self.current_block)
            self.current_block = self.next_block
            self.next_block = self.get_new_block()

            if not self.is_block_on_valid_position(self.current_block):
                self.stop = True

            self.remove_complete_line()

    def pause(self):
        self.show_text('Paused')
        self.freeze()

    def freeze(self):
        pygame.display.update()
        
        event = pygame.event.wait()
        while (event.type != pygame.KEYDOWN and event.type != pygame.QUIT):
            event = pygame.event.wait()  

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

    game.freeze()

if __name__ == '__main__':
    main()

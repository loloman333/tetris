import unittest, pygame
from Assignment_Lastname_StudentID import Block, Game


class TestBlock(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Game()
        self.game.level = 0
        self.game.score = 0
        self.game.speed = 0

        self.game.score_dictionary = {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }

    def getBottomBlock(self, game):
        block = Block(game, "hero")
        block.rotation = 0
        block.shape = ['xxxx']
        block.width = 4
        block.height = 1
        block.x = int(game.board_width / 2) - int(block.width / 2)
        block.y = 17
        return block

    # Public Test 1
    def testIsCoordinateOnBoard(self):
        res = self.game.is_coordinate_on_board(2, 4)
        self.assertTrue(res, msg="Returnvalue {} is not True".format(res))

    # Public Test 2
    def testCheckLineComplete(self):
        board = []

        for i in range(17):
            board.append(['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'])
        board.append(
            ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
             'lightblue', 'lightblue'])

        self.game.gameboard = board
        res = self.game.check_line_complete(17)
        self.assertTrue(res, msg="Returnvalue {} is not True".format(res))

    # Public Test 3
    def testGetNewBlock(self):
        block = self.game.get_new_block()
        self.assertTrue(type(block) is Block, msg="Returnvalue {} is not <class 'main.Block'>".format(type(block)))

    # Public Test 4
    def testRemoveLineToAddToScore(self):
        board = []

        for i in range(17):
            board.append(['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'])
        board.append(['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
                      'lightblue', 'lightblue', 'lightblue'])

        self.game.gameboard = board
        self.game.remove_complete_line()
        self.assertTrue(self.game.score == 40, msg="Remove line does not calculate score correctly")

    # Public Test 5
    def testCalculateNewLevel(self):
        res = []

        for score in range(0, 3000, 300):
            self.game.calculate_new_level(score)
            res.append(self.game.level)
        self.assertTrue(res == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], msg="calculateNewLevel does not work correctly")

    # Public Test 6
    def testSetGameSpeed(self):
        self.game.set_game_speed(100)
        self.assertTrue(self.game.speed == 100, msg="setGameSpeed does not work correctly")

    # Public Test 7
    def testBlockNameAndColor(self):
        block = Block(self.game, "teewee")
        self.assertTrue(block.name == "teewee", msg="Name {} is not teewee".format(block.name))
        self.assertTrue(block.color == "purple", msg="Color {} is not purple".format(block.color))

    # Public Test 8
    def testAddBlockToBoard(self):
        block = self.getBottomBlock(self.game)
        self.game.add_block_to_board(block)

        res = []

        for i in range(17):
            res.append(['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'])
        res.append(['.', '.', '.', 'lightblue', 'lightblue', 'lightblue', 'lightblue', '.', '.', '.'])

        self.assertTrue(res == self.game.gameboard, msg="Block is not correctly placed")

    # Public Test 9
    def testRotateRight(self):
        block = self.getBottomBlock(self.game)
        block.y = 5
        res = 1
        block.right_rotation(self.game.block_list[block.name])
        self.assertTrue(res == block.rotation,
        msg="Block was not correctly rotated: is {} should be {}".format(block.rotation, res))

    # Public Test 10
    def testSetShape(self):
        block = self.game.get_new_block();
        block.set_shape(['xxxx'])
        self.assertTrue(['xxxx'] == block.shape, msg="Block does not have correct width: is {} should be {}".format(block.shape, ['xxxx']))
        self.assertTrue(4 == block.width, msg="Block does not have correct width: is {} should be {}".format(block.width, 4))
        self.assertTrue(1 == block.height, msg="Block does not have correct height: is {} should be {}".format(block.height, 1))

if __name__ == '__main__':
    unittest.main()
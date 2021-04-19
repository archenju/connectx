import unittest
from gameboard import Board
from gamerules import Checker


class TestBoard(unittest.TestCase):

    def test_create_board(self):
        board = Board(7)
        self.assertEqual(board.cols, 7, "Should be 7")
        self.assertEqual(board.rows, 6, "Should be 6")
        self.assertEqual(board.grid.shape, (6,7), "Should be (6,7)")
        self.assertEqual(board.winner, 0, "Should be 0")
        self.assertEqual(board.maxturns, 42, "Should be 42")

    def test_play_once(self):
        board = Board(6)
        self.assertEqual(board.grid[0,0], 0, "Should be 0")
        board.insert(0, 1)
        self.assertEqual(board.grid[0,0], 1, "Should be 1")
    
    def test_play_twice(self):
        board = Board(6)
        self.assertEqual(board.grid[0,0], 0, "Should be 0")
        board.insert(0, 1)
        board.insert(0, 1)
        self.assertEqual(board.grid[0,0], 1, "Should be 1")
        self.assertEqual(board.grid[1,0], 1, "Should be 1")

    def test_column_full(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        result = board.insert(0, 1)
        self.assertEqual(result, -1, "Should be -1 (column full)")

    # cannot test PRIVATE method
    # def test_checkX_val(self):
    #     board = Board(6)
    #     board.insert(0, 1)
    #     board.insert(1, 1)
    #     board.insert(2, 1)
    #     checker = Checker(board)
    #     result = checker.__checkX(0, 0, 1)
    #     self.assertEqual(result, 3, "Should be 3")

    # cannot test PRIVATE method
    # def test_checkY_val(self):
    #     board = Board(6)
    #     board.insert(0, 1)
    #     board.insert(0, 1)
    #     board.insert(0, 1)
    #     checker = Checker(board)
    #     result = checker.__checkY(0, 0, 1)
    #     self.assertEqual(result, 3, "Should be 3")

    # cannot test PRIVATE method
    # def test_checkDiagUp_val(self):
    #     board = Board(6)
    #     board.insert(0, 1)
    #     board.insert(1, -1)
    #     board.insert(1, 1)
    #     board.insert(2, -1)
    #     board.insert(2, -1)
    #     board.insert(2, 1)
    #     checker = Checker(board)
    #     result = checker.__checkDiagUp(0, 0, 1)
    #     self.assertEqual(result, 3, "Should be 3")

    # cannot test PRIVATE method
    # def test_checkDiagDown_val(self):
    #     board = Board(6)
    #     board.insert(0, -1)
    #     board.insert(0, -1)
    #     board.insert(0, -1)
    #     board.insert(0, 1)
    #     board.insert(1, -1)
    #     board.insert(1, -1)
    #     board.insert(1, 1)
    #     board.insert(2, -1)
    #     board.insert(2, 1)
    #     checker = Checker(board)
    #     result = checker.__checkDiagDown(1, 2, 1)
    #     self.assertEqual(result, 3, "Should be 3")

    def test_column_score3(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        checker = Checker(board)
        result = checker.checkgrid(1, 0, 0)
        self.assertEqual(result, 3, "Should be 3")

    def test_column_win(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        checker = Checker(board)
        result = checker.checkgrid(1, 0, 0)
        (_ , _ , game_over) = checker.check4win(1, 0, 0)
        self.assertEqual(game_over, True, "Should be True")
        self.assertEqual(result, 4, "Should be 4")

    def test_line_score3(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(1, 1)
        board.insert(2, 1)
        checker = Checker(board)
        result = checker.checkgrid(1, 0, 0)
        self.assertEqual(result, 3, "Should be 3")

    def test_line_win(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(1, 1)
        board.insert(2, 1)
        board.insert(3, 1)
        checker = Checker(board)
        result = checker.checkgrid(1, 0, 0)
        (_ , _ , game_over) = checker.check4win(1, 0, 0)
        self.assertEqual(game_over, True, "Should be True")
        self.assertEqual(result, 4, "Should be 4")

    def test_diag_up_score3(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(1, -1)
        board.insert(1, 1)
        board.insert(2, -1)
        board.insert(2, -1)
        board.insert(2, 1)
        checker = Checker(board)
        result = checker.checkgrid(1, 0, 0)
        self.assertEqual(result, 3, "Should be 3")

    def test_diag_up_win(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(1, -1)
        board.insert(1, 1)
        board.insert(2, -1)
        board.insert(2, -1)
        board.insert(2, 1)
        board.insert(3, -1)
        board.insert(3, -1)
        board.insert(3, -1)
        board.insert(3, 1)
        checker = Checker(board)
        result = checker.checkgrid(1, 0, 0)
        (_ , _ , game_over) = checker.check4win(1, 0, 0)
        self.assertEqual(game_over, True, "Should be True")
        self.assertEqual(result, 4, "Should be 4")

    def test_diag_down_score3(self):
        board = Board(6)
        board.insert(1, -1)
        board.insert(1, -1)
        board.insert(1, 1)
        board.insert(2, -1)
        board.insert(2, 1)
        board.insert(3, 1)
        checker = Checker(board)
        result = checker.checkgrid(1, 2, 1)
        self.assertEqual(result, 3, "Should be 3")

    def test_diag_down_win(self):
        board = Board(6)
        board.insert(0, -1)
        board.insert(0, -1)
        board.insert(0, -1)
        board.insert(0, 1)
        board.insert(1, -1)
        board.insert(1, -1)
        board.insert(1, 1)
        board.insert(2, -1)
        board.insert(2, 1)
        board.insert(3, 1)
        checker = Checker(board)
        result = checker.checkgrid(1, 0, 3)
        (_ , _ , game_over) = checker.check4win(1, 0, 3)
        self.assertEqual(game_over, True, "Should be True")
        self.assertEqual(result, 4, "Should be 4")




if __name__ == '__main__':
    unittest.main()

import unittest
from gameboard import Board
from gamerules import Checker


class TestBoard(unittest.TestCase):

    def test_create_board(self):
        board = Board(6)
        self.assertEqual(board.cols, 6, "Should be 6")
        self.assertEqual(board.rows, 6, "Should be 6")
        self.assertEqual(board.grid.shape, (6,6), "Should be (6,6)")

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

    def test_checkX_val(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(1, 1)
        board.insert(2, 1)
        checker = Checker(board)
        result = checker._checkX(0, 0, 1)
        self.assertEqual(result, 3, "Should be 3")

    def test_checkY_val(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        checker = Checker(board)
        result = checker._checkY(0, 0, 1)
        self.assertEqual(result, 3, "Should be 3")

    def test_checkDiagUp_val(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(1, -1)
        board.insert(1, 1)
        board.insert(2, -1)
        board.insert(2, -1)
        board.insert(2, 1)
        checker = Checker(board)
        result = checker._checkDiagUp(0, 0, 1)
        self.assertEqual(result, 3, "Should be 3")

    def test_checkDiagDown_val(self):
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
        checker = Checker(board)
        result = checker._checkDiagDown(1, 2, 1)
        self.assertEqual(result, 3, "Should be 3")

    def test_column_win(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        board.insert(0, 1)
        checker = Checker(board)
        result = checker.check4win(1, 0, 0)
        self.assertEqual(result, True, "Should be True")

    def test_line_win(self):
        board = Board(6)
        board.insert(0, 1)
        board.insert(1, 1)
        board.insert(2, 1)
        board.insert(3, 1)
        checker = Checker(board)
        result = checker.check4win(1, 0, 0)
        self.assertEqual(result, True, "Should be True")

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
        result = checker.check4win(1, 0, 0)
        self.assertEqual(result, True, "Should be True")

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
        result = checker.check4win(1, 0, 3)
        self.assertEqual(result, True, "Should be True")




if __name__ == '__main__':
    unittest.main()

import unittest
import chess


class CheckmateTests(unittest.TestCase):

    def setUp(self):
        self.board = chess.ChessBoard()

    def tearDown(self):
        del self.board

    def test_checkmate(self):
        self.board.move_piece((4, 6), (4, 4))
        self.board.move_piece((1, 1), (1, 2))
        self.board.move_piece((3, 7), (5, 5))
        self.board.move_piece((1, 0), (2, 2))
        self.board.move_piece((5, 7), (2, 4))
        self.board.move_piece((2, 0), (1, 1))
        self.board.move_piece((5, 5), (5, 1))
        status = 'White win!'
        self.assertEqual(status, self.board.get_game_status())

    def test_chechmate_again(self):
        self.board.move_piece((4, 6), (4, 4))
        self.board.move_piece((1, 1), (1, 2))
        self.board.move_piece((3, 7), (5, 5))
        self.board.move_piece((1, 0), (2, 2))
        self.board.move_piece((5, 7), (2, 4))
        self.board.move_piece((3, 1), (3, 2))
        self.board.move_piece((5, 5), (5, 1))
        self.board.move_piece((4, 0), (3, 1))
        self.board.move_piece((2, 4), (4, 2))
        status = 'White win!'
        self.assertEqual(status, self.board.get_game_status())

    def test_checkmate_third_time(self):
        self.board.move_piece((4, 6), (4, 4))
        self.board.move_piece((4, 1), (4, 3))
        self.board.move_piece((5, 7), (2, 4))
        self.board.move_piece((5, 0), (2, 3))
        self.board.move_piece((3, 7), (7, 3))
        self.board.move_piece((6, 0), (5, 2))
        self.board.move_piece((7, 3), (5, 1))
        status = 'White win!'
        self.assertEqual(status, self.board.get_game_status())

    def test_checkmate_black(self):
        self.board.move_piece((4, 6), (4, 4))
        self.board.move_piece((5, 1), (5, 2))
        self.board.move_piece((3, 6), (3, 4))
        self.board.move_piece((6, 1), (6, 3))
        self.board.move_piece((3, 7), (7, 3))
        status = 'White win!'
        self.assertEqual(status, self.board.get_game_status())

    def test_checkmate_black_win(self):
        self.assertTrue(self.board.move_piece((4, 6), (4, 4)))
        self.assertTrue(self.board.move_piece((4, 1), (4, 3)))
        self.assertTrue(self.board.move_piece((5, 6), (5, 4)))
        self.assertTrue(self.board.move_piece((5, 0), (2, 3)))
        self.assertTrue(self.board.move_piece((5, 4), (4, 3)))
        self.assertTrue(self.board.move_piece((3, 0), (7, 4)))
        self.assertTrue(self.board.move_piece((4, 7), (4, 6)))
        self.assertTrue(self.board.move_piece((7, 4), (4, 4)))
        status = 'Black win!'
        self.assertEqual(status, self.board.get_game_status())

if __name__ == '__main__':
    unittest.main()

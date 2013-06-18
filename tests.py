import unittest
import chess


class ChessBoardTests(unittest.TestCase):

    def setUp(self):
        self.board = chess.ChessBoard()

    def tearDown(self):
        del self.board

    def test_on_board(self):
        result = self.board.on_board((-1, -2), (4, 5))
        self.assertFalse(result)
        result = self.board.on_board((1, 2), (-5, -6))
        self.assertFalse(result)

    def test_player_color(self):
        actual = self.board.player_color((3, 7))
        expected = 'white'
        self.assertEqual(expected, actual)
        actual = self.board.player_color((3, 0))
        expected = 'black'
        self.assertEqual(expected, actual)

    def test_empty(self):
        result = self.board.empty((4, 4))
        self.assertTrue(result)
        result = self.board.empty((7, 7))
        self.assertFalse(result)

    def test_obstructions_check(self):
        result = self.board.obstructions_check(1, -1, 4, (3, 7))
        self.assertTrue(result)
        result = self.board.obstructions_check(1, -1, 2, (5, 5))
        self.assertFalse(result)

    def test_same_color(self):
        result = self.board.same_color((6, 7), (6, 0))
        self.assertFalse(result)
        result = self.board.same_color((6, 7), (6, 5))
        self.assertFalse(result)
        result = self.board.same_color((6, 7), (7, 7))
        self.assertTrue(result)

    def test_valid_direction(self):
        result = self.board.valid_direction((4, 6), (4, 4))
        self.assertTrue(result)
        result = self.board.valid_direction((4, 1), (4, 3))
        self.assertTrue(result)
        result = self.board.valid_direction((4, 6), (4, 7))
        self.assertFalse(result)
        result = self.board.valid_direction((4, 1), (4, 0))
        self.assertFalse(result)

    def test_valid_king_move(self):
        directions = ((-1, 0), (1, 0), (-1, -1), (1, -1), (0, -1))
        for dx, dy in directions:
            result = self.board.valid_king_move((4, 7), (4 + dx, 7 + dy))
            self.assertTrue(result)
        result = self.board.valid_king_move((4, 7), (6, 7))
        self.assertFalse(result)
        self.board.board[7][5], self.board.board[7][6] = None, None
        result = self.board.valid_king_move((4, 7), (6, 7))
        self.assertTrue(result)
        result = self.board.valid_king_move((4, 7), (4, 5))
        self.assertFalse(result)

    def test_valid_bishop_move(self):
        result = self.board.valid_bishop_move((2, 7), (0, 5))
        self.assertFalse(result)
        result = self.board.valid_bishop_move((2, 7), (2, 5))
        self.assertFalse(result)
        result = self.board.valid_bishop_move((2, 5), (5, 2))
        self.assertTrue(result)

    def test_valid_rook_move(self):
        result = self.board.valid_rook_move((7, 0), (7, 3))
        self.assertFalse(result)
        result = self.board.valid_rook_move((7, 2), (7, 5))
        self.assertTrue(result)
        result = self.board.valid_rook_move((7, 0), (5, 2))
        self.assertFalse(result)

    def test_valid_queen_move(self):
        result = self.board.valid_queen_move((5, 4), (1, 4))
        self.assertTrue(result)
        result = self.board.valid_queen_move((5, 4), (3, 2))
        self.assertTrue(result)

    def test_valid_knight_move(self):
        result = self.board.valid_knight_move((6, 0), (7, 2))
        self.assertTrue(result)
        result = self.board.valid_knight_move((4, 4), (2, 3))
        self.assertTrue(result)
        result = self.board.valid_knight_move((4, 4), (1, 3))
        self.assertFalse(result)

    def test_valid_pawn_move(self):
        result = self.board.valid_pawn_move((4, 6), (4, 4))
        self.assertTrue(result)
        result = self.board.valid_pawn_move((6, 6), (7, 6))
        self.assertFalse(result)
        result = self.board.valid_pawn_move((5, 1), (5, 0))
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

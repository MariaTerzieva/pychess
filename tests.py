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
        result = self.board.valid_king_move((4, 7), (7, 7))
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

    def test_king_safe(self):
        self.board.move_piece((3, 6), (3, 4))
        self.board.move_piece((4, 1), (4, 3))
        self.board.move_piece((5, 6), (5, 5))
        self.board.move_piece((5, 0), (1, 4))
        result = self.board.king_safe((4, 7), 'white')
        self.assertFalse(result)

    def test_king_guard(self):
        self.board.move_piece((3, 6), (3, 4))
        self.board.move_piece((4, 1), (4, 3))
        self.board.move_piece((5, 6), (5, 5))
        self.board.move_piece((5, 0), (1, 4))
        result = self.board.king_guard((3, 6), (3, 7))
        self.assertTrue(result)

    def test_castle_check(self):
        self.board.board[7][5], self.board.board[7][6] = None, None
        result = self.board.castle_check((4, 7), (7, 7), 'white')
        self.assertTrue(result)
        self.board.board[7][7] = None
        result = self.board.castle_check((4, 7), (7, 7), 'white')
        self.assertFalse(result)
        self.board.board[0][1], self.board.board[0][2] = None, None
        self.board.board[0][3] = None
        result = self.board.castle_check((4, 0), (0, 0), 'black')
        self.assertTrue(result)

    def test_valid_move(self):
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1))
        result = self.board.valid_move((3, 7), directions)
        self.assertFalse(result)
        self.board.board[6][2] = None
        result = self.board.valid_move((3, 7), directions)
        self.assertTrue(result)

    def test_any_valid_moves(self):
        self.board.move_piece((3, 6), (3, 4))
        self.board.move_piece((4, 1), (4, 3))
        self.board.move_piece((5, 6), (5, 5))
        self.board.move_piece((5, 0), (1, 4))
        result = self.board.any_valid_moves()
        self.assertTrue(result)

    def test_any_valid_moves_again(self):
        self.board.move_piece((5, 6), (5, 5))
        self.board.move_piece((4, 1), (4, 3))
        self.board.move_piece((6, 6), (6, 4))
        self.board.move_piece((3, 0), (7, 4))
        result = self.board.any_valid_moves()
        self.assertFalse(result)

    def test_en_passant(self):
        self.board.move_piece((2, 6), (2, 4))
        self.board.move_piece((1, 1), (1, 3))
        self.board.move_piece((2, 4), (2, 3))
        self.board.move_piece((1, 3), (1, 4))
        self.board.move_piece((0, 6), (0, 4))
        result = self.board.move_piece((1, 4), (0, 5))
        self.assertTrue(result)
        result = self.board.empty((0, 4))
        self.assertTrue(result)

    def test_check(self):
        self.board.move_piece((5, 6), (5, 5))
        self.board.move_piece((4, 1), (4, 3))
        self.board.move_piece((6, 6), (6, 4))
        self.board.move_piece((3, 0), (7, 4))
        result = self.board.check()
        self.assertTrue(result)

    def test_switch_turn(self):
        white = self.board.turn
        self.board.switch_turn()
        black = self.board.turn
        self.assertNotEqual(white, black)

    def test_valid_player(self):
        result = self.board.valid_player((4, 0))
        self.assertFalse(result)

    def test_move(self):
        self.board.move((4, 6), (4, 4))
        result = self.board.empty((4, 6))
        self.assertTrue(result)

    def test_move_queen(self):
        result = self.board.move_queen((3, 7), (5, 5))
        self.assertFalse(result)

    def test_move_bishop(self):
        self.board.board[6][3] = None
        result = self.board.move_bishop((2, 7), (6, 3))
        self.assertTrue(result)

    def test_move_rook(self):
        self.board.board[6][7] = None
        self.board.move_rook((7, 7), (7, 2))
        result = self.board.empty((7, 7))
        self.assertTrue(result)

    def test_move_knight(self):
        self.board.move_knight((6, 0), (5, 2))
        result = self.board.empty((6, 0))
        self.assertTrue(result)

    def test_move_king(self):
        self.board.board[7][5], self.board.board[7][6] = None, None
        self.board.move_king((4, 7), (6, 7))
        result = self.board.empty((4, 7))
        self.assertTrue(result)
        result = self.board.empty((7, 7))
        self.assertTrue(result)

    def test_move_pawn(self):
        self.board.move_pawn((5, 6), (5, 4))
        self.board.move_pawn((5, 1), (5, 3))
        result = self.board.move_pawn((5, 3), (5, 4))
        self.assertFalse(result)

    def test_move_piece(self):
        self.board.move_piece((4, 6), (4, 4))
        self.board.move_piece((4, 1), (4, 3))
        self.board.move_piece((6, 7), (5, 5))
        self.board.move_piece((1, 0), (2, 2))
        self.board.move_piece((1, 7), (2, 5))
        self.board.move_piece((6, 0), (5, 2))
        self.board.move_piece((0, 6), (0, 5))
        self.board.move_piece((3, 1), (3, 3))
        self.board.move_piece((4, 4), (3, 3))
        self.board.move_piece((5, 2), (3, 3))
        self.board.move_piece((5, 7), (4, 6))
        self.board.move_piece((4, 3), (4, 4))
        self.board.move_piece((2, 5), (4, 4))
        self.board.move_piece((3, 3), (5, 4))
        self.board.move_piece((4, 7), (6, 7))
        self.board.move_piece((5, 4), (4, 6))
        self.board.move_piece((3, 7), (4, 6))
        self.board.move_piece((2, 0), (6, 4))
        self.board.move_piece((4, 4), (5, 2))
        result = self.board.check()
        self.assertTrue(result)
        result = self.board.any_valid_moves()
        self.assertFalse(result)
        status = 'White win!'
        self.assertEqual(status, self.board.get_game_status())

    def test_get_game_status(self):
        status = 'Game in progress.'
        self.assertEqual(status, self.board.get_game_status())

if __name__ == '__main__':
    unittest.main()

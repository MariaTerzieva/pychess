class Piece:

    def __init__(self, color):
        self.color = color


class Pawn(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        self.moved = False


class Bishop(Piece):
    pass


class Queen(Piece):
    pass


class King(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        self.moved = False


class Rook(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        self.moved = False


class Knight(Piece):
    pass


class ChessBoard:
    EMPTY = None
    WHITE = 'white'
    BLACK = 'black'
    GAME_IN_PROGRESS = 'Game in progress.'
    BLACK_WIN = 'Black win!'
    WHITE_WIN = 'White win!'
    STALEMATE = 'Stalemate!'

    def __init__(self):
        self.board = [[Rook('black'), Knight('black'), Bishop('black'),
                       Queen('black'), King('black'), Bishop('black'),
                       Knight('black'), Rook('black')],
                      [Pawn('black'), Pawn('black'), Pawn('black'),
                       Pawn('black'), Pawn('black'), Pawn('black'),
                       Pawn('black'), Pawn('black')],
                      [self.EMPTY] * 8,
                      [self.EMPTY] * 8,
                      [self.EMPTY] * 8,
                      [self.EMPTY] * 8,
                      [Pawn('white'), Pawn('white'), Pawn('white'),
                       Pawn('white'), Pawn('white'), Pawn('white'),
                       Pawn('white'), Pawn('white')],
                      [Rook('white'), Knight('white'), Bishop('white'),
                       Queen('white'), King('white'), Bishop('white'),
                       Knight('white'), Rook('white')]]
        self.en_passant = None
        self.turn = self.WHITE
        self.white_king = (4, 7)
        self.black_king = (4, 0)
        self.game_status = self.GAME_IN_PROGRESS

    def on_board(self, old_pos, new_pos):
        x_new, y_new = new_pos
        x_old, y_old = old_pos

        if (x_new < 0 or x_new > 7 or y_new < 0 or y_new > 7 or x_old < 0 or
                x_old > 7 or y_old < 0 or y_old > 7):
            return False
        return True

    def player_color(self, pos):
        return self.board[pos[1]][pos[0]].color

    def empty(self, pos):
        return self.board[pos[1]][pos[0]] is self.EMPTY

    def obstructions_check(self, dx, dy, steps, pos):
        """Check for obstructions from `pos`
        in direction `(dx, dy)` `steps` - 1 positions ahead.

        """
        for i in range(1, steps):
            x = pos[0] + i * dx
            y = pos[1] + i * dy
            if not self.empty((x, y)):
                return True
        return False

    def same_color(self, old_pos, new_pos):
        if not self.empty(new_pos):
            return self.player_color(old_pos) == self.player_color(new_pos)
        return False

    def clear_en_passant(self):
        self.en_passant = None

    def valid_direction(self, old_pos, new_pos):
        """Check if pawns move correctly."""
        if self.player_color(old_pos) == self.WHITE:
            return new_pos[1] < old_pos[1]
        else:
            return new_pos[1] > old_pos[1]

    def valid_king_move(self, old_pos, new_pos):
        x_old, y_old = old_pos
        x_new, y_new = new_pos

        if abs(x_old - x_new) > 1:
            color = self.player_color(old_pos)

            if x_new == x_old + 2 and y_new == y_old:
                rook = 7, 7
            elif x_new == x_old - 2 and y_new == y_old:
                rook = 0, 7

            return self.castle_check(old_pos, rook, color)

        if abs(y_old - y_new) > 1:
            return False

        return self.king_guard(new_pos, old_pos, 'king')

    def valid_bishop_move(self, old_pos, new_pos):
        x_old, y_old = old_pos
        x_new, y_new = new_pos

        if abs(x_old - x_new) != abs(y_old - y_new):
            return False

        directions = (1, -1)
        dx = directions[x_new < x_old]
        dy = directions[y_new < y_old]
        steps = abs(x_old - x_new)

        if self.obstructions_check(dx, dy, steps, old_pos):
            return False

        return self.king_guard(new_pos, old_pos)

    def valid_rook_move(self, old_pos, new_pos):
        x_old, y_old = old_pos
        x_new, y_new = new_pos

        if x_old != x_new and y_old != y_new:
            return False

        dx = (x_new > x_old) - (x_new < x_old)
        dy = (y_new > y_old) - (y_new < y_old)
        steps = max(abs(x_old - x_new), abs(y_old - y_new))

        if self.obstructions_check(dx, dy, steps, old_pos):
            return False

        return self.king_guard(new_pos, old_pos)

    def valid_queen_move(self, old_pos, new_pos):
        if not self.valid_rook_move(old_pos, new_pos):
            return self.valid_bishop_move(old_pos, new_pos)
        return True

    def valid_knight_move(self, old_pos, new_pos):
        x_old, y_old = old_pos
        x_new, y_new = new_pos

        fst_case = abs(x_old - x_new) == 2 and abs(y_old - y_new) == 1
        snd_case = abs(x_old - x_new) == 1 and abs(y_old - y_new) == 2

        if not fst_case and not snd_case:
            return False

        return self.king_guard(new_pos, old_pos)

    def valid_pawn_move(self, old_pos, new_pos):
        old_x, old_y = old_pos
        new_x, new_y = new_pos

        if not self.valid_direction(old_pos, new_pos):
            return False

        if not self.king_guard(new_pos, old_pos, 'pawn'):
            return False

        if abs(new_y - old_y) == 1:
            if new_x == old_x:
                return self.empty(new_pos)
            elif abs(new_x - old_x) == 1:
                if self.empty(new_pos) and self.en_passant is not None:
                    return (new_x, old_y) == self.en_passant
                return not self.empty(new_pos)
            else:
                return False
        elif abs(new_y - old_y) == 2:
            dx, dy = 0, (new_y > old_y) - (new_y < old_y)
            return (new_x == old_x and not self.board[old_y][old_x].moved and
                    not self.obstructions_check(dx, dy, 3, old_pos))
        else:
            return False

    def king_safe(self, pos, color):
        """Check if the king of `color` is safe from `pos`."""
        x, y = pos

        if color == self.WHITE:
            if x < 7 and y > 0 and isinstance(self.board[y - 1][x + 1], Pawn):
                if self.player_color((x + 1, y - 1)) != self.WHITE:
                    return False

            if x > 0 and y > 0 and isinstance(self.board[y - 1][x - 1], Pawn):
                if self.player_color((x - 1, y - 1)) != self.WHITE:
                    return False
        else:
            if x < 7 and y < 7 and isinstance(self.board[y + 1][x + 1], Pawn):
                if self.player_color((x + 1, y + 1)) != self.BLACK:
                    return False

            if x > 0 and y < 7 and isinstance(self.board[y + 1][x - 1], Pawn):
                if self.player_color((x - 1, y + 1)) != self.BLACK:
                    return False

        knight_moves = ((x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1),
                        (x - 2, y - 1), (x + 1, y + 2), (x + 1, y - 2),
                        (x - 1, y + 2), (x - 1, y - 2))

        for move in knight_moves:
            if self.on_board(pos, move):
                if isinstance(self.board[move[1]][move[0]], Knight):
                    if self.player_color(move) != color:
                        return False

        directions = ((1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1))

        for direction in directions:
            new_x, new_y = pos
            dx, dy = direction
            steps = 0
            while(True):
                steps += 1
                new_x += dx
                new_y += dy
                if new_x < 0 or new_x > 7 or new_y < 0 or new_y > 7:
                    break
                elif self.empty((new_x, new_y)):
                    continue
                elif self.player_color((new_x, new_y)) == color:
                    break
                else:
                    piece = self.board[new_y][new_x]
                    if isinstance(piece, King) and steps == 1:
                        return False
                    elif isinstance(piece, Queen):
                        return False
                    elif isinstance(piece, Rook) and abs(dx) != abs(dy):
                        return False
                    elif isinstance(piece, Bishop) and abs(dx) == abs(dy):
                        return False
                    break
        return True

    def king_guard(self, new_pos, old_pos, piece=None):
        """Check if the king will be safe if there is a move from
        `old_pos` to `new_pos`.

        """
        new_x, new_y = new_pos
        old_x, old_y = old_pos
        old = self.board[old_y][old_x]
        new = self.board[new_y][new_x]
        special = None

        self.board[old_y][old_x] = self.EMPTY
        self.board[new_y][new_x] = old

        if piece == 'pawn' and self.en_passant == (new_x, old_y):
            special = self.board[old_y][new_x]
            self.board[old_y][new_x] = self.EMPTY

        if self.turn == self.WHITE:
            king_pos = self.white_king
        else:
            king_pos = self.black_king

        if piece == 'king':
            king_pos = new_pos

        guarded = self.king_safe(king_pos, self.turn)

        if special:
            self.board[old_y][new_x] = special

        self.board[old_y][old_x] = old
        self.board[new_y][new_x] = new

        return guarded

    def castle_check(self, king_pos, rook_pos, color):
        """Check if castling for `color` is possible."""
        kx, ky = king_pos
        rx, ry = rook_pos

        if self.board[ky][kx].moved:
            return False

        if not isinstance(self.board[ry][rx], Rook):
            return False

        if self.board[ry][rx].moved:
            return False

        if rx > kx:
            dx, dy = 1, 0
            steps = 3
        else:
            dx, dy = -1, 0
            steps = 4

        if self.obstructions_check(dx, dy, steps, king_pos):
            return False

        for i in range(3):
            if not self.king_safe((kx, ky), color):
                return False
            kx += dx

        return True

    def valid_move(self, pos, directions, max_steps=8, piece=None):
        """Check if there is a valid move from `pos` in `directions`."""
        x, y = pos

        for direction in directions:
            dx, dy = direction
            new_x = x
            new_y = y
            steps = 0
            while True:
                new_x += dx
                new_y += dy
                if new_x < 0 or new_x > 7 or new_y < 0 or new_y > 7:
                    break
                elif self.empty((new_x, new_y)):
                    if self.king_guard((new_x, new_y), pos, piece):
                        return True
                elif self.player_color((new_x, new_y)) != self.turn:
                    if self.king_guard((new_x, new_y), pos, piece):
                        return True
                else:
                    break
                steps += 1
                if steps == max_steps:
                    break

        return False

    def any_valid_moves(self):
        """Check for any valid moves for whoever turn it is."""
        color = self.turn
        move = False

        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if not self.empty((x, y)) and piece.color == color:
                    if isinstance(piece, Queen):
                        directions = ((1, 0), (-1, 0), (0, 1), (0, -1),
                                      (1, 1), (-1, 1), (1, -1), (-1, -1))
                        move = self.valid_move((x, y), directions)
                    elif isinstance(piece, Rook):
                        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
                        move = self.valid_move((x, y), directions)
                    elif isinstance(piece, Bishop):
                        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))
                        move = self.valid_move((x, y), directions)
                    elif isinstance(piece, King):
                        directions = ((1, 0), (-1, 0), (0, 1), (0, -1),
                                      (1, 1), (-1, 1), (1, -1), (-1, -1))
                        move = self.valid_move((x, y), directions, 1, 'king')
                        if self.castle_check((x, y), (x + 3, y), color):
                            move = True
                        elif self.castle_check((x, y), (x - 4, y), color):
                            move = True
                    elif isinstance(piece, Knight):
                        positions = ((x + 1, y + 2), (x + 2, y + 1),
                                     (x + 2, y - 1), (x + 1, y - 2),
                                     (x - 1, y + 2), (x - 2, y + 1),
                                     (x - 1, y - 2), (x - 2, y - 1))
                        for px, py in positions:
                            if px >= 0 and px <= 7 and py >= 0 and py <= 7:
                                if not self.same_color((x, y), (px, py)):
                                    if self.king_guard((px, py), (x, y)):
                                        move = True
                                        break
                    elif isinstance(piece, Pawn):
                        if color == self.WHITE:
                            positions = ((x, y - 1), (x, y - 2),
                                         (x + 1, y - 1), (x - 1, y - 1))
                        else:
                            positions = ((x, y + 1), (x, y + 2),
                                         (x + 1, y + 1), (x - 1, y + 1))
                        for px, py in positions:
                            if px <= 7 and px >= 0 and py <= 7 and py >= 0:
                                if self.valid_pawn_move((x, y), (px, py)):
                                    move = True
                                    break
                if move:
                    return True

        return False

    def check(self):
        if self.turn == self.WHITE:
            king_pos = self.white_king
        else:
            king_pos = self.black_king

        return not self.king_safe(king_pos, self.turn)

    def switch_turn(self):
        if self.turn == self.WHITE:
            self.turn = self.BLACK
        else:
            self.turn = self.WHITE

    def valid_player(self, pos):
        return self.turn == self.player_color(pos)

    def move(self, old_pos, new_pos):
        new_x, new_y = new_pos
        old_x, old_y = old_pos
        self.board[new_y][new_x] = self.board[old_y][old_x]
        self.board[old_y][old_x] = self.EMPTY
        return True

    def move_queen(self, old_pos, new_pos):
        if not self.valid_queen_move(old_pos, new_pos):
            return False

        self.clear_en_passant()

        return self.move(old_pos, new_pos)

    def move_bishop(self, old_pos, new_pos):
        if not self.valid_bishop_move(old_pos, new_pos):
            return False

        self.clear_en_passant()

        return self.move(old_pos, new_pos)

    def move_rook(self, old_pos, new_pos):
        if not self.valid_rook_move(old_pos, new_pos):
            return False

        self.clear_en_passant()
        self.board[old_pos[1]][old_pos[0]].moved = True

        return self.move(old_pos, new_pos)

    def move_knight(self, old_pos, new_pos):
        if not self.valid_knight_move(old_pos, new_pos):
            return False

        self.clear_en_passant()

        return self.move(old_pos, new_pos)

    def move_king(self, old_pos, new_pos):
        new_x, new_y = new_pos
        old_x, old_y = old_pos

        if not self.valid_king_move(old_pos, new_pos):
            return False

        if new_x == old_x + 2:
            self.board[7][7].moved = True
            self.move((7, 7), (5, 7))
        elif new_x == old_x - 2:
            self.board[7][0].moved = True
            self.move((0, 7), (3, 7))

        if self.turn == self.WHITE:
            self.white_king = new_pos
        else:
            self.black_king = new_pos

        self.clear_en_passant()
        self.board[old_y][old_x].moved = True

        return self.move(old_pos, new_pos)

    def move_pawn(self, old_pos, new_pos):
        new_x, new_y = new_pos
        old_x, old_y = old_pos

        if not self.valid_pawn_move(old_pos, new_pos):
            return False

        if abs(new_y - old_y) == 2:
            if new_x > 0:
                left = new_x - 1, new_y
                if not (self.empty(left) and self.same_color(old_pos, left)):
                    self.en_passant = new_pos
            if new_x < 7:
                right = new_x + 1, new_y
                if not (self.empty(right) and self.same_color(old_pos, right)):
                    self.en_passant = new_pos
        elif abs(new_x - old_x) == abs(new_y - old_y):
            if self.empty(new_pos):
                self.board[old_y][new_x] = self.EMPTY

        if self.en_passant != new_pos:
            self.clear_en_passant()

        self.board[old_y][old_x].moved = True

        return self.move(old_pos, new_pos)

    def move_piece(self, old_pos, new_pos):
        if self.empty(old_pos):
            return False

        if not self.on_board(old_pos, new_pos):
            return False

        if self.same_color(old_pos, new_pos):
            return False

        if old_pos[0] == new_pos[0] and old_pos[1] == new_pos[1]:
            return False

        if not self.valid_player(old_pos):
            return False

        piece = self.board[old_pos[1]][old_pos[0]]

        if isinstance(piece, Pawn):
            if not self.move_pawn(old_pos, new_pos):
                return False
        elif isinstance(piece, Rook):
            if not self.move_rook(old_pos, new_pos):
                return False
        elif isinstance(piece, Bishop):
            if not self.move_bishop(old_pos, new_pos):
                return False
        elif isinstance(piece, Knight):
            if not self.move_knight(old_pos, new_pos):
                return False
        elif isinstance(piece, Queen):
            if not self.move_queen(old_pos, new_pos):
                return False
        elif isinstance(piece, King):
            if not self.move_king(old_pos, new_pos):
                return False

        self.switch_turn()

        if not self.any_valid_moves():
            if self.check():
                if self.turn == self.WHITE:
                    self.game_status = self.BLACK_WIN
                else:
                    self.game_status = self.WHITE_WIN
            else:
                self.game_status = self.STALEMATE

        return True

    def get_game_status(self):
        return self.game_status

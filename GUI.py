import pygame
import os
import sys
import chess
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEBUTTONDOWN

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOX_SIZE = 50
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * BOX_SIZE)) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * BOX_SIZE)) / 2)
LIGHT_BOX_COLOR = (255, 170, 85)
DARK_BOX_COLOR = (102, 51, 0)
BACKGROUND = (50, 0, 0)
TEXT_COLOR = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 155, 0)
TEXT_BACKGROUND = GREEN
WHITE = 'white'
BLACK = 'black'
EMPTY = None


def left_top_coords_of_box(box):
    left = box[0] * BOX_SIZE + X_MARGIN
    top = box[1] * BOX_SIZE + Y_MARGIN
    return (left, top)


def get_box_at_pixel(pixel):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            left, top = left_top_coords_of_box((x, y))
            box_rect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if box_rect.collidepoint(pixel):
                return (x, y)
    return (None, None)


def draw_pieces(board):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] is EMPTY:
                continue

            topleft = left_top_coords_of_box((x, y))

            if isinstance(board[y][x], chess.Pawn):
                if board[y][x].color == WHITE:
                    DISPLAYSURF.blit(IMAGES['w_pawn'], topleft)
                else:
                    DISPLAYSURF.blit(IMAGES['b_pawn'], topleft)
            elif isinstance(board[y][x], chess.Rook):
                if board[y][x].color == WHITE:
                    DISPLAYSURF.blit(IMAGES['w_rook'], topleft)
                else:
                    DISPLAYSURF.blit(IMAGES['b_rook'], topleft)
            elif isinstance(board[y][x], chess.Bishop):
                if board[y][x].color == WHITE:
                    DISPLAYSURF.blit(IMAGES['w_bishop'], topleft)
                else:
                    DISPLAYSURF.blit(IMAGES['b_bishop'], topleft)
            elif isinstance(board[y][x], chess.Knight):
                if board[y][x].color == WHITE:
                    DISPLAYSURF.blit(IMAGES['w_knight'], topleft)
                else:
                    DISPLAYSURF.blit(IMAGES['b_knight'], topleft)
            elif isinstance(board[y][x], chess.King):
                if board[y][x].color == WHITE:
                    DISPLAYSURF.blit(IMAGES['w_king'], topleft)
                else:
                    DISPLAYSURF.blit(IMAGES['b_king'], topleft)
            elif isinstance(board[y][x], chess.Queen):
                if board[y][x].color == WHITE:
                    DISPLAYSURF.blit(IMAGES['w_queen'], topleft)
                else:
                    DISPLAYSURF.blit(IMAGES['b_queen'], topleft)


def draw_board():
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            left, top = left_top_coords_of_box((x, y))
            box = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if (x + y) % 2 == 0:
                pygame.draw.rect(DISPLAYSURF, LIGHT_BOX_COLOR, box)
            else:
                pygame.draw.rect(DISPLAYSURF, DARK_BOX_COLOR, box)


def winning_animation(display, game_status):
    text = BIGFONT.render(game_status, True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    if display:
        DISPLAYSURF.blit(text, text_rect)


def ask_promotion(color):
    center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    text = 'Please choose pawn promotion value:'
    question = FONT.render(text, True, TEXT_COLOR, TEXT_BACKGROUND)
    question_rect = question.get_rect()
    question_rect.center = center
    knight = FONT.render('Knight', True, TEXT_COLOR, TEXT_BACKGROUND)
    knight_rect = knight.get_rect()
    knight_rect.center = (center[0] - 120, center[1] + 30)
    queen = FONT.render('Queen', True, TEXT_COLOR, TEXT_BACKGROUND)
    queen_rect = queen.get_rect()
    queen_rect.center = (center[0] - 60, center[1] + 30)
    rook = FONT.render('Rook', True, TEXT_COLOR, TEXT_BACKGROUND)
    rook_rect = rook.get_rect()
    rook_rect.center = (center[0] + 60, center[1] + 30)
    bishop = FONT.render('Bishop', True, TEXT_COLOR, TEXT_BACKGROUND)
    bishop_rect = bishop.get_rect()
    bishop_rect.center = (center[0] + 120, center[1] + 30)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mouse_pos = event.pos
                if knight_rect.collidepoint(mouse_pos):
                    return chess.Knight(color)
                elif queen_rect.collidepoint(mouse_pos):
                    return chess.Queen(color)
                elif rook_rect.collidepoint(mouse_pos):
                    return chess.Rook(color)
                elif bishop_rect.collidepoint(mouse_pos):
                    return chess.Bishop(color)

        DISPLAYSURF.blit(question, question_rect)
        DISPLAYSURF.blit(queen, queen_rect)
        DISPLAYSURF.blit(knight, knight_rect)
        DISPLAYSURF.blit(rook, rook_rect)
        DISPLAYSURF.blit(bishop, bishop_rect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def main():
    global DISPLAYSURF, IMAGES, FONT, BIGFONT, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    pygame.display.set_caption('Chess Game - Maria Tezieva')

    IMAGES = {'w_pawn': pygame.image.load(os.path.join('images', 'WP.png')),
              'b_pawn': pygame.image.load(os.path.join('images', 'BP.png')),
              'w_rook': pygame.image.load(os.path.join('images', 'WR.png')),
              'b_rook': pygame.image.load(os.path.join('images', 'BR.png')),
              'w_knight': pygame.image.load(os.path.join('images', 'WN.png')),
              'b_knight': pygame.image.load(os.path.join('images', 'BN.png')),
              'w_bishop': pygame.image.load(os.path.join('images', 'WB.png')),
              'b_bishop': pygame.image.load(os.path.join('images', 'BB.png')),
              'w_queen': pygame.image.load(os.path.join('images', 'WQ.png')),
              'b_queen': pygame.image.load(os.path.join('images', 'BQ.png')),
              'w_king': pygame.image.load(os.path.join('images', 'WK.png')),
              'b_king': pygame.image.load(os.path.join('images', 'BK.png'))}

    first_selection = None
    display = True
    animation = False
    game = chess.ChessBoard()

    while True:
        mouse_clicked = False
        chess_board = game.get_board()
        DISPLAYSURF.fill(BACKGROUND)
        draw_board()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP:
                mouse_pos = event.pos
                mouse_clicked = True
                box = get_box_at_pixel(mouse_pos)

        if mouse_clicked is True:
            if box != (None, None):
                if first_selection is None:
                    first_selection = box
                else:
                    game.move_piece(first_selection, box)
                    first_selection = None

        if first_selection:
            left, top = left_top_coords_of_box(first_selection)
            selected_box = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(DISPLAYSURF, RED, selected_box, 5)

        if game.promotion_allowed():
            color = game.promotion_color()
            piece = ask_promotion(color)
            game.set_pawn_promotion(piece)

        draw_pieces(chess_board)

        if game.white_win() or game.black_win() or game.stalemate():
            status = game.get_game_status()
            winning_animation(display, status)
            display = not display
            animation = True

        pygame.display.update()

        if animation:
            pygame.time.wait(500)

        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()

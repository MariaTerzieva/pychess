import pygame, os, sys, chess
from pygame.locals import QUIT

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOX_SIZE = 50
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * BOX_SIZE)) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * BOX_SIZE)) / 2)
LIGHT_BOX_COLOR = (255, 170, 85)
DARK_BOX_COLOR  = (102, 51, 0)
BACKGROUND = (50, 0, 0)
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
            if box_rect.collidepoint(pixel[0], pixel[1]):
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

def main():
    global DISPLAYSURF, IMAGES
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

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

    DISPLAYSURF.fill(BACKGROUND)
    draw_board()
    game = chess.ChessBoard()
    chess_board = game.board
    draw_pieces(chess_board)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()

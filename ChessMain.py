"""
This file will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import ChessEngine
import os

WIDTH = HEIGHT = 513  # 512 x 512 px
DIMESION = 8
SQ_SIZE = HEIGHT // DIMESION
MAX_FPS = 15  # for the animation
IMAGES = {}
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

"""Loading the images, this will be runned only once in the main"""


def load_images():
    pieces = ["bQ", "bK", "bB", "bN", "bR", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]

    for piece in pieces:
        filepath = os.path.join(DIR_PATH, ("images/" + piece + ".png"))
        # print(filepath)
        IMAGES[piece] = p.transform.smoothscale(p.image.load(filepath), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    # screen.fill(p.Color("black"))
    gs = ChessEngine.GameState()
    load_images()
    running = True
    sq_selected = ()  # keep track of the last click of the user (tuple: (row,col))
    player_clicks = []  # keep track of player clicks (two tuples: [(6,4),(4,4)]

    while running:
        for e in p.event.get():  # get all events from the event queue
            if e.type == p.QUIT:  # if there is a quit event, end the programm
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # get the (x,y) of the mouse position
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # the user clicked the same square
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                if len(player_clicks) == 2:      #action after the second click
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_a_move(move)
                    sq_selected = () #reset the user clicks
                    player_clicks = [] #reset the user clicks



        draw_gamestate(screen, gs)
        clock.tick(MAX_FPS)

        p.display.flip()


"""Responsible for all graphics"""


def draw_gamestate(screen, gs):
    draw_board(screen)  # draw the squares on the board
    draw_pieces(screen, gs.board)  # draw the pieces on top of the squares


"""Draw the squares"""


def draw_board(screen):
    colors = [p.Color(232, 144, 5), p.Color(105, 20, 14)]
    # colors = [p.Color("white"), p.Color("black")]

    for r in range(DIMESION):
        for c in range(DIMESION):
            color = colors[((r + c) % 2)]
            # print("" + str((r + c) % 2))
            # print("" + str((r + c)))
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""Draw the pieces on the squares"""


def draw_pieces(screen, board):
    for r in range(DIMESION):
        for c in range(DIMESION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
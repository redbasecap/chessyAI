"""
This file will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import ChessEngine
import os

WIDTH = HEIGHT = 513  # 512 x 512 px
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for the animation
IMAGES = {}
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# Farben
COLORS = [p.Color(232, 144, 5), p.Color(105, 20, 14)]
HIGHLIGHT_COLOR = p.Color(186, 202, 68)  # Grün für gültige Züge
SELECTED_COLOR = p.Color(255, 255, 0, 100)  # Gelb für ausgewählte Figur
LAST_MOVE_COLOR = p.Color(170, 162, 58)  # Letzter Zug
CHECK_COLOR = p.Color(255, 0, 0, 150)  # Rot für Schach

"""Loading the images, this will be runned only once in the main"""


def load_images():
    pieces = ["bQ", "bK", "bB", "bN", "bR", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]

    for piece in pieces:
        filepath = os.path.join(DIR_PATH, ("images/" + piece + ".png"))
        IMAGES[piece] = p.transform.smoothscale(p.image.load(filepath), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chessy - Chess Engine")
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False  # Flag für wenn ein Zug gemacht wurde

    load_images()
    running = True
    sq_selected = ()  # keep track of the last click of the user (tuple: (row,col))
    player_clicks = []  # keep track of player clicks (two tuples: [(6,4),(4,4)]
    game_over = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mausklick
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if sq_selected == (row, col):  # Gleiche Feld erneut geklickt
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)

                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(
                            player_clicks[0], player_clicks[1], gs.board
                        )

                        for valid_move in valid_moves:
                            if move == valid_move:
                                gs.make_move(valid_move)
                                move_made = True
                                print(valid_move.get_chess_notation())
                                sq_selected = ()
                                player_clicks = []
                                break

                        if not move_made:
                            player_clicks = [sq_selected]

            # Tastatur
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Z = Zug rückgängig
                    gs.undo_move()
                    move_made = True
                    game_over = False
                if e.key == p.K_r:  # R = Reset
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    game_over = False

        # Gültige Züge neu berechnen nach einem Zug
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

            # Spielende prüfen
            if gs.checkmate:
                game_over = True
                winner = "Schwarz" if gs.whiteToMove else "Weiß"
                print(f"Schachmatt! {winner} gewinnt!")
            elif gs.stalemate:
                game_over = True
                print("Patt! Unentschieden!")

        draw_gamestate(screen, gs, valid_moves, sq_selected)

        # Spielende-Text anzeigen
        if game_over:
            draw_end_game_text(screen, gs)

        clock.tick(MAX_FPS)
        p.display.flip()


def draw_gamestate(screen, gs, valid_moves, sq_selected):
    """Responsible for all graphics"""
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    """Draw the squares"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = COLORS[((r + c) % 2)]
            p.draw.rect(
                screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def highlight_squares(screen, gs, valid_moves, sq_selected):
    """Hebt ausgewählte Figur und gültige Züge hervor"""
    if sq_selected != ():
        r, c = sq_selected
        # Prüfen ob ausgewähltes Feld eine eigene Figur enthält
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            # Ausgewähltes Feld hervorheben
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(SELECTED_COLOR)
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

            # Gültige Züge hervorheben
            s.fill(HIGHLIGHT_COLOR)
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))

    # Letzten Zug hervorheben
    if len(gs.moveLog) > 0:
        last_move = gs.moveLog[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(80)
        s.fill(LAST_MOVE_COLOR)
        screen.blit(s, (last_move.start_col * SQ_SIZE, last_move.start_row * SQ_SIZE))
        screen.blit(s, (last_move.end_col * SQ_SIZE, last_move.end_row * SQ_SIZE))

    # König im Schach hervorheben
    if gs.is_in_check():
        if gs.whiteToMove:
            king_pos = gs.whiteKingLocation
        else:
            king_pos = gs.blackKingLocation
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(150)
        s.fill(CHECK_COLOR)
        screen.blit(s, (king_pos[1] * SQ_SIZE, king_pos[0] * SQ_SIZE))


def draw_pieces(screen, board):
    """Draw the pieces on the squares"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_end_game_text(screen, gs):
    """Zeigt Spielende-Text an"""
    font = p.font.SysFont("Helvetica", 32, True, False)
    if gs.checkmate:
        winner = "Schwarz" if gs.whiteToMove else "Weiß"
        text = f"Schachmatt! {winner} gewinnt!"
    else:
        text = "Patt! Unentschieden!"

    text_object = font.render(text, True, p.Color("gray"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - text_object.get_width() / 2,
        HEIGHT / 2 - text_object.get_height() / 2,
    )
    screen.blit(text_object, text_location)

    # Schatten-Effekt
    text_object = font.render(text, True, p.Color("black"))
    screen.blit(text_object, text_location.move(2, 2))
    text_object = font.render(text, True, p.Color("white"))
    screen.blit(text_object, text_location)

    # Hinweis zum Neustart
    small_font = p.font.SysFont("Helvetica", 16, False, False)
    hint = "Drücke 'R' für neues Spiel oder 'Z' zum Rückgängig"
    hint_object = small_font.render(hint, True, p.Color("white"))
    hint_location = text_location.move(0, 40)
    hint_location.x = WIDTH / 2 - hint_object.get_width() / 2
    screen.blit(hint_object, hint_location)


if __name__ == "__main__":
    main()

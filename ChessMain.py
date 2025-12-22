"""
This file will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import ChessEngine
import ChessAI
import os
from datetime import datetime

WIDTH = HEIGHT = 513  # 512 x 512 px
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = HEIGHT
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60  # Erhöht für flüssige Animationen
IMAGES = {}
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# Farben
COLORS = [p.Color(232, 144, 5), p.Color(105, 20, 14)]
HIGHLIGHT_COLOR = p.Color(186, 202, 68)  # Grün für gültige Züge
SELECTED_COLOR = p.Color(255, 255, 0, 100)  # Gelb für ausgewählte Figur
LAST_MOVE_COLOR = p.Color(170, 162, 58)  # Letzter Zug
CHECK_COLOR = p.Color(255, 0, 0, 150)  # Rot für Schach

# Animation
ANIMATION_SPEED = 15  # Frames pro Animation

# Sound aktivieren
SOUND_ENABLED = True

# Timer Einstellungen (in Sekunden)
TIMER_ENABLED = True
INITIAL_TIME = 600  # 10 Minuten pro Spieler


def load_images():
    """Lädt alle Figurenbilder"""
    pieces = ["bQ", "bK", "bB", "bN", "bR", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        filepath = os.path.join(DIR_PATH, ("images/" + piece + ".png"))
        IMAGES[piece] = p.transform.smoothscale(p.image.load(filepath), (SQ_SIZE, SQ_SIZE))


def load_sounds():
    """Lädt Soundeffekte"""
    sounds = {}
    sound_files = {
        "move": "move.wav",
        "capture": "capture.wav",
        "check": "check.wav",
        "castle": "castle.wav",
        "game_over": "game_over.wav",
    }

    sounds_dir = os.path.join(DIR_PATH, "sounds")
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
        # Erstelle einfache Platzhalter-Sounds wenn keine existieren
        return None

    for name, filename in sound_files.items():
        filepath = os.path.join(sounds_dir, filename)
        if os.path.exists(filepath):
            sounds[name] = p.mixer.Sound(filepath)

    return sounds if sounds else None


def main():
    p.init()
    p.mixer.init()

    screen = p.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    p.display.set_caption("Chessy - Chess Engine")
    clock = p.time.Clock()

    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False  # Flag für Animation

    load_images()
    sounds = load_sounds()

    running = True
    sq_selected = ()
    player_clicks = []
    game_over = False

    # Spieler-Konfiguration (True = Mensch, False = KI)
    player_one = True  # Weiß
    player_two = False  # Schwarz (KI)

    ai_thinking = False
    move_log_font = p.font.SysFont("Arial", 14, False, False)

    # Timer
    white_time = INITIAL_TIME
    black_time = INITIAL_TIME
    last_time = p.time.get_ticks()

    # Bauernumwandlung
    promotion_screen = False
    promotion_move = None

    while running:
        human_turn = (gs.whiteToMove and player_one) or (
            not gs.whiteToMove and player_two
        )

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mausklick
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn and not promotion_screen:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if col < 8:  # Nur auf dem Schachbrett
                        if sq_selected == (row, col):
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
                                    # Bauernumwandlung prüfen
                                    if valid_move.is_pawn_promotion:
                                        promotion_screen = True
                                        promotion_move = valid_move
                                    else:
                                        gs.make_move(valid_move)
                                        move_made = True
                                        animate = True
                                        play_sound(sounds, valid_move, gs)
                                        print(valid_move.get_chess_notation())
                                    sq_selected = ()
                                    player_clicks = []
                                    break

                            if not move_made and not promotion_screen:
                                player_clicks = [sq_selected]

                # Bauernumwandlung Auswahl
                elif promotion_screen:
                    location = p.mouse.get_pos()
                    piece = get_promotion_choice(location, gs.whiteToMove)
                    if piece:
                        promotion_move.promotion_piece = piece
                        gs.make_move(promotion_move)
                        move_made = True
                        animate = True
                        play_sound(sounds, promotion_move, gs)
                        promotion_screen = False
                        promotion_move = None

            # Tastatur
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Z = Zug rückgängig
                    gs.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                    promotion_screen = False
                if e.key == p.K_r:  # R = Reset
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    promotion_screen = False
                    white_time = INITIAL_TIME
                    black_time = INITIAL_TIME
                if e.key == p.K_s:  # S = Speichern als PGN
                    save_pgn(gs)
                if e.key == p.K_f:  # F = KI-Zug erzwingen
                    if not game_over and human_turn:
                        ai_move = ChessAI.find_best_move(gs, valid_moves)
                        if ai_move:
                            gs.make_move(ai_move)
                            move_made = True
                            animate = True
                            play_sound(sounds, ai_move, gs)

        # KI Zug
        if not game_over and not human_turn and not promotion_screen:
            ai_move = ChessAI.find_best_move(gs, valid_moves)
            if ai_move is None:
                ai_move = ChessAI.find_random_move(valid_moves)
            if ai_move:
                gs.make_move(ai_move)
                move_made = True
                animate = True
                play_sound(sounds, ai_move, gs)

        # Gültige Züge neu berechnen
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

            if gs.checkmate:
                game_over = True
                winner = "Schwarz" if gs.whiteToMove else "Weiß"
                print(f"Schachmatt! {winner} gewinnt!")
                if sounds and "game_over" in sounds:
                    sounds["game_over"].play()
            elif gs.stalemate:
                game_over = True
                print("Patt! Unentschieden!")
                if sounds and "game_over" in sounds:
                    sounds["game_over"].play()

        # Timer aktualisieren
        if TIMER_ENABLED and not game_over and not promotion_screen:
            current_time = p.time.get_ticks()
            elapsed = (current_time - last_time) / 1000
            last_time = current_time

            if gs.whiteToMove:
                white_time -= elapsed
                if white_time <= 0:
                    white_time = 0
                    game_over = True
                    print("Zeit abgelaufen! Schwarz gewinnt!")
            else:
                black_time -= elapsed
                if black_time <= 0:
                    black_time = 0
                    game_over = True
                    print("Zeit abgelaufen! Weiß gewinnt!")

        draw_gamestate(screen, gs, valid_moves, sq_selected)
        draw_move_log(screen, gs, move_log_font)

        if TIMER_ENABLED:
            draw_timer(screen, white_time, black_time, gs.whiteToMove)

        if promotion_screen:
            draw_promotion_screen(screen, gs.whiteToMove)

        if game_over:
            draw_end_game_text(screen, gs, white_time, black_time)

        clock.tick(MAX_FPS)
        p.display.flip()

    p.quit()


def play_sound(sounds, move, gs):
    """Spielt den passenden Sound ab"""
    if not sounds or not SOUND_ENABLED:
        return

    if gs.is_in_check():
        if "check" in sounds:
            sounds["check"].play()
    elif move.is_castle_move:
        if "castle" in sounds:
            sounds["castle"].play()
    elif move.piece_captured != "--":
        if "capture" in sounds:
            sounds["capture"].play()
    else:
        if "move" in sounds:
            sounds["move"].play()


def get_promotion_choice(location, is_white):
    """Ermittelt die gewählte Umwandlungsfigur"""
    x, y = location
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Prüfen ob Klick im Auswahlbereich
    if center_y - SQ_SIZE // 2 <= y <= center_y + SQ_SIZE // 2:
        pieces = ["Q", "R", "B", "N"]
        start_x = center_x - 2 * SQ_SIZE
        for i, piece in enumerate(pieces):
            if start_x + i * SQ_SIZE <= x <= start_x + (i + 1) * SQ_SIZE:
                return piece
    return None


def draw_promotion_screen(screen, is_white):
    """Zeigt Bauernumwandlungs-Dialog"""
    # Hintergrund abdunkeln
    s = p.Surface((WIDTH, HEIGHT))
    s.set_alpha(200)
    s.fill(p.Color("black"))
    screen.blit(s, (0, 0))

    # Auswahlbox
    pieces = ["Q", "R", "B", "N"]
    color = "w" if is_white else "b"
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Hintergrund für Auswahl
    box_rect = p.Rect(
        center_x - 2 * SQ_SIZE, center_y - SQ_SIZE // 2 - 30, 4 * SQ_SIZE, SQ_SIZE + 50
    )
    p.draw.rect(screen, p.Color("white"), box_rect)
    p.draw.rect(screen, p.Color("black"), box_rect, 3)

    # Text
    font = p.font.SysFont("Helvetica", 20, True, False)
    text = font.render("Wähle Umwandlung:", True, p.Color("black"))
    screen.blit(text, (center_x - text.get_width() // 2, center_y - SQ_SIZE // 2 - 25))

    # Figuren zeichnen
    for i, piece in enumerate(pieces):
        piece_key = color + piece
        x = center_x - 2 * SQ_SIZE + i * SQ_SIZE
        y = center_y - SQ_SIZE // 2 + 20
        screen.blit(IMAGES[piece_key], p.Rect(x, y, SQ_SIZE, SQ_SIZE))


def draw_gamestate(screen, gs, valid_moves, sq_selected):
    """Zeichnet das komplette Spielfeld"""
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    """Zeichnet das Schachbrett"""
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
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(SELECTED_COLOR)
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

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

    # König im Schach
    if gs.is_in_check():
        king_pos = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(150)
        s.fill(CHECK_COLOR)
        screen.blit(s, (king_pos[1] * SQ_SIZE, king_pos[0] * SQ_SIZE))


def draw_pieces(screen, board):
    """Zeichnet die Figuren"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_move_log(screen, gs, font):
    """Zeichnet das Zugprotokoll"""
    move_log_rect = p.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color(40, 40, 40), move_log_rect)

    # Titel
    title_font = p.font.SysFont("Arial", 18, True, False)
    title = title_font.render("Zugprotokoll", True, p.Color("white"))
    screen.blit(title, (WIDTH + 10, 10))

    move_log = gs.moveLog
    move_texts = []

    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + ". " + move_log[i].get_chess_notation()
        if i + 1 < len(move_log):
            move_string += "  " + move_log[i + 1].get_chess_notation()
        move_texts.append(move_string)

    padding = 40
    line_spacing = 20

    for i, text in enumerate(move_texts[-20:]):  # Letzte 20 Züge
        text_object = font.render(text, True, p.Color("white"))
        text_location = (WIDTH + 10, padding + i * line_spacing)
        screen.blit(text_object, text_location)


def draw_timer(screen, white_time, black_time, white_to_move):
    """Zeichnet die Schachuhren"""
    font = p.font.SysFont("Arial", 24, True, False)

    # Weiß Timer
    white_mins = int(white_time // 60)
    white_secs = int(white_time % 60)
    white_text = f"Weiß: {white_mins:02d}:{white_secs:02d}"
    white_color = p.Color("yellow") if white_to_move else p.Color("white")
    white_surface = font.render(white_text, True, white_color)
    screen.blit(white_surface, (WIDTH + 10, HEIGHT - 80))

    # Schwarz Timer
    black_mins = int(black_time // 60)
    black_secs = int(black_time % 60)
    black_text = f"Schwarz: {black_mins:02d}:{black_secs:02d}"
    black_color = p.Color("yellow") if not white_to_move else p.Color("white")
    black_surface = font.render(black_text, True, black_color)
    screen.blit(black_surface, (WIDTH + 10, HEIGHT - 50))


def draw_end_game_text(screen, gs, white_time=None, black_time=None):
    """Zeigt Spielende-Text"""
    font = p.font.SysFont("Helvetica", 32, True, False)

    if gs.checkmate:
        winner = "Schwarz" if gs.whiteToMove else "Weiß"
        text = f"Schachmatt! {winner} gewinnt!"
    elif gs.stalemate:
        text = "Patt! Unentschieden!"
    elif white_time is not None and white_time <= 0:
        text = "Zeit abgelaufen! Schwarz gewinnt!"
    elif black_time is not None and black_time <= 0:
        text = "Zeit abgelaufen! Weiß gewinnt!"
    else:
        text = "Spielende!"

    # Hintergrund
    s = p.Surface((WIDTH, 100))
    s.set_alpha(200)
    s.fill(p.Color("black"))
    screen.blit(s, (0, HEIGHT // 2 - 50))

    text_object = font.render(text, True, p.Color("white"))
    text_location = (WIDTH // 2 - text_object.get_width() // 2, HEIGHT // 2 - 20)
    screen.blit(text_object, text_location)

    small_font = p.font.SysFont("Helvetica", 16, False, False)
    hint = "R=Neustart | Z=Rückgängig | S=PGN Speichern"
    hint_object = small_font.render(hint, True, p.Color("white"))
    hint_location = (WIDTH // 2 - hint_object.get_width() // 2, HEIGHT // 2 + 20)
    screen.blit(hint_object, hint_location)


def save_pgn(gs):
    """Speichert die Partie als PGN-Datei"""
    pgn_dir = os.path.join(DIR_PATH, "games")
    if not os.path.exists(pgn_dir):
        os.makedirs(pgn_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(pgn_dir, f"game_{timestamp}.pgn")

    with open(filename, "w") as f:
        # PGN Header
        f.write('[Event "Chessy Game"]\n')
        f.write(f'[Date "{datetime.now().strftime("%Y.%m.%d")}"]\n')
        f.write('[White "Player"]\n')
        f.write('[Black "Chessy AI"]\n')

        # Ergebnis
        if gs.checkmate:
            result = "0-1" if gs.whiteToMove else "1-0"
        elif gs.stalemate:
            result = "1/2-1/2"
        else:
            result = "*"
        f.write(f'[Result "{result}"]\n\n')

        # Züge
        moves = []
        for i, move in enumerate(gs.moveLog):
            if i % 2 == 0:
                moves.append(f"{i // 2 + 1}.")
            moves.append(move.get_chess_notation())

        f.write(" ".join(moves))
        f.write(f" {result}\n")

    print(f"Partie gespeichert: {filename}")


def load_pgn(filename):
    """Lädt eine PGN-Datei (TODO: Vollständige Implementierung)"""
    # Grundlegende PGN-Parsing Logik
    pass


if __name__ == "__main__":
    main()

# ♟️ ChessyAI - Chess Engine

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/redbasecap)

A fully-featured chess engine with graphical user interface and AI opponent built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)

## ✨ Features

### Complete Chess Rules
- ✅ All piece movements (Pawn, Rook, Knight, Bishop, Queen, King)
- ✅ Check detection
- ✅ Checkmate & Stalemate detection
- ✅ Castling (Kingside & Queenside)
- ✅ En Passant
- ✅ Pawn Promotion with piece selection dialog

### 🤖 AI Opponent
- ✅ Minimax algorithm with Alpha-Beta pruning
- ✅ Position evaluation with piece-square tables
- ✅ Configurable search depth
- ✅ Play as White against AI (Black)

### User Interface
- ✅ Visual highlighting of valid moves
- ✅ Selected piece highlighting
- ✅ Last move highlighting
- ✅ Check warning (King highlighted in red)
- ✅ Game over dialog
- ✅ Move log panel
- ✅ Chess clock (10 min per player)

### 🔊 Sound Effects
- ✅ Move sounds
- ✅ Capture sounds
- ✅ Check warning
- ✅ Castling sound
- ✅ Game over sound

### 💾 Save & Export
- ✅ PGN export (save games)

### Controls
| Key | Action |
|-----|--------|
| `Z` | Undo last move |
| `R` | Restart game |
| `S` | Save game as PGN |
| `F` | Force AI move (hint) |
| Mouse | Select and move pieces |

## 🚀 Installation

### Using uv (Recommended)

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/redbasecap/ChessyAI.git
cd ChessyAI

# Install dependencies
uv sync

# Generate sound effects (first time only)
uv run python generate_sounds.py

# Run the game
uv run python ChessMain.py
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/redbasecap/ChessyAI.git
cd ChessyAI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pygame

# Generate sound effects (first time only)
python generate_sounds.py

# Run the game
python ChessMain.py
```

## 🎮 How to Play

1. **Start the game** with `uv run python ChessMain.py`
2. **Click on a piece** to select it (valid moves will be highlighted in green)
3. **Click on a highlighted square** to move the piece
4. **White (you) moves first**, AI (Black) responds automatically
5. **Pawn promotion**: When a pawn reaches the last rank, click on the piece you want
6. The game ends when checkmate, stalemate, or time runs out

### Player Configuration

Edit `ChessMain.py` to change who plays:

```python
player_one = True   # White: True = Human, False = AI
player_two = False  # Black: True = Human, False = AI
```

## 📁 Project Structure

```
ChessyAI/
├── ChessEngine.py      # Game logic and state management
├── ChessMain.py        # GUI and user input handling
├── ChessAI.py          # AI opponent (Minimax + Alpha-Beta)
├── generate_sounds.py  # Sound effect generator
├── images/             # Chess piece sprites (PNG)
├── sounds/             # Sound effects (WAV)
├── games/              # Saved PGN files
├── pyproject.toml      # Project configuration
└── README.md
```

## 🔧 Technical Details

### Piece Notation
```
w = White, b = Black
K = King, Q = Queen, R = Rook, B = Bishop, N = Knight, p = Pawn
Example: "wK" = White King, "bp" = Black Pawn
```

### Board Representation
The board is represented as an 8x8 2D array where `"--"` indicates an empty square.

### AI Evaluation
| Piece | Value |
|-------|-------|
| King | ∞ |
| Queen | 900 |
| Rook | 500 |
| Bishop | 330 |
| Knight | 320 |
| Pawn | 100 |

The AI also uses position tables to prefer central control and piece development.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

### Possible Enhancements
- [ ] PGN import (load games)
- [ ] Move animations
- [ ] Online multiplayer
- [ ] Opening book
- [ ] Endgame tablebase

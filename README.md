# ♟️ Chessy - Chess Engine

A fully-featured chess engine with graphical user interface built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### Complete Chess Rules
- ✅ All piece movements (Pawn, Rook, Knight, Bishop, Queen, King)
- ✅ Check detection
- ✅ Checkmate & Stalemate detection
- ✅ Castling (Kingside & Queenside)
- ✅ En Passant
- ✅ Pawn Promotion (auto-promotes to Queen)

### User Interface
- ✅ Visual highlighting of valid moves
- ✅ Selected piece highlighting
- ✅ Last move highlighting
- ✅ Check warning (King highlighted in red)
- ✅ Game over dialog

### Controls
| Key | Action |
|-----|--------|
| `Z` | Undo last move |
| `R` | Restart game |
| Mouse | Select and move pieces |

## 🚀 Installation

### Using uv (Recommended)

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/redbasecap/chessy.git
cd chessy

# Install dependencies
uv sync

# Run the game
uv run python ChessMain.py
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/redbasecap/chessy.git
cd chessy

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pygame

# Run the game
python ChessMain.py
```

## 🎮 How to Play

1. **Start the game** with `uv run python ChessMain.py`
2. **Click on a piece** to select it (valid moves will be highlighted in green)
3. **Click on a highlighted square** to move the piece
4. **White moves first**, then players alternate turns
5. The game ends when checkmate or stalemate is detected

## 📁 Project Structure

```
chessy/
├── ChessEngine.py    # Game logic and state management
├── ChessMain.py      # GUI and user input handling
├── images/           # Chess piece sprites (PNG)
├── pyproject.toml    # Project configuration
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

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

### Possible Enhancements
- [ ] AI opponent (Minimax/Alpha-Beta)
- [ ] Choose promotion piece
- [ ] Move timer
- [ ] PGN export/import
- [ ] Sound effects
- [ ] Move animations

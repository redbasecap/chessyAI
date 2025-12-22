# Chessy - Chess Engine Analyse

## Projektübersicht

**Projektname:** Chessy  
**Typ:** Schach-Engine mit grafischer Benutzeroberfläche  
**Technologie:** Python + Pygame  
**Status:** ✅ Vollständig spielbar (v2.0) - mit KI-Gegner!

---

## Aktuelle Implementierung

### Dateistruktur

| Datei               | Beschreibung                          |
| ------------------- | ------------------------------------- |
| `ChessEngine.py`    | Spiellogik und Zustandsverwaltung     |
| `ChessMain.py`      | GUI und Benutzereingaben              |
| `ChessAI.py`        | KI-Gegner (Minimax + Alpha-Beta)      |
| `generate_sounds.py`| Sound-Generator für Soundeffekte      |
| `images/`           | 12 Schachfiguren-Sprites (PNG)        |
| `sounds/`           | Soundeffekte (WAV)                    |
| `games/`            | Gespeicherte Partien (PGN)            |

### ChessEngine.py - Spiellogik

#### `GameState` Klasse

- ✅ **Board-Repräsentation:** 8x8 2D-Array mit String-Notation (z.B. "wK" = weißer König)
- ✅ **Zugverfolgung:** `moveLog` speichert alle gespielten Züge
- ✅ **Spielerwechsel:** `whiteToMove` Boolean für Zugrecht
- ✅ **Zugausführung:** `make_move()` Methode mit vollständiger Regelprüfung
- ✅ **Zug-Rücknahme:** `undo_move()` Methode
- ✅ **Zugvalidierung:** `get_valid_moves()` gibt nur legale Züge zurück
- ✅ **Schach-Erkennung:** `is_in_check()` und `square_under_attack()`
- ✅ **Figurenbewegungen:** Separate Methoden für jede Figur
- ✅ **Rochade:** Kurz und lang für beide Seiten
- ✅ **En Passant:** Vollständig implementiert
- ✅ **Bauernumwandlung:** Mit Auswahlmenü (Dame, Turm, Läufer, Springer)
- ✅ **Schachmatt/Patt:** Automatische Erkennung

#### `Move` Klasse

- ✅ **Schachnotation:** Konvertierung zwischen Array-Indizes und algebraischer Notation (a1-h8)
- ✅ **Zugdaten:** Start-/Endposition, bewegte und geschlagene Figur
- ✅ **Spezialzüge:** Flags für En Passant, Rochade, Bauernumwandlung
- ✅ **Zugvergleich:** `__eq__` für korrekte Zugidentifikation

### ChessAI.py - Künstliche Intelligenz

- ✅ **Minimax-Algorithmus:** Mit Suchtiefe 3
- ✅ **Alpha-Beta Pruning:** Optimierte Suche
- ✅ **Stellungsbewertung:** Material + Positionstabellen
- ✅ **Figurenwerte:** K=∞, Q=900, R=500, B=330, N=320, p=100
- ✅ **Positionstabellen:** Für alle Figurentypen

### ChessMain.py - Benutzeroberfläche

- ✅ **Pygame-Fenster:** 513x763 Pixel (mit Seitenpanel)
- ✅ **Schachbrett-Rendering:** Farbiges 8x8 Schachbrett (Orange/Dunkelrot)
- ✅ **Figuren-Darstellung:** Alle 12 Figuren werden geladen und skaliert
- ✅ **Mausinteraktion:** Klick-basierte Figurenauswahl und Bewegung
- ✅ **Zugprotokoll:** Seitenpanel mit allen Zügen
- ✅ **Gültige Züge:** Grün hervorgehoben
- ✅ **Ausgewählte Figur:** Gelb hervorgehoben
- ✅ **Letzter Zug:** Olive hervorgehoben
- ✅ **Schach-Warnung:** König rot hervorgehoben
- ✅ **Spielende-Dialog:** Zeigt Gewinner oder Unentschieden
- ✅ **Bauernumwandlung:** Grafischer Auswahldialog
- ✅ **Schachuhr:** 10 Minuten pro Spieler
- ✅ **Soundeffekte:** Für Züge, Schlagen, Schach, Rochade, Spielende
- ✅ **PGN-Export:** Partien speichern

---

## Implementierte Features

### Kern-Features ✅

| Feature              | Status           |
| -------------------- | ---------------- |
| Zuggültigkeit prüfen | ✅ Implementiert |
| Schach-Erkennung     | ✅ Implementiert |
| Schachmatt-Erkennung | ✅ Implementiert |
| Patt-Erkennung       | ✅ Implementiert |
| Rochade              | ✅ Implementiert |
| En Passant           | ✅ Implementiert |
| Bauernumwandlung     | ✅ Implementiert |

### Erweiterte Features ✅

| Feature                        | Status           |
| ------------------------------ | ---------------- |
| KI-Gegner (Minimax/Alpha-Beta) | ✅ Implementiert |
| Bauernumwandlung wählen        | ✅ Implementiert |
| Zug-Timer (Schachuhr)          | ✅ Implementiert |
| PGN-Export                     | ✅ Implementiert |
| Soundeffekte                   | ✅ Implementiert |
| Zugprotokoll                   | ✅ Implementiert |

### UX-Features ✅

| Feature                       | Status           |
| ----------------------------- | ---------------- |
| Zug-Rücknahme (Undo)          | ✅ Implementiert |
| Gültige Züge hervorheben      | ✅ Implementiert |
| Ausgewählte Figur hervorheben | ✅ Implementiert |
| Letzten Zug hervorheben       | ✅ Implementiert |
| Spielende-Anzeige             | ✅ Implementiert |

### Mögliche Erweiterungen (TODO)

| Priorität  | Feature                        | Status                 |
| ---------- | ------------------------------ | ---------------------- |
| 🟢 Niedrig | PGN-Import                     | ❌ Nicht implementiert |
| 🟢 Niedrig | Zuganimationen                 | ❌ Nicht implementiert |
| 🟢 Niedrig | Online-Multiplayer             | ❌ Nicht implementiert |
| 🟢 Niedrig | Eröffnungsbibliothek           | ❌ Nicht implementiert |

---

## Tastatursteuerung

| Taste | Aktion                        |
| ----- | ----------------------------- |
| `Z`   | Letzten Zug rückgängig machen |
| `R`   | Neues Spiel starten           |
| `S`   | Partie als PGN speichern      |
| `F`   | KI-Zug erzwingen              |

---

## Technische Details

### Abhängigkeiten

- Python >=3.9
- Pygame >=2.5.0

### Installation

```bash
# Mit uv (empfohlen)
uv sync
uv run python ChessMain.py

# Sounds generieren (einmalig)
uv run python generate_sounds.py
```

### Figuren-Notation

```
w = Weiß, b = Schwarz
K = König, Q = Dame, R = Turm, B = Läufer, N = Springer, p = Bauer
Beispiel: "wK" = weißer König, "bp" = schwarzer Bauer
```

### Board-Layout (Startposition)

```
Row 0: bR bN bB bQ bK bB bN bR  (Reihe 8)
Row 1: bp bp bp bp bp bp bp bp  (Reihe 7)
Row 2-5: -- -- -- -- -- -- -- --
Row 6: wp wp wp wp wp wp wp wp  (Reihe 2)
Row 7: wR wN wB wQ wK wB wN wR  (Reihe 1)
```

### KI-Konfiguration

In `ChessMain.py` können die Spieler konfiguriert werden:

```python
player_one = True   # Weiß: True=Mensch, False=KI
player_two = False  # Schwarz: True=Mensch, False=KI
```

---

## Fazit

Der Chess Engine ist **vollständig spielbar** mit allen Features:

- ✅ Alle Schachregeln korrekt implementiert
- ✅ KI-Gegner mit Minimax + Alpha-Beta Pruning
- ✅ Bauernumwandlung mit Auswahlmenü
- ✅ Schachuhr (10 Minuten pro Spieler)
- ✅ Soundeffekte für alle Aktionen
- ✅ PGN-Export für Partien
- ✅ Zugprotokoll im Seitenpanel
- ✅ Visuelles Feedback für alle Aktionen

**Geschätzter Fertigstellungsgrad:** ~95% (Feature-komplett)

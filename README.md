# 🏰 Carcassonne – Python Edition

A digital implementation of the classic tile-placement board game **Carcassonne**, developed as part of a university internship project.

---

## 📖 About the Project

This project is a fully playable digital version of the Carcassonne board game, built with Python and Pygame. Players take turns drawing and placing tiles to build cities, roads, monasteries, and fields — and strategically place their followers (Meeples) to score points.

---

## 🎮 Features

- 2–5 player support
- Tile placement with rotation
- Drag-and-drop tile mechanic
- Follower (Meeple) placement system
- Score tracking per player
- Save & load game state (JSON)
- Tutorial / rules info panel
- Interactive main menu

---

## 🗂️ Project Structure

```
Carcassonne/
├── main.py
├── Menu.py
├── spiel.json
├── Backend/
│   ├── klassen.py
│   ├── Karteninfo.py
│   ├── control.py
│   ├── model.py
│   ├── save_system.py
│   ├── backend_test.py
│   └── model_test.py
└── Frontend/
    ├── spielboard.py
    ├── left_panel.py
    ├── karten_frontend.py
    ├── drag_manager.py
    ├── Button.py
    ├── tutorial.py
    └── Images/
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Pygame](https://www.pygame.org/)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/carcassonne-python.git
cd carcassonne-python

# Install dependencies
pip install pygame
```

### Run the Game

```bash
python Menu.py
```

---

## 🧪 Running Tests

```bash
python Backend/backend_test.py
```

---

## 🛠️ Built With

- **Python 3** – Core language
- **Pygame** – Game rendering and event handling
- **JSON** – Game state persistence

---

## 👥 Authors

Developed as part of a university internship project.

---

## 📄 License

This project is for educational purposes only.  
The original Carcassonne board game is a trademark of **Hans im Glück**.

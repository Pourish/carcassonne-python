# carcassonne-python
🏰 Carcassonne board game in Python – university internship project
    A digital implementation of the classic tile-placement board game Carcassonne, developed as part of a university internship project.

📖 About the Project
This project is a fully playable digital version of the Carcassonne board game, built with Python and Pygame. Players take turns drawing and placing tiles to build cities, roads, monasteries, and fields — and strategically place their followers (Meeples) to score points.


🎮 Features
 - 2–5 player support
 -  Tile placement with rotation
 -  Drag-and-drop tile mechanic
 -  Follower (Meeple) placement system
 -  Score tracking per player
 -  Save & load game state (JSON)
 -  Tutorial / rules info panel
 -  Interactive main menu

   
🗂️ Project Structure  
     Carcassonne/
   │
   ├── main.py               # Entry point of the game
   ├── Menu.py               # Main menu screen
   ├── spiel.json            # Saved game state
   │
   ├── Backend/
   │   ├── klassen.py        # Core game classes (Tile, Player, GameState, etc.)
   │   ├── Karteninfo.py     # Tile definitions and area data
   │   ├── control.py        # Game logic controller
   │   ├── model.py          # Game model and initialization
   │   ├── save_system.py    # Save/load functionality
   │   ├── backend_test.py   # Backend unit tests
   │   └── model_test.py     # Model unit tests
   │
   └── Frontend/
       ├── spielboard.py     # Game board rendering
       ├── left_panel.py     # Player info panel (scores, meeples, current tile)
       ├── karten_frontend.py# Tile image loading and rendering
       ├── drag_manager.py   # Drag-and-drop logic
       ├── Button.py         # Reusable button components
       ├── tutorial.py       # In-game rules / scoring guide
       └── Images/           # Game assets (tiles, UI graphics)
  

🚀Getting Started
   -  Prerequisites
   -  Python 3.10+
   -  Pygame
    
Installation
# Clone the repository
git clone https://github.com/pourish/carcassonne-python.git
cd carcassonne-python

# Install dependencies
pip install pygame

Run the Game
   python Menu.py

👥Authors
   Developed as part of a university internship project.
   
📄 License
  This project is for educational purposes only.
  The original Carcassonne board game is a trademark of Hans im Glück.








  

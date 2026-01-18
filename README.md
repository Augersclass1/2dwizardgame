# 🧙 Wizard Open World Game (Pygame)

A simple 2D open-world sandbox game built with **Python** and **Pygame**.  
The game features procedurally generated terrain, chunk loading, basic physics, player movement, and block placement/removal—similar to a very lightweight Minecraft-style world.

---

## 📸 Features

- Procedurally generated terrain using math-based height functions
- Chunk-based world generation for infinite scrolling
- Basic tile system (dirt, stone, grass, wood, leaves, etc.)
- Tree generation
- Player movement with gravity and collision
- Block placement and removal with mouse
- Camera that follows the player
- Debug overlay (FPS, coordinates, chunk info)

---

## 🕹️ Controls

### Movement
- **A** – Move left  
- **D** – Move right  
- **W** – Jump (only when on the ground)

### Mouse
- **Right Click** – Place a block  
- **Left Click** – Remove a block  
(Block placement is limited by distance from the player)

### Other
- **F3** – Toggle debug information  
- **ESC** – Quit the game  

---

## 🧱 Blocks

| Block | Description |
|------|------------|
| Dirt | Basic ground material |
| Stone | Underground material |
| Grass | Surface tile |
| Wood | Tree trunk |
| Leaves | Tree canopy |
| Air | Empty space |

---

## 🛠 Requirements

- Python **3.8+**
- Pygame

Install pygame with:
"""pip install pygame"""
▶️ How to Run

From the terminal or command prompt:

python 2dminecraft.py
The game runs in fullscreen mode by default.

🗺️ World Generation

Terrain height is generated using sine waves for smooth hills

The world is divided into chunks (16×16 tiles)

Chunks are generated only when needed and stored in memory

Trees spawn randomly on valid ground tiles

🧪 Debug Mode (F3)

Displays:

FPS

Player position

Current chunk

Loaded chunk count

Mouse screen, world, and tile coordinates

🚧 Known Limitations

No saving/loading of worlds

No enemies or combat yet

Single block type selection

No UI or inventory system

🚀 Future Ideas

Inventory system

Multiple selectable blocks

Enemies and combat

World saving/loading

Biomes

Sound effects and music

📄 License

This project is for learning and experimentation.
Feel free to modify, expand, and build upon it.


If you want, I can also:
- Add **screenshots section**
- Write a **dev notes** section
- Make a **GitHub-style badge header**
- Tailor it to a **school or portfolio project**

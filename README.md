---

# 🎮 Linja: Minimax AI Game

Welcome to **Linja**, a strategic board game brought to life through AI using the **Minimax algorithm**! This project was developed as part of an AI course, where we designed an agent to play the game Linja against human players, featuring an intuitive **graphical interface** with sprites in pixel art.

---

## 📝 Project Overview

The goal of this project is to implement an agent that plays **Linja** by applying the **Minimax algorithm**, a decision-making process widely used in AI for games. In this project:

- We used **Python** with **Pygame** and **Tkinter** to create an interactive environment for human players to face off against an AI.
- The initial and final states of the game are managed through **text files**.
- The project also includes a visually appealing **pixel art** interface, designed to immerse players in the game.

> 🎥 **Learn more about Linja**: [Watch the game rules](https://www.youtube.com/watch?v=vJvAXQIwZko)

---

## 👥 Team Members

- **Joann Esteban Bedoya Lopez** 
- **Carlos Eduardo Guerrero Jaramillo** 
- **John Jader Marulanda Valero** 

---

## 🧠 How It Works

The game allows a human player to compete against an AI, with the AI's moves being determined by the **Minimax algorithm**. Here's a breakdown of the main components:

### Minimax Algorithm:
- **Minimax** is applied to evaluate all possible moves and choose the optimal one that maximizes the agent’s chance of winning.
- **Heuristic**: Our heuristic focuses on assessing the number of pieces on each stripe, considering both offensive and defensive moves.

### Alpha-Beta Pruning:
For groups of four members, **alpha-beta pruning** was implemented to optimize the search by eliminating unnecessary branches in the decision tree.

### Game Rules:
- Players make a **first move**, and the second move is based on the number of pieces (both their own and the opponent's) in the stripe where the first move was made.
- **Maximum of 6 pieces** in each stripe, except for the final ones.
- If the first move reaches an empty stripe, no second move is allowed.

---

## 🎨 Features and Design

This project includes a carefully crafted **pixel art** interface to enhance the player's experience. Some key design elements include:

- **Game Board**: A pixelated grid representing the stripes and pieces.
- **Pieces**: Colorful, animated tokens that move based on the player’s or AI's decisions.
- **Interactive Buttons**: Includes a start button for easy interaction.

> _Insert Game Board Screenshot Here_  
> _Insert Piece and Button Design Screenshot Here_

---

## 🔧 Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Linja-Game.git
   cd Linja-Game
   ```
   
2. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python LinjaGui.py
   ```

---

## 🕹️ How to Play

1. **Load the Initial State**: The game starts by loading a text file that defines the initial positions of the pieces.
2. **Human vs AI**: A human player makes the first move, followed by the AI agent using the Minimax algorithm.
3. **Track the Final State**: The game stores the final state in a separate text file, allowing for easy review and replays.

---

## 🤝 How to Contribute

We’d love to see your contributions! You can help us in several ways:

1. **Report Bugs**: Found a bug? [Open an issue](#).
2. **Enhance the Game**: Got an idea for a new feature? [Submit an enhancement](#).
3. **Pull Requests**: We welcome code contributions! Please make sure to follow our coding guidelines before submitting a PR.

---

## 📚 Additional Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Minimax Algorithm Overview](https://en.wikipedia.org/wiki/Minimax)
- [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

---

Thank you for checking out our **Linja Minimax AI Game**!. 🚀

---

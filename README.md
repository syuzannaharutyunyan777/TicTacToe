
````markdown
# Tic-Tac-Toe XMPP Game

## Project Overview
This project is a **console-based Tic-Tac-Toe game** that allows **two players to play over the XMPP network**.  
Each player logs into any XMPP server and plays the game in real time using chat messages to communicate moves.

The game is written in **Python**, using **asyncio** for asynchronous input and **Slixmpp** for XMPP messaging.  
This implementation meets the requirement of a **decentralized network game**, as both players communicate directly via XMPP without a central server.

---

## Features
- Play Tic-Tac-Toe between two XMPP users.
- Players can choose their symbol (`X` or `O`).
- Detects win, loss, and draw automatically.
- Allows restarting the game after it ends.
- Simple console interface showing the current board.

---

## Requirements
- Python 3.8 or higher
- Slixmpp library:
  ```bash
  pip install slixmpp
````

* Two XMPP accounts on any server (e.g., jabber.org, xmpp.jp)
* Internet connection

---

## How to Run

1. Save the code in a file, for example: `tic_tac_toe_xmpp.py`
2. Open terminal and navigate to the folder containing the file.
3. Run the game:

   ```bash
   python tic_tac_toe_xmpp.py
   ```
4. Follow the prompts in the console:

   * Enter your XMPP JID and password.
   * Enter your peer's XMPP JID.
   * Specify if you are Player 1 (y) or Player 2 (n).
   * Player 1 chooses a symbol (X or O).
   * Enter moves in the format `row,col` (e.g., `0,2`).
5. The board updates after each move. The game announces the result automatically.
6. After the game ends, you can choose to restart or exit.

---

## Game Rules

* Players take turns placing their symbol on a 3x3 board.
* The first player to get 3 symbols in a row, column, or diagonal wins.
* If all cells are filled and no player wins → draw.

---

## How It Works

* The `TicTacToeClient` class handles XMPP communication and game logic.
* Game events are sent as chat messages:

  * `START <symbol>` → Player 1 chooses symbol.
  * `MOVE <row> <col>` → Sends the move to the opponent.
  * `GAME_OVER_LOSE / GAME_OVER_DRAW` → Notifies the opponent about game result.
  * `RESTART_REQUEST / RESTART_ACK` → Used to restart the game.
* Uses `asyncio` to handle input and messages simultaneously.
* Supports fully decentralized gameplay over any XMPP server.

---

## Example Board

```
X |   | O
---------
  | X |  
---------
O |   | X
```

```

---


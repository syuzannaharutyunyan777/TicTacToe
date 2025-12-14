# Tic-Tac-Toe over XMPP

This is a simple Tic-Tac-Toe game that works over XMPP. Two players can play remotely by logging in to any XMPP server. The game communicates directly using XML messages.

## Features
- Two-player Tic-Tac-Toe game
- Decentralized: works over XMPP, no central server
- Win, draw, and restart detection
- Console-based interface

## Requirements
- Python 3.10 or higher
- `slixmpp` library
- An XMPP account for each player

## How to Run
1. Install dependencies:
```

pip install slixmpp

```
2. Run the game:
```

python tic_tac_toe_xmpp_console.py

```
3. Enter your XMPP JID and password.
4. Enter your peer's XMPP JID.
5. Choose if you are Player 1.
6. Follow the prompts to play.

## How It Works
- Player 1 chooses a symbol (X or O) and sends a START message to the peer.
- Players take turns sending MOVE messages.
- Game detects win, draw, and allows restart.
- All communication is done via XMPP messages.

## Notes
- Both players must have an active XMPP account.
- Works on any XMPP server.
```




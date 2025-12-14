import asyncio
from slixmpp import ClientXMPP
import getpass

BOARD_SIZE = 3

async def ainput(prompt=""):
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)

class TicTacToeClient(ClientXMPP):
    def __init__(self, jid, password, peer_jid, is_initiator):
        super().__init__(jid, password)
        self.peer_jid = peer_jid
        self.is_initiator = is_initiator

        self.symbol = None
        self.opponent_symbol = None
        self.board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.turn = "X"
        self.game_started = False

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message_received)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        print("Connected.")

        if self.is_initiator:
            while True:
                s = (await ainput("Choose your symbol (X/O): ")).upper()
                if s in ("X", "O"):
                    self.symbol = s
                    self.opponent_symbol = "O" if s == "X" else "X"
                    break

            self.send_message(
                mto=self.peer_jid,
                mbody=f"START {self.symbol}",
                mtype="chat"
            )

            self.game_started = True
            print(f"Game started. You are {self.symbol}.")
            self.print_board()

            if self.turn == self.symbol:
                asyncio.create_task(self.make_move())
        else:
            print("Waiting for Player 1 to choose symbol...")

    async def make_move(self):
        while self.turn == self.symbol:
            if not self.game_started:
                await asyncio.sleep(0.5)
                continue
            try:
                move = await ainput(f"Your move ({self.symbol}), enter row,col (0-{BOARD_SIZE-1}): ")
                r, c = map(int, move.strip().split(","))
                if self.board[r][c] == " ":
                    self.board[r][c] = self.symbol
                    self.print_board()
                    self.send_message(
                        mto=self.peer_jid,
                        mbody=f"MOVE {r} {c}",
                        mtype="chat"
                    )
                    if self.check_winner():
                        print("You win!")
                        self.send_message(
                            mto=self.peer_jid,
                            mbody="GAME_OVER_LOSE",
                            mtype="chat"
                        )
                        await self.ask_restart()
                        return
                    elif self.is_draw():
                        print("It's a draw!")
                        self.send_message(
                            mto=self.peer_jid,
                            mbody="GAME_OVER_DRAW",
                            mtype="chat"
                        )
                        await self.ask_restart()
                        return
                    self.turn = self.opponent_symbol
                else:
                    print("Cell already taken, try again.")
            except (ValueError, IndexError):
                print("Invalid input. Format: row,col")

    def message_received(self, msg):
        body = msg['body'].strip()

        if body.startswith("START"):
            _, s = body.split()
            self.board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
            self.opponent_symbol = s
            self.symbol = "O" if s == "X" else "X"
            self.turn = "X"
            self.game_started = True
            print(f"\nGame started. You are {self.symbol}. Player 1 is {self.opponent_symbol}.")
            self.print_board()
            if self.turn == self.symbol:
                asyncio.create_task(self.make_move())

        elif body.startswith("MOVE"):
            _, r, c = body.split()
            r, c = int(r), int(c)
            self.board[r][c] = self.opponent_symbol
            print(f"\nOpponent moved at {r},{c}")
            self.print_board()
            if self.check_winner():
                print("You lose!")
                asyncio.create_task(self.ask_restart())
                return
            elif self.is_draw():
                print("It's a draw!")
                asyncio.create_task(self.ask_restart())
                return
            self.turn = self.symbol
            asyncio.create_task(self.make_move())

        elif body == "GAME_OVER_LOSE":
            print("You lose!")
            asyncio.create_task(self.ask_restart())
        elif body == "GAME_OVER_DRAW":
            print("It's a draw!")
            asyncio.create_task(self.ask_restart())

        elif body == "RESTART_REQUEST":
            self.board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
            self.game_started = True
            self.turn = "X"
            print("\nOpponent wants to restart the game. Board reset.")
            self.print_board()
            self.send_message(mto=self.peer_jid, mbody="RESTART_ACK", mtype="chat")
            if self.turn == self.symbol:
                asyncio.create_task(self.make_move())

        elif body == "RESTART_ACK":
            self.board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
            self.game_started = True
            self.turn = "X"
            print("\nRestart acknowledged by opponent. Board reset.")
            self.print_board()
            if self.turn == self.symbol:
                asyncio.create_task(self.make_move())

    async def ask_restart(self):
        if self.is_initiator:
            choice = (await ainput("\nDo you want to restart the game? (y/n): ")).lower()
            if choice == "y":
                self.send_message(mto=self.peer_jid, mbody="RESTART_REQUEST", mtype="chat")
            else:
                print("Game ended. Goodbye!")
                self.disconnect()
        else:
            print("Waiting for Player 1 to restart the game...")

    def print_board(self):
        print("\nBoard:")
        print("\n".join([" | ".join(row) for row in self.board]))
        print("")

    def check_winner(self):
        b = self.board
        for r in range(BOARD_SIZE):
            if b[r][0] != " " and all(b[r][i] == b[r][0] for i in range(BOARD_SIZE)):
                return True
        for c in range(BOARD_SIZE):
            if b[0][c] != " " and all(b[i][c] == b[0][c] for i in range(BOARD_SIZE)):
                return True
        if b[0][0] != " " and all(b[i][i] == b[0][0] for i in range(BOARD_SIZE)):
            return True
        if b[0][BOARD_SIZE-1] != " " and all(b[i][BOARD_SIZE-1-i] == b[0][BOARD_SIZE-1] for i in range(BOARD_SIZE)):
            return True
        return False

    def is_draw(self):
        return all(self.board[r][c] != " " for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))

async def main():
    jid = ""
    while not jid.strip():
        jid = input("Your XMPP JID: ").strip()

    password = ""
    while not password.strip():
        password = getpass.getpass("Password: ").strip()

    peer = ""
    while not peer.strip():
        peer = input("Peer XMPP JID: ").strip()

    role = ""
    while role.lower() not in ("y", "n"):
        role = input("Are you Player 1? (y/n): ").strip().lower()

    xmpp = TicTacToeClient(jid, password, peer, is_initiator=(role == "y"))

    await xmpp.connect()
    await xmpp.disconnected

if __name__ == "__main__":
    asyncio.run(main())

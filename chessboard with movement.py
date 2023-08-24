import tkinter as tk
import chess.pgn
import chess.engine
from tkinter import filedialog
import subprocess

class ChessboardGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chessboard")
        self.geometry("1100x600")
        self.piece_size = 75
        self.create_chessboard()
        self.create_sidebar()
        self.current_move_index = 0
        self.update_board()
        self.bind("<Left>", self.prev_move)
        self.bind("<Right>", self.next_move)

        self.upload_button = tk.Button(self.sidebar, text="Upload PGN", command=self.upload_pgn)
        self.upload_button.pack(pady=10)

    def create_chessboard(self):
        self.chessboard = [[None for _ in range(8)] for _ in range(8)]
        self.colors = ["#FFCE9E", "#D18B47"]
        self.empty_tile_size = 75
        for row in range(8):
            for col in range(8):
                color_idx = (row + col) % 2
                tile_size = self.piece_size if (row + col) % 2 else self.empty_tile_size
                self.chessboard[row][col] = tk.Canvas(self, width=tile_size, height=tile_size, bg=self.colors[color_idx], highlightthickness=0)
                self.chessboard[row][col].grid(row=row, column=col)

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, width=250, bg="#EFEFEF")
        self.sidebar.grid(row=0, column=8, rowspan=8, sticky="ns")
        self.best_move_label = tk.Label(self.sidebar, text="Best Move:", font=("Arial", 16))
        self.best_move_label.pack(pady=10)
        self.best_move_var = tk.StringVar(value="N/A")
        self.best_move_text = tk.Label(self.sidebar, textvariable=self.best_move_var, font=("Arial", 16))
        self.best_move_text.pack(pady=5)

    def load_pgn_moves(self, pgn_filename):
        self.moves = []
        with open(pgn_filename) as pgn_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if not game:
                    break
                self.moves.extend(game.mainline_moves())

    def next_move(self, event):
        if self.current_move_index < len(self.moves):
            self.current_move_index += 1
            self.update_board()

    def prev_move(self, event):
        if self.current_move_index > 0:
            self.current_move_index -= 1
            self.update_board()

    def update_board(self):
        board = chess.Board()
        for i in range(self.current_move_index):
            board.push(self.moves[i])

        best_move_san = self.analyze_game(board)
        self.best_move_var.set(best_move_san)

    def analyze_game(self, board):
        output = subprocess.check_output(["python", "best_move_script.py", str(board.fen())], text=True)
        return output.strip()

if __name__ == "__main__":
    app = ChessboardGUI()
    app.mainloop()

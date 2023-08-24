import tkinter as tk
import chess.pgn
import chess.engine

class ChessboardGUI(tk.Tk):
    def __init__(self, engine_path, depth):
        super().__init__()
        self.title("Chess Analysis")
        self.geometry("800x600")
        self.engine_path = engine_path
        self.depth = depth
        self.piece_size = 75
        self.create_chessboard()
        self.load_pgn_moves()  # Load moves from the PGN file
        self.current_move_index = 0
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        self.update_board()

        # Bind the left and right arrow keys to navigate through moves
        self.bind("<Left>", self.prev_move)
        self.bind("<Right>", self.next_move)

    def create_chessboard(self):
        self.chessboard = [[None for _ in range(8)] for _ in range(8)]
        self.colors = ["#FFCE9E", "#D18B47"]
        for row in range(8):
            for col in range(8):
                color_idx = (row + col) % 2
                self.chessboard[row][col] = tk.Canvas(self, width=self.piece_size, height=self.piece_size, bg=self.colors[color_idx], highlightthickness=0)
                self.chessboard[row][col].grid(row=row, column=col)

    def load_pgn_moves(self):
        pgn_filename = "game.pgn"
        self.moves = []
        with open(pgn_filename) as pgn_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if not game:
                    break
                self.moves.extend([move for move in game.mainline_moves()])

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

        for row in range(8):
            for col in range(8):
                color_idx = (row + col) % 2
                self.chessboard[row][col].config(bg=self.colors[color_idx])

                # Clear the canvas for each cell before updating with the new piece
                for widget in self.chessboard[row][col].winfo_children():
                    widget.destroy()

                piece = board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_str = self.get_piece_unicode(piece)
                    color = "#FFFFFF" if piece.color == chess.WHITE else "#000000"
                    label = tk.Label(self.chessboard[row][col], text=piece_str, font=("Arial Unicode MS", self.piece_size // 2), bg=self.colors[color_idx], fg=color)
                    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Update the sidebar evaluation
        evaluation = self.engine.analyse(board, chess.engine.Limit(depth=self.depth))
        self.sidebar.update_evaluation(evaluation)

    def get_piece_unicode(self, piece):
        piece_unicode = {
            chess.PAWN: ["♟"],
            chess.ROOK: ["♜"],
            chess.KNIGHT: ["♞"],
            chess.BISHOP: ["♝"],
            chess.QUEEN: ["♛"],
            chess.KING: ["♚"]
        }
        return piece_unicode.get(piece.piece_type)

class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.parent = parent
        self.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.evaluation_label = tk.Label(self, text="", bg="white", font=("Arial", 14))
        self.evaluation_label.pack(pady=10)

    def update_evaluation(self, evaluation):
        if evaluation.is_mate():
            if evaluation.mate() > 0:
                text = f"White is winning in {evaluation.mate()} moves."
            else:
                text = f"Black is winning in {abs(evaluation.mate())} moves."
        else:
            text = f"The evaluation is: {evaluation.score()}."

        self.evaluation_label.config(text=text)

if __name__ == "__main__":
    engine_path = "C:\\Users\\jibreal\\Downloads\\stockfish-windows-x86-64-avx2 (1)\\stockfish\\stockfish.exe"
    depth = 10
    app = ChessboardGUI(engine_path, depth)
    app.mainloop()

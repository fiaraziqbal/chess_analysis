import chess
import chess.pgn
import chess.engine

def analyze_game(pgn_path, stockfish_path, depth=20):
    # Load the Stockfish engine
    stockfish = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    # Read the PGN file
    with open(pgn_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # End of file

            # Skip games with opening moves (first move is not standard start position)
            if game.board().move_stack:
                continue

            print(f"Analyzing game: {game.headers['Event']} - {game.headers['White']} vs {game.headers['Black']}")

            # Initialize board and result for each game
            board = chess.Board()
            result = None

            for move_number, node in enumerate(game.mainline()):
                # Check if the game is over
                if board.is_game_over():
                    result = board.result()
                    break

                try:
                    # Analyze the position with Stockfish
                    result = stockfish.analyse(board, chess.engine.Limit(depth=depth))

                    # Get the best move from the analysis
                    best_move = result.get("pv")[0]

                    # Make sure the best move is legal before applying it to the board
                    if best_move in board.legal_moves:
                        board.push(best_move)
                    else:
                        print("Stockfish suggested an illegal move. Stopping analysis.")
                        break

                    # Check if the game is over after applying the best move
                    if board.is_game_over():
                        result = board.result()
                        break

                    # Get the UCI representation of the best move
                    best_move_uci = best_move.uci()

                    # Determine whether it's Black or White's move based on the move number
                    if (move_number + 1) % 2 == 0:
                        print(f"Move {move_number + 1}: Black's Best Move: {best_move_uci}")
                    else:
                        print(f"Move {move_number + 1}: White's Best Move: {best_move_uci}")

                except ValueError:
                    print("Invalid or corrupted move found. Skipping to the next move.")
                    continue

            # Print the final result of the game
            print(f"\nGame Result: {result}\n")

    # Close the Stockfish engine
    stockfish.quit()

if __name__ == "__main__":
    pgn_file_path = "game.pgn"  # Replace with the actual path to your "game.pgn" file
    stockfish_path = "C:\\Users\\jibreal\\Downloads\\stockfish-windows-x86-64-avx2 (1)\\stockfish\\stockfish.exe"
    analyze_game(pgn_file_path, stockfish_path, depth=20)

import sys
import chess.engine

def evaluate_score(score):
    return score.relative.score() / 100.0

def categorize_move_quality(score):
    if score <= -2.0:
        return "Blunder"
    elif score <= -1.0:
        return "Mistake"
    elif score <= -0.5:
        return "Inaccuracy"
    elif score >= 3.0:
        return "Brilliant"
    elif score >= 1.0:
        return "Excellent"
    elif score >= 0.5:
        return "Good"
    else:
        return "Neutral"

def analyze_game(fen):
    stockfish_path = "C:\\Users\\jibreal\\Downloads\\stockfish-windows-x86-64-avx2 (1)\\stockfish\\stockfish.exe"
    stockfish = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    board = chess.Board(fen)
    result = stockfish.analyse(board, chess.engine.Limit(depth=20))
    best_move_san = board.san(result.get("pv")[0])
    evaluation = evaluate_score(result.get("score"))
    move_quality = categorize_move_quality(evaluation)

    stockfish.quit()
    return best_move_san, evaluation, move_quality

if __name__ == "__main__":
    fen_position = sys.argv[1] if len(sys.argv) > 1 else None
    if fen_position:
        best_move_san, evaluation, move_quality = analyze_game(fen_position)
        print(f"Best Move: {best_move_san}")
        print(f"Evaluation: {evaluation:.1f}")
        print(f"Move Quality: {move_quality}")

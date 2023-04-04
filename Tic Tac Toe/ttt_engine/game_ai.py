from math import inf
from typing import TypeAlias

from .grid import Coordinate
from .state_data import GameState

Board: TypeAlias = 'Board'

DRAW = 0
MAXIMIZER_WIN = 1
MINIMIZER_WIN = -1


def minmax(minmax_board: Board, maximizing: bool = True, evaluating: bool = False):
    """ Minmax AI for Tic Tac Toe

    It uses the MinMax Algorithm to either get the best move
    or the current evaluation of the position with best play by both sides

    Parameters
    ----------
        minmax_board : Board
            A copy of the original board
        maximizing : bool
            Maximizing or the Minimizing player in the minmax algorithm
        evaluating : bool
            When evaluating is True, returns the evaluation of the position
            When evaluating is False, returns the best move on the board """

    min_eval = inf
    max_eval = -inf
    best_move: Coordinate | None = None

    # BASE CASES
    game_state = minmax_board.state_checker.check_state(minmax_board.get_previous_mark(), update_win_data=False)
    if game_state == GameState.WIN:
        if evaluating:
            # If current player is the maximizing player then it means the other player played the winning move
            # Hence it returns MINIMIZER_WIN as eval, and vice versa
            return MINIMIZER_WIN if maximizing else MAXIMIZER_WIN
        else:
            return best_move
    if game_state == GameState.DRAW:
        return DRAW if evaluating else None

    # MINMAX ALGORITHM
    for move in minmax_board.grid.get_legal_moves():
        evaluation = evaluate(minmax_board, move, not maximizing)
        if maximizing:
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            if max_eval == MAXIMIZER_WIN:
                return max_eval if evaluating else best_move
        else:
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            if min_eval == MINIMIZER_WIN:
                return min_eval if evaluating else best_move

    if evaluating:
        return max_eval if maximizing else min_eval
    return best_move


def evaluate(board: Board, move: Coordinate, maximizing: bool):
    """Evaluates the move and returns the evaluation
    Parameters
    ----------
        board : Board
            board object to make a move on, must be a copy to prevent changing data of the actual board
        move : Coordinate
            coordinates (row, column) of the move to evaluate
        maximizing : bool
            boolean to tell to evaluate from the maximizing size or the minimizing side"""

    board.play_move(move[0], move[1])
    evaluation = minmax(board, maximizing, evaluating=True)
    board.play_move(move[0], move[1], unplay=True)
    return evaluation

import Othello_Core as core
import random
import math
from Othello_Core import *
#from coreSubclass import coreSubclass as player2

import os, signal
import time
from multiprocessing import Process, Value
time_limit=5

BLACK = core.BLACK
WHITE = core.WHITE
SQUARE_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

class Strategy(core.OthelloCore):  # extending Othello Core

    def is_valid(self, move):
        """Is move a square on the board?"""
        return isinstance(move, int) and move in self.squares()

    def opponent(self, player):
        """Get player's opponent piece."""
        return core.BLACK if player == core.WHITE else core.WHITE

    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        Returns the index of the bracketing square if found
        """
        square += direction
        if board[square] == player:
            return None
        opp = self.opponent(player)
        while board[square] == opp:
            square += direction
        return None if board[square] in (core.OUTER, core.EMPTY) else square
        """c = 0
        while True:
            square += direction
            if board[square] == core.OUTER or board[square] == player:
                return None
            if board[square] == self.opponent(player):
                c += 1
            if board[square] == core.EMPTY and c > 0:
                return square
            else: return None"""

    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        # looks in all directions to see if there is a bracket
        hasbracket = lambda direction: self.find_bracket(move, player, board, direction) #anon function
        return board[move] == core.EMPTY and any(map(hasbracket, core.DIRECTIONS)) #checks bracket in every direction
        """for direction in core.DIRECTIONS:
            bracket = self.find_bracket(move, player, board, direction)
            if bracket != None: return True
        return False"""

    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    def make_move(self, move, player, board):
        """Update the board to reflect the move by the specified player."""
        board[move] = player
        for d in core.DIRECTIONS:
            self.make_flips(move, player, board, d)
        return board

    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        bracket = self.find_bracket(move, player, board, direction)
        if not bracket:
            return
        move += direction
        while move != bracket:
            board[move] = player
            move += direction

        """move += direction
        if (board[move] == player or board[move] == core.EMPTY or board[move] == core.OUTER):
            return board  # as is
        while (board[move] != player):
            board[move] = player
            move += direction
        return board"""

    def legal_moves(self, player, board):
        """Get a list of all legal moves for player, as a list of integers"""
        x=[sq for sq in self.squares() if self.is_legal(sq, player, board)]
        random.shuffle(x)
        return x
        """moves = set()
        squares = self.squares()
        for s in squares:
            if board[s] == player:
                for d in core.DIRECTIONS:
                    m = self.find_bracket(s, player, board, d)
                    if m != None: moves.add(m)
        legal_moves = list(moves)
        return legal_moves"""
#####################################
    def terminal_test(self, board):
        if not self.any_legal_move(core.WHITE, board) and not self.any_legal_move(core.BLACK, board):
            score_black = self.score(core.BLACK, board)
            score_white = self.score(core.WHITE, board)
            return score_black if score_black > score_white else score_white
        return False

    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
        return any(self.is_legal(sq, player, board) for sq in self.squares())
        """legal_moves = self.legal_moves(player, board)
        return True if legal_moves else False"""

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        opp = self.opponent(prev_player)
        if self.any_legal_move(opp, board):
            return opp
        elif self.any_legal_move(prev_player, board):
            return prev_player
        return None

    def weighted_score(self, player, board):
        #
        def strategy(player, board):
            opp = self.opponent(player)
            total = 0
            for sq in self.squares():
                if board[sq] == player:
                    total += SQUARE_WEIGHTS[sq]
                elif board[sq] == opp:
                    total -= SQUARE_WEIGHTS[sq]
            return total

        return strategy

    def score(self, player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        player_count = 0
        opp_count = 0
        opponent = self.opponent(player)
        for s in self.squares():
            if board[s] == player:
                player_count += 1
            elif board[s] == opponent:
                opp_count += 1
        return player_count - opp_count

    def my_random(self):
        def strategy(player, board):
            if self.any_legal_move(player, board):
                return random.choice(self.legal_moves(player, board))
            return None

        return strategy

    def final_value(self, player, board):
        #
        diff = self.score(player, board)
        if diff < 0:
            return MIN_VALUE
        elif diff > 0:
            return MAX_VALUE
        return diff

    def maximizer(self, evaluate):
        #
        def strategy(player, board):
            #
            def score_move(move):
                return evaluate(player, self.make_move(move, player, list(board)))
            if self.any_legal_move(player, board):
                return max(self.legal_moves(player, board), key=score_move)
        return strategy
    #negamax implementation of alpha beta
    def alphabeta(self, player, board, alpha, beta, depth, evaluate):
        if depth == 0 and self.any_legal_move(player, board):
            return evaluate(player, board), None

        def value(board, alpha, beta):
            return -self.alphabeta(self.opponent(player), board, -beta, -alpha, depth - 1, evaluate)[0]

        moves = self.legal_moves(player, board)
        if not moves:
            if not self.any_legal_move(self.opponent(player), board):
                return self.final_value(player, board), None
            return value(board, alpha, beta), None

        best_move = moves[0]
        for move in moves:
            if alpha >= beta:
                break
            val = value(self.make_move(move, player, list(board)), alpha, beta)
            if val > alpha:
                alpha = val
                best_move = move
        return alpha, best_move #board

    def alphabeta_searcher(self, depth, evaluate):
        def strategy(player, board):
            return self.alphabeta(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate)[1]

        return strategy

    def get_move(self, strategy, player, board):
        #
        copy = list(board)  # copy the board to prevent cheating
        move = strategy(player, copy)
        if not self.is_valid(move) or not self.is_legal(move, player, board):
            raise OthelloCore.IllegalMoveError(player, move, copy)
        return move

    def best_strategy(self,board,player, best_move, still_running):
        while (still_running.value > 0 and best_move.value < 1000):
            time.sleep(1)
            best_move.value= self.alphabeta(player, board, MIN_VALUE, MAX_VALUE, 4, self.maximizer(self.weighted_score(player, board)))[1]






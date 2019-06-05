from Othello_Core import OthelloCore as superClass
import Othello_Core as core
import random
import os, signal
from time import time
#import time
from multiprocessing import Process, Value
time_limit = 5
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
visited = dict([])
def f(name):
    print('hello ', name)

class Strategy(superClass):
    def print_hello():
        print("hello")
    def f2(self, name):
        print('hello ', name)
    def best_strategy(self, board, player, best_move, still_running):
        #playerPiece = core.BLACK
        #if player == "WHITE":
            #playerPiece = core.WHITE
    #while(still_running.value > 0):
        #time.sleep(1)
        #print("hi")
        #print(playerPiece)
        while board[best_move.value]!=core.EMPTY:
            best_move.value += 1
        while(still_running.value > 0):
        #startTime = time()
            self.alpha_beta_search(6, board, player, best_move)
        #endTime = time()
        #print(endTime - startTime)
    def strategy_1(self, board, player):
        possibleMoves = self.legal_moves(player, board)
        random.shuffle(possibleMoves)
        return possibleMoves.pop()
        #self.make_move(move, player, board)
    def strategy_2(self, maxDepth):
        def strategy(board, player):
            return self.alpha_beta_search(maxDepth, board, player)
        return strategy
    def alpha_beta_search(self, maxDepth, board, player, best_move):
        """returns the best possible move"""
        """j refers to the list where j[0] = score and j[1] = move"""
        start = time()
        #playerPiece = core.BLACK
        #if player == "BLACK":
            #print("hi")
            #playerPiece = core.WHITE
        self.max_value(board, -1*float("inf"), float("inf"), player, 0, maxDepth, best_move)
        endTime = time()
        #print(endTime - start)
        #sort by square weights
        #how many flips each move will make
        #change the scoring matrix
        #dictionary
        #time limits
        #return j[1]
    def max_value(self, board, alpha, beta, player, depth, maxDepth, best_move): #good depth 3
        mySuccessors = self.legal_moves(player, board)
        #oppSuccessors = self.legal_moves(self.opponent(player), board)
        """ if at the terminal case [can't make any more moves] or reached max depth, just return the score """
        if len(mySuccessors)==0 or depth == maxDepth:
            #print(depth)
            return self.score(player, board)
        # if player has to pass, then just return the score
        #if len(mySuccessors)==0:
            #return self.score(player, board), None
        """ if my player can make a move """
        v = -1*float("inf")
        #m = -1
        """ successors are possible moves """
        #random.shuffle(mySuccessors)
        """ sorts the successors so that it chooses the best move first """
        mySuccessors.sort(key = lambda x: SQUARE_WEIGHTS[x], reverse = True)
        for move in mySuccessors:
            #temp_move = Value("i", move)
            
            succBoard = self.make_move(move, player, board.copy())
            #print("1", self.print_board(succBoard))
            #succBoard = self.make_move(move, player, board)
            #v = self.score(player, succBoard)
            """ checks to see if board and player have already been visited """
            if (player, str(succBoard)) in visited:
                v = visited[(player, str(succBoard))]
            else:
                v = self.score(player, succBoard)
                visited[(player, str(succBoard))] = v
                #print("hi")
            v = max(v, self.min_value(succBoard, alpha, beta, self.opponent(player), depth+1, maxDepth))
            """ pruning nodes if v >= upper bound """
            if v >= beta:
                #print(v)
                best_move.value = move
                #if depth==0:
                    #print("Alpha", alpha, "Beta", beta, "Value", v, "Move", move, "Best Move", best_move.value)
                #print("Move", move)
                #print("Depth", depth, "When v >= beta", best_move.value)
                return v
            """ sees if alpha has been changed, if so update move """
            alpha = max(alpha, v)
            if alpha == v:
                best_move.value = move
                #print("Depth", depth,"When alpha == v", best_move.value)
                #best_move = move
            #if depth==0:
                #print("Alpha", alpha, "Beta", beta, "Value", v, "Move", move, "Best Move", best_move.value)
            #print(best_move.value)
        return v
        #for a, s in successors of the current state:
            # v = max(v, self.min_value(board, alpha, beta)[0])
            # if v >= beta:
                #return v, None
            # alpha = max(alpha, v)
            # if alpha == v:
                # m = s
        # return v, m
    def min_value(self, board, alpha, beta, player, depth, maxDepth):
        mySuccessors = self.legal_moves(player, board)
        #oppSuccessors = self.legal_moves(self.opponent(player), board)
        """ if no more moves or reached max depth, just return the score """
        if len(mySuccessors)==0 or depth == maxDepth:
            #print(depth)
            return self.score(player, board)
        # if player has to pass, then just return the score
        #and len(oppSuccessors)==0
        #if len(mySuccessors)==0:
            #return self.score(player, board), None
        """ if my player can make a move """
        v = float("inf")
        m = -1
        #successors are possibly just the moves?
        #random.shuffle(mySuccessors)
        """ sorts, so that the worst move for opponent is chosen first """
        mySuccessors.sort(key = lambda x: SQUARE_WEIGHTS[x])
        for move in mySuccessors:
            #temp_move = Value("i", move)
            succBoard = self.make_move(move, player, board.copy())
            #print("Min ", self.print_board(succBoard))
            #v = self.score(player, succBoard)
            """ checks to see if board and player have already been visited """
            if (player, str(succBoard)) in visited:
                #print("hi")
                v = visited[(player, str(succBoard))]
            else:
                v = self.score(player, succBoard)
                visited[(player, str(succBoard))] = v
                #print("hi")
            """ pruning nodes if v <= lower bound """
            temp_best_move = Value("i", 0)
            v = min(v, self.max_value(succBoard, alpha, beta, self.opponent(player), depth+1, maxDepth, temp_best_move))
            if v <= alpha:
                #print(v)
                return v
            beta = min(beta, v)
            #if beta == v:
                #m = move
        return v#, m
        # for a, s in successors of the current state:
            # v = min(v, self.max_value(board, alpha, beta)[0])
            # if v <= alpha:
                #return v, None
            # beta = min(beta, v)
            # if beta == v:
                # m = s
        # return v, m
    def is_valid(self, move):
        """Is move a square on the board?"""
        return move > 10 and move < 89

    def opponent(self, player):
        """Get player's opponent piece."""
        # player = core.BLACK (can do this for any static var)
        if player == core.BLACK:
            return core.WHITE
        else:
            return core.BLACK
    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        Returns the index of the bracketing square if found
        """
        curr = square+ direction
        opp = self.opponent(player)
        if(board[curr]!=opp):
            return None
        while(self.is_valid(curr) and board[curr]==opp):
            curr+=direction
        if(self.is_valid(curr) and board[curr] == player):
            return curr
        return None
    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        if(self.is_valid(move)==False):
            return False
        if(board[move]!=core.EMPTY):
            return False
        return True

    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    def make_move(self, move, player, board):
        """Update the board to reflect the move by the specified player."""
        #nBoard = board.copy()
        board[move] = player
        for d in core.DIRECTIONS:
            if self.find_bracket(move, player, board, d)!=None:
                self.make_flips(move, player, board, d)
        return board
    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        curr = move + direction
        opp = self.opponent(player)
        while(board[curr]==opp):
            board[curr] = player
            curr += direction
        #return board
    def legal_moves(self, player, board):
        """Get a list of all legal moves for player, as a list of integers"""
        #go through the whole board and check whether the piece is on the board or not
        #num/row size - num%col == num2/row size - num@%col
        #num/row size + num%col
        moves = list()
        opp = self.opponent(player)
        #print(board)
        for i in self.squares():
            if board[i] == core.EMPTY:
                for d in core.DIRECTIONS:
                    endPt = self.find_bracket(i, player, board, d)
                    if endPt!= None:
                        moves.append(i)
                        break

        return moves
    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
        moves = self.legal_moves(player, board)
        #print(moves)
        return len(moves)!=0
    def next_player(self,board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        opp = self.opponent(prev_player)
        isOpp = self.any_legal_move(opp, board)
        isPrev = self.any_legal_move(prev_player, board)
        if(isOpp==False and isPrev==False):
            return None
        elif(isOpp == False and isPrev == True):
            return prev_player
        else:
            return opp
    def score(self,player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        numPlayer = 0
        numOpp = 0
        for i in self.squares():
            if board[i] == player:
                numPlayer+= SQUARE_WEIGHTS[i]
            else:
                numOpp+=SQUARE_WEIGHTS[i]
        return numPlayer-numOpp
    def score2(self,player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        numPlayer = 0
        numOpp = 0
        for i in self.squares():
            if board[i] == player:
                numPlayer+= 1
            else:
                numOpp+=1
        return numPlayer-numOpp
    def terminal_test(self, board):
        """Determine which player won or TIED"""
        blackScore = board.count(core.BLACK)
        whiteScore = board.count(core.WHITE)
        if blackScore > whiteScore:
            return core.PLAYERS[core.BLACK]
        elif blackScore < whiteScore:
            return core.PLAYERS[core.WHITE]
        else:
            return "TIE"
    #server = my_strategy()
    #print("hi")
    #while(still_running.value > 0 and best_move.value<1000):
    #    time.sleep(1)
    #    playerPiece = core.BLACK
    #    if player == "WHITE":
    #        playerPiece = core.WHITE
    #    best_move.value = server.alpha_beta_search(7, board, playerPiece)

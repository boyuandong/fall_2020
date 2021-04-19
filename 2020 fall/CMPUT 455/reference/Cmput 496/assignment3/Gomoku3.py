#!/usr/bin/python3
#/usr/local/bin/python3
# Set the path to your python3 above
import re
import random

from simple_board import SimpleGoBoard
from gtp_connection import GtpConnection
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, PASS, \
                       MAXSIZE, coord_to_point


class SimulationPlayer():
    def __init__(self, numSimulations=10):
        self.numSimulations = numSimulations
        self.type = ""


    def name(self):
        return "Simulation Player ({0} sim.)".format(self.numSimulations)

    def genmove(self, state):
        assert not state.endOfGame()
        moves = state.legalMoves()
        numMoves = len(moves)
        score = [0] * numMoves
        for i in range(numMoves):
            move = moves[i]
            score[i] = self.simulate(state, move)
        #print(score)
        bestIndex = score.index(max(score))
        best = moves[bestIndex]
        #print("Best move:", best, "score", score[best])
        assert best in state.legalMoves()
        return best



    def simulate(self,board,move):
        stats = [0] * 3
        board.play_move_gomoku2(move,board.current_player)
        moveNr = len(board.move)
        
        for _ in range(self.numSimulations):
            winner, _ = self.simulate_random(board)
            stats[winner] += 1
            self.resetToMoveNumber(board,moveNr)
        
        assert sum(stats) == self.numSimulations
        assert moveNr == len(board.move)
        self.undoMove(board)
        eval = (stats[BLACK] + 0.5 * stats[EMPTY]) / self.numSimulations
        if board.current_player == WHITE:
            eval = 1 - eval
        return eval

    def simulate_rule(self,board,move):
        currentplayer = board.current_player
        opponent = GoBoardUtil.opponent(board.current_player)
        board.play_move_gomoku2(move,board.current_player)

        if self.endofGame(board) and board.check_game_end_gomoku()[1] != None:
            self.type = "Win"
            self.undoMove(board)
            return 10000


        else:

            direction = [ -board.NS, -1, -board.NS-1, -board.NS+1, board.NS-1, board.NS+1, 1, board.NS]
            directionofopponent=self.check(board,move,opponent)

            for k in range(4):
                if (directionofopponent[k][0] + directionofopponent[7-k][0]>=4):
                    self.undoMove(board)
                    return 8000

            directionofcurrent = self.check(board,move,currentplayer)
            for k in range(4):
                if (directionofcurrent[k][0]+directionofcurrent[7-k][0]==3) and ((directionofcurrent[k][1]) == True) and (directionofcurrent[7-k][1] == True):
                    self.undoMove(board)
                    return 6000
            for k in range(8):
                if (directionofopponent[k][0] == 3) and (directionofopponent[k][1] == True):
                    self.undoMove(board)
                    return 4000
                elif (directionofopponent[k][0] + directionofopponent[7 - k][0] == 3) and (directionofopponent[k][1] == True) and (
                        directionofopponent[7 - k][1] == True):
                    self.undoMove(board)
                    return 4000

            for i in range(8):
                oppo_points = 0
                empty_points = 0
                pos = move + direction[i]
                if (pos < board.maxpoint) and (board.board[pos] == EMPTY):
                    pos += direction[i]
                    while (pos < board.maxpoint) and (board.board[pos] != BORDER) and (board.board[pos] == opponent):
                        oppo_points += 1
                        pos += direction[i]
                    while (pos < board.maxpoint) and (board.board[pos] != BORDER) and (board.board[pos] == EMPTY):
                        empty_points += 1
                        pos += direction[i]
                    if (oppo_points == 3 and empty_points == 1):
                        self.undoMove(board)
                        return 4000
                elif (pos + 4 * direction[i] < board.maxpoint) and (board.board[pos] == opponent):
                    if (board.board[pos + 3 * direction[i]] == opponent) and (board.board[pos + 4 * direction[i]] == EMPTY):
                        if ((board.board[pos + direction[i]] == opponent) and (
                                board.board[pos + 2 * direction[i]] == EMPTY)) or (
                                (board.board[pos + direction[i]] == EMPTY) and (
                                board.board[pos + 2 * direction[i]] == opponent)):
                            self.undoMove(board)
                            return 4000


            self.undoMove(board)
            return 2000


    def simulate_random(self,board):
        i = 0
        if not self.endofGame(board):
            moves = GoBoardUtil.generate_legal_moves_gomoku(board)
            
            random.shuffle(moves)
            

            while not self.endofGame(board):
                board.play_move_gomoku2(moves[i],board.current_player)
                
                i += 1
        return self.winner(board), i

    def endofGame(self,board):
        return(len(board.move)==board.size*board.size or self.winner(board) != EMPTY )
    
    def winner(self,board):
        if board.check_game_end_gomoku()[1] == BLACK:
            return BLACK
        if board.check_game_end_gomoku()[1] == WHITE:
            return WHITE
        return EMPTY



    def resetToMoveNumber(self,board,moveNr):
        numUndos = len(board.move) - moveNr
        assert numUndos >= 0
        for _ in range (numUndos):
            self.undoMove(board)
        assert len(board.move) == moveNr

    def undoMove(self,board):
        location = board.move.pop()
        board.board[location] = EMPTY
        board.current_player = GoBoardUtil.opponent(board.current_player)

    def check(self, board, move, player):
        direction = [ -board.NS, -1, -board.NS-1, -board.NS+1, board.NS-1, board.NS+1, 1, board.NS]
        dir_cur = [[0, False], [0, False], [0, False], [0, False], [0, False], [0, False], [0, False], [0, False]]
        for i in range(8):
            pos = move + direction[i]
            while (pos < board.maxpoint) and (board.board[pos] != BORDER) and (board.board[pos] == player):
                dir_cur[i][0] += 1
                pos += direction[i]
            if (pos < board.maxpoint) and (board.board[pos] != BORDER) and (board.board[pos] == EMPTY):
                dir_cur[i][1] = True
        return dir_cur


        
class Gomoku():
    def __init__(self):
        """

        Gomoku player that selects moves randomly 
        from the set of legal moves.
        Passe/resigns only at the end of game.

        """
        self.name = "GomokuAssignment3"
        self.version = 1.0
        
    def get_move(self, board, color):
        return GoBoardUtil.generate_random_move_gomoku(board)

def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    s = SimulationPlayer()
    con = GtpConnection(Gomoku(),board,s)
    con.start_connection()

if __name__=='__main__':
    run()


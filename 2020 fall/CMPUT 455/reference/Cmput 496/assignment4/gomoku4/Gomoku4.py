#!/usr/bin/env python
#/usr/local/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil, EMPTY
from simple_board import SimpleGoBoard

import random
import numpy as np

def undo(board,move):
    board.board[move]=EMPTY
    board.current_player=GoBoardUtil.opponent(board.current_player)

def play_move(board, move, color):
    board.play_move_gomoku(move, color)

def game_result(board):
    game_end, winner = board.check_game_end_gomoku()
    moves = board.get_empty_points()
    board_full = (len(moves) == 0)
    if game_end:
        #return 1 if winner == board.current_player else -1
        return winner
    if board_full:
        return 'draw'
    return None

class GomokuSimulationPlayer(object):
    """
    For each move do `n_simualtions_per_move` playouts,
    then select the one with best win-rate.
    playout could be either random or rule_based (i.e., uses pre-defined patterns) 
    """
    def __init__(self, n_simualtions_per_move=10, playout_policy='rule_based', board_size=7):
        assert(playout_policy in ['random', 'rule_based'])
        self.n_simualtions_per_move=n_simualtions_per_move
        self.board_size=board_size
        self.playout_policy=playout_policy

        #NOTE: pattern has preference, later pattern is ignored if an earlier pattern is found
        self.pattern_list=['Win', 'BlockWin', 'OpenFour', 'BlockOpenFour', 'Random', 'maketwo']

        self.name="Gomoku3"
        self.version = 3.0
        self.best_move=None
    
    def set_playout_policy(self, playout_policy='random'):
        assert(playout_policy in ['random', 'rule_based'])
        self.playout_policy=playout_policy

    def _random_moves(self, board, color_to_play):
        return GoBoardUtil.generate_legal_moves_gomoku(board)
    
    def policy_moves(self, board, color_to_play):
        
        assert(self.playout_policy=='rule_based')
        assert(isinstance(board, SimpleGoBoard))
        ret=board.get_pattern_moves()
        
        if len(board.get_empty_points()) == 49:
            return "mid", [36]
        if ret is None:
            return "Random", self._random_moves(board, color_to_play)
        movetype_id, moves=ret
        
        return 0, moves
    
    def _do_playout(self, board, color_to_play):
        
        _ , candidate_moves = self.policy_moves(board, board.current_player)
        
        playout_move=random.choice(candidate_moves)
        
        return playout_move

    def get_move(self, board, color_to_play):
        """
        The genmove function called by gtp_connection
        """
        
        ret=self._do_playout(board, color_to_play)
            
        assert(ret is not None)
        return ret

def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(GomokuSimulationPlayer(), board)
    con.start_connection()

if __name__=='__main__':
    run()

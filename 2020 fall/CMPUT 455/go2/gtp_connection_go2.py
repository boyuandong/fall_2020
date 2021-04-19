"""
gtp_connection_go2.py
Example for extending a GTP engine with extra commands
"""
from gtp_connection import GtpConnection


class GtpConnectionGo2(GtpConnection):
    def __init__(self, go_engine, board, debug_mode=False):
        """
        GTP connection of Go2

        Parameters
        ----------
        go_engine:
            a program that is capable of playing go by reading GTP commands
        board: GoBoard
        """
        GtpConnection.__init__(self, go_engine, board, debug_mode)
        self.commands["board"] = self.board_cmd
        self.argmap["board"] = (0, "Usage: board")

    def board_cmd(self, args):
        """ Print board Command """
        self.respond("Board: " + str(self.board.__dict__))

#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

import unittest
from unittest.mock import patch
import numpy as np
from gtp_connection import GtpConnection
from board_util import BLACK, WHITE, EMPTY, BORDER, PASS, where1d, GoBoardUtil
from board import GoBoard

class MockGoEngine:
    def __init__(self):
        self.name = "Mock"
        self.version = 1.234

    def get_move(self, board, color):
        return board.pt(1, 1)


class GtpConnectionTestCase(unittest.TestCase):
    """Tests for board.py"""

    def test_size_2(self):
        board = GoBoard(2)
        con = GtpConnection(MockGoEngine(), board)


#         con.start_connection()
#     To do: This test does not do much.
#     I started researching how to mock the stdin to put some gtp commands in
#     a string for testing. But I did not find a working solution.
#     We could make GtpConnection take input/output streams as arguments
#     but it makes to code messier.

"""Main"""
if __name__ == "__main__":
    unittest.main()

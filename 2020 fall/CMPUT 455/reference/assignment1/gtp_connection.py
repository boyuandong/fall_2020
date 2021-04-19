"""
gtp_connection.py
Module for playing games of Go using GoTextProtocol

Parts of this code were originally based on the gtp module 
in the Deep-Go project by Isaac Henrion and Amos Storkey 
at the University of Edinburgh.
"""
import traceback
from sys import stdin, stdout, stderr
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, PASS, \
                       MAXSIZE, coord_to_point
import numpy as np
import re
import random

class GtpConnection():

    def __init__(self, go_engine, board, debug_mode = False):
        """
        Manage a GTP connection for a Go-playing engine

        Parameters
        ----------
        go_engine:
            a program that can reply to a set of GTP commandsbelow
        board: 
            Represents the current board state.
        """
        self.next_player = 1
        self._debug_mode = debug_mode
        self.go_engine = go_engine
        self.board = board
        self.commands = {
            "protocol_version": self.protocol_version_cmd,
            "quit": self.quit_cmd,
            "name": self.name_cmd,
            "boardsize": self.boardsize_cmd,
            "showboard": self.showboard_cmd,
            "clear_board": self.clear_board_cmd,
            "komi": self.komi_cmd,
            "version": self.version_cmd,
            "known_command": self.known_command_cmd,
            "genmove": self.genmove_cmd,
            "list_commands": self.list_commands_cmd,
            "play": self.play_cmd,
            "legal_moves": self.legal_moves_cmd,
            "gogui-rules_game_id": self.gogui_rules_game_id_cmd,
            "gogui-rules_board_size": self.gogui_rules_board_size_cmd,
            "gogui-rules_legal_moves": self.gogui_rules_legal_moves_cmd,
            "gogui-rules_side_to_move": self.gogui_rules_side_to_move_cmd,
            "gogui-rules_board": self.gogui_rules_board_cmd,
            "gogui-rules_final_result": self.gogui_rules_final_result_cmd,
            "gogui-analyze_commands": self.gogui_analyze_cmd
        }

        # used for argument checking
        # values: (required number of arguments, 
        #          error message on argnum failure)
        self.argmap = {
            "boardsize": (1, 'Usage: boardsize INT'),
            "komi": (1, 'Usage: komi FLOAT'),
            "known_command": (1, 'Usage: known_command CMD_NAME'),
            "genmove": (1, 'Usage: genmove {w,b}'),
            "play": (2, 'Usage: play {b,w} MOVE'),
            "legal_moves": (1, 'Usage: legal_moves {w,b}'),
        }
    
    def write(self, data):
        stdout.write(data) 

    def flush(self):
        stdout.flush()

    def start_connection(self):
        """
        Start a GTP connection. 
        This function continuously monitors standard input for commands.
        """
        line = stdin.readline()
        while line:
            self.get_cmd(line)
            line = stdin.readline()

    def get_cmd(self, command):
        """
        Parse command string and execute it
        """
        if len(command.strip(' \r\t')) == 0:
            return
        if command[0] == '#':
            return
        # Strip leading numbers from regression tests
        if command[0].isdigit():
            command = re.sub("^\d+", "", command).lstrip()

        elements = command.split()
        if not elements:
            return
        command_name = elements[0]; args = elements[1:]
        if self.has_arg_error(command_name, len(args)):
            return
        if command_name in self.commands:
            try:
                self.commands[command_name](args)
            except Exception as e:
                self.debug_msg("Error executing command {}\n".format(str(e)))
                self.debug_msg("Stack Trace:\n{}\n".
                               format(traceback.format_exc()))
                raise e
        else:
            self.debug_msg("Unknown command: {}\n".format(command_name))
            self.error('Unknown command')
            stdout.flush()

    def has_arg_error(self, cmd, argnum):
        """
        Verify the number of arguments of cmd.
        argnum is the number of parsed arguments
        """
        if cmd in self.argmap and self.argmap[cmd][0] != argnum:
            self.error(self.argmap[cmd][1])
            return True
        return False

    def debug_msg(self, msg):
        """ Write msg to the debug stream """
        if self._debug_mode:
            stderr.write(msg)
            stderr.flush()

    def error(self, error_msg):
        """ Send error msg to stdout """
        stdout.write('? {}\n\n'.format(error_msg))
        stdout.flush()

    def respond(self, response=''):
        """ Send response to stdout """
        stdout.write('= {}\n\n'.format(response))
        stdout.flush()

    def reset(self, size):
        """
        Reset the board to empty board of given size
        """
        self.board.reset(size)

    def board2d(self):
        return str(GoBoardUtil.get_twoD_board(self.board))
        
    def protocol_version_cmd(self, args):
        """ Return the GTP protocol version being used (always 2) """
        self.respond('2')

    def quit_cmd(self, args):
        """ Quit game and exit the GTP interface """
        self.respond()
        exit()

    def name_cmd(self, args):
        """ Return the name of the Go engine """
        self.respond(self.go_engine.name)

    def version_cmd(self, args):
        """ Return the version of the Go engine """
        self.respond(self.go_engine.version)

    def clear_board_cmd(self, args):
        """ clear the board """
        self.reset(self.board.size)
        self.respond()

    def boardsize_cmd(self, args):
        """
        Reset the game with new boardsize args[0]
        """
        self.reset(int(args[0]))
        self.respond()

    """
    ==========================================================================
    Assignment 1 - game-specific commands start here
    ==========================================================================
    """

    def gogui_analyze_cmd(self, args):
        """ We already implemented this function for Assignment 1 """
        self.respond("pstring/Legal Moves For ToPlay/gogui-rules_legal_moves\n"
                     "pstring/Side to Play/gogui-rules_side_to_move\n"
                     "pstring/Final Result/gogui-rules_final_result\n"
                     "pstring/Board Size/gogui-rules_board_size\n"
                     "pstring/Rules GameID/gogui-rules_game_id\n"
                     "pstring/Show Board/gogui-rules_board\n"
                     )

    def gogui_rules_game_id_cmd(self, args):
        """ We already implemented this function for Assignment 1 """
        self.respond("NoGo")

    def gogui_rules_board_size_cmd(self, args):
        """ We already implemented this function for Assignment 1 """
        self.respond(str(self.board.size))

    def gogui_rules_legal_moves_cmd(self,args):
        legal_list=self.generate_gogui_legal_moves(args)
        my_moves = ' '.join(sorted(legal_list)) 
        self.respond(my_moves)

    def generate_gogui_legal_moves(self,args):
        """ 
        We create a new function to generate legal moves,
        return a list that contains all possible legal moves
        """
        legal_list = []
        board_size = self.board.size
        end_point = board_size+1

        temp_color = self.board.current_player 
        if temp_color == BLACK:
            color = "b"
        else:
            color = "w"

        color = color_to_int(color)
        alpha_list = ["A", "B", "C", "D", "E", "F", "G","H","J","K","L",
                "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        
        for i in range (1, end_point):
            for j in range (1, end_point):
                whole_arg = []
                str_j = str(j)
                coord = alpha_list[i-1] + str_j
                whole_arg.append(color)
                whole_arg.append(coord)
                temp_coord = move_to_coord(coord, self.board.size)
                move = coord_to_point(temp_coord[0],temp_coord[1], self.board.size)
                # 1 is for valid play_move
                # -4 for occupied, -5 for capture, -6 for sucide
                if self.board.play_move(move, color, 'not play') == 1:
                    legal_list.append(coord)
        return legal_list

    def gogui_rules_side_to_move_cmd(self, args):
        """ We already implemented this function for Assignment 1 """
        color = "black" if self.board.current_player == BLACK else "white"
        self.respond(color)

    def gogui_rules_board_cmd(self, args):
        """ We already implemented this function for Assignment 1 """
        size = self.board.size
        str = ''
        for row in range(size-1, -1, -1):
            start = self.board.row_start(row + 1)
            for i in range(size):
                #str += '.'
                point = self.board.board[start + i]
                if point == BLACK:
                    str += 'X'
                elif point == WHITE:
                    str += 'O'
                elif point == EMPTY:
                    str += '.'
                else:
                    assert False
            str += '\n'
        self.respond(str)
            
    def gogui_rules_final_result_cmd(self, args):
        """ 
        Implement this function for Assignment 1 
        There is no draw in NoGo
        """
        b_list=["b"]
        w_list=["w"]
        b_result=self.generate_gogui_legal_moves(b_list)
        w_result=self.generate_gogui_legal_moves(w_list)
       
        if (self.next_player == 1 and len(b_result)==0):
            self.respond("white")
            return
        elif (self.next_player == 2 and len(w_result)==0):
            self.respond("black")
            return 
        else:
            self.respond("unknown")
            return

    def play_cmd(self, args):
        """ 
        Modify this function for Assignment 1
        Play a move, args[1] for given color, args[0] represents {'b','w'}
        """
        board_color_orginal = args[0] 
        board_color = args[0].lower()
        board_move = args[1]

        #check color first, 1 for valid and -1 for invalid
        flag_color = self.check_valid_color(board_color)
        #if color is valid 
        if flag_color ==1:
            color = color_to_int(board_color)
        #if color is not valid, report the error
        else: 
            self.respond("illegal move: \"{}".format(board_color_orginal)+" "+board_move+"\" wrong color")
            return -2
        
        if args[1].lower() == 'pass':
            self.board.current_player = GoBoardUtil.opponent(color)
            self.respond("illegal move: \"{}".format(board_color_orginal)+" "+board_move+"\" wrong coordinate")
            return -2

        
        # check coordiate, 1 for valid and -1 for invalid
        flag_coord = self.check_valid_coord(board_move)
        #if the coordiate is valid
        if flag_coord == 1: 
            coord = move_to_coord(board_move, self.board.size)
            move = coord_to_point(coord[0],coord[1], self.board.size)
        #coordiate is not valid, report the error
        else: 
             self.respond("illegal move: \"{}".format(board_color_orginal)+" "+board_move+"\" wrong coordinate")
             return -2

        # 1 is for valid play_move
        # -4 for occupied, -5 for capture, -6 for sucide
        if self.board.play_move(move, color, 'play') != 1: # same as not self.play_move()
            flag_illegal = self.board.play_move(move, color, 'play')
            if flag_illegal == -4:
                self.respond("illegal move: \"{}".format(board_color_orginal)+" "+board_move+"\" occupied")
                return -2
            elif flag_illegal == -5:
                self.respond("illegal move: \"{}".format(board_color_orginal)+" "+board_move+"\" capture")
                return -2
            elif flag_illegal == -6:
                self.respond("illegal move: \"{}".format(board_color_orginal)+" "+board_move+"\" suicide")
                return -2
        else: 
            self.debug_msg("Move: {}\nBoard:\n{}\n".format(board_move, self.board2d()))
        self.respond()

        #change the next player, used for determing the winner
        if self.next_player == 1:
            self.next_player = 2
        else:
            self.next_player = 1

        return 2

    def check_valid_coord(self,point_str): 
        """
        We create this function to check if the coordinate is valid or not.
        """
        #check the length of the coord, -1 is for thr invalid input
        s = point_str.lower()
        board_size = self.board.size
        if len(s) != 2:
            return -1

        alpha = s[0]
        num = s[1]
        end_point = ord("a") + board_size - 1
        temp_num = int(num)
        #check if the first one of the coord is letter or not and 
        #whether it is within the board size range
        if (not ord("a") <= ord(alpha) <= end_point): 
            return -1
        #check whether the second one of the coord is a intger
        if not num.isdigit(): 
            return -1
        #check whether the second one is within the board size range
        if not (1 <= temp_num <= board_size): 
            return -1

        return 1 

    def check_valid_color(self, board_color):
        """
        We create this function to check if the color is valid or not.
        """
        if (board_color != "w" and board_color != "b"):
            return -1
        return 1                       

    def genmove_cmd(self, args):
        """ 
        Modify this function for Assignment 1 
        generate a move for color args[0] in {'b','w'}
        """
        self_color = args[0].lower()
        self_color1 = color_to_int(self_color)
        valid_list_self = self.generate_gogui_legal_moves(args)
        oppoent_color = []
        if self_color == "w":
            oppoent_color.append("b")
        else:
            oppoent_color.append("w")

        valid_list_opponent = self.generate_gogui_legal_moves(oppoent_color)
        if (len(valid_list_opponent) == 0 or len(valid_list_self) == 0): #end of the game
            self.respond("resign")
            return 
        else:
            board_move = random.choice(valid_list_self)
            coord = move_to_coord(board_move, self.board.size)
            move = coord_to_point(coord[0],coord[1], self.board.size)
            self.board.play_move(move, self_color1, 'play')     

    """
    ==========================================================================
    Assignment 1 - game-specific commands end here
    ==========================================================================
    """

    def showboard_cmd(self, args):
        self.respond('\n' + self.board2d())

    def komi_cmd(self, args):
        """
        Set the engine's komi to args[0]
        """
        self.go_engine.komi = float(args[0])
        self.respond()

    def known_command_cmd(self, args):
        """
        Check if command args[0] is known to the GTP interface
        """
        if args[0] in self.commands:
            self.respond("true")
        else:
            self.respond("false")

    def list_commands_cmd(self, args):
        """ list all supported GTP commands """
        self.respond(' '.join(list(self.commands.keys())))

    """ Assignment 1: ignore this command, implement 
        gogui_rules_legal_moves_cmd  above instead """
    def legal_moves_cmd(self, args):
        """
        List legal moves for color args[0] in {'b','w'}
        """
        board_color = args[0].lower()
        color = color_to_int(board_color)
        moves = GoBoardUtil.generate_legal_moves(self.board, color)
        gtp_moves = []
        for move in moves:
            coords = point_to_coord(move, self.board.size)
            gtp_moves.append(format_point(coords))
        sorted_moves = ' '.join(sorted(gtp_moves))
        self.respond(sorted_moves)


def point_to_coord(point, boardsize):
    """
    Transform point given as board array index 
    to (row, col) coordinate representation.
    Special case: PASS is not transformed
    """
    if point == PASS:
        return PASS
    else:
        NS = boardsize + 1
        return divmod(point, NS)

def format_point(move):
    """
    Return move coordinates as a string such as 'A1', or 'PASS'.
    """
    column_letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    if move == PASS:
        return "PASS"
    row, col = move
    if not 0 <= row < MAXSIZE or not 0 <= col < MAXSIZE:
        raise ValueError
    return column_letters[col - 1]+ str(row) 
    
def move_to_coord(point_str, board_size):
    """
    Convert a string point_str representing a point, as specified by GTP,
    to a pair of coordinates (row, col) in range 1 .. board_size.
    Raises ValueError if point_str is invalid
    """
    '''if not 2 <= board_size <= MAXSIZE:
        raise ValueError("board_size out of range")'''
    if not 2 <= board_size <= MAXSIZE:
        raise ValueError("board_size out of range")
    s = point_str.lower()
    if s == "pass":
        return PASS
    try:
        col_c = s[0]
        if (not "a" <= col_c <= "z") or col_c == "i":
            raise ValueError
        col = ord(col_c) - ord("a")
        if col_c < "i":
            col += 1
        row = int(s[1:])
        if row < 1:
            raise ValueError
    except (IndexError, ValueError):
        raise ValueError("invalid point: '{}'".format(s))
    if not (col <= board_size and row <= board_size):
        raise ValueError("point off board: '{}'".format(s))
    return row, col

def color_to_int(c):
    """convert character to the appropriate integer code"""
    color_to_int = {"b": BLACK , "w": WHITE, "e": EMPTY, 
                    "BORDER": BORDER}
    return color_to_int[c] 

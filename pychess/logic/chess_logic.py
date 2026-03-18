from pychess.main import board
import constants

class MoveInfo:
    def __init__(self):
        """
        Black/White
        Previous Move
        Is the move valid
        Is the move en passant
        Is the move a castle
        """
        self.player = "White"
        self.previous_move = ""
        self.is_valid = False
        self.en_passant = False
        self.castle = False

class ChessLogic:
    def __init__(self):
        """
        Initalize the ChessLogic Object. External fields are board and result

        board -> Two Dimensional List of string Representing the Current State of the Board
            P, R, N, B, Q, K - White Pieces

            p, r, n, b, q, k - Black Pieces

            '' - Empty Square

        result -> The current result of the game
            w - White Win

            b - Black Win

            d - Draw

            '' - Game In Progress
        """
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        self.result = ""
        self.update_move_info_dispatch = {
            "P":self.pawn_move_update,
            "R":self.rook_move_update,
            "N":self.knight_move_update,
            "B":self.bishop_move_update,
            "Q":self.queen_move_update,
            "K":self.king_move_update,
        }
        self.move_info = MoveInfo()
        #todo
        #need to add a ton of things such as previous move, current player, etc

    def update_move_info(self, moving_piece,move):
        self.is_move_valid_dispatch[moving_piece.upper()](move)
       
    def play_en_passant(self, moving_piece,move) -> str:
        start_indices = self.get_board_index(move[0:2])
        end_indices = self.get_board_index(move[2:4])
        captured_pawn_col_offset = 1 if self.move_info.player == "White" else -1
        self.board[start_indices[0]][start_indices[1]] = ""
        self.board[end_indices[0] + captured_pawn_col_offset][end_indices[1]] = moving_piece
        self.board[end_indices[0]][end_indices[1]] = moving_piece


        return move[0:2] + 'x' + move[2:4]
    
    def play_castle(self, moving_piece,move) -> str:
        #We might need to make a castle
        start_indices = self.get_board_index(move[0:2])
        end_indices = self.get_board_index(move[2:4])
        self.board[start_indices[0]][start_indices[1]] = ""
        if move[2] < 'e': # kingside castle
            self.board[start_indices[0]][start_indices[1] - 2] = moving_piece
            self.board[end_indices[0]][end_indices[1] + 1] = self.board[end_indices[0]][end_indices[1]]
            self.board[end_indices[0]][end_indices[1]] = ""
            return "O-O"
        else: # queenside castle
            self.board[start_indices[0]][start_indices[1] + 2] = moving_piece
            self.board[end_indices[0]][end_indices[1] - 1] = self.board[end_indices[0]][end_indices[1]]
            self.board[end_indices[0]][end_indices[1]] = ""
            return "O-O-O"
    
    def play_normal_move(self, moving_piece,move) -> str:
        start_indices =  self.get_board_index(move[0:2])
        end_indices = self.get_board_index(move[2:4])

        notation = moving_piece if moving_piece.upper() == "P" else ""
        notation += move[0:2]

        if self.board[start_indices[0]][start_indices[1]] != "":
            notation += 'x'
        notation += move[2:4]
        #todo Add + if king is in check
        self.board[start_indices[0]][start_indices[1]] = ""
        self.board[end_indices[0]][end_indices[1]] = moving_piece

        if
        return notation
        
    def play_move(self, moving_piece, move) -> str:
        if self.move_info.en_passant:
            self.move_info.en_passant = False
            return self.play_en_passant(moving_piece,move)
        elif self.move_info.castle:
            self.move_info.play_castle = False
            return self.play_castle(moving_piece,move)
        else:
            self.play_normal_move(moving_piece,move)

        return self.move_info.previous_move
        
    def try_move(self, moving_piece,move) -> str:
        self.update_move_info(moving_piece,move)
        if not self.move_info.is_valid:
            return ""
        
        return self.play_move(moving_piece,move)

    def pawn_move_update(self,move:str):
        #hardest one to implement by far.
        #need to check if there are pieces in front of it
        #if en passant is possible
        #if piece is currently pinned to king
        if move[2] != '1' or move[2] != '6'


        return
    
    def queen_move_update(self,move:str):
        #This function can just check if a bishop and rook move is update
        self.rook_move_update(move)
        if not self.move_info.valid_move:
            return
        self.bishop_move_update(move)

    def rook_move_update(self,move:str):
        start_indices = self.get_board_index(move[0:2])
        end_indices = self.get_board_index(move[2:4])

        if start_indices == end_indices:
            self.move_info.is_valid = False
            return
        elif start_indices[0] == end_indices[0]: # same row
            smaller, larger = min(start_indices[1], end_indices[1]), max(start_indices[1], end_indices[1])
            for i in range(smaller + 1, end_indices[1]):
                if self.board[start_indices[0]][start_indices[0]+i] != "":
                    self.move_info.is_valid = False
                    return
        elif start_indices[1] == end_indices[1]: # same col
            smaller, larger = min(start_indices[0], end_indices[0]), max(start_indices[0], end_indices[])
            for i in range(smaller + 1,larger):
                if self.board[start_indices[0] + i][start_indices[i]] != "":
                    self.move_info.is_valid = False
                    return
        else:
            self.move_info.is_valid = False
            return
        self.move_info.is_valid = True
    
    def knight_move_update(self,move:str):
        start_indices = self.get_board_index(move[0:2])
        end_indices = self.get_board_index(move[2:4])

        #Eligible knight moves are always one column and two rows
        # or one row and two columns from the starting square
        #Assuming that the moves are never out of bounds.

        row_diff = abs(start_indices[0] - end_indices[0])
        col_diff = abs(start_indices[1] - end_indices[1])

        if start_indices == end_indices:
            self.move_info.is_valid = False
            return
        elif (row_diff == 1 and col_diff ==2) or (row_diff == 2 and col_diff == 1): #
            self.move_info.is_valid = True
            return
        else:
            self.move_info.is_valid = False
            return

    def bishop_move_update(self,move:str):
        start_indices = self.get_board_index(move[0:2])
        end_indices = self.get_board_index(move[2:4])

        if start_indices == end_indices:
            self.move_info.is_valid = False
            return
        else:
            # pick a direction that makes sense
            start_row, start_col = start_indices
            end_row, end_col = end_indices
            if start_row < end_row and start_col < end_col:
                increment = (1,1)
            elif start_row < end_row and start_col > end_col:
                increment = (1, -1)
            elif start_row > end_row and start_col < end_col:
                increment = (-1, 1)
            else:
                increment = (-1, -1)

            # simulate the traversal that makes most sense
            cur_row, cur_col = start_row, start_col
            while cur_row != end_row and cur_col != end_col:
                cur_row += increment[0]
                cur_col += increment[1]

                # we go out of bounds when input isn't actually diagonal
                if cur_row > BOUND or cur_row < 0 or cur_col > BOUND or cur_col < 0:
                    self.move_info.is_valid = False
                    return

                if self.board[cur_row][cur_col] != "":
                    self.move_info.is_valid = False
                    return

            self.move_info.is_valid = True
            return
        
    def king_move_update(self,move:str):
        # i
        return

    def get_board_index(self,coordinates:str):
        col = (coordinates[0] - ord('a'))
        row = (8 - int(coordinates[1]))
        return row,col

    def stalemated(self) -> bool:
        return False
    
    def checkmated(self) -> bool:
        
        return False
    
    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the board

        Args:
            move (str): The move which is proposed. The format is the following: starting_sqaure}{ending_square}
            
            i.e. e2e4 - This means that whatever piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """

        start_square = move[0:2]
        
        moving_piece = self.board[self.get_board_index(start_square)]
        
        return self.try_move(moving_piece,move)
        
        

        # Sections
        # 	Parsing

        # 	Handling invalid moves
        # 		There's a lot of these.

        # 	Updating board if valid

        # 	Return extended chess notation

        # Bulk of work is seeing move and seeing if its valid or invalid.
        # We just need to check if valid, board update will vary based on move?
        #

        # parse
        # get first piece
        # get second piece
        # see if move is valid
        # if valid
        # 	call update board with positions.
        # 	if castling, swap -- is there any other weird case?
        #
        # 	the only spots updated will always be start and end -> NOT THE CASE IN EN PASSANT
        # 	king will sometimes panic, but thats not a feature of our board.
        # 		should be checked in if move valid

        #    en passant doesnt have the captured piece on the end pos.
        #
        # UPDATE THE BOARD
        # return extended chess notation based on what happened
        # should be handled alongside is valid?
        # just make is_valid return a string
        # 	easyyyyyyyyyy. this string might actually be really useful in the other functions like update board.
        # 	something like g7xh8=Q doesnt tell me if en passant occurred
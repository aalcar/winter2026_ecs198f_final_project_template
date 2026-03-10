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
        
        #todo
        #need to add a ton of things such as previous move, current player, etc
        
    def move_pawn(self,move:str) -> str:
        if not self.pawn_move_valid():
            return ""
        return "notation"

    def pawn_move_valid(self,move:str) -> bool:
        #hardest one to implement by far.
        #need to check if there are pieces in front of it
        #if en passant is possible
        #if piece is currently pinned to king
        return True
    
    def move_queen(self,move:str) -> str:
        if not self.queen_move_valid():
            return
        return "notation"
    
    def queen_move_valid(self,move:str) -> bool:
        #This function can just check if a bishop and rook move is valid
        return True

    def move_rook(self,move:str) -> str:
        if not self.rook_move_valid():
            return 
        return "notation"
    
    def rook_move_valid(self,move:str) -> bool:
        return True
    
    def move_knight(self,move:str) -> str:
        if not self.knight_move_valid():
            return ""
        return "notation"
    
    def knight_move_valid(self,move:str) -> bool:
        return ""
    
    def move_bishop(self,move:str) -> str:
        if not self.bishop_move_valid():
            return ""
        return "notation"
    
    def bishop_move_valid(self,move:str) -> bool:
        return True
    
    def move_king(self,move:str) -> bool:
        if not self.king_move_valid():
            return ""
        return "notation"
        
    def king_move_valid(self,move:str) -> str:
        return True
    
    move_if_valid_dispatch = {
        "P":move_pawn,
        "R":move_rook,
        "N":move_knight,
        "B":move_bishop,
        "Q":move_queen,
        "K":move_king,
    }

    def get_board_index(self,coordinates:str) -> int:
        index = (coordinates[0] - ord('a'))
        index += (8 - int(coordinates[1]))*8
        return index
    
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
        
        #don't think we need this one
        #end_square = move[0:2]
        
        #need to implement the following functions
        
        moving_piece = self.board[self.get_board_index(start_square)].upper()
        
        notation = self.move_if_valid_dispatch[moving_piece](move)
        
        if (self.checkmated()):
            #todo should keep track of whose move it is since it'll save time here
            self.result = "b"
            self.result = "w"
        elif(self.stalemated()):
            self.result =  "d"
        
        return notation

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
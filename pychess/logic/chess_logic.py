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
        self.current_player = "White"
        self.last_move = None # for en passant
        self.pieces_moved = {} # for castling

        # (row, col) -> [validmove1, validmove2, ...]
        self.valid_moves_dict = {} # so checking isnt a pain in the ass

        # i learned that you put an _ (underscore) to signify methods 
        #   that should be private
        self._build_valid_moves() # build valid moves for initial board state

    def is_in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def is_own_piece(self, row: int, col: int) -> bool:
        # Starting a move
        piece = self.board[row][col]

        if piece == "":
            return False
        
        if self.current_player == "White":
            return piece.isupper()
        else:
            return piece.islower()
    
    def is_opp_piece(self, row: int, col: int) -> bool:
        piece = self.board[row][col]

        if piece == "":
            return False
        
        if self.current_player == "White":
            return piece.islower()
        else:
            return piece.isupper()
    
    def get_board_index(self, coordinates: str) -> tuple[int, int]:
        row = 8 - int(coordinates[1])
        col = ord(coordinates[0]) - ord('a')

        return (row, col)
    
    def _build_valid_moves(self):
        # dictionary gets rebuilt here
        self.valid_moves_dict = {}

        for row in range(8):
            for col in range(8):
                if self.is_own_piece(row, col):
                    valid_moves = self._get_valid_moves_for_piece(row, col)
                    if valid_moves:
                        self.valid_moves_dict[(row, col)] = valid_moves

    def _get_valid_moves_for_piece(self, row: int, col: int) -> list:
        piece = self.board[row][col].upper()

        validator = {
            'P': self._get_pawn_moves,
            'N': self._get_knight_moves,
            'R': self._get_rook_moves,
            'B': self._get_bishop_moves,
            'Q': self._get_queen_moves,
            'K': self._get_king_moves,
        }

        return validator[piece](row, col)
    
    def _get_pawn_moves(self, row: int, col: int) -> list:
        # TODO
        return []
    
    def _get_knight_moves(self, row: int, col: int) -> list:
        # Only 8 possible moves a knight can do 
        valid_moves = []
        offsets = [
            (-2, 1), (-1, 2), (1, 2), (2, 1),
            (2, -1), (1, -2), (-1, -2), (-2, -1)
        ]

        for offset in offsets:
            new_row, new_col = row + offset[0], col + offset[1]
            if self.is_in_bounds(new_row, new_col) and not self.is_own_piece(new_row, new_col):
                valid_moves.append((new_row, new_col))

        return valid_moves
    
    def _get_bishop_moves(self, row: int, col: int) -> list:
        # TODO
        return []
    
    def _get_rook_moves(self, row: int, col: int,) -> list:
        # TODO
        return []
    
    def _get_queen_moves(self, row: int, col: int) -> list:
        # TODO
        return []

    def _get_king_moves(self, row: int, col: int) -> list:
        # TODO
        return []

    def play_move(self, move: str) -> str:
        # TODO
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the board

        Args:
            move (str): The move which is proposed. The format is the following: starting_sqaure}{ending_square}
            
            i.e. e2e4 - This means that whatever piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """

        return ""
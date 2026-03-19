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
        self.pieces_moved = { # for castling
            (7, 4): False, # white king
            (7, 0): False, # white queenside rook
            (7, 7): False, # white kingside rook
            (0, 4): False, # black king
            (0, 0): False, # black queenside rook
            (0, 7): False  # black kingside rook
        } 

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
    
    def is_move_promotion(self, moving_piece: str, row: int):
        if moving_piece == "p" and row == 0:
            return True
        elif moving_piece == "P" and row == 7:
            return True
        
        return False

    def is_square_attacked(self, row: int, col: int, by_player: str) -> bool:
        original_player = self.current_player
        self.current_player = by_player

        # can any opposing pieces move to this square
        for piece_row in range(8):
            for piece_col in range(8):
                if self.is_own_piece(piece_row, piece_col):
                    possible_moves = self._get_valid_moves_for_piece(piece_row, piece_col)
                    if (row, col) in possible_moves:
                        self.current_player = original_player
                        return True
                    
        self.current_player = original_player
        return False
    
    def is_king_in_check(self, player: str) -> bool:
        king = "K" if player == "White" else 'k'

        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    opponent = "Black" if player == "White" else "White"
                    return self.is_square_attacked(row, col, opponent)
        
        return False
    
    def update_pieces_moved(self, row: int, col: int):
        if (row, col) in self.pieces_moved:
            self.pieces_moved[(row, col)] = True

    # mimic every possible move to see if there's a way out of check
    def has_legal_move(self, player: str):
        for (start_row, start_col), moves in self.valid_moves_dict.items():
            for (end_row, end_col) in moves:
                original_board = [row[:] for row in self.board]
                piece = self.board[start_row][start_col]
                self.board[start_row][start_col] = ""
                self.board[end_row][end_col] = piece

                still_in_check = self.is_king_in_check(player)

                self.board = original_board

                if not still_in_check:
                    return True
        # no way out of check
        return False
    
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
        valid_moves = []

        # direction changes based on color
        piece = self.board[row][col]
        if piece.isupper():
            direction = -1
            # to determine if pawn is allowed to move 2 spaces
            starting_row = 6
        else:
            direction = 1
            starting_row = 1

        # check 1 forward and 2 forward afterwards
        one_forward = (row + direction ,col)
        if self.is_in_bounds(one_forward[0], one_forward[1]) \
        and self.board[one_forward[0]][one_forward[1]] == "":
            valid_moves.append(one_forward)

            if row == starting_row:
                two_forward = (row + 2 * direction, col)
                # no need check in_bounds bc starting pos is always valid
                if self.board[two_forward[0]][two_forward[1]] == "":
                    valid_moves.append(two_forward)
        
        # captures
        for diagonal in [-1, 1]:
            potential_capture = (row + direction, col + diagonal)
            if self.is_in_bounds(potential_capture[0], potential_capture[1]) \
            and self.is_opp_piece(potential_capture[0], potential_capture[1]):
                valid_moves.append(potential_capture)

        # en passant
        if self.last_move is not None:
            last_start_row, last_start_col, last_end_row, last_end_col = self.last_move
            last_piece = self.board[last_end_row][last_end_col]
            
            if last_piece.lower() == "p" and abs(last_start_row - last_end_row) == 2 \
            and last_end_col in [col - 1, col + 1] \
            and last_end_row == row:
                valid_moves.append((row + direction, last_end_col))

        return valid_moves
    
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
        valid_moves = []
        directions = [(-1 ,1), (1 ,1), (1, -1), (-1, -1)]

        # simulate slide in all directions
        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]

            while self.is_in_bounds(new_row, new_col):
                if self.is_own_piece(new_row, new_col): # want to continue if empty or enemy
                    break

                valid_moves.append((new_row, new_col))

                if self.is_opp_piece(new_row, new_col):
                    break

                new_row += direction[0]
                new_col += direction[1]


        return valid_moves
    
    def _get_rook_moves(self, row: int, col: int) -> list:
        valid_moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # simulate slide in all directions
        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]

            while self.is_in_bounds(new_row, new_col):
                if self.is_own_piece(new_row, new_col): # want to continue if empty or enemy
                    break

                valid_moves.append((new_row, new_col))

                if self.is_opp_piece(new_row, new_col):
                    break

                new_row += direction[0]
                new_col += direction[1]

        return valid_moves
    
    def _get_queen_moves(self, row: int, col: int) -> list:
        return self._get_bishop_moves(row, col) + self._get_rook_moves(row, col)

    def _get_king_moves(self, row: int, col: int) -> list:
        valid_moves = []
        directions = [
            (-1 ,1), (1 ,1), (1, -1), (-1, -1),
            (0, 1), (1, 0), (0, -1), (-1, 0)   
        ]

        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]

            if self.is_in_bounds(new_row, new_col) and not self.is_own_piece(new_row, new_col):
                valid_moves.append((new_row, new_col))

        # castling
        pos = (row, col)
        if pos in self.pieces_moved and not self.pieces_moved[pos]: # castling is available
            # queenside
            if not self.pieces_moved[(row, 0)] \
            and all(self.board[row][c] == "" for c in [1, 2, 3]):
                valid_moves.append((row, 2))
            # kingside
            if not self.pieces_moved[(row, 7)] \
            and all(self.board[row][c] == "" for c in [5, 6]):
                valid_moves.append((row, 6))

        return valid_moves

    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the board

        Args:
            move (str): The move which is proposed. The format is the following: starting_sqaure}{ending_square}
            
            i.e. e2e4 - This means that whatever piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """
        # parsing
        start_pos = move[0:2]
        end_pos = move[2: 4]

        start_row, start_col = self.get_board_index(start_pos)
        end_row, end_col = self.get_board_index(end_pos)

        # start pos never added to dict if there aren't any valid moves from that pos
        if (start_row, start_col) not in self.valid_moves_dict:
            return ""
        
        if (end_row, end_col) not in self.valid_moves_dict[(start_row, start_col)]:
            return ""
        
        # initiate move
        moving_piece = self.board[start_row][start_col]

        is_capture = self.board[end_row][end_col] != ""
        is_castling = moving_piece.lower() == "k" and abs(start_col - end_col) == 2
        is_en_passant = moving_piece.lower() == "p" and is_capture and self.board[end_row][end_col] == ""
        is_promotion = self.is_move_promotion(moving_piece, end_row)

        # save incase move sequence causes our king to be in check
        original_board = [row[:] for row in self.board]

        # update board
        self.board[start_row][start_col] = ""
        self.board[end_row][end_col] = moving_piece

        # castling check here
        if is_castling:
            opponent = "Black" if self.current_player == "White" else "White"

            if end_col > start_col: # kingside
                self.board[start_row][7] = ""
                self.board[start_row][5] = "R" if self.current_player == "White" else "r"
                notation = "0-0"
                if self.is_square_attacked(start_row, 5, opponent):
                    self.board = original_board
                    return ""
            else: # queenside
                self.board[start_row][0] = ""
                self.board[start_row][3] = "R" if self.current_player == "White" else "r"
                notation = "0-0-0"
                if self.is_square_attacked(start_row, 3, opponent) \
                or self.is_square_attacked(start_row, 2, opponent):
                    self.board = original_board
                    return ""

        if is_en_passant:
            # start row is where the opp. pawn is
            is_capture = True
            self.board[start_row][end_col] = ""

        if is_promotion:
            self.board[end_row][end_col] = "Q" if self.current_player == "White" else "q"

        # undo if king in check from this move, invalid move
        if self.is_king_in_check(self.current_player):
            self.board = original_board
            return ""

        # construct notation
        if not is_castling:
            notation = "" if moving_piece.lower() == "p" else f"{moving_piece}"

            if is_capture:
                notation += f"{start_pos}x{end_pos}"
            else:
                notation += f"{start_pos}{end_pos}"
            
            if is_promotion:
                notation += "=Q"
        
        # update properties
        self.update_pieces_moved(start_row, start_col)

        self.last_move = (start_row, start_col, end_row, end_col)
        self.current_player = "Black" if self.current_player == "White" else "White"

        self._build_valid_moves()

        # need to have the valid moves dictionary built to check
        if self.is_king_in_check(self.current_player) and not self.has_legal_move(self.current_player):
            self.result = "w" if self.current_player == "Black" else "b"
        elif not self.is_king_in_check(self.current_player) and not self.has_legal_move(self.current_player):
            self.result = "d"

        return notation

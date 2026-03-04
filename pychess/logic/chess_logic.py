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

    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the board

        Args:
            move (str): The move which is proposed. The format is the following: starting_sqaure}{ending_square}
            
            i.e. e2e4 - This means that whatever piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """

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
        pass
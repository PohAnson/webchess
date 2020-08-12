import copy
from Stack import Stack

class WebInterface:
    def __init__(self):
        self.inputlabel = None
        self.btnlabel = None
        self.errmsg = None
        self.board =None
        self.inputlabel = 'inputlabel'
        self.btnlabel = 'btnlabel'
        self.errmsg = 'errmsg'
        self.board ='board'

class Board:
    '''
    The game board is represented as an 8×8 grid,
    with each position on the grid described as
    a pair of ints (range 0-7): col followed by row

    07  17  27  37  47  57  67  77
    06  16  26  36  46  56  66  76
    05  15  25  35  45  55  65  75
    04  14  24  34  44  54  64  74
    03  13  23  33  43  53  63  73
    02  12  22  32  42  52  62  72
    01  11  21  31  41  51  61  71
    00  10  20  30  40  50  60  70
    '''
    def __init__(self, **kwargs):
        self.position = {}
        if 'debug' in kwargs.keys():
            if kwargs['debug']:
                self.debug = True
            else:
                self.debug = False
        else:
            self.debug = False

    def coords(self, colour=None):
        '''
        Return list of piece coordinates.
        Allows optional filtering by colour
        '''
        if colour == None:
            return self.position.keys()
        else:
            pieces_coords_list = list(self.position.keys())
            found_pieces_coord = []

            for coord in pieces_coords_list:
                piece = self.get_piece(coord)
                if piece.colour == colour:
                    found_pieces_coord.append(coord)
            return found_pieces_coord

        

    def pieces(self, colour=None):
        '''Return list of board pieces.
        Allows optional filtering by colour'''
        if colour == None:
            return list(self.position.values())
        else:
            pieces_list = []
            for pieces in self.position.values():
                if pieces.colour == colour:
                    pieces_list.append(pieces)
            return pieces_list


    def get_piece(self, coord):
        '''
        Return the piece at coord.
        Returns None if no piece at coord.
        '''
        return self.position.get(coord, None)

    def add(self, coord, piece, track=True):
        '''Add a piece at coord.'''
        if track:
            self.movehistory.push(('add', coord, piece))
        self.position[coord] = piece

    def remove(self, coord, track=True):
        '''
        Remove the piece at coord, if any.
        Does nothing if there is no piece at coord.
        '''
        if coord in self.coords():
            if track:
                self.movehistory.push(('remove', coord, self.get_piece(coord)))
            del self.position[coord]

    def move(self, start, end):
        '''
        Move the piece at start to end.
        Validation should be carried out first
        to ensure the move is valid.
        '''
        piece = self.get_piece(start)
        piece.moved = True
        self.remove(start)
        self.add(end, piece)

    def start(self):
        '''
        Set up the pieces and start the game. Create CSV file movelog_file.
        '''
        self.movehistory = Stack()
        colour = 'black'
        self.add((0, 7), Rook(colour))
        self.add((1, 7), Knight(colour))
        self.add((2, 7), Bishop(colour))
        self.add((3, 7), Queen(colour))
        self.add((4, 7), King(colour))
        self.add((5, 7), Bishop(colour))
        self.add((6, 7), Knight(colour))
        self.add((7, 7), Rook(colour))
        for x in range(0, 8):
            self.add((x, 6), Pawn(colour))

        colour = 'white'
        self.add((0, 0), Rook(colour))
        self.add((1, 0), Knight(colour))
        self.add((2, 0), Bishop(colour))
        self.add((3, 0), Queen(colour))
        self.add((4, 0), King(colour))
        self.add((5, 0), Bishop(colour))
        self.add((6, 0), Knight(colour))
        self.add((7, 0), Rook(colour))
        for x in range(0, 8):
            self.add((x, 1), Pawn(colour))
        self.turn = 'white'
        self.winner = None
        f = open('movelog_file', 'w')
        f.close()

    def display(self):
        '''
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        '''
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order
        # Row 8 is for column labels, Column -1 is for Row labels
        for row in range(8, -1, -1):
            for col in range(-1, 8):
                coord = (col, row)  # tuple
                if coord in self.coords():
                    piece = self.get_piece(coord)
                    print(f'{piece.symbol()}', end='')
                elif row == 8:
                    if col == -1:
                        print(' ', end='')
                    else:
                        print(f'{col}', end='')
                elif col == -1:
                    print(f'{row}', end='')
                else:
                    piece = None
                    print(' ', end='')
                if col == 7:     # Put line break at the end
                    print('')
                else:            # Print a space between pieces
                    print(' ', end='')

    def prompt(self):
        '''
        Input format should be two ints,
        followed by a space,
        then another 2 ints
        e.g. 07 27
        '''
        def valid_format(inputstr):
            '''
            Ensure input is 5 characters: 2 numerals,
            followed by a space,
            followed by 2 numerals
            '''
            return len(inputstr) == 5 and inputstr[2] == ' ' \
                and inputstr[0:1].isdigit() \
                and inputstr[3:4].isdigit()

        def valid_num(inputstr):
            '''Ensure all inputted numerals are 0-7.'''
            for char in (inputstr[0:1] + inputstr[3:4]):
                if char not in '01234567':
                    return False
            return True

        def split_and_convert(inputstr):
            '''Convert 5-char inputstr into start and end tuples.'''
            start, end = inputstr.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            return (start, end)

        def printmove(start, end):
            '''Print the player\'s move'''
            if self.castling(start, end):
                return f'{self.turn} castling.'
            else:
                a, b = start
                c, d = end
                movedpiece = str(self.get_piece(start))
                return f'{movedpiece} {a}{b} -> {c}{d}'

        def movelog(start, end):
            '''
            Save all moves made into the CSV file movelog_file
            '''
            with open('movelog_file', 'a') as f:
                f.write(f'\n{printmove(start, end)}')

        while True:
            if self.debug:
                print("\nBefore prompting", end='')
            if self.check(self.turn):
                print(f"{self.turn} king is in check")
            inputstr = input(f'{self.turn.title()} player: ')
            if not valid_format(inputstr):
                print('Invalid input. Please enter your move in the '
                      'following format: __ __, _ represents a digit.')
            elif not valid_num(inputstr):
                print('Invalid input. Move digits should be 0-7.')
            else:
                start, end = split_and_convert(inputstr)
                if self.valid_move(start, end):
                    print(printmove(start, end))
                    self.previousmove = (start, end)
                    print(self.moveclassifier(start, end))  # maybe combine with printmove??
                    movelog(start, end)
                    return start, end
                else:
                    print(f'Invalid move for {self.get_piece(start)}.')

    def valid_move(self, start, end):
        '''
        Returns True if all conditions are met:
        1. There is a start piece of the player's colour
        2. There is no end piece, or end piece is not of player's colour
        3. The move is not invalid for the selected piece
        4. There is no moving over other pieces
        Returns False otherwise
        5. Special moves
        '''
        
        def pawn_isvalid():
          """
          Extra validation for pawn capturing and en passant moves
          Returns True if move is valid, else returns False
          """
          x, y, dist = start_piece.vector(start, end)
          if x == 1 or x == -1:
              is_capture = True
          else:
              is_capture = False
          if is_capture and end_piece is None:
            xcord = end[0]
            ycord = start[1]
            sidepiece = self.get_piece((xcord, ycord))
            if sidepiece.name == 'pawn':
              if not sidepiece.doublemoveprevturn:
                return False
              elif (xcord, ycord) == self.previousmove[1]:
                self.move((xcord, ycord), end)
                return True
              else:
                return False
            else:
              return False
          elif not is_capture and end_piece is not None:
            return False
          else:
            return True

        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if self.castling(start, end):
            if self.debug:
                print(f'Castling from {start} -> {end} is a valid move')
            return True
        elif start_piece is None or start_piece.colour != self.turn:
            return False
        elif end_piece is not None and end_piece.colour == self.turn:
            return False
        elif not start_piece.isvalid(start, end):
            return False

        elif start_piece.name == 'pawn':
          if not pawn_isvalid():
            return False
        elif not self.nojumpcheck(start, end):
            return False
        return True
        
    def nojumpcheck(self, start, end):
        '''
        self.nojumpcheck(start, end)
        
        check if the piece moved will move over another piece
        return boolean:
        False if jumping over happens
        else True
        yuheng
        '''
        x = end[0]- start[0]
        y = end[1]- start[1]
        position_checking = start
        nojump = True
        if abs(x) == 1 or abs(y) == 1:
            nojump = True
        elif x == 0:
            # moving vertically
            for i in range(0, abs(y)-1):
                position_checking = list(position_checking)
                position_checking[1] += y/abs(y)
                position_checking = tuple(position_checking)
                if self.get_piece(position_checking) != None:
                    nojump = False
        elif y == 0:
            # moving horizontally
            for i in range(0, abs(x)-1):
                position_checking = list(position_checking)
                position_checking[0] += x/abs(x)
                position_checking = tuple(position_checking)
                if self.get_piece(position_checking) != None:
                    nojump = False
        else:
            # moving diagonally
            for i in range(0, abs(x)-1):
                position_checking = list(position_checking)
                position_checking[0] += x/abs(x)
                position_checking[1] += y/abs(y)
                position_checking = tuple(position_checking)
                if self.get_piece(position_checking) != None:
                    nojump = False
        return nojump

    def castling(self, start, end):
        '''
        Check if castling move is valid. 
        Returns a boolean: True if valid, False otherwise

        special move: castling
        1. The king and the chosen rook are on the player's first rank.
        2. Neither the king nor the chosen rook has previously moved.
        3. There are no pieces between the king and the chosen rook.
        4. The king is not currently in check.
        5. The king does not pass through a square that is attacked by an enemy piece.
        yuheng
        '''
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if start_piece == None or end_piece == None:
            return False
        elif start_piece.colour != end_piece.colour:
            return False
        elif start_piece.moved or end_piece.moved:
            return False
        elif not ((start_piece.name == 'king' and end_piece.name == 'rook') or (start_piece.name == 'rook' and end_piece.name == 'king')):
            return False
        elif not self.nojumpcheck(start, end):
            return False
        else:
            if start_piece.name == 'king':
                king_pos = start
                rook_pos = end
            else:
                king_pos = end
                rook_pos = start
            if self.check(self.turn) == True:
                return False
            else:
                x = rook_pos[0] - king_pos[0]
                position_checking = king_pos
                for i in range(0, 2):
                    position_checking = list(position_checking)
                    position_checking[0] += x/abs(x)
                    position_checking = tuple(position_checking)
                    self.add(position_checking, King(self.turn))
                    if self.check(self.turn) == True:
                        self.remove(position_checking)
                        return False
                    self.remove(position_checking)
                return True

    def castlingmove(self, start, end):
        """
        To conduct castling
        """
        start_piece = self.get_piece(start)
        if start_piece.name == 'king':
            king_pos = start
            rook_pos = end
        else:
            king_pos = end
            rook_pos = start
        x = rook_pos[0] - king_pos[0]
        king_pos_end = list(king_pos)
        king_pos_end[0] += 2*(x/abs(x))
        king_pos_end = tuple(king_pos_end)
        self.move(king_pos, king_pos_end)
        rook_pos_end = list(rook_pos)
        rook_pos_end[0] = king_pos_end[0] - x/abs(x)
        rook_pos_end = tuple(rook_pos_end)
        self.move(rook_pos, rook_pos_end)

    def winnercheck(self):
        '''check for winner'''
        # possible use of get_coords to find king??
        no_of_kings = 0
        for pieces in list(self.pieces()):
            if pieces.name == 'king':
              no_of_kings += 1
        if no_of_kings != 2:
            self.winner = self.turn
    
    def promotioncheck(self):
        '''check for pawn promotion'''
        for coord , piece in self.position.items():  # Use the self.pieces method to get the items.
            if piece.name == "pawn" and (coord[1] == 0 or coord[1] == 7):
                self.position[coord] = Queen(piece.colour)

    def get_coords(self, colour, name):
        """
        Return a list of coords where piece colour and name match.
        Returns empty list if no such piece found.
        (Meant to be used in a for loop.)
        """
        found_piece_coord = []

        for coord in self.coords(colour):
            piece = self.get_piece(coord)
            if piece.name == name:
                found_piece_coord.append(coord)
        return found_piece_coord

    def get_kingthreat_coords(self, colour):
        """
        Checks for pieces with a valid move for attacking king of the specified colour.
        Returns a list of the coordinates of these pieces.
        """
        if self.debug:
            print(f"Finding king threat pieces for {colour}")
        # print("KING THREAT INITIAL TURN COLOUR", colour) is printed when debug False
        initial_turn = self.turn
        opponent_colour = 'white' if colour == 'black' else 'black'
        self.turn = opponent_colour
        attacking_pieces = []
        opponent_coords_list = self.coords(opponent_colour) 
        own_king_coord = self.get_coords(colour, 'king')[0]
        for start_coord in opponent_coords_list:
            if self.debug:
                print(f"checking for {self.get_piece(start_coord)} at {start_coord} moving to {own_king_coord}")
            if self.valid_move(start_coord, own_king_coord):
                attacking_pieces.append(start_coord)
        if self.debug:
            print(f"King threat pieces are {attacking_pieces}")
        self.turn = initial_turn
        return attacking_pieces

    def get_valid_move_coords(self, piece_coord):
        '''
        Returns a list of valid end coordinates for the piece at piece_coord.
        Returns an empty list if there are no valid moves.
        '''
        initial_turn = self.turn
        self.turn = self.get_piece(piece_coord).colour
        valid_coord_list = []
        for i in range(8):
            for j in range(8):
                if self.valid_move(piece_coord, (i, j)):
                    valid_coord_list.append((i, j))
        self.turn = initial_turn
        return valid_coord_list

    def check(self, colour, start=None, end =None):
        """
        the colour argument tells which king to check if it is checked. Assuming that it is a validated move (except if the move would result in check)
        return boolean
        """
        initial_turn = self.turn
        self.turn = colour
        if self.debug:
            print(f"\nNow checking if the {colour} king is being checked")
        if start != None and end != None:
            self.update(start, end)
            if self.debug:
                print(f"displaying move after a temporary move in check ({start} -> {end}")
                self.display()
            king_threat_pieces = self.get_kingthreat_coords(colour)
            self.undo()
        else:
            king_threat_pieces = self.get_kingthreat_coords(colour)
        self.turn = initial_turn
        if len(king_threat_pieces) == 0:
            return False
        return True

    def checkmate(self, colour):
        """
        self.checkmate(colour)

        Check if the colour is in checkmate 

        Steps:
        1. if there are two attacking pieces, King must move away,

        2. if only one attacking piece, see if king can move away or
        see if any other pieces are able to block/eat it

        3. see if it will now result in check, if it does not, it will not checkmate
        """
        if self.debug:
            print("\nChecking for checkmate for", colour)

        own_king_coord = self.get_coords(colour, 'king')[0]


        # Generating possible king moves
        possible_king_move = set(self.get_valid_move_coords(own_king_coord))

        initial_turn = self.turn
        self.turn = colour

        if self.debug:
            print("Possible king move set:", possible_king_move)

        # See if king can move or capture
        if self.debug:
            print("\nChecking for king escape moves:")
        for end_coord in possible_king_move:
            print("Possible king moves ares", possible_king_move)
            if self.debug:
                print(f"Checking for move {own_king_coord} -> {end_coord}")
            if not self.check(colour, own_king_coord, end_coord):
                if self.debug:
                    print(f"Valid move found for king to escape: {own_king_coord} -> {end_coord}")

                    self.turn = initial_turn
                    return False

            else:
                if self.debug:
                    print("No valid move for king to move to")

        attacking_pieces = self.get_kingthreat_coords(colour)
        own_pieces_list = self.coords(colour)
        if len(attacking_pieces) == 0:
            self.turn = initial_turn
            return False

        # if king is the only piece left, if king cannot move, checkmate
        # If attacking pieces is more than 2, and king cannot move away, checkmate
        if len(attacking_pieces) >= 2 or len(own_pieces_list) == 1:
            self.turn = initial_turn
            return True

        # For only one piece attacking.
        # Check if it can be eaten.
        for coord in own_pieces_list:
            if self.valid_move(coord, attacking_pieces[0]):
                if self.debug:
                    print(f'\nChecking if attacking piece can be eaten by moving {coord} -> {attacking_pieces[0]}: ' , end='')
                if self.check(colour, coord, attacking_pieces[0]):
                    print('invalid move')
                    self.turn = initial_turn
                else:
                    self.turn = initial_turn
                    return False
            
        # Get all attacking piece valid_move square
        attacking_valid_move_set = set(self.get_valid_move_coords(attacking_pieces[0]))
        if self.debug:
            print("Attacking pieces possible moves:", attacking_valid_move_set)
        # See if any piece can block it.
        if self.debug:
            print('\nSee if any move can block it')
        for coord in own_pieces_list:
            for move in attacking_valid_move_set:
                if self.debug:
                    print(f"Checking for {coord} -> {move}", end="\t")
                if self.valid_move(coord, move) and not self.check(colour, coord, move):
                    if self.debug:
                        print(f"Valid move found: {coord} -> {move}")
                    return False
                else:
                    if self.debug:
                        print("Not Valid")
        return True

    def moveclassifier(self, start, end):
        """
        a method that classifies and returns the type of move being made.
        """
        end_piece = self.get_piece(end)
        if self.castling(start, end):
            return 'castling'
        elif end_piece is not None:
            return 'capture'
        else:
            return 'move'

    def update(self, start, end):
        '''Update board information with the player's move.'''
        if self.castling(start, end):
            self.castlingmove(start, end)
        else:
            self.movehistory.push('update')
            self.remove(end)
            self.move(start, end)
        self.winnercheck()
        self.promotioncheck()
        if self.turn == 'white':
            if self.check('black'):
                if self.checkmate('black'):
                    self.winner = self.turn
        else:
            if self.check('white'):
                if self.checkmate('white'):
                    self.winner = self.turn
    
    def undo(self):
        """Reverses the Board to before update and reprompt"""
        if self.debug:
            print("\nBefore undo, move history:\n", self.movehistory)
        while self.movehistory[-1] != 'update':
            if self.debug:
                print(self.movehistory[-1])
            if self.movehistory[-1][0] == 'remove':
                self.add(self.movehistory[-1][1], self.movehistory[-1][2], track=False)
            elif self.movehistory[-1][0] == 'add':
                self.remove(self.movehistory[-1][1], track=False)
            self.movehistory.pop()
            
        self.movehistory.pop()
        self.display()
        # start, end = self.prompt()
        # self.update(start, end)

    def next_turn(self):
        '''Hand the turn over to the other player.'''
        if self.winner is None:
            if self.turn == 'white':
                self.turn = 'black'
            elif self.turn == 'black':
                self.turn = 'white'

class BasePiece:
    name = 'piece'
    def __init__(self, colour, moved = False):
        if type(colour) != str:
            raise TypeError('colour argument must be str')
        elif colour.lower() not in {'white', 'black'}:
            raise ValueError('colour must be {white, black}')
        else:
            self.colour = colour
            self.moved = moved

    def __repr__(self):
        return f'BasePiece({repr(self.colour)})'

    def __str__(self):
        return f'{self.colour} {self.name}'

    def symbol(self):
        return f'{self.sym[self.colour]}'
    

    @staticmethod
    def vector(start, end):
        '''
        Return three values as a tuple:
        - x, the number of spaces moved horizontally,
        - y, the number of spaces moved vertically,
        - dist, the total number of spaces moved.
        
        positive integers indicate upward or rightward direction,
        negative integers indicate downward or leftward direction.
        dist is always positive.
        '''
        x = end[0] - start[0]
        y = end[1] - start[1]
        dist = abs(x) + abs(y)
        return x, y, dist

    


class King(BasePiece):
    name = 'king'
    sym = {'white': '♔', 'black': '♚'}
    def __repr__(self):
        return f"King('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        King can move one step in any direction
        horizontally, vertically, or diagonally.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 1) or (abs(x) == abs(y) == 1)

    
class Queen(BasePiece):
    name = 'queen'
    sym = {'white': '♕', 'black': '♛'}
    def __repr__(self):
        return f"Queen('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Queen can move any number of steps horizontally,
        vertically, or diagonally.
        '''
        x, y, dist = self.vector(start, end)
        return (abs(x) == abs(y) != 0) \
            or ((abs(x) == 0 and abs(y) != 0) \
            or (abs(y) == 0 and abs(x) != 0))


class Bishop(BasePiece):
    name = 'bishop'
    sym = {'white': '♗', 'black': '♝'}
    def __repr__(self):
        return f"Bishop('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''Bishop can move any number of steps diagonally.'''
        x, y, dist = self.vector(start, end)
        return (abs(x) == abs(y) != 0)


class Knight(BasePiece):
    name = 'knight'
    sym = {'white': '♘', 'black': '♞'}
    def __repr__(self):
        return f"Knight('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Knight moves 2 spaces in any direction, and
        1 space perpendicular to that direction, in an L-shape.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 3) and (abs(x) != 3 and abs(y) != 3)


class Rook(BasePiece):
    name = 'rook'
    sym = {'white': '♖', 'black': '♜'}
    def __repr__(self):
        return f"Rook('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Rook can move any number of steps horizontally
        or vertically.
        '''
        x, y, dist = self.vector(start, end)
        return (abs(x) == 0 and abs(y) != 0) \
            or (abs(y) == 0 and abs(x) != 0) 


class Pawn(BasePiece):
    name = 'pawn'
    sym = {'white': '♙', 'black': '♟︎'}
    doublemoveprevturn = False
    def __repr__(self):
        return f"Pawn('{self.name}')"
    

    def isvalid(self, start: tuple, end: tuple):
        '''
        Pawn can only move 1 step forward into empty space, or 1 step horizontally and 1 step forward while capturing.
        Attribute self.doublemoveprevturn is True when the Pawn moves 2 spaces. Else self.doublemoveprevturn is False

        Ryan - PawnCapture enpassant
        '''
        x, y, dist = self.vector(start, end)
        if x == -1 or x == 1 or x == 0:
          if self.colour == 'black':
            self.doublemoveprevturn = False
            if start[1] ==  6:
              if y == -2:
                self.doublemoveprevturn = True
              return (y == -1 or y == -2)
            return (y == -1)
          elif self.colour == 'white':
            self.doublemoveprevturn = False
            if start[1] ==  1:
                if y == 2:
                  self.doublemoveprevturn = True
                return (y == 1 or y == 2)
            return (y == 1)
          else:
            return False
        else:
            return False



class MoveError(Exception):
  """
  Raised when an invalid move is made.
  """
pass
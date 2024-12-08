# Author: Van Huynh
# GitHub username: huynhvan126
# Date: 12/08/2024
# Description: Create a class called ChessVar to implement an abstract board game based on a chess variant known as Fog of War chess.
class ChessVar:
    def __init__(self):
        """Initialise the ChessVar object"""
        self._board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        self._turn = 'white'
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """Return the current game state"""
        return self._game_state

    def _convert_position(self, pos):
        """Convert the given position to the corresponding chess position"""
        col = ord(pos[0]) - ord('a')  # Ensure this line uses consistent indentation
        row = 8 - int(pos[1])
        return row, col

    def _is_within_bounds(self, row, col):
        """Check if the given position is within the bounds of the board."""
        return 0<= row < 8 and 0 <= col < 8

    def get_board(self, perspective):
        """Return the board for the given perspective."""

        def generate_hidden_board(player):
            visible_board = [['*' for _ in range(8)] for _ in range(8)]
            for r in range(8):
                for c in range(8):
                    piece = self._board[r][c]
                    if (player == 'white' and piece.isupper()) or (player == 'black' and piece.islower()):
                        visible_board[r][c] = piece
                        for move in self._get_moves(r, c):
                            mr, mc = move
                            visible_board[mr][mc] = self._board[mr][mc]
                return visible_board

        if perspective == 'white':
            return generate_hidden_board('white')
        elif perspective == 'black':
            return generate_hidden_board('black')
        elif perspective == 'audience':
            return self._board
        else:
            raise ValueError("Invalid perspective. Choose 'white', 'black', or 'audience'.")

    def _get_moves(self, row, col):
        """Return the possible moves for the given position."""
        piece = self._board[row][col]
        moves = []

        if piece.lower() == 'p':
            direction = -1 if piece.isupper() else 1
            start_row = 6 if piece.isupper() else 1

            if self._is_within_bounds(row +direction +col) and self._board[row + direction][col] == ' ':
            moves.append(row +direction + col)
                if row == start_row and self._board[row + 2 * direction][col] == ' ':
                moves.append(row + 2 * direction, col)

            for dc in [-1, 1]:
                if self._is_within_bounds(row +direction, col +dc):
                    target = self._board[row + direction][col +dc]
                    if (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        moves.append(row +direction, col + dc)

        return moves

    def make_move(self, start, end):
        """Make a move on the given position."""
        if self._game_state != 'UNFINISHED':
            return False

        start_row, start_col = self._convert_position(start)
        end_row, end_col = self._convert_position(end)

        if not self._is_within_bounds(start_row, start_col) or not self._is_within_bounds(end_row, end_col):
            return False

        piece = self._board[start_row][start_col]
        if (self._turn =='white' and not piece.isupper()) or (self._turn =='black' and not piece.islower()):
            return False

        legal_moves = self._get_moves(start_row, start_col)
        if (end_row, end_col) not in legal_moves:
            return False

        self._board[end_row][end_col] = piece
        self._board[start_row][start_col] = ' '

        if piece.lower() == 'k':
            self._game_state = 'WHITE_WON' if self._turn == 'white' else 'BLACK_WON'

        self._turn = 'black' if self._turn == 'white' else 'white'

        return True

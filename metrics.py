# Base packages:

# Installed packages:
import chess 

# Project-local packages:


class SquareMap:
    """
    A SquareMap is a 64-list of numbers indicating some quantity that
    is associated with each square of the chessboard.
    """

    def __init__(self, vals=None):
        if vals:
            self._vals = vals
        else:
            self._vals = [0]*64
        return None

    def __str__(self):
        vstr = [str(i) for i in self._vals]
        max_vstr_len = max(map(len, vstr))
        max_vstr_len = min(max_vstr_len, 5)
        vstr = [vs.rjust(max_vstr_len)[0:max_vstr_len] for vs in vstr]
        rows = [' '.join(vstr[8*i:8*(i+1)]) for i in range(8)]
        rows.reverse()
        rows = '\n'.join(rows)
        rows
        return ''.join(rows)

    def __getitem__(self, key):
        return self._vals[key]

    def __setitem__(self, key, value):
        self._vals[key] = value
        return None

    def __add__(self, other):
        if isinstance(other, SquareMap):
            return SquareMap([self[sq] + other[sq] for sq in range(64)])
        elif isinstance(other, int) or isinstance(other, float):
            return SquareMap([self[sq] + other for sq in range(64)])

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, SquareMap):
            return SquareMap([self[sq]*other[sq] for sq in range(64)])
        elif isinstance(other, int) or isinstance(other, float):
            return SquareMap([other*self[sq] for sq in range(64)])

    def __rmul__(self, k):
        return self.__mul__(k)

    def __neg__(self):
        return SquareMap([-self[sq] for sq in range(64)])

    def __sub__(self, other):
        return -other + self

    def __truediv__(self, other):
        return SquareMap([self[sq]/other[sq] for sq in range(64)])

    def __abs__(self):
        return SquareMap([abs(self[sq]) for sq in range(64)])

    def _mask(self):
        return SquareMap([1 if self[sq] else 0 for sq in range(64)])

    def to_heatmap(self):
        heatmap = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        for row in range(8):
            for col in range(8):
                heatmap[row][col] = self[8*(7-row) + col]
        return heatmap
        

def control(board):
    """
    Returns two square maps indicating the number of attackers at each
    square, for both white and black.  
    """
    w = SquareMap()
    b = SquareMap()
    for sq in range(64):
        w[sq] = len(board.attackers(chess.WHITE, sq))
        b[sq] = len(board.attackers(chess.BLACK, sq))
    return w, b 

    
def contested(board):
    """
    Identifies 'hot' squares where both white and black have a high
    number of attackers.
    """
    w, b = control(board)
    return (w*b._mask() + b*w._mask())/(abs(w-b)+1)
    

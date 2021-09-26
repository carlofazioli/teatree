"""
When iterating over a board FEN string array, the rows (ranks) index
will enumerate from 0 to 7 as the rank varies from 8 to 1.  Similarly, 
the chars in each row (the files) will enumerate from 0 to 7 as the
file varies from A to H.  

    |-------------------------------------------------------------------------------|
    |         |         |         |         |         |         |         |         |
 8  | (0, 0)  | (0, 1)  | (0, 2)  | (0, 3)  | (0, 4)  | (0, 5)  | (0, 6)  | (0, 7)  |
    |         |         |         |         |         |         |         |         |
    |-------------------------------------------------------------------------------|
    |         |         |         |         |         |         |         |         |
 7  | (1, 0)  | (1, 1)  | (1, 2)  | (1, 3)  | (1, 4)  | (1, 5)  | (1, 6)  | (1, 7)  |
    |         |         |         |         |         |         |         |         |
    |-------------------------------------------------------------------------------|
    |         |         |         |         |         |         |         |         |
 6  | (2, 0)  | (2, 1)  | (2, 2)  | (2, 3)  | (2, 4)  | (2, 5)  | (2, 6)  | (2, 7)  |
    |         |         |         |         |         |         |         |         |
    |-------------------------------------------------------------------------------|
    |         |         |         |         |         |         |         |         |
 5  | (3, 0)  | (3, 1)  | (3, 2)  | (3, 3)  | (3, 4)  | (3, 5)  | (3, 6)  | (3, 7)  |
    |         |         |         |         |         |         |         |         |
    |-------------------------------------------------------------------------------|
    |         |         |         |         |         |         |         |         |
 4  | (4, 0)  | (4, 1)  | (4, 2)  | (4, 3)  | (4, 4)  | (4, 5)  | (4, 6)  | (4, 7)  |
    |         |         |         |         |         |         |         |         |
    |-------------------------------------------------------------------------------|
    |         |         |         |         |         |         |         |         |
 3  | (5, 0)  | (5, 1)  | (5, 2)  | (5, 3)  | (5, 4)  | (5, 5)  | (5, 6)  | (5, 7)  |
    |         |         |         |         |         |         |         |         |
    |-------------------------------------------------------------------------------|
    |         |         |         |         |         |         |         |         |
 2  | (6, 0)  | (6, 1)  | (6, 2)  | (6, 3)  | (6, 4)  | (6, 5)  | (6, 6)  | (6, 7)  |
    |         |         |         |         |         |         |         |         |
    |-------------------------------------------------------------------------------|
    |         |         |         |         |         |         |         |         |
 1  | (7, 0)  | (7, 1)  | (7, 2)  | (7, 3)  | (7, 4)  | (7, 5)  | (7, 6)  | (7, 7)  |
    |         |         |         |         |         |         |         |         |
    |-------------------------------------------------------------------------------|

         A         B         C         D         E         F         G         H

The constants below allow conversion between these coordinate systems.
"""

RANKS = '87654321'
FILES = 'abcdefgh'
INDEX_TO_SQUARE = {(row, col): FILES[col]+RANKS[row] for row in range(8) for col in range(8)}
SQUARE_TO_INDEX = {val:key for key,val in INDEX_TO_SQUARE.items()}
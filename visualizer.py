from PIL import Image


# IMAGE_PATH is the subdir with each piece image.
# PIECE_NAMES are the FEN string names of each piece; image filenames
#             should match.
# IMAGES are the loaded PNG images, in a dict keyed by FEN string name.
# IMAGE_SIZE is the pixel size of the PNG images.  Must be square.  All
#            images must be the same size.  
# IMAGE_WIDTH is the side length of a piece image.
# BOARD_SIZE is 8* the image size.  
# IMAGES is the dict of piece images, keyed by piece FEN name.  
IMAGE_PATH = './images/'
PIECE_NAMES = 'rnbqkpRNBQKP'
IMAGES = {imname: Image.open(IMAGE_PATH + imname + '.png') for imname in PIECE_NAMES}
IMAGE_SIZE = IMAGES['r'].size
assert IMAGE_SIZE[0] == IMAGE_SIZE[1]
assert all([im.size == IMAGE_SIZE for im in IMAGES.values()])
IMAGE_WIDTH = IMAGE_SIZE[0]
BOARD_SIZE = (8*IMAGE_SIZE[0], 8*IMAGE_SIZE[0])
BOARD_MIDPOINT = (BOARD_SIZE[0]/2, BOARD_SIZE[1]/2)
IMAGES[' '] = Image.new('RGBA', IMAGE_SIZE, (255, 255, 255, 0))

"""
TeaTree displays information by way of *heatmap* colorings on the chess
board.  A heatmap coloring is an assignment of a float in [0, 1] to
each square of the board.  The float value gives an amount of linear
interpolation between Blue (0) and Red (1) by which to color the 
square.

Once each RGB interpolated color is computed and stored in a *colormap*
dictionary, the dark and light square shades and tints are added.  This
is done with the instruction on the following link:

https://stackoverflow.com/questions/6615002/given-an-rgb-value-how-do-i-create-a-tint-or-shade/6615053

"""

SHADE_FACTOR = 0.2
TINT_FACTOR = 0.2
COLD = (30, 130, 230)
HOT = (230, 30, 30)


def shade(rgb):
    """
    The incoming RGB triple is scaled toward Black (0, 0, 0) by a
    factor of (1-SHADE_FACTOR).  Larger SHADE_FACTORs produce darker 
    colors.
    """
    return tuple(round(c*(1-SHADE_FACTOR)) for c in rgb)


def tint(rgb):
    """
    The incoming RGB triple is scaled toward White (255, 255, 255) by a
    factor of (255-RGB)*TINT_FACTOR.  Larger TINT_FACTORs produce
    lighter colors.
    """
    return tuple(round(c + (255-c)*TINT_FACTOR) for c in rgb)


def interp_color(t):
    """
    Given a float in [0, 1], this function produces a linear RGB 
    interpolation between COLD and HOT.  
    """
    return tuple(round(COLD[i] + (HOT[i] - COLD[i])*t) for i in range(3))


def shade_or_tint(t, i, j):
    """
    Given a heatmap float in [0, 1], this function interpolates the RGB
    color and then applies a shade or tint based on the square's 
    location on the chess board.  
    """
    c = interp_color(t)
    f = tint if (i+j)%2==0 else shade
    return f(c)
    

def heatmap_to_colormap(heatmap=None):
    """
    Given a heatmap (an 8x8 list of lists or numpy.array), create a
    colormap, which is a dictionary keyed by (i, j) board locations
    whose values are RGB tuples.  
    """
    if heatmap is None:
        colormap = {(i, j): shade_or_tint(0.5, i, j)
                    for i in range(8) for j in range(8)}
    else:
        colormap = {(i, j): shade_or_tint(heatmap[i][j], i, j) 
                    for i in range(8) for j in range(8)}
    return colormap
    

def construct_board_img(colormap=None):
    """
    Given a colormap, construct the PIL image consisting of colored
    squares.  If no colormap is given, default neutral coloring is 
    used.  
    """
    if colormap is None:
        colormap = heatmap_to_colormap()
    board_img = Image.new('RGB', BOARD_SIZE)
    for i in range(8):
        for j in range(8):
            sq = Image.new('RGB', IMAGE_SIZE, colormap[(i, j)])
            board_img.paste(sq, (j*IMAGE_WIDTH, i*IMAGE_WIDTH))
    return board_img


def construct_piece_img(board_array):
    """
    Given the board FEN that has been changed to an array using
    board_fen_to_array(), construct the 'foreground' image of the 
    pieces.  The blank space is transparent, so the piece image is
    intended to be pasted onto the board image backgroun.  
    """
    piece_img = Image.new('RGBA', BOARD_SIZE)
    for i, row in enumerate(board_array):
        for j, ch in enumerate(row):
            fg = IMAGES[ch]
            piece_img.paste(fg, (j*IMAGE_WIDTH, i*IMAGE_WIDTH))
    return piece_img


def board_fen_to_array(b):
    """
    The board FEN str parameter b is copied into a new string a.  
    Within the new string, each FEN integer indicator of empty squares
    is replaced by a corresponding number of spaces.  The modified FEN
    string is then split on '/' to produce an array or rank strings.
    For example, the board FEN excerpt '3P4/k1K5' would be transformed
    into the array ['   P    ', 'k K     '].  
    """
    a = str(b)
    for i in range(1, 9):
        a = a.replace(str(i), i*' ')
    return a.split('/')


def board_fen_to_img(board_fen, heatmap=None):
    """
    Combining all of the above utilities, this function ingests a 
    board FEN, converts it to a board array, and creates an image of 
    that layout colored according to the given heatmap.  
    """
    board_array = board_fen_to_array(board_fen)
    colormap = heatmap_to_colormap(heatmap=heatmap)
    bg = construct_board_img(colormap=colormap)
    fg = construct_piece_img(board_array)
    bg.paste(fg, fg)
    return bg

if __name__ == '__main__':
    s = '2q5/r5P1/2k3b1/n3p3/P7/P2ppK2/3p1p2/B3R3'
    import random
    heat_boi = [[random.random() for j in range(8)] for i in range(8)]
    plain_img = board_fen_to_img(s)
    color_img = board_fen_to_img(s, heat_boi)
    plain_img.show()
    color_img.show()

# Base packages:

# Installed packages:
import chess 
from PIL import ImageTk
from tkinter import Frame, Canvas, StringVar
from tkinter.ttk import Label, Entry, Button

# Project-local packages:
from metrics import contested
from utilities import RANKS, FILES
from visualizer import BOARD_SIZE, BOARD_MIDPOINT, IMAGE_WIDTH
from visualizer import board_fen_to_img, construct_board_img

        
class AnalysisBoard(Frame):
    def __init__(self, parent, name, metric):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.metric = metric
        w, h = BOARD_SIZE
        self.canvas = Canvas(self, width=w, height=h)
        self.caption = Label(self, text=name)
        self.canvas.grid(row=0, column=0)
        self.caption.grid(row=1, column=0)

    def update(self):
        overlay = self.metric(self.parent.board).to_heatmap()
        self.img = board_fen_to_img(self.parent.board.board_fen(), heatmap=overlay)
        self.photo_img = ImageTk.PhotoImage(image=self.img, size=BOARD_SIZE)
        self.canvas.create_image(BOARD_MIDPOINT, image=self.photo_img)
        

class TextEntry(Frame):
    def __init__(self, 
                 parent, 
                 label_text, 
                 text_variable, 
                 default_entry,
                 button_name,
                 bind):
        super().__init__(parent)
        self.label = Label(self, text=label_text)
        self.entry = Entry(self, textvariable=text_variable)
        text_variable.set(default_entry)
        self.button = Button(self, text=button_name, command=bind)
        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.button.grid(row=0, column=2)


class TeaTreeApp(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.pack()

        self.fen = StringVar()
        self.move_uci = StringVar()
        self.img = construct_board_img()
        self.photo_img = ImageTk.PhotoImage(image=self.img, size=BOARD_SIZE)

        self.main_game = Frame(self)
        self.fen_frame = TextEntry(self.main_game, 
                                   'FEN: ', 
                                   self.fen, 
                                   'default', 
                                   'Start Game', 
                                   self.start_game)

        w, h = BOARD_SIZE
        self.board_canvas = Canvas(self.main_game, width=w, height=h)
        self.board_canvas.create_image(BOARD_MIDPOINT, image=self.photo_img)
        self.board_canvas.bind('<Button-1>', self.get_start_square)

        self.move_frame = TextEntry(self.main_game, 
                                    'UCI: ', 
                                    self.move_uci, 
                                    '', 
                                    'Submit Move', 
                                    self.submit_move)

        self.fen_frame.grid(row=0, column=0)
        self.board_canvas.grid(row=1, column=0)
        self.move_frame.grid(row=2, column=0)
        self.main_game.grid(row=0, column=0, padx=20, pady=20)

        self.analysis_board_configs = [
            {'name': 'Contested Squares', 'metric': contested}
        ]
        self.analysis_board_frames = []
        for config in self.analysis_board_configs:
            self.analysis_board_frames.append(AnalysisBoard(self, **config))
        for col, f in enumerate(self.analysis_board_frames):
            f.grid(row=0, column=col+1, padx=20, pady=20)

    def start_game(self, event=None):
        fen = self.fen.get()
        if fen == 'default':
            fen = chess.Board.starting_fen
        self.fen.set('')
        self.move_uci.set('Type Move UCI or click board')
        self.board = chess.Board(fen=fen)
        self.update()

    def update(self):
        self.img = board_fen_to_img(self.board.board_fen())
        self.photo_img = ImageTk.PhotoImage(image=self.img, size=BOARD_SIZE)
        self.board_canvas.create_image(BOARD_MIDPOINT, image=self.photo_img)
        for f in self.analysis_board_frames:
            print('updating analysis board...')
            f.update()

    def get_start_square(self, event):
        self.move_uci.set('')
        row_index = event.y // IMAGE_WIDTH
        col_index = event.x // IMAGE_WIDTH
        square = FILES[col_index] + RANKS[row_index]
        self.move_uci.set(square)
        self.board_canvas.bind('<Button-1>', self.get_end_square)

    def get_end_square(self, event):
        row_index = event.y // IMAGE_WIDTH
        col_index = event.x // IMAGE_WIDTH
        square = FILES[col_index] + RANKS[row_index]
        self.move_uci.set(self.move_uci.get() + square)
        self.board_canvas.bind('<Button-1>', self.get_start_square)

    def submit_move(self, event=None):
        move_uci = self.move_uci.get()
        move = chess.Move.from_uci(move_uci)
        if self.board.is_legal(move):
            self.board.push(move)
            self.move_uci.set('')
        else:
            self.move_uci.set('Invalid move!  Re-enter.')
        self.update()

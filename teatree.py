# Base packages:

# Installed packages:
from tkinter import Tk

# Project-local packages:
from app import TeaTreeApp


root = Tk()
root.title('TeaTree')
application = TeaTreeApp(parent=root)
application.mainloop()

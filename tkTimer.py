import tkinter as tk
from datetime import datetime


class Timer:  # figure out key release
    start = 0
    stop = 0

    def __init__(self, master):
        self.master = master
        self.master.geometry('400x400')
        self.master.title('PTimer GUI')
        self.master.bind('<Key>', self.timeIt)
        self.timeLabel = tk.Label(self.master, text='')
        self.timeLabel.pack()

    def timeIt(self, *args):  # this is the one I think (will have to update to be able to run multiple times)
        if args and Timer.start:  # and I'd like to have the timer start on the release of the first spacebar
            Timer.stop = datetime.now()
        else:
            if args and not Timer.start:
                Timer.start = datetime.now()
            elif not (args or Timer.stop):
                elapsed = str(datetime.now() - Timer.start)
                self.timeLabel.configure(text=elapsed[:-4])
            self.master.after(10, self.timeIt)


def main():
    root = tk.Tk()
    Timer(root)
    root.mainloop()


main()

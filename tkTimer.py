import tkinter as tk
from datetime import datetime


class Timer:  # figure out key release
    start = 0
    stop = 0
    running = False

    def __init__(self, master):
        self.master = master
        self.master.geometry('400x400')
        self.master.title('PTimer GUI')
        self.master.bind('<space>', self.timeIt)
        self.timeLabel = tk.Label(self.master, text='')
        self.timeLabel.pack()

    def timeIt(self, *event):
        if not Timer.running:
            if event:
                Timer.start = datetime.now()
                Timer.running = True
                self.master.after(10, self.timeIt)
        else:
            if not event:
                elapsed = str(datetime.now() - Timer.start)
                self.timeLabel.configure(text=elapsed[5:-4])
                self.master.after(10, self.timeIt)
            else:
                Timer.running = False
                print(self.timeLabel['text'])

        # if event and Timer.start:  # and I'd like to have the timer start on the release of the first spacebar
        #     Timer.stop = datetime.now()
        # else:
        #     if event and not Timer.start:
        #         Timer.start = datetime.now()
        #         Timer.running = True
        #     elif not (event or Timer.stop):
        #         elapsed = str(datetime.now() - Timer.start)
        #         self.timeLabel.configure(text=elapsed[:-4])
        #     self.master.after(10, self.timeIt)


def main():
    root = tk.Tk()
    Timer(root)
    root.mainloop()


main()

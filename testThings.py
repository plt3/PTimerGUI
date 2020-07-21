import tkinter as tk
import time
from datetime import datetime


class Timer:
    stopTime = 0
    total = 0
    cont = True

    def __init__(self, master):
        self.master = master
        self.master.geometry('400x400')
        self.master.title('PTimer GUI')
        self.master.bind('<space>', self.start)
        self.master.bind('<KeyRelease-space>', self.stop)
        self.master.after(3, self.checc)

    def checc(self):  # this doesn't work if you click the space bar really fast
        if Timer.stopTime and Timer.total > 1:
            if time.time() - Timer.stopTime > 0.04:  # so this works but you have to use a magic number based on how fast
                print('you have released the space bar')  # the key repetitions are ugh (but not the pause before repeating)
                toDo = datetime.fromtimestamp(Timer.stopTime)
                print(f'it was at {toDo}')
                Timer.total = 0
        self.master.after(3, self.checc)

    def start(self, event):
        Timer.cont = True

    def stop(self, event):
        Timer.stopTime = time.time()
        Timer.total += 1


def main():
    root = tk.Tk()
    Timer(root)
    root.mainloop()


main()

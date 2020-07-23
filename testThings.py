import tkinter as tk
import time
from datetime import datetime


class Timer:
    startVal = 0
    stopVal = 0
    stopTime = 0
    total = 0
    running = False

    def __init__(self, master):
        self.master = master
        self.master.geometry('400x400')
        self.master.title('PTimer GUI')
        self.timeLabel = tk.Label(self.master, text='')
        self.timeLabel.pack()
        self.master.bind('<space>', self.stopOrRestart)
        self.master.bind('<KeyRelease-space>', self.stop)
        self.master.after(3, self.checc)

    def checc(self):  # this doesn't work if you click the space bar really fast
        if Timer.stopTime and Timer.total > 1:
            if time.time() - Timer.stopTime > 0.04:  # so this works but you have to use a magic number based on how fast
                # print('you have released the space bar')  # the key repetitions are ugh (but not the pause before repeating)
                # toDo = datetime.fromtimestamp(Timer.stopTime)
                # print(f'it was at {toDo}')
                Timer.running = True
                self.timeIt(1)
                Timer.total = 0
        self.master.after(3, self.checc)

    def stopOrRestart(self, event):
        if Timer.running:
            self.timeLabel.configure(text='')
        else:
            self.timeLabel.configure(text='00.00')

    def stop(self, event):
        Timer.stopTime = time.time()
        Timer.total += 1

    def timeIt(self, *args):  # this is the one I think (will have to update to be able to run multiple times)
        if args and Timer.startVal:  # and I'd like to have the timer start on the release of the first spacebar
            Timer.stopVal = datetime.now()
        else:
            if args and not Timer.startVal:
                Timer.startVal = datetime.now()
            elif not (args or Timer.stopVal):
                elapsed = str(datetime.now() - Timer.startVal)
                self.timeLabel.configure(text=elapsed[5:-4])
            self.master.after(10, self.timeIt)


def main():
    root = tk.Tk()
    Timer(root)
    root.mainloop()


# main()


class FloatTime:
    def __init__(self, time):
        self.time = time

    def niceTime(self, precision=5):
        rawHours, remainder = divmod(int(self.time), 3600)
        rawMins, wholeSeconds = divmod(remainder, 60)
        rawSecs = round(wholeSeconds + (self.time - int(self.time)), precision)

        strList = []

        for index, num in enumerate([rawHours, rawMins, rawSecs]):
            if num or index == 2:
                if num < 10:
                    strList.append(f'0{num}')
                else:
                    strList.append(str(num))

        if len(strList) == 1 and rawSecs < 1:
            joinedStr = ':'.join(strList)[1:]
        else:
            joinedStr = ':'.join(strList).lstrip('0')

        endZeros = ['0' for i in range(precision)]

        try:
            missing = joinedStr[joinedStr.index('.') + 1:]
        except ValueError:
            return joinedStr + '.' + ''.join(endZeros)

        return joinedStr + ''.join(endZeros[len(missing):])


a = FloatTime(0.0005)
print(a.niceTime(7))

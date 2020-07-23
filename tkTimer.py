import tkinter as tk
import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Float, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///solveTimes.db')
Base = declarative_base()
DBSession = sessionmaker(bind=eng)
session = DBSession()


class TimeModel(Base):
    __tablename__ = 'times'
    id = Column(Integer, primary_key=True)
    time = Column(Float, nullable=False)
    scramble = Column(String(60), nullable=False)
    date = Column(DateTime, nullable=False)


class Timer:
    timesLabs = []
    opposites = {'U': 'D', 'F': 'B', 'L': 'R', 'D': 'U', 'B': 'F', 'R': 'L'}
    moveslist = [a + b for a in ['U', 'D', 'F', 'B', 'L', 'R'] for b in ['', "'", '2']]
    scram = ''
    solveStart = 0
    solveFloat = 0
    running = False
    precision = 2  # anything greater than 6 makes no sense because microseconds

    def __init__(self, master):
        self.master = master
        self.master.bind('<Key>', self.timeIt)  # key or space?
        self.optsBut = tk.Button(self.master, text='Options', command=self.openOptions,
                                 font=('TkDefaultFont', 18), padx=10, pady=10)
        self.optsBut.grid(row=0, column=0, padx=20, pady=20)
        self.makeScramble()
        self.scramLab = tk.Label(self.master, text=Timer.scram, font=('TkDefaultFont', 18),
                                 borderwidth=1, relief='solid', padx=10, pady=10, width=40)
        self.scramLab.grid(row=0, column=1, pady=20)
        zeros = ''.join(['0' for i in range(Timer.precision)])
        self.timeLabel = tk.Label(self.master, text=f'0.{zeros}', font=('TkDefaultFont', 50))
        self.timeLabel.grid(row=1, column=1, pady=20)

        self.timesFrame = tk.Frame(self.master, borderwidth=1, relief='solid')
        self.timesTitle = tk.Label(self.timesFrame, text='Times:', font=('TkDefaultFont', 18))
        self.timesTitle.grid(row=0, column=0)

        rawLast = session.query(TimeModel).order_by(TimeModel.id.desc())

        for index, timeObj in enumerate(rawLast.limit(10).all()):  # this list does not work when there are < 10 times in the database
            timeLab = tk.Label(self.timesFrame, text=f'{timeObj.id}: {Timer.niceTime(timeObj.time, Timer.precision)}')
            timeLab.bind('<Button-1>', self.editTime)
            timeLab.grid(row=index + 1, column=0)
            Timer.timesLabs.append(timeLab)

        self.timesFrame.grid(row=1, column=0)

    def editTime(self, event):
        print(event.widget['text'])  # open up some sort of popup to edit penalty, etc.

    def openOptions(self):
        pass  # but like probably open up different window (so different class)

    def makeScramble(self):  # generate random move 3x3 scramble
        scramble = ''
        i = 0
        prevchoice = 'Z'
        oldchoice = 'X'
        while True:
            choice = random.choice(Timer.moveslist)  # MAKE THIS A STATIC METHOD DUMMY BOYYYYYYYYYYYYYYYYYYYY (maybe?)
            if i == 20:
                break
            elif choice[0] == prevchoice[0]:
                continue
            elif Timer.opposites[choice[0]] == prevchoice[0] and choice[0] == oldchoice[0]:
                continue
            scramble += choice + ' '
            i += 1
            oldchoice = prevchoice
            prevchoice = choice

        Timer.scram = scramble.rstrip()

    def addTime(self):
        timeObj = TimeModel(time=Timer.solveFloat, scramble=Timer.scram, date=Timer.solveStart)  # add time to database
        session.add(timeObj)
        session.commit()

        oldText = f'{timeObj.id}: {Timer.niceTime(Timer.solveFloat, Timer.precision)}'

        for label in Timer.timesLabs:  # update the labels saying the times
            prevText = label['text']
            label.configure(text=oldText)
            oldText = prevText

    @staticmethod
    def niceTime(secs, precision):
        rawHours, remainder = divmod(int(secs), 3600)
        rawMins, wholeSeconds = divmod(remainder, 60)
        rawSecs = round(wholeSeconds + (secs - int(secs)), precision)

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

    def timeIt(self, *event):
        if not Timer.running:
            if event:  # to start timer
                Timer.solveStart = datetime.now()
                Timer.running = True
                self.master.after(10, self.timeIt)
        else:
            elapsed = datetime.now() - Timer.solveStart
            timeFloat = elapsed.seconds + elapsed.microseconds / 1000000

            if not event:  # for time to update itself during timing
                self.timeLabel.configure(text=Timer.niceTime(timeFloat, Timer.precision))
                self.master.after(10, self.timeIt)
            else:  # to stop timer
                Timer.solveFloat = timeFloat
                self.timeLabel.configure(text=Timer.niceTime(Timer.solveFloat, Timer.precision))
                Timer.running = False
                self.addTime()
                self.makeScramble()
                self.scramLab.configure(text=Timer.scram)


def main():  # do something to create the times table if it is first time running the program
    root = tk.Tk()  # maybe like try open('solveTimes.db') before the sqlite connect or something
    root.geometry('700x700')
    root.title('PTimer GUI')
    Timer(root)
    root.mainloop()


main()

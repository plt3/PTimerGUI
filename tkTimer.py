import tkinter as tk
import random
from datetime import datetime
from functools import partial
from tkinter import messagebox
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
    penalty = Column(String(4), default='OK')


class Edit:
    def __init__(self, master, labText):
        self.master = master
        self.master.geometry('580x320')
        self.master.title('Add Penalty')

        self.timeId = int(labText[:labText.index(':')])
        self.timeObj = session.query(TimeModel).filter_by(id=self.timeId).first()

        self.idLab = tk.Label(self.master, text=f'Solve {self.timeObj.id}:', font=('TkDefaultFont', 18))
        self.idLab.pack(pady=(10, 0))
        self.timeLab = tk.Label(self.master, text=Timer.niceTime(self.timeObj.time, Timer.precision, penalty=self.timeObj.penalty, dnfTime=True), font=('TkDefaultFont', 30), pady=20)
        self.timeLab.pack()
        self.scramLab = tk.Label(self.master, text=f'Scramble: {self.timeObj.scramble}', font=('TkDefaultFont', 18))
        self.scramLab.pack()
        niceDate = self.timeObj.date.strftime('%m-%d-%Y %H:%M:%S')
        self.dateLab = tk.Label(self.master, text=f'Date: {niceDate}', font=('TkDefaultFont', 18))
        self.dateLab.pack(pady=(10, 0))

        self.penaltyFrame = tk.Frame(self.master, borderwidth=1, relief='solid')
        self.penaltyLab = tk.Label(self.penaltyFrame, text='Penalty:', font=('TkDefaultFont', 18), padx=10, pady=10)
        self.penaltyLab.grid(row=0, column=0)

        for index, penalty in enumerate(['OK', '+2', 'DNF']):
            penLab = tk.Label(self.penaltyFrame, text=penalty, font=('TkDefaultFont', 18), padx=5, pady=5)
            if penalty == self.timeObj.penalty:
                penLab.configure(background='light gray')
                penLab.bind('<Enter>', partial(Timer.changeBackground, static=True))
                penLab.bind('<Leave>', partial(Timer.changeBackground, static=True))
            else:
                penLab.bind('<Enter>', Timer.changeBackground)
                penLab.bind('<Leave>', Timer.changeBackground)

            penLab.bind('<Button-1>', self.editTime)
            penLab.grid(row=0, column=index + 1, sticky=tk.N + tk.S)

        self.penaltyFrame.pack(pady=(10, 20))

        self.bottomFrame = tk.Frame(self.master)
        self.deleteButton = tk.Button(self.bottomFrame, text='Delete solve', font=('TkDefaultFont', 18), padx=5, pady=5, command=self.deleteSolve)
        self.deleteButton.grid(row=0, column=0, padx=(0, 10))
        self.exitButton = tk.Button(self.bottomFrame, text='Done', font=('TkDefaultFont', 18), padx=5, pady=5, command=self.master.destroy)
        self.exitButton.grid(row=0, column=1)
        self.bottomFrame.pack()

    def deleteSolve(self):
        confirmDelete = messagebox.askokcancel('Confirm deletion', 'Are you sure you want to delete this solve?')
        if confirmDelete:
            session.delete(self.timeObj)
            session.commit()
            aboveTimes = session.query(TimeModel).filter(TimeModel.id > self.timeObj.id).all()
            for time in aboveTimes:
                time.id -= 1
            session.commit()
            self.master.destroy()

            if not aboveTimes:
                Timer.timeLabel.configure(text='0.00')

            if len(session.query(TimeModel).all()) < 10:  # shrink times list if < 10 times in the database
                Timer.timesLabs[-1].destroy()
                del Timer.timesLabs[-1]

            Timer.refreshTimes()

    def editTime(self, event):
        for widget in self.penaltyFrame.grid_slaves():
            if widget['text'] != 'Penalty:':
                widget.configure(background='White')
                widget.bind('<Enter>', Timer.changeBackground)
                widget.bind('<Leave>', Timer.changeBackground)

        event.widget.configure(background='light gray')
        event.widget.bind('<Enter>', partial(Timer.changeBackground, static=True))
        event.widget.bind('<Leave>', partial(Timer.changeBackground, static=True))

        self.timeObj.penalty = event.widget['text']
        session.commit()
        # the label change lags a little bit if you don't click the physical mouse but ehhhhhh
        self.timeLab.configure(text=Timer.niceTime(self.timeObj.time, Timer.precision, penalty=self.timeObj.penalty, dnfTime=True))
        Timer.refreshTimes()


class Timer:
    timesLabs = []
    timeLabel = ''
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
        Timer.timeLabel = tk.Label(self.master, text=f'0.{zeros}', font=('TkDefaultFont', 50))
        Timer.timeLabel.grid(row=1, column=1, pady=20)

        self.timesFrame = tk.Frame(self.master, borderwidth=1, relief='solid')
        self.timesTitle = tk.Label(self.timesFrame, text='Times:', font=('TkDefaultFont', 18))
        self.timesTitle.grid(row=0, column=0)

        rawLast = session.query(TimeModel).order_by(TimeModel.id.desc())

        for index, timeObj in enumerate(rawLast.limit(10).all()):
            timeLab = tk.Label(self.timesFrame, text=f'{timeObj.id}: {Timer.niceTime(timeObj.time, Timer.precision, penalty=timeObj.penalty)}')
            timeLab.bind('<Button-1>', self.editTime)
            timeLab.bind('<Enter>', Timer.changeBackground)
            timeLab.bind('<Leave>', Timer.changeBackground)
            timeLab.grid(row=index + 1, column=0, sticky=tk.W + tk.E)
            Timer.timesLabs.append(timeLab)

        self.timesFrame.grid(row=1, column=0)

    def editTime(self, event):
        self.editWindow = tk.Toplevel(self.master)
        self.editApp = Edit(self.editWindow, event.widget['text'])

    @staticmethod
    def refreshTimes():
        rawLast = session.query(TimeModel).order_by(TimeModel.id.desc()).limit(10).all()
        if Timer.timeLabel['text'] != '0.00':
            Timer.timeLabel.configure(text=Timer.niceTime(rawLast[0].time, precision=Timer.precision, penalty=rawLast[0].penalty))
        for timeObj, timeLab in zip(rawLast, Timer.timesLabs):
            timeLab.configure(text=f'{timeObj.id}: {Timer.niceTime(timeObj.time, precision=Timer.precision, penalty=timeObj.penalty)}')

    @staticmethod
    def changeBackground(event, static=False):  # highlight time cell when mouse is over it
        if not static:
            if event.widget['background'] == 'White':
                event.widget.configure(background='light gray')
            else:
                event.widget.configure(background='White')

    def openOptions(self):  # let this control how many times to show in the list?
        pass  # but like probably open up different window (so different class)
        # make these choices register in the db so that they are saved from session to session
        # number precision, amount of times to show, color theme, timer font

    def makeScramble(self):  # generate random move 3x3 scramble
        scramble = ''
        i = 0
        prevchoice = 'Z'
        oldchoice = 'X'
        while True:
            choice = random.choice(Timer.moveslist)
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
        timeObj = TimeModel(time=Timer.solveFloat, scramble=Timer.scram, date=Timer.solveStart)
        session.add(timeObj)  # add time to database
        session.commit()

        if len(Timer.timesLabs) < 10:  # dynamically add labels if < 10 times in the database
            timeLab = tk.Label(self.timesFrame)
            timeLab.bind('<Button-1>', self.editTime)
            timeLab.bind('<Enter>', Timer.changeBackground)
            timeLab.bind('<Leave>', Timer.changeBackground)
            timeLab.grid(row=len(Timer.timesLabs) + 1, column=0, sticky=tk.W + tk.E)
            Timer.timesLabs.append(timeLab)

        oldText = f'{timeObj.id}: {Timer.niceTime(Timer.solveFloat, Timer.precision)}'

        for label in Timer.timesLabs:  # update the labels saying the times
            prevText = label['text']
            label.configure(text=oldText)
            oldText = prevText

    @staticmethod
    def niceTime(secs, precision, penalty='OK', dnfTime=False):
        if penalty == 'DNF' and not dnfTime:
            return 'DNF'
        elif penalty == '+2':
            secs += 2

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
            donestr = joinedStr + ''.join(endZeros[len(missing):])
        except ValueError:
            donestr = joinedStr + '.' + ''.join(endZeros)

        if penalty == '+2':
            return donestr + '+'
        elif penalty == 'DNF':
            return f'DNF({donestr})'
        else:
            return donestr

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
                Timer.timeLabel.configure(text=Timer.niceTime(timeFloat, Timer.precision))
                self.master.after(10, self.timeIt)
            else:  # to stop timer
                Timer.solveFloat = timeFloat
                Timer.timeLabel.configure(text=Timer.niceTime(Timer.solveFloat, Timer.precision))
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

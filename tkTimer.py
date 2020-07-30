import tkinter as tk
import random
from datetime import datetime
from runTimer import session
from models import TimeModel, PreferencesModel
from editWindow import Edit
from optionsWindow import Options
from averagesWindow import Average
from colorMap import colorThemes


class Timer:
    userChoice = session.query(PreferencesModel).first()
    timesLabs = []
    avgsLabs = []
    timeLabel = ''
    scram = ''
    solveStart = 0
    solveFloat = 0
    running = False
    # user's choices are values below
    precision = userChoice.precision
    color = userChoice.colorTheme
    avg1 = userChoice.avg1
    avg2 = userChoice.avg2

    def __init__(self, master):
        Timer.master = master
        Timer.master.configure(background=colorThemes[Timer.color]['normal'])
        Timer.master.bind('<Key>', self.timeIt)  # key or space?
        self.optsBut = tk.Button(Timer.master, text='Options', command=self.openOptions,
                                 font=('TkDefaultFont', 18), padx=10, pady=10)
        self.optsBut.grid(row=0, column=0, padx=20, pady=20)
        self.makeScramble()
        self.scramLab = tk.Label(Timer.master, text=Timer.scram, font=('TkDefaultFont', 24),
                                 borderwidth=1, relief='solid', padx=10, pady=10, width=40, background=colorThemes[Timer.color]['dark'])
        self.scramLab.grid(row=0, column=1, padx=(0, 40), pady=20)
        zeros = ''.join(['0' for i in range(Timer.precision)])
        Timer.timeLabel = tk.Label(Timer.master, text=f'0.{zeros}', font=('TkDefaultFont', 70), background=colorThemes[Timer.color]['normal'])
        Timer.timeLabel.grid(row=1, column=1, pady=20)

        self.bigTimesFrame = tk.Frame(Timer.master, borderwidth=1, relief='solid')

        self.timesTitle = tk.Label(self.bigTimesFrame, text='Times:', font=('TkDefaultFont', 24), pady=3, background=colorThemes[Timer.color]['dark'])
        self.timesTitle.pack(fill='both')

        Timer.timesCanvas = tk.Canvas(self.bigTimesFrame, borderwidth=0, height=330, background=colorThemes[Timer.color]['dark'])  # good height to hold 10 times
        Timer.timesFrame = tk.Frame(Timer.timesCanvas)
        self.vsb = tk.Scrollbar(self.bigTimesFrame, orient='vertical', command=Timer.timesCanvas.yview)
        Timer.timesCanvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side='right', fill='y')
        Timer.timesCanvas.pack()
        Timer.timesCanvas.create_window((0, 0), window=Timer.timesFrame, anchor='nw', tags='Timer.timesFrame')

        Timer.timesFrame.bind('<Configure>', self.onFrameConfigure)

        rawLast = session.query(TimeModel).order_by(TimeModel.id.desc()).all()
        maxChars = 8  # good start to have 'times' label fit well

        for index, timeObj in enumerate(rawLast):
            labText = f'{timeObj.id}: {Timer.niceTime(timeObj.time, Timer.precision, penalty=timeObj.penalty)}'
            timeLab = tk.Label(Timer.timesFrame, text=labText, font=('TkDefaultFont', 18), padx=3, pady=3, background=colorThemes[Timer.color]['dark'])
            timeLab.bind('<Button-1>', self.editTime)
            timeLab.bind('<Enter>', Timer.changeBackground)
            timeLab.bind('<Leave>', Timer.changeBackground)
            timeLab.grid(row=index + 1, column=0, sticky=tk.W + tk.E)
            Timer.timesLabs.append(timeLab)

            if len(labText) > maxChars:
                maxChars = len(labText)

        Timer.timesCanvas.configure(width=maxChars * 10)  # this is a good estimate for the width of the canvas

        self.bigTimesFrame.grid(row=1, column=0, padx=(10, 0))

        self.averagesFrame = tk.Frame(Timer.master, borderwidth=1, relief='solid')

        for i in range(2):
            quickAvgLab = tk.Label(self.averagesFrame, text='', font=('TkDefaultFont', 24), background=colorThemes[Timer.color]['dark'], padx=6, pady=3)
            quickAvgLab.pack(fill='both')
            Timer.avgsLabs.append(quickAvgLab)

        Timer.refreshAverages()
        self.averagesFrame.grid(row=2, column=1, pady=(0, 40))

    def onFrameConfigure(self, event):
        Timer.timesCanvas.configure(scrollregion=Timer.timesCanvas.bbox('all'))

    def editTime(self, event):
        self.editWindow = tk.Toplevel(Timer.master)
        self.editApp = Edit(self.editWindow, event.widget['text'])

    @staticmethod
    def showAverage(event):
        Timer.averagesWindow = tk.Toplevel(Timer.master)
        Timer.editApp = Average(Timer.averagesWindow, event.widget['text'])

    @staticmethod
    def refreshAll():
        Timer.userChoice = session.query(PreferencesModel).first()
        Timer.precision = Timer.userChoice.precision
        Timer.color = Timer.userChoice.colorTheme
        Timer.avg1 = Timer.userChoice.avg1
        Timer.avg2 = Timer.userChoice.avg2

        Timer.refreshTimes()
        Timer.refreshAverages()

        Timer.master.configure(background=colorThemes[Timer.color]['normal'])

        for widget in Timer.master.grid_slaves():
            if widget.winfo_class() == 'Frame':
                for subWidget in widget.pack_slaves():
                    if subWidget.winfo_class() == 'Canvas':
                        for subSubWidget in list(subWidget.children.items())[0][1].grid_slaves():
                            subSubWidget.configure(background=colorThemes[Timer.color]['dark'])
                    subWidget.configure(background=colorThemes[Timer.color]['dark'])
            else:
                try:
                    float(widget['text'])
                    widget.configure(background=colorThemes[Timer.color]['normal'])
                except Exception:
                    if widget['text'].endswith('+') or widget['text'] == 'DNF':
                        widget.configure(background=colorThemes[Timer.color]['normal'])
                    else:
                        widget.configure(background=colorThemes[Timer.color]['dark'])

    @staticmethod
    def refreshTimes():
        rawLast = session.query(TimeModel).order_by(TimeModel.id.desc()).all()
        zeros = ''.join(['0' for i in range(Timer.precision)])
        try:
            if float(Timer.timeLabel['text']):
                Timer.timeLabel.configure(text=Timer.niceTime(rawLast[0].time, precision=Timer.precision, penalty=rawLast[0].penalty))
            else:
                Timer.timeLabel.configure(text=f'0.{zeros}')
        except ValueError:
            Timer.timeLabel.configure(text=Timer.niceTime(rawLast[0].time, precision=Timer.precision, penalty=rawLast[0].penalty))

        maxChars = 8

        for timeObj, timeLab in zip(rawLast, Timer.timesLabs):
            labText = f'{timeObj.id}: {Timer.niceTime(timeObj.time, precision=Timer.precision, penalty=timeObj.penalty)}'
            timeLab.configure(text=labText)

            if len(labText) > maxChars:
                maxChars = len(labText)

        Timer.timesCanvas.configure(width=maxChars * 10)

    @staticmethod
    def refreshAverages():
        tup1 = (Timer.avg1[0], int(Timer.avg1[2:]))
        tup2 = (Timer.avg2[0], int(Timer.avg2[2:]))

        maxToGet = max(tup1[1], tup2[1])
        minToGet = min(tup1[1], tup2[1])

        if tup1[1] > tup2[1]:
            longest = tup1
        else:
            longest = tup2

        lastNTimes = session.query(TimeModel).order_by(TimeModel.id.desc()).limit(maxToGet).all()

        mostTimes = []

        for object in lastNTimes:
            if object.penalty == 'DNF':
                mostTimes.append('DNF')
            elif object.penalty == '+2':
                mostTimes.append(object.time + 2)
            else:
                mostTimes.append(object.time)

        toCalculate = {}

        for tuple in [tup1, tup2]:
            if tuple == longest:
                toCalculate[tuple] = mostTimes
            else:
                toCalculate[tuple] = mostTimes[:minToGet]

        for avg, times in toCalculate.items():
            if avg[0] == 'a':
                toCalculate[avg] = sorted(times, key=lambda v: (isinstance(v, str), v))[1:-1]

        for text, tup, label in [(Timer.avg1, tup1, Timer.avgsLabs[0]), (Timer.avg2, tup2, Timer.avgsLabs[1])]:
            times = toCalculate[tup]
            try:
                if len(lastNTimes) < tup[1]:
                    label.configure(text=f'{text}: -')
                    label.unbind('<Button-1>')
                    label.unbind('Enter>')
                    label.unbind('<Leave>')
                    continue

                avg = Timer.niceTime(sum(times) / len(times), Timer.precision)
                label.configure(text=f'{text}: {avg}')
            except TypeError:
                label.configure(text=f'{text}: DNF')

            label.bind('<Button-1>', Timer.showAverage)  # only clickable if average is defined
            label.bind('<Enter>', Timer.changeBackground)
            label.bind('<Leave>', Timer.changeBackground)

    @staticmethod
    def changeBackground(event, static=False):  # highlight time cell when mouse is over it
        if not static:
            if event.widget['background'] == colorThemes[Timer.color]['dark']:
                event.widget.configure(background=colorThemes[Timer.color]['select'])
            else:
                event.widget.configure(background=colorThemes[Timer.color]['dark'])

    def openOptions(self):
        self.optionsWindow = tk.Toplevel(Timer.master)
        self.optionsApp = Options(self.optionsWindow)

    def makeScramble(self):  # generate random move 3x3 scramble
        opposites = {'U': 'D', 'F': 'B', 'L': 'R', 'D': 'U', 'B': 'F', 'R': 'L'}
        moveslist = [a + b for a in ['U', 'D', 'F', 'B', 'L', 'R'] for b in ['', "'", '2']]
        scramble = ''
        i = 0
        prevchoice = 'Z'
        oldchoice = 'X'
        while True:
            choice = random.choice(moveslist)
            if i == 20:
                break
            elif choice[0] == prevchoice[0]:
                continue
            elif opposites[choice[0]] == prevchoice[0] and choice[0] == oldchoice[0]:
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

        timeLab = tk.Label(Timer.timesFrame, text='', font=('TkDefaultFont', 18), padx=3, pady=3, background=colorThemes[Timer.color]['dark'])  # add new time label
        timeLab.bind('<Button-1>', self.editTime)
        timeLab.bind('<Enter>', Timer.changeBackground)
        timeLab.bind('<Leave>', Timer.changeBackground)
        timeLab.grid(row=len(Timer.timesLabs) + 1, column=0, sticky=tk.W + tk.E)
        Timer.timesLabs.append(timeLab)

        oldText = f'{timeObj.id}: {Timer.niceTime(Timer.solveFloat, Timer.precision)}'
        maxChars = len(oldText)

        for label in Timer.timesLabs:  # update the labels saying the times
            prevText = label['text']
            label.configure(text=oldText)

            if len(prevText) > maxChars:
                maxChars = len(prevText)

            oldText = prevText

        Timer.timesCanvas.configure(width=maxChars * 10)

        Timer.refreshAverages()

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
                Timer.master.after(10, self.timeIt)
        else:
            elapsed = datetime.now() - Timer.solveStart
            timeFloat = elapsed.seconds + elapsed.microseconds / 1000000

            if not event:  # for time to update itself during timing
                Timer.timeLabel.configure(text=Timer.niceTime(timeFloat, Timer.precision))
                Timer.master.after(10, self.timeIt)
            else:  # to stop timer
                Timer.solveFloat = timeFloat
                Timer.timeLabel.configure(text=Timer.niceTime(Timer.solveFloat, Timer.precision))
                Timer.running = False
                self.addTime()
                self.makeScramble()
                self.scramLab.configure(text=Timer.scram)

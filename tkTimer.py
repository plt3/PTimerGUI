import tkinter as tk
import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Float, Integer
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


class Timer:  # figure out key release
    opposites = {'U': 'D', 'F': 'B', 'L': 'R', 'D': 'U', 'B': 'F', 'R': 'L'}
    moveslist = [a + b for a in ['U', 'D', 'F', 'B', 'L', 'R'] for b in ['', "'", '2']]
    start = 0
    stop = 0
    running = False

    def __init__(self, master):
        self.master = master
        self.master.bind('<Key>', self.timeIt)  # key or space?
        self.scrambleLabel = tk.Label(self.master, text=self.makeScramble(), font=('TkDefaultFont', 18))
        self.scrambleLabel.pack(pady=(20, 0))
        self.timeLabel = tk.Label(self.master, text='00.00', font=('TkDefaultFont', 50))
        self.timeLabel.pack(pady=20)
        self.timesTitle = tk.Label(self.master, text='Times:', font=('TkDefaultFont', 18))
        self.timesTitle.pack()
        rawLast = session.query(TimeModel).order_by(TimeModel.id.desc())
        lastList = [str(t.time) for t in rawLast.limit(10).all()]
        lastTimes = '\n'.join(lastList)
        self.timesList = tk.Label(self.master, text=lastTimes)
        self.timesList.pack()

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

        return scramble.rstrip()

    def addTime(self):
        doneTime = float(self.timeLabel['text'])  # update last 10 times label
        last = self.timesList['text'].split('\n')
        newList = [last[i - 1] if i else str(doneTime) for i in range(len(last))]
        newTimes = '\n'.join(newList)
        self.timesList.configure(text=newTimes)

        timeObj = TimeModel(time=doneTime)  # add time to database
        session.add(timeObj)
        session.commit()

    def timeIt(self, *event):
        if not Timer.running:
            if event:  # to start timer
                Timer.start = datetime.now()
                Timer.running = True
                self.master.after(10, self.timeIt)
        else:
            if not event:  # for time to update itself during timing
                elapsed = str(datetime.now() - Timer.start)
                self.timeLabel.configure(text=elapsed[5:-4])
                self.master.after(10, self.timeIt)
            else:  # to stop timer
                Timer.running = False
                self.scrambleLabel.configure(text=self.makeScramble())
                self.addTime()

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


def main():  # do something to create the times table if it is first time running the program
    root = tk.Tk()  # maybe like try open('solveTimes.db') before the sqlite connect or something
    root.geometry('500x500')
    root.title('PTimer GUI')
    Timer(root)
    root.mainloop()


main()

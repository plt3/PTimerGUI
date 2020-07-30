import tkinter as tk
import datetime
from runTimer import session
from models import TimeModel
from colorMap import colorThemes


class Average:
    def __init__(self, master, labText):
        from tkTimer import Timer  # need this in every function to avoid circular import
        self.master = master
        self.master.configure(background=colorThemes[Timer.color]['normal'])

        avgType, avgTime = labText[:labText.index(':')], labText[labText.index(':') + 2:]
        length = int(avgType[2:])
        self.master.title(f'Current {avgType}')

        times = session.query(TimeModel).order_by(TimeModel.id.desc()).limit(length).all()
        oldest = times[-1].date.strftime('%m-%d-%Y %H:%M:%S')
        newest = times[0].date + datetime.timedelta(seconds=times[0].time)

        titleText = f'Mean of {length}' if avgType.startswith('m') else f'Average of {length}'

        if times[0].date.day == times[-1].date.day:
            niceNewest = newest.strftime('%H:%M:%S')
        else:
            niceNewest = newest.strftime('%m-%d-%Y %H:%M:%S')

        titleText += f' from {oldest} to {niceNewest}'

        self.titleLab = tk.Label(self.master, text=titleText, background=colorThemes[Timer.color]['normal'], font=('TkDefaultFont', 14, 'bold'))
        self.timeLab = tk.Label(self.master, text=f'Time: {avgTime}', background=colorThemes[Timer.color]['normal'], font=('TkDefaultFont', 14, 'bold'))
        self.titleLab.pack(pady=(20, 0))
        self.timeLab.pack()

        self.timesFrame = tk.Frame(self.master, background=colorThemes[Timer.color]['normal'])
        self.timesTitle = tk.Label(self.timesFrame, text='Times list:', background=colorThemes[Timer.color]['normal'], font=('TkDefaultFont', 14, 'bold'))
        self.timesTitle.grid(row=0, column=0, sticky=tk.W)

        for index, timeObj in enumerate(times[::-1]):
            timeTime = Timer.niceTime(timeObj.time, Timer.precision, penalty=timeObj.penalty, dnfTime=True)
            if times[0].date.day == times[-1].date.day:
                dateDate = timeObj.date.strftime('%H:%M:%S')
            else:
                dateDate = timeObj.date.strftime('%m-%d-%Y %H:%M:%S')
            timeText = f'{index + 1}: {timeTime}  {timeObj.scramble}  at {dateDate}'
            tk.Label(self.timesFrame, text=timeText, background=colorThemes[Timer.color]['normal'], font=('TkDefaultFont', 14, 'bold')).grid(row=index + 1, column=0, stick=tk.W)

        self.timesFrame.pack(padx=20, pady=(0, 20))

        self.exit = tk.Button(self.master, text='Exit', font=('TkDefaultFont', 18), highlightthickness=0, padx=5, pady=5, command=self.master.destroy)
        self.exit.pack(pady=(0, 20))

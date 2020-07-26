import tkinter as tk
from functools import partial
from tkinter import messagebox
from runTimer import session
from models import TimeModel


class Edit:
    def __init__(self, master, labText):
        from tkTimer import Timer  # need this in every function to avod circuar import
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
        from tkTimer import Timer
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

            Timer.timesLabs[-1].destroy()  # shrink the times list
            del Timer.timesLabs[-1]

            Timer.refreshTimes()
            Timer.refreshAverages()

    def editTime(self, event):
        from tkTimer import Timer
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
        Timer.refreshAverages()

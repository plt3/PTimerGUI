import tkinter as tk
from runTimer import session
from tkinter import messagebox
from models import PreferencesModel, TimeModel
from colorMap import colorThemes


class Options:
    def __init__(self, master):
        from tkTimer import Timer
        self.master = master
        self.master.configure(background=colorThemes[Timer.color]['normal'])
        self.master.title('Options')

        self.currentChoice = session.query(PreferencesModel).first()

        self.colorVar = tk.StringVar()
        self.colorVar.set(self.currentChoice.colorTheme)
        opts = colorThemes.keys()

        self.optionsFrame = tk.Frame(self.master, background=colorThemes[Timer.color]['normal'])

        self.colorFrame = tk.Frame(self.optionsFrame, background=colorThemes[Timer.color]['normal'])
        self.colorLabel = tk.Label(self.colorFrame, text='Color theme:', font=('TkDefaultFont', 14, 'bold'), background=colorThemes[Timer.color]['normal'])
        self.colorLabel.pack(side='left')
        self.colorBox = tk.OptionMenu(self.colorFrame, self.colorVar, *opts)
        self.colorBox.config(background=colorThemes[Timer.color]['normal'])
        self.colorBox.pack(side='left')
        self.colorFrame.grid(row=0, column=0, sticky=tk.W)

        self.avg1Var = tk.StringVar()
        self.avg1Var.set(self.currentChoice.avg1[0])

        self.avgsFrame = tk.Frame(self.optionsFrame, background=colorThemes[Timer.color]['normal'])

        self.avg1Label = tk.Label(self.avgsFrame, text='Stat 1:', font=('TkDefaultFont', 14, 'bold'), background=colorThemes[Timer.color]['normal'])
        self.avg1Label.grid(row=0, column=0, pady=(10, 0))
        self.mean1 = tk.Radiobutton(self.avgsFrame, text='mean', variable=self.avg1Var, value='m', background=colorThemes[Timer.color]['normal'])
        self.average1 = tk.Radiobutton(self.avgsFrame, text='average  of ', variable=self.avg1Var, value='a', background=colorThemes[Timer.color]['normal'])
        self.num1 = tk.Scale(self.avgsFrame, from_=3, to=100, orient='horizontal', background=colorThemes[Timer.color]['normal'], length=200)
        self.num1.set(int(self.currentChoice.avg1[2:]))
        self.mean1.grid(row=0, column=1, pady=(10, 0))
        self.average1.grid(row=0, column=2, pady=(10, 0))
        self.num1.grid(row=0, column=3, pady=(10, 0))

        self.avg2Var = tk.StringVar()
        self.avg2Var.set(self.currentChoice.avg2[0])

        self.avg2Label = tk.Label(self.avgsFrame, text='Stat 2:', font=('TkDefaultFont', 14, 'bold'), background=colorThemes[Timer.color]['normal'])
        self.avg2Label.grid(row=1, column=0)
        self.mean2 = tk.Radiobutton(self.avgsFrame, text='mean', variable=self.avg2Var, value='m', background=colorThemes[Timer.color]['normal'])
        self.average2 = tk.Radiobutton(self.avgsFrame, text='average  of ', variable=self.avg2Var, value='a', background=colorThemes[Timer.color]['normal'])
        self.num2 = tk.Scale(self.avgsFrame, from_=3, to=100, orient='horizontal', background=colorThemes[Timer.color]['normal'], length=200)
        self.num2.set(int(self.currentChoice.avg2[2:]))
        self.mean2.grid(row=1, column=1, pady=(10, 0))
        self.average2.grid(row=1, column=2, pady=(10, 0))
        self.num2.grid(row=1, column=3, pady=(10, 0))

        self.avgsFrame.grid(row=1, column=0)

        self.precisionFrame = tk.Frame(self.optionsFrame, background=colorThemes[Timer.color]['normal'])
        self.precisionLabel = tk.Label(self.precisionFrame, text='Time precision:', font=('TkDefaultFont', 14, 'bold'), background=colorThemes[Timer.color]['normal'])
        self.precision = tk.Scale(self.precisionFrame, from_=1, to=6, orient='horizontal', background=colorThemes[Timer.color]['normal'])
        self.precision.set(self.currentChoice.precision)
        self.precisionLabel.grid(row=0, column=0)
        self.precision.grid(row=0, column=1)
        self.precisionFrame.grid(row=2, column=0, sticky=tk.W)

        self.buttonsFrame = tk.Frame(self.optionsFrame, background=colorThemes[Timer.color]['normal'])
        self.submit = tk.Button(self.buttonsFrame, text='Submit', command=self.submitChanges, font=('TkDefaultFont', 18), highlightthickness=0, padx=5, pady=5, background=colorThemes[Timer.color]['normal'])
        self.exit = tk.Button(self.buttonsFrame, text='Exit', font=('TkDefaultFont', 18), highlightthickness=0, padx=5, pady=5, command=self.master.destroy)
        self.deleteAll = tk.Button(self.buttonsFrame, text='Reset session', font=('TkDefaultFont', 18), highlightthickness=0, padx=5, pady=5, command=self.dropAllTimes)
        self.submit.pack(side='left')
        self.exit.pack(side='left', padx=(20, 0))
        self.deleteAll.pack(side='right')
        self.buttonsFrame.grid(row=3, column=0, sticky=tk.W + tk.E, pady=(10, 0))

        self.optionsFrame.pack(padx=20, pady=20)

    def submitChanges(self):
        from tkTimer import Timer
        vals = [self.colorVar.get(), f'{self.avg1Var.get()}o{self.num1.get()}', f'{self.avg2Var.get()}o{self.num2.get()}', self.precision.get()]

        for attribute, value in zip(['colorTheme', 'avg1', 'avg2', 'precision'], vals):
            setattr(self.currentChoice, attribute, value)

        session.commit()

        Timer.refreshAll()
        self.refreshOptions()

    def refreshOptions(self):
        from tkTimer import Timer
        self.master.configure(background=colorThemes[Timer.color]['normal'])
        self.optionsFrame.configure(background=colorThemes[Timer.color]['normal'])
        for widget in self.optionsFrame.grid_slaves():
            widget.configure(background=colorThemes[Timer.color]['normal'])
            for subWidget in widget.pack_slaves():
                subWidget.configure(background=colorThemes[Timer.color]['normal'])
            for subWidget in widget.grid_slaves():
                subWidget.configure(background=colorThemes[Timer.color]['normal'])

    def dropAllTimes(self):
        from tkTimer import Timer
        confirmReset = messagebox.askokcancel('Confirm reset', 'Are you sure you want to delete all solves in this session?')
        if confirmReset:
            session.query(TimeModel).delete()
            session.commit()
            zeros = ''.join(['0' for i in range(Timer.precision)])
            Timer.timeLabel.configure(text=f'0.{zeros}')

            for label in Timer.timesLabs:
                label.destroy()

            Timer.timesLabs.clear()

            Timer.refreshTimes()
            Timer.refreshAverages()

            Timer.timesFrame.configure(background=colorThemes[Timer.color]['dark'])

            self.master.destroy()

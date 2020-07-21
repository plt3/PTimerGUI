import tkinter as tk
import time
from datetime import datetime
from functools import partial
#
# root = tk.Tk()
# root.geometry('400x350')
# root.title('Air Quality Index')
#
#
# class Yo:
#     def __init__(self, master):
#         f = tk.Frame(master)
#         f.pack()
#
#         self.b = tk.Button(f, text='click', command=Yo.myFunc)
#         self.b.pack()
#
#     @staticmethod
#     def myFunc():
#         print('done')
#         # print(f'you clicked {event.x}, {event.y} with {event.char}')
#
#
# # but = tk.Button(root, text='something')
# # root.bind('<Key>', myFunc)
# # but.bind('<space>', myFunc)
# # but.pack()
# Yo(root)
#
# root.mainloop()


class Timer:  # figure out key release
    oldTime = 0
    start = 0
    stop = 0

    def __init__(self, master):
        self.master = master
        self.master.geometry('400x400')
        self.master.title('PTimer GUI')
        self.master.bind('<Key>', self.timeIt)
        # self.button = tk.Button(self.master, text="clicc", command=self.startClock)
        # self.button.pack()
        # self.button2 = tk.Button(self.master, text="stopp", command=self.stopClock)
        # self.button2.pack()
        self.timeLabel = tk.Label(self.master, text='')
        self.timeLabel.pack()

    def timeIt(self, *args):  # this is the one I think (will have to update to be able to run multiple times)
        if args and Timer.start:  # and I'd like to have the timer start on the release of the first spacebar
            Timer.stop = datetime.now()
        else:
            if args and not Timer.start:
                Timer.start = datetime.now()
            elif not (args or Timer.stop):
                elapsed = str(datetime.now() - Timer.start)
                self.timeLabel.configure(text=elapsed[:-4])
            self.master.after(10, self.timeIt)

        # if args:
        #     if not Timer.start:
        #         Timer.start = datetime.now()
        #         self.master.after(10, self.timeIt)
        #     else:
        #         Timer.stop = datetime.now()
        # elif not Timer.stop:
        #     elapsed = str(datetime.now() - Timer.start)
        #     self.timeLabel.configure(text=elapsed[:-4])
        #     self.master.after(10, self.timeIt)

        #
        # if Timer.start == 0:
        #     Timer.start = datetime.now()
        #     self.master.after(10, self.timeIt)
        #     return
        # if not (args or Timer.stop):  # not args and not Timer.stop
        #     elapsed = str(datetime.now() - Timer.start)
        #     self.timeLabel.configure(text=elapsed[:-4])
        #     self.master.after(10, self.timeIt)
        # else:
        #     Timer.stop = datetime.now()

    def printKey(self, event):
        newTime = time.time()
        if Timer.oldTime == 0:
            self.welcome.pack_forget()
        else:
            try:
                self.myLab.pack_forget()
            except AttributeError:
                pass
            self.myLab = tk.Label(self.master, text=f'Time: {newTime - Timer.oldTime}')
            self.myLab.pack()
        Timer.oldTime = newTime

    def startClock(self):
        Timer.start = datetime.now()
        self.updateClock()

    def updateClock(self):
        if Timer.stop != 0:
            self.timeLabel.configure(text=str(Timer.stop - Timer.start)[:-4])
            return
        elapsed = str(datetime.now() - Timer.start)
        self.timeLabel.configure(text=elapsed[:-4])
        self.master.after(10, self.updateClock)

    def stopClock(self):
        Timer.stop = datetime.now()
#
#
# class Timer:  # figure out key release
#     oldTime = 0
#     start = 0
#
#     def __init__(self, master):
#         self.master = master
#         self.master.geometry('400x400')
#         self.master.title('PTimer GUI')
#         App.start = datetime.now()
#         self.master.bind('<Key>', self.updateClock)
#         self.welcome = tk.Label(self.master, text='Press any key to start, then press it again!')
#         self.welcome.pack()
#         self.timeLabel = tk.Label(self.master, text="")
#         self.timeLabel.pack()
#
#     def printKey(self, event):
#         newTime = time.time()
#         if Timer.oldTime == 0:
#             self.welcome.pack_forget()
#         else:
#             try:
#                 self.myLab.pack_forget()
#             except AttributeError:
#                 pass
#             self.myLab = tk.Label(self.master, text=f'Time: {newTime - Timer.oldTime}')
#             self.myLab.pack()
#         Timer.oldTime = newTime
#
#     def updateClock(self, event):
#         elapsed = str(datetime.now() - App.start)
#         self.timeLabel.configure(text=elapsed[:-4])
#         self.master.after(10, lambda x: self.updateClock(1))


class App():
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(self.master, text="")
        self.label.pack()
        App.start = datetime.now()
        self.update_clock()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S:%f")[:-4]
        self.label.configure(text=now)
        self.master.after(10, self.update_clock)


def main():
    root = tk.Tk()
    Timer(root)
    # App(root)
    root.mainloop()


main()
# import tkinter as tk
#
# class Demo1:
#     def __init__(self, master):
#         self.master = master
#         self.frame = tk.Frame(self.master)
#         # frame = tk.Frame(master)
#         self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
#         self.button1.pack()
#         self.frame.pack()
#     def new_window(self):
#         self.newWindow = tk.Toplevel(self.master)
#         self.app = Demo2(self.newWindow)
#
# class Demo2:
#     def __init__(self, master):
#         self.master = master
#         self.frame = tk.Frame(self.master)
#         # frame = tk.Frame(master)
#         self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
#         self.quitButton.pack()
#         self.frame.pack()
#     def close_windows(self):
#         self.master.destroy()
#
# def main():
#     root = tk.Tk()
#     app = Demo1(root)
#     root.mainloop()
#
# if __name__ == '__main__':
#     main()

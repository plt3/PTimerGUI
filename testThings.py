import tkinter as tk
import time
from datetime import datetime


# def step(*event):
#     label['text'] += 1
#
#     if label._repeat_on:
#         root.after(label._repeat_freq, step)
#
#
# def stop(*event):
#     if label._repeat_on:
#         label._repeat_on = False
#         root.after(label._repeat_freq + 1, stop)
#     else:
#         # print('stopped')
#         label._repeat_on = True
#
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     label = tk.Label(root, text=0)
#     label._repeat_freq = 100
#     label._repeat_on = True
#
#     root.bind('<KeyPress-space>', step)
#     root.bind('<KeyRelease-space>', stop)
#
#     label.pack()
#     root.mainloop()


class Timer:
    # startTime = 0
    stopTime = 0
    total = 0
    cont = True
    # lastCont = True
    # secondCont = True
    # contStart = 0

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
    #
    # def startStop(self):
    #     print('\nrecords')
    #     print(Timer.startTime)
    #     print(Timer.stopTime)
    #     print(Timer.stopTime - Timer.startTime)

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

# root = tk.Tk()
# root.geometry('400x350')
# beg = 0
#
#
# def start(event):
#     beg = time.time()
#     print(event.char)
#
#
# def stop(event):
#     print(event.char)
#
#
# root.bind('<space>', start)
# root.bind('<KeyRelease-space>', stop)
#
# root.mainloop()
# class SampleApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         self.text = tk.Text(self)
#         self.text.pack()
#         self.text.bind("<KeyRelease>", self.on_return_release)
#         self.text.bind("<Key>", self.stop)
#
#     def on_return_release(self, event):
#         self.text.insert("end", "boink! ")
#
#     def stop(self, event):
#         return 'break'
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()

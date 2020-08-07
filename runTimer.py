import tkinter as tk
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if not os.path.exists('solveTimes.db'):
    createDb = True
else:
    createDb = False

eng = create_engine('sqlite:///solveTimes.db')
Base = declarative_base()
DBSession = sessionmaker(bind=eng)
session = DBSession()


if __name__ == '__main__':
    if createDb:
        from models import PreferencesModel, meta
        meta.create_all(eng)  # create database if first time running
        pref = PreferencesModel()  # create a row with default preferences if first time running
        session.add(pref)
        session.commit()

    from tkTimer import Timer
    root = tk.Tk()
    root.title('PTimer GUI')
    Timer(root)
    root.mainloop()

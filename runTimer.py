import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///solveTimes.db')
Base = declarative_base()
DBSession = sessionmaker(bind=eng)
session = DBSession()

if __name__ == '__main__':
    from tkTimer import Timer  # need to check that the database exists first to create the tables if need be
    root = tk.Tk()  # maybe like try open('solveTimes.db') before the sqlite connect or something
    root.title('PTimer GUI')
    Timer(root)
    root.mainloop()

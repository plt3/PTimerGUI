from sqlalchemy import Column, Float, Integer, DateTime, String
from runTimer import Base


class TimeModel(Base):
    __tablename__ = 'times'
    id = Column(Integer, primary_key=True)
    time = Column(Float, nullable=False)
    scramble = Column(String(60), nullable=False)
    date = Column(DateTime, nullable=False)
    penalty = Column(String(4), default='OK')


class PreferencesModel(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    colorTheme = Column(String(10), nullable=False, default='dark')
    avg1 = Column(String(10), nullable=False, default='ao5')
    avg2 = Column(String(10), nullable=False, default='ao12')
    precision = Column(Integer, nullable=False, default=2)

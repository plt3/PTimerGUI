from sqlalchemy import Column, Float, Integer, DateTime, String
from runTimer import Base


class TimeModel(Base):
    __tablename__ = 'times'
    id = Column(Integer, primary_key=True)
    time = Column(Float, nullable=False)
    scramble = Column(String(60), nullable=False)
    date = Column(DateTime, nullable=False)
    penalty = Column(String(4), default='OK')

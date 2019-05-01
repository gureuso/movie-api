# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey

from apps.common.database import Base


class TheaterTicket(Base):
    __tablename__ = 'theater_tickets'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    theater_id = Column(Integer(), ForeignKey('theaters.id'))
    showtime_id = Column(Integer())
    x = Column(Integer())
    y = Column(Integer())

    def __init__(self, theater_id=None, showtime_id=None, x=None, y=None):
        self.theater_id = theater_id
        self.showtime_id = showtime_id
        self.x = x
        self.y = y

    def __repr__(self):
        return '<TheaterTicket {}>'.format(self.id)

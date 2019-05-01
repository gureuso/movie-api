# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from apps.common.database import Base


class Theater(Base):
    __tablename__ = 'theaters'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer())
    title = Column(String(10))
    seat = Column(Integer())

    theater_tickets = relationship('TheaterTicket')

    def __init__(self, cinema_id=None, title=None, seat=None):
        self.cinema_id = cinema_id
        self.title = title
        self.seat = seat

    def __repr__(self):
        return '<Theater {}>'.format(self.id)

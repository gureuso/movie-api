# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from apps.common.database import Base


class Showtime(Base):
    __tablename__ = 'showtimes'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    cinema_id = Column(Integer)
    theater_id = Column(Integer, ForeignKey('theaters.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    theater = relationship('Theater')

    def __init__(self, movie_id=None, cinema_id=None, theater_id=None, start_time=None, end_time=None):
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.theater_id = theater_id
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Showtime {}>'.format(self.id)

# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship


from apps.common.database import Base


class Movie(Base):
    __tablename__ = 'movies'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(120))
    director = Column(String(20))
    description = Column(Text)
    poster_url = Column(Text)
    running_time = Column(Integer)
    age_rating = Column(Integer)

    showtimes = relationship('Showtime')

    def __init__(self, title=None, director=None, description=None, poster_url=None, running_time=None, age_rating=None):
        self.title = title
        self.director = director
        self.description = description
        self.poster_url = poster_url
        self.running_time = running_time
        self.age_rating = age_rating

    def __repr__(self):
        return '<Movie {}>'.format(self.id)

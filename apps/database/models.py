# -*- coding: utf-8 -*-
import random
import string
import time

from datetime import datetime

from apps.database.session import db


def get_token():
    random_string = string.ascii_lowercase + string.digits + string.ascii_uppercase
    timestamp = str(time.mktime(datetime.today().timetuple()))
    return ''.join(random.choice(random_string) for _ in range(28)) + timestamp


class CinemaMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30))
    image_url = db.Column(db.Text())
    address = db.Column(db.String(50))
    detail_address = db.Column(db.String(30))

    def __init__(self, title=None, image_url=None, address=None, detail_address=None):
        self.title = title
        self.image_url = image_url
        self.address = address
        self.detail_address = detail_address

    def __repr__(self):
        return '<Cinema {}>'.format(self.id)


class Cinema(db.Model, CinemaMixin):
    __tablename__ = 'cinemas'
    __table_args__ = {'extend_existing': True}


class TestCinema(CinemaMixin):
    __tablename__ = 'test_cinemas'
    __table_args__ = {'extend_existing': True}


class MovieMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    director = db.Column(db.String(20))
    description = db.Column(db.Text)
    poster_url = db.Column(db.Text)
    running_time = db.Column(db.Integer)
    age_rating = db.Column(db.Integer)

    def __init__(self, title=None, director=None, description=None, poster_url=None, running_time=None,
                 age_rating=None):
        self.title = title
        self.director = director
        self.description = description
        self.poster_url = poster_url
        self.running_time = running_time
        self.age_rating = age_rating

    def __repr__(self):
        return '<Movie {}>'.format(self.id)


class Movie(db.Model, MovieMixin):
    __tablename__ = 'movies'
    __table_args__ = {'extend_existing': True}

    showtimes = db.relationship('Showtime')


class TestMovie(db.Model, MovieMixin):
    __tablename__ = 'test_movies'
    __table_args__ = {'extend_existing': True}

    showtimes = db.relationship('TestShowtime')


class ShowtimeMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cinema_id = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __init__(self, movie_id=None, cinema_id=None, theater_id=None, start_time=None, end_time=None):
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.theater_id = theater_id
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Showtime {}>'.format(self.id)


class Showtime(db.Model, ShowtimeMixin):
    __tablename__ = 'showtimes'
    __table_args__ = {'extend_existing': True}

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'))

    theater = db.relationship('Theater')


class TestShowtime(db.Model, ShowtimeMixin):
    __tablename__ = 'test_showtimes'
    __table_args__ = {'extend_existing': True}

    movie_id = db.Column(db.Integer, db.ForeignKey('test_movies.id'))
    theater_id = db.Column(db.Integer, db.ForeignKey('test_theaters.id'))

    theater = db.relationship('TestTheater')


class Test(db.Model):
    __tablename__ = 'tests'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(120))

    def __init__(self, message=None):
        self.message = message

    def __repr__(self):
        return '<Test {0}>'.format(self.message)


class TheaterTicketMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    showtime_id = db.Column(db.Integer())
    x = db.Column(db.Integer())
    y = db.Column(db.Integer())

    def __init__(self, theater_id=None, showtime_id=None, x=None, y=None):
        self.theater_id = theater_id
        self.showtime_id = showtime_id
        self.x = x
        self.y = y

    def __repr__(self):
        return '<TheaterTicket {}>'.format(self.id)


class TheaterTicket(db.Model, TheaterTicketMixin):
    __tablename__ = 'theater_tickets'
    __table_args__ = {'extend_existing': True}

    theater_id = db.Column(db.Integer(), db.ForeignKey('theaters.id'))


class TestTheaterTicket(db.Model, TheaterTicketMixin):
    __tablename__ = 'test_theater_tickets'
    __table_args__ = {'extend_existing': True}

    theater_id = db.Column(db.Integer(), db.ForeignKey('test_theaters.id'))


class TheaterMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cinema_id = db.Column(db.Integer())
    title = db.Column(db.String(10))
    seat = db.Column(db.Integer())

    def __init__(self, cinema_id=None, title=None, seat=None):
        self.cinema_id = cinema_id
        self.title = title
        self.seat = seat

    def __repr__(self):
        return '<Theater {}>'.format(self.id)


class Theater(db.Model, TheaterMixin):
    __tablename__ = 'theaters'
    __table_args__ = {'extend_existing': True}

    theater_tickets = db.relationship('TheaterTicket')


class TestTheater(db.Model, TheaterMixin):
    __tablename__ = 'test_theaters'
    __table_args__ = {'extend_existing': True}

    theater_tickets = db.relationship('TestTheaterTicket')


class UserMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    nickname = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    age = db.Column(db.Integer)
    profile_url = db.Column(db.Text)
    token = db.Column(db.String(40), unique=True, default=get_token())

    def __init__(self, email=None, nickname=None, password=None, phone_number=None, age=None, profile_url=None,
                 token=None):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.phone_number = phone_number
        self.age = age
        self.profile_url = profile_url
        self.token = token

    def __repr__(self):
        return '<User {}>'.format(self.id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}


class TestUser(db.Model, UserMixin):
    __tablename__ = 'test_users'
    __table_args__ = {'extend_existing': True}

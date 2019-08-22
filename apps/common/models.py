# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import and_

from apps.common.time import utc2local
from apps.database.models import Movie, Showtime, TheaterTicket


class Movies:
    def __init__(self, movie_id, selected_date, cinema_id):
        self.movie_id = movie_id
        self.selected_date = selected_date
        self.cinema_id = cinema_id
        self.query_start_time = datetime.strptime(self.selected_date, '%Y-%m-%d') - timedelta(hours=9)
        self.query_end_time = datetime.strptime(self.selected_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(hours=9)

    def get_movies(self):
        if self.cinema_id:
            movies = Movie.\
                query.\
                join(Showtime, and_(Showtime.movie_id == Movie.id, Showtime.cinema_id == self.cinema_id))
        else:
            movies = Movie \
                .query \
                .join(Showtime, Showtime.movie_id == Movie.id) \

        if self.movie_id:
            movies = movies.filter_by(movie_id=self.movie_id)
        return movies.filter(Showtime.start_time >= self.query_start_time, Showtime.end_time < self.query_end_time).all()

    def get_showtimes(self, movie):
        showtime_list = []
        showtimes = Showtime.query.filter(Showtime.start_time >= self.query_start_time,
                                          Showtime.end_time < self.query_end_time, Showtime.movie_id == movie.id).all()
        showtimes = sorted(showtimes, key=lambda movie: movie.start_time)
        for showtime in showtimes:
            theater = showtime.theater
            seat_cnt = TheaterTicket.query.filter_by(theater_id=theater.id, showtime_id=showtime.id).count()
            theater_seat = theater.seat
            theater_seat -= seat_cnt

            showtime_result = showtime.asdict()
            showtime_result['start_time'] = utc2local(showtime_result['start_time']).strftime('%Y%m%d%H%M')
            showtime_result['end_time'] = utc2local(showtime_result['end_time']).strftime('%Y%m%d%H%M')
            showtime_result['theater'] = dict(id=theater.id, cinema_id=theater.cinema_id, title=theater.title,
                                              seat=theater_seat)
            showtime_list.append(showtime_result)
        return showtime_list

    def result(self):
        movies = self.get_movies()
        movies_result = []
        for movie in movies:
            movie_result = movie.asdict()
            movie_result['showtimes'] = self.get_showtimes(movie)
            movies_result.append(movie_result)
        return movies_result

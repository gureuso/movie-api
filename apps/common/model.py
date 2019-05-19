# -*- coding: utf-8 -*-
from sqlalchemy import and_, func

from apps.models.movies import Movie
from apps.models.showtimes import Showtime
from apps.models.theater_tickets import TheaterTicket


class ShowtimesMoviesModel:
    def __init__(self, movie_id, selected_date, cinema_id):
        self.movie_id = movie_id
        self.selected_date = selected_date
        self.cinema_id = cinema_id

    def get_movies(self):
        movies = Movie \
            .query \
            .join(Showtime, and_(Showtime.movie_id == Movie.id, Showtime.cinema_id == self.cinema_id)) \
            .filter(func.date(Showtime.start_time) == self.selected_date)
        if self.movie_id:
            movies = movies.filter_by(movie_id=self.movie_id)
        return movies.all()

    def get_showtimes_as_dict(self, movie):
        showtimes_result = []
        showtimes = Showtime.query.filter(Showtime.start_time.like(self.selected_date+'%'),
                                          Showtime.movie_id == movie.id).all()
        showtimes = sorted(showtimes, key=lambda movie: movie.start_time)
        for showtime in showtimes:
            theater = showtime.theater
            seat_cnt = TheaterTicket.query.filter_by(theater_id=theater.id, showtime_id=showtime.id).count()
            theater_seat = theater.seat
            theater_seat -= seat_cnt

            showtime_result = showtime.asdict()
            showtime_result['start_time'] = showtime_result['start_time'].strftime('%Y%m%d%H%M')
            showtime_result['end_time'] = showtime_result['end_time'].strftime('%Y%m%d%H%M')
            showtime_result['theater'] = dict(id=theater.id, cinema_id=theater.cinema_id, title=theater.title,
                                              seat=theater_seat)
            showtimes_result.append(showtime_result)
        return showtimes_result

    def result(self):
        movies = self.get_movies()
        movies_result = []
        for movie in movies:
            movie_result = movie.asdict()
            movie_result['showtimes'] = self.get_showtimes_as_dict(movie)
            movies_result.append(movie_result)
        return movies_result

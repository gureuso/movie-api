# -*- coding: utf-8 -*-
import unittest2
import json

from datetime import datetime, timedelta
from freezegun import freeze_time

from apps.database.session import db
from apps.controllers.router import app
from apps.database.models import Movie, Cinema, Theater, Showtime


@freeze_time('2019-06-21 12:00:00')
class Test(unittest2.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        now = datetime.now()
        self.movie = Movie(title='movie01', director='director01', description='desc01', poster_url='poster01.jpg',
                           running_time=120, age_rating=12)
        db.session.add(self.movie)
        db.session.commit()

        self.cinema = Cinema(title='cinema01', image_url='image01', address='address01', detail_address='detail01')
        db.session.add(self.cinema)
        db.session.commit()

        self.theater = Theater(cinema_id=self.cinema.id, title='theater01', seat=120)
        db.session.add(self.theater)
        db.session.commit()

        self.showtime = Showtime(movie_id=self.movie.id, cinema_id=self.cinema.id, theater_id=self.theater.id,
                                 start_time=now+timedelta(hours=2), end_time=now+timedelta(hours=4))
        db.session.add(self.showtime)
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.movie)
        db.session.delete(self.cinema)
        db.session.delete(self.theater)
        db.session.delete(self.showtime)
        db.session.commit()

    def test_over_the_time(self):
        with freeze_time('2019-06-22 00:00:00'):
            result = self.app.get('/v1/theaters/{}/showtimes/{}'.format(self.theater.id, self.showtime.id))
            self.assertEqual(result.status_code, 404)
            data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(data['code'], 40400)

    def test_showtime_with_date(self):
        result = self.app.get('/v1/showtimes')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data.decode('utf-8'))['data']
        week = data['week']
        selected = data['selected']
        self.assertEqual(week[0]['date'], '2019-06-21')
        self.assertEqual(selected['date'], '2019-06-21')

        result = self.app.get('/v1/showtimes?date={}'.format('2019-06-22'))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data.decode('utf-8'))['data']
        selected = data['selected']
        self.assertEqual(selected['date'], '2019-06-22')
        movies = data['movies']
        for movie in movies:
            for showtime in movie['showtimes']:
                self.assertNotEqual(showtime['id'], self.showtime.id)


if __name__ == '__main__':
    unittest2.main()

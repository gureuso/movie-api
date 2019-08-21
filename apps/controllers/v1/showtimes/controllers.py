# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import Blueprint, request

from apps.common.models import Movies
from apps.common.response import ok
from apps.common.time import current_time

app = Blueprint('v1_showtimes', __name__, url_prefix='/v1/showtimes')


@app.route('', methods=['get'])
def main():
    week = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}
    week_list = []
    now = current_time()
    now_weekday = now.weekday()

    args = request.args
    movie_id = args.get('movie_id')
    selected_date = args.get('date', now.strftime('%Y-%m-%d'))
    selected_cinema_id = args.get('cinema_id')
    selected = {'date': selected_date, 'cinema_id': selected_cinema_id, 'movie_id': movie_id}

    for i in range(now_weekday, now_weekday+7):
        day = i - now_weekday
        date = now + timedelta(days=day)
        i %= 7
        week_list.append({'weekday': week[i], 'date': date.strftime('%Y-%m-%d')})

    movies = Movies(movie_id=movie_id, selected_date=selected_date, cinema_id=selected_cinema_id).result()
    return ok(dict(week=week_list, selected=selected, movies=movies))

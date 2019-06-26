# -*- coding: utf-8 -*-
from flask import Blueprint

from apps.common.response import ok
from apps.database.models import Movie

app = Blueprint('v1_movies', __name__, url_prefix='/v1/movies')


@app.route('', methods=['get'])
def main():
    movies = Movie.query.all()
    return ok(dict(movies=[movie.asdict() for movie in movies]))


@app.route('/<int:movie_id>', methods=['get'])
def detail(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first().asdict()
    return ok(dict(movie=movie))

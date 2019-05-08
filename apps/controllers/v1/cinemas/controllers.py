# -*- coding: utf-8 -*-
from flask import Blueprint, request

from apps.common.decorator import login_required
from apps.common.response import ok
from apps.models.cinemas import Cinema

app = Blueprint('v1_cinemas', __name__, url_prefix='/v1/cinemas')


@app.route('', methods=['get'])
@login_required
def main():
    args = request.args
    movie_id = args.get('movie_id', 1)

    cinemas = Cinema.query.all()
    return ok(dict(cinemas=[cinema.asdict() for cinema in cinemas], movie_id=movie_id))

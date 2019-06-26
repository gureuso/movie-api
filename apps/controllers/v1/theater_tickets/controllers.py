# -*- coding: utf-8 -*-
from flask import Blueprint, request

from apps.common.response import ok, error
from apps.database.session import db
from apps.database.models import TheaterTicket, Showtime

app = Blueprint('v1_theater_tickets', __name__, url_prefix='/v1/theater_tickets')


@app.route('', methods=['post'])
def create():
    form = request.form
    theater_id = form['theater_id']
    showtime_id = form['showtime_id']
    x = form['x']
    y = form['y']

    showtime = Showtime.query.filter_by(id=showtime_id, theater_id=theater_id).first()
    if not showtime:
        return error(40400)

    theater_ticket = TheaterTicket(theater_id=theater_id, showtime_id=showtime_id, x=x, y=y)
    db.session.add(theater_ticket)
    db.session.commit()
    return ok()

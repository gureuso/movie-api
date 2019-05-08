# -*- coding: utf-8 -*-
from flask import Blueprint, request

from apps.common.decorator import login_required
from apps.common.response import ok, error
from apps.common.database import db_session
from apps.models.theater_tickets import TheaterTicket
from apps.models.showtimes import Showtime

app = Blueprint('v1_theater_tickets', __name__, url_prefix='/v1/theater_tickets')


@app.route('', methods=['post'])
@login_required
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
    db_session.add(theater_ticket)
    db_session.commit()
    return ok()

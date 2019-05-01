# -*- coding: utf-8 -*-
from flask import Blueprint, request

from apps.common.response import ok
from apps.common.database import db_session
from apps.models.theater_tickets import TheaterTicket

app = Blueprint('v1_theater_tickets', __name__, url_prefix='/v1/theater_tickets')


@app.route('', methods=['post'])
def create():
    form = request.form
    theater_id = form['theater_id']
    showtime_id = form['showtime_id']
    x = form['x']
    y = form['y']

    theater_ticket = TheaterTicket(theater_id=theater_id, showtime_id=showtime_id, x=x, y=y)
    db_session.add(theater_ticket)
    db_session.commit()
    return ok()

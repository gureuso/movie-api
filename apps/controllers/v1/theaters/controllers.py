# -*- coding: utf-8 -*-
from flask import Blueprint

from apps.common.decorator import login_required
from apps.common.response import ok, error
from apps.models.showtimes import Showtime
from apps.models.theaters import Theater
from apps.models.theater_tickets import TheaterTicket

app = Blueprint('v1_theaters', __name__, url_prefix='/v1/theaters')


@app.route('/<int:theater_id>/showtimes/<int:showtime_id>', methods=['get'])
@login_required
def detail(theater_id, showtime_id):
    showtime = Showtime.query.filter_by(id=showtime_id, theater_id=theater_id).first()
    if not showtime:
        return error(40400)

    theater = Theater.query.filter_by(id=theater_id).first()

    seats = []
    x, y = 1, 1
    for _ in range(theater.seat):
        data = {
            'seat_number': '{}-{}'.format(x, y),
            'selected_seat': False
        }
        theater_tickets = TheaterTicket.query.filter_by(theater_id=theater_id, showtime_id=showtime_id).all()
        for theater_ticket in theater_tickets:
            if theater_ticket.x == x and theater_ticket.y == y:
                data['selected_seat'] = True
        seats.append(data)
        if y > 9:
            y = 0
            x += 1
        y += 1
    return ok(dict(seats=seats, theater_id=theater_id, showtime_id=showtime_id))

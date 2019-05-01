# -*- coding: utf-8 -*-
from flask import Blueprint

from apps.common.response import ok
from apps.models.theaters import Theater

app = Blueprint('v1_theaters', __name__, url_prefix='/v1/theaters')


@app.route('/<int:theater_id>/showtimes/<int:showtime_id>', methods=['get'])
def detail(theater_id, showtime_id):
    theater = Theater.query.filter_by(id=theater_id).first()

    seats = []
    x, y = 1, 1
    for _ in range(theater.seat):
        data = {
            'seat_number': '{}-{}'.format(x, y),
            'selected_seat': False
        }
        for theater_ticket in theater.theater_tickets:
            if theater_ticket.showtime_id != showtime_id:
                continue
            if theater_ticket.x == x and theater_ticket.y == y:
                data['selected_seat'] = True
        seats.append(data)
        if y > 9:
            y = 0
            x += 1
        y += 1
    return ok(dict(seats=seats, theater_id=theater_id, showtime_id=showtime_id))

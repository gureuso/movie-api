# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from sqlalchemy import or_

from apps.common.response import error
from apps.models.users import User


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return error(40000)
        user = User.query.filter_by(or_(token=token, google_id=token)).first()
        if not user:
            return error(40000)
        return func(user, *args, **kwargs)
    return wrapper

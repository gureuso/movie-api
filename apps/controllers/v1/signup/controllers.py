# -*- coding: utf-8 -*-
import hashlib

from flask import Blueprint, request

from apps.common.database import db_session
from apps.common.response import ok, error
from apps.models.users import User

app = Blueprint('v1_signup', __name__, url_prefix='/v1/signup')


@app.route('', methods=['post'])
def create():
    form = request.form
    email = form['email']
    password = form['password']
    nickname = form['nickname']
    phone = form['phone']
    age = form['age']

    if not (email and password and nickname and phone and age):
        return error(50000)

    user = User.query.filter_by(email=email).first()
    if not user:
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        u = User(email=email, nickname=nickname, password=password, phone_number=phone, age=age)
        db_session.add(u)
        db_session.commit()
    return ok()

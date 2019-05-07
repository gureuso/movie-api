# -*- coding: utf-8 -*-
import hashlib

from flask import Blueprint, request
from sqlalchemy import or_

from apps.common.database import db_session
from apps.common.response import ok, error
from apps.models.users import User

app = Blueprint('v1_signup', __name__, url_prefix='/v1/signup')


@app.route('', methods=['post'])
def create():
    form = request.form
    email = form.get('email')
    password = form.get('password')
    nickname = form.get('nickname')
    phone = form.get('phone')
    age = form.get('age')

    if not (email and password and nickname and phone and age):
        return error(40000)

    user = User.query.filter(or_(User.email == email, User.nickname == nickname)).first()
    if user:
        return error(40000)

    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user = User(email=email, nickname=nickname, password=password, phone_number=phone, age=age)
    db_session.add(user)
    db_session.commit()

    res = {'nickname': user.nickname, 'email': user.email, 'age': user.age, 'phone_number': user.phone_number,
           'profile_url': user.profile_url}
    return ok(res)

# -*- coding: utf-8 -*-
import hashlib

import requests
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from flask import Blueprint, request
from sqlalchemy import or_

from apps.common.response import error, ok
from apps.common.database import db_session
from apps.models.users import User
from config import Config

app = Blueprint('v1_users', __name__, url_prefix='/v1/users')


@app.route('/signin', methods=['post'])
def signin():
    form = request.form
    email = form.get('email')
    password = form.get('password')
    if not (email and password):
        return error(40000)

    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return error(40400)

    res = {'nickname': user.nickname, 'email': user.email, 'age': user.age, 'phone_number': user.phone_number,
           'profile_url': user.profile_url, 'token': user.token}
    return ok(res)


@app.route('/signup', methods=['post'])
def signup():
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
    return ok()


@app.route('/callback', methods=['post'])
def callback():
    id_token = request.form.get('id_token')

    if not id_token:
        return error(50000, 'required id_token')

    try:
        id_info = google_id_token.verify_oauth2_token(
            id_token,
            google_requests.Request(),
            Config.GOOGLE_CLIENT_ID
        )
    except ValueError:
        # wrong id_token
        return error(50000, 'wrong id_token')

    # wrong issuer
    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return error(50000, 'wrong issuer')

    res = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo', {'id_token': id_token})
    data = res.json()

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        user = User(email=data['email'], nickname=data['name'], profile_url=data['picture'])
        db_session.add(user)
        db_session.commit()

    res = {'nickname': user.nickname, 'email': user.email, 'age': user.age, 'phone_number': user.phone_number,
           'profile_url': user.profile_url, 'token': user.token}
    return ok(res)

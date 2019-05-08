# -*- coding: utf-8 -*-
import random
import string
import time

from sqlalchemy import Column, Integer, String, Text
from datetime import datetime

from apps.common.database import Base


def get_token():
    random_string = string.ascii_lowercase + string.digits + string.ascii_uppercase
    timestamp = str(time.mktime(datetime.today().timetuple()))
    return ''.join(random.choice(random_string) for _ in range(28)) + timestamp


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True)
    nickname = Column(String(20), unique=True)
    password = Column(String(255))
    phone_number = Column(String(20))
    age = Column(Integer)
    profile_url = Column(Text)
    token = Column(String(40), unique=True, default=get_token())

    def __init__(self, email=None, nickname=None, password=None, phone_number=None, age=None, profile_url=None,
                 token=None):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.phone_number = phone_number
        self.age = age
        self.profile_url = profile_url
        self.token = token

    def __repr__(self):
        return '<User {}>'.format(self.id)

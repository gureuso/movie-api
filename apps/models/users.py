# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text

from apps.common.database import Base


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

    def __init__(self, email=None, nickname=None, password=None, phone_number=None, age=None, profile_url=None):
        self.email = email
        self.nickname = nickname
        self.password = password
        self.phone_number = phone_number
        self.age = age
        self.profile_url = profile_url

    def __repr__(self):
        return '<User {}>'.format(self.id)

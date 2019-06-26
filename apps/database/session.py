# -*- coding: utf-8 -*-
from dictalchemy import make_class_dictable
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from config import Config
from apps.controllers.router import app

db = SQLAlchemy(app)
make_class_dictable(db.Model)
cache = Redis(host=Config.REDIS_HOST, password=Config.REDIS_PASSWD)


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

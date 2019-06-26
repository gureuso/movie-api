# -*- coding: utf-8 -*-
import unittest2
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from apps.controllers.router import app, db
from config import Config

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """test code"""
    loader = unittest2.TestLoader()
    start_dir = '{0}/apps'.format(Config.ROOT_DIR)
    suite = loader.discover(start_dir)

    runner = unittest2.TextTestRunner()
    runner.run(suite)


@manager.option('-h', '--host', dest='host', default=Config.APP_HOST)
@manager.option('-p', '--port', dest='port', default=Config.APP_PORT)
def runserver(host, port):
    """run flask server"""
    app.run(host=host, port=int(port))

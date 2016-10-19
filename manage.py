#!/usr/bin/env python
import os
from app import db, create_app
from app import models
from flask.ext.script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from gunicorn_wsgi import *

config = os.environ['APP_SETTINGS']
print("Environment from env vars: " + config)


def make_app():
    return create_app(config)


def _make_shell_context():
    """
    so that we can do >>>models.User.query.all() without having to import models every time
    """
    return dict(app=make_app(), db=db, models=models)


# we can pass a function returning an app to the Manager, instead of passing him an app straight away
manager = Manager(make_app)

# Flask local development server vs. Production server
if config in ['development', 'staging']:
    manager.add_command("runserver", Server(host="0.0.0.0"))
else:
    # http://stackoverflow.com/questions/15693192/heroku-node-js-error-web-process-failed-to-bind-to-port-within-60-seconds-of
    # the port 5000 is specific to heroku.
    manager.add_command("runserver", Gunicorn(host="0.0.0.0", port=os.getenv('PORT', 5000)))

manager.add_command("shell", Shell(make_context=_make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """
    enables us to do
    $ python manage.py test
    to run our tests
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def init_db():
    """
    Initialise an empty db and run data population scripts
    """
    try:
        db.session.remove()
        db.create_all()
        from app import db_init # importing it executes it
    except Exception as ex:
        print(str(ex))


@manager.command
def init_empty_db():
    try:
        db.session.remove()
        db.create_all()
    except Exception as ex:
        print(str(ex))


@manager.command
def drop_db():
    db.session.remove()
    db.reflect()
    try:
        db.drop_all()
    except Exception as ex:
        print(str(ex))


@manager.command
def drop_and_init_db():
    drop_db()
    init_db()


@manager.command
def print_tables():
    if len(db.metadata.tables.keys()):
        for t in db.metadata.tables.keys():
            print(t)
    else:
        print("no tables")


if __name__ == '__main__':
    manager.run()

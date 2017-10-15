#!/usr/bin/env python
import os
from app import create_app
from flask_script import Manager, Server
from gunicorn_wsgi import *

try:
    config = os.environ['APP_MODE']
except KeyError:
    print("Set the APP_SETTINGS environmental variable: 'development', 'testing', 'staging', 'production")
    exit(1)

print("Environment from env vars: " + config)


def make_app():
    return create_app(config)


# we can pass a function returning an app to the Manager, instead of passing the Manager an app object
manager = Manager(make_app)

# Flask local development server vs. Production server
if config in ['development', 'staging']:
    manager.add_command("runserver", Server(host="0.0.0.0"))
else:
    # http://stackoverflow.com/questions/15693192/heroku-node-js-error-web-process-failed-to-bind-to-port-within-60-seconds-of
    # the port 5000 is specific to heroku.
    manager.add_command("runserver", Gunicorn(host="0.0.0.0", port=os.getenv('PORT', 5000)))


@manager.command
def test():
    """
    $ python manage.py test
    to run our tests
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

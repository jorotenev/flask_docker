#!/usr/bin/env python
import os
import sys
from os.path import dirname, join
from dotenv import load_dotenv


if os.environ.get("ENV_DOT_FILE"):
    dotenv_path = join(dirname(__file__), os.environ.get("ENV_DOT_FILE"))  # will fail silently if file is missing
    load_dotenv(dotenv_path, verbose=True)
else:
    print("Not using .env file to load env vars")

from app import create_app
from config import EnvironmentName

app_mode = None
try:
    app_mode = os.environ['APP_STAGE']
    print('app mode is %s' % app_mode)
except KeyError:
    print("Set the APP_STAGE environmental variable: %s" % ",".join(EnvironmentName.all_names()))
    exit(1)

app = create_app(app_mode)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    sys.exit(not result.wasSuccessful())



@app.cli.command()
def boom():
    print("command ran in %s" % app.config['APP_STAGE'])

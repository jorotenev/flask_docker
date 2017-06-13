from flask import Flask
from config import config
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from flask_wtf.csrf import CsrfProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
csrf = CsrfProtect()



def _base_app(config_name):
    """
    initialise a barebone flask app.
    if it is needed to create multiple flask apps,
    use this function to create a base app which can be further modified later

    :arg config_name [string] - the name of the environment; must be a key in the "config" dict
    """
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    SSLify(app)

    initRollbar(app, config_name)


    app.jinja_env.globals['datetime'] = datetime

    return app

def create_app(config_name):
    """
    creates the Flask app.
    """
    from app.models import load_normal_user
    app = _base_app(config_name=config_name)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def initRollbar(app,env):
    """
    Rollbar is an exception handling service
    Make sure you have set the ROLLBAR_ACCESS_TOKEN variables.
    If they are not set, initialising will be skipped.
    """
    token = app.config.get('ROLLBAR_ACCESS_TOKEN')

    if not token:
        # if no rollbar credentials are given, silently skip initialising it
        return
    print("Initialising Exception handling")
    import os, rollbar
    from rollbar.contrib import flask as rollbar_flask
    from flask import got_request_exception

    """
    init rollbar module
    this can fail if there's no internet connection or invalid credentials are given
    """
    try:
        rollbar.init(
            token,
            env,
            # server root directory, makes tracebacks prettier
            root=os.path.dirname(os.path.realpath(__file__)),
            # flask already sets up logging
            allow_logging_basic_config=False)
    except Exception as ex:
        print("Rollbar exception handling is not initialised. %s" % str(ex))
        return
    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar_flask.report_exception, app)

    from flask import Request
    # override the default request class, to give additional context to exceptions
    # it will be possible to see for which user the exception occurred
    # if the user is not logged in, a default string will be used as email and id
    class CustomRequest(Request):
        @property
        def rollbar_person(self):
            from flask import current_app
            # 'id' is required, 'username' and 'email' are indexed but optional.
            # all values are strings.
            default_id = "not_logged_in"
            try:
                with current_app.request_context():
                    from flask_login import current_user
                    user_id = current_user.id or default_id
                    email = current_user.email
                assert user_id and email
            except:
                user_id = default_id
                email = "not_logged_in"
            return {'id': user_id, 'email': email}
    app.request_class = CustomRequest

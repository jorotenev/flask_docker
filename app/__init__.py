from flask import Flask
from config import config
# from datetime import datetime
from flask_bootstrap import Bootstrap


def _base_app(config_name):
    """
    initialise a barebone flask app.
    if it is needed to create multiple flask apps,
    use this function to create a base app which can be further modified later

    :arg config_name [string] - the name of the environment; must be a key in the "config" dict
    """
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # app.jinja_env.globals['datetime'] = datetime

    return app


def create_app(config_name):
    """
    creates the Flask app.
    """
    app = _base_app(config_name=config_name)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    # register other blueprints below

    return app


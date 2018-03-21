from flask import Flask


def _base_app(config_name):
    """
    initialise a barebone flask app.
    if it is needed to create multiple flask apps,
    use this function to create a base app which can be further modified later

    :arg config_name [string] - the name of the environment; must be a key in the "config" dict
    """
    from config import configs
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    return app


def create_app(config_name):
    """
    Creates the Flask app.
    """
    from config import EnvironmentName
    print("Creating an app for environment: [%s]" % config_name)

    if config_name not in EnvironmentName.all_names():
        raise KeyError('config_name must be one of [%s]' % ", ".join(EnvironmentName.all_names()))

    app = _base_app(config_name=config_name)

    from .main import main as main_blueprint
    from .api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app

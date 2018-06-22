import os

from dotenv import load_dotenv

# DOT_ENV_FILE holds the name of file in which all environment vars are set.
# If present, we try to load the vars from this file. it will continue gracefully if file not found etc.
dot_env_file = os.environ.get("DOT_ENV_FILE")
if dot_env_file:
    load_dotenv(dot_env_file, verbose=True)


class BaseConfig(object):
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SITE_NAME = os.environ.get("SITE_NAME", "site_name.com")

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(BaseConfig):

    @classmethod
    def init_app(cls, app):
        super(DevelopmentConfig, cls).init_app(app)


class TestingConfig(DevelopmentConfig):
    TESTING = True

    @classmethod
    def init_app(cls, app):
        super(TestingConfig, cls).init_app(app)


class ProductionConfig(BaseConfig):

    @classmethod
    def init_app(cls, app):
        super(ProductionConfig, cls).init_app(app)


class EnvironmentName:
    """
    use this class to refer to names of environments.
    """
    development = 'development'
    testing = 'testing'
    production = 'production'
    default = 'default'

    @classmethod
    def all_names(cls):
        return [attr for attr in dir(cls)
                if not (attr.startswith('__') or attr == 'all_names')]


configs = {
    EnvironmentName.development: DevelopmentConfig,
    EnvironmentName.testing: TestingConfig,
    EnvironmentName.production: ProductionConfig,
    EnvironmentName.default: DevelopmentConfig
}

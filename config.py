# config.py
import os


class BaseConfig(object):

    TESTING = False
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']  # this will fail if the SECRET_KEY environmental variables is not set
    CI = False # are we in a continuous integration environment
    SITE_NAME = os.environ.get("SITE_NAME", "site_name.com")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
 
    @staticmethod
    def init_app(app):
        pass



class TestingConfig(DevelopmentConfig):
    TESTING = True

    @staticmethod
    def init_app(app):
        pass


class StagingConfig(BaseConfig):

    CI = True

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(BaseConfig):

    @staticmethod
    def init_app(app):
        pass


class EnvironmentName:
    """
    use this class to refer to names of environments to ensure you don't mistype a string
    """
    development = 'development'
    testing = 'testing'
    staging = 'staging'
    production = 'production'
    default = 'default'


config = {
    EnvironmentName.development: DevelopmentConfig,
    EnvironmentName.testing: TestingConfig,
    EnvironmentName.staging: StagingConfig,
    EnvironmentName.production: ProductionConfig,
    EnvironmentName.default: DevelopmentConfig
}

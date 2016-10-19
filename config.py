# config.py
import os

class BaseConfig(object):

    TESTING = False
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY'] # this will fail if empty
    CSRF_ENABLED = True

    SITE_NAME = os.environ.get("SITE_NAME", "site_name.com")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Rollbar settings. (Exception handling)
    # Not setting the variable in the .env will effectively disable rollbar
    ROLLBAR_ENDPOINT = "https://api.rollbar.com/api/1/item/"
    ROLLBAR_ACCESS_TOKEN = os.getenv('ROLLBAR_ACCESS_TOKEN')

    """
    Depending on the environment, we initialise the
    redis cache in a different manner. We do that by setting the appropriate
    config variable. Flask-Cache will see which one is set and use it.
    Whatever the env, the post is usually 6379.
    Remove this config var/not setting in the .env will effectively disable the cache
    """
    CACHE_REDIS_PORT = "6379"

    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(BaseConfig):
    DEBUG = True
 
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_SERVICE = "postgres"
    DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )

    CACHE_REDIS_HOST = 'redis'

    @staticmethod
    def init_app(app):
        pass



class TestingConfig(DevelopmentConfig):
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = False
    TESTING = True
    DB_SERVICE = "postgres_test"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DevelopmentConfig.DB_USER, DevelopmentConfig.DB_PASS, DB_SERVICE, DevelopmentConfig.DB_PORT, DevelopmentConfig.DB_NAME
    )

    @staticmethod
    def init_app(app):
        pass


class StagingConfig(BaseConfig):
    """
    Needed to set environment variables. Check the init_app()
    """
    "Codeship & Semaphore-friendly settings"
    DB_NAME = None  # this is set in the test configuration of semaphore
    DB_USER = None
    DB_PASS = None
    DB_SERVICE = "localhost"
    DB_PORT = 5432
    SQLALCHEMY_ECHO = False

    # this is set in the init_app method
    SQLALCHEMY_DATABASE_URI = None

    CACHE_REDIS_HOST = 'localhost'


    @staticmethod
    def init_app(app):

        semaphore = {
            "DB_NAME": "test_db",
            "DB_USER": 'runner',
            'DB_PASS': 'semaphoredb'
        }
        codeship = {
            "DB_NAME": "test",
            "DB_USER":  os.environ.get("PGUSER"),
            'DB_PASS':  os.environ.get('PGPASSWORD', None)
        }
        staging_config = None
        if os.environ.get('SEMAPHORE', False):
            staging_config = semaphore
        elif os.environ.get("CODESHIP", False):
            staging_config = codeship

        for key, val in staging_config.items():
            setattr(StagingConfig, key, val)

        StagingConfig.SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            StagingConfig.DB_USER, StagingConfig.DB_PASS, StagingConfig.DB_SERVICE, StagingConfig.DB_PORT, StagingConfig.DB_NAME
    )


class ProductionConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # for the cache to be enabled, the CACHE_REDIS_PORT must be set in the BaseConfig.
    CACHE_REDIS_URL = os.environ.get("REDIS_URL")

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

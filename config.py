import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app():
        print("starting aplication...")


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    def __init__(self):
        print(
            "THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION."
        )
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    def __init__(self):
        print(
            "THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION."
        )
        self.SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


class ProductionConfig(Config):
    DEBUG = False
    USE_RELOADER = False

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
    "default": DevelopmentConfig,
}

class Config(object):
    SECRET_KEY = b'ZGRbIHvAxp-Yl0TsoXbfLA'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

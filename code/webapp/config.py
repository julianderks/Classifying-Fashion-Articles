
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
    SECRET_KEY= "9as8df(*S*8(das0^S^Df5a67900SA(D*00"
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    ENV="development"
    SECRET_KEY= "9as8df(*S*8(das0^S^Df5a67900SA(D*00"
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
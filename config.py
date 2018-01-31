class Config:
    PROPAGATE_EXCEPTIONS = True

    SECRET_KEY = 'YOUR_SECRET_KEY_HERE'
    DATABASE_PASSWORD = 'YOUR_PASSWORD_HERE'

    SESSION_COOKIE_NAME = 'session_cookie'

    SESSION_COOKIE_PATH = '/'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_REFRESH_EACH_REQUEST = True

    LOGGER_NAME = 'logger.dietr'
    LOGGER_HANDLER_POLICY = 'always'

    APPLICATION_ROOT = None

    PREFERRED_URL_SCHEME = 'http'

    JSON_AS_ASCII = False
    JSON_SORT_KEYS = True

    SESSION_TYPE = 'redis'
    SESSION_REDIS = '127.0.0.1:6379'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

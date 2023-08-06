class Config:
    FIREBASE_API_KEY = 'AIzaSyDBbIiCyAFkz_bZQb0hbP5wFB-ioF6xOyw'
    FIREBASE_AUTH_DOMAIN = 'trail-ml-9e15e.firebaseapp.com'
    GQL_ENDPOINT_URL = ''

    PRIMARY_USER_CONFIG_PATH = 'trailconfig.yml'
    SECONDARY_USER_CONFIG_PATH = '~/.config/trail.yml'


class ProductionConfig(Config):
    GQL_ENDPOINT_URL = 'https://trail-ml-9e15e.ew.r.appspot.com/graphql'


class DevelopmentConfig(Config):
    GQL_ENDPOINT_URL = 'http://127.0.0.1:5002/graphql'

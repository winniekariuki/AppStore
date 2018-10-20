class Config():
    # Parent confuguration file
    DEBUG = False

class Development(Config):
    '''Configuration for development environment'''
    DEBUG = True

class Testing(Config):
    '''Configuration for testing environment'''
    WTF_CSRF_ENABLED = False
    DEBUG = True

class Production(Config):
    '''Configuration for production environment'''
    DEBUG = False

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
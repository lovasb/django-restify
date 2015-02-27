SECRET_KEY = 'verysecret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'restify.db',
    }
}

MIDDLEWARE_CLASSES = ()

INSTALLED_APPS=[
    'restify', 'tests',
]
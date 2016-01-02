DEBUG = True
SECRET_KEY = 'verysecret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIDDLEWARE_CLASSES = (
    'restify.middleware.PostInBodyMiddleware',
)

INSTALLED_APPS=[
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'restify', 'tests',
]

ROOT_URLCONF = 'tests.urls'
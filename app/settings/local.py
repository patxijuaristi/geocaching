from .base import *

SECRET_KEY = 'gqy9bd-qokr5=*eo^#agl*n3j(5za*&hohv*f0%ktb#ffey1k#'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = '/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'app/static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'app/media')

MEDIA_URL = '/media/'
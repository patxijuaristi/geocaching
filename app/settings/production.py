from .base import *
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DJANGO_DEBUG')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': env('DB_NAME'),
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
                'host': env('DB_CLIENT')
        }
    }
}

STATIC_ROOT = '/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'app/static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'app/media')

MEDIA_URL = '/media/'
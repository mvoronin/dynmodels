import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_APP_DIR = os.path.join(BASE_DIR, 'dynmodels/')

SECRET_KEY = 'r&v3ybzk_pe=dg$1sc2d@xumkvjvqo#8-5qttv)3b+-6yyn&!q'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hr',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dynmodels.urls'
WSGI_APPLICATION = 'dynmodels.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_APP_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_APP_DIR, 'media/')
STATICFILES_DIRS = (
    os.path.join(BASE_APP_DIR, 'static-dev/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_APP_DIR, 'templates'),
)
FIXTURE_DIRS = (
    os.path.join(BASE_APP_DIR, 'fixtures'),
)
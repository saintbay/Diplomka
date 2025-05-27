import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-j))kqv11m*r&axucj7-+i@x-tweg%)9i-!fkd_iwybx56jp=*('

DEBUG = True

ALLOWED_HOSTS = []

LOGGING = {

'version' :1 , 
    'disable_existing_loggers':True,
    'filters':{
        'require_debug_false': {
            '()' : 'django.utils.log.RequireDebugFalse',

        },
        'require_debug_true': {
            '()' : 'django.utils.log.RequireDebugTrue',

        },
    },
    'formatters':{
        'simple':{
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S',
        }
    },
    'handlers':{
        'console_dev':{
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ["require_debug_true"]
        },
        'console_prod':{
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'ERROR',
            'filters': ["require_debug_false"]
        },
        'file':{
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':BASE_DIR / 'debug.log',
            'maxBytes':1048576,
            'backupCount':10,
            'formatter':'simple',
        }
    },
    'loggers':{
        'django':{
            'hendlers':['console_dev', 'console_prod'],
        },
        'django.server':{
            'handlers':['file'],
            'level': 'INFO',
            'propagate':True,
        }
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Qyzylorda'

USE_I18N = True

USE_TZ = True
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'home'  
CART_SESSION_ID = 'cart'


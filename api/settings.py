"""
Django settings for api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bu6^b)ie@)t%#sjo14k50_%7$rk$@(k*jg+d71ru25l+8!wrgj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG=True
# TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base_api',
    'django.contrib.admin',
    'mptt',
    'media_tree',
    'bootstrap_pagination',
    'djangosphinx',
    'mathfilters'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'api.urls'

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base_for_api',
        'USER': 'root',
        'PASSWORD': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'assets', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets', 'static')
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'multiuploader.context_processors.booleans',
    # 'api.role_backends.AuthorModelBackend',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

DATETIME_FORMAT = (
    'd.m.Y H:i'
)

DATE_FORMAT = (
    'd.m.Y'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MULTIUPLOADER_FILES_FOLDER = os.path.join(BASE_DIR, 'assets', 'media')

MULTIUPLOADER_FILE_EXPIRATION_TIME = 3600

MULTIUPLOADER_FORMS_SETTINGS = {
    'default': {
        'FILE_TYPES' : ["txt","zip","jpg","jpeg","flv","png"],
        'CONTENT_TYPES' : [
                'image/jpeg',
                'image/png',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/vnd.oasis.opendocument.text',
                'application/vnd.oasis.opendocument.spreadsheet',
                'application/vnd.oasis.opendocument.presentation',
                'text/plain',
                'text/rtf',
                    ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER':5,
        'AUTO_UPLOAD': True,
    },
    'images':{
        'FILE_TYPES' : ['jpg', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'tiff', 'ico' ],
        'CONTENT_TYPES' : [
            'image/gif',
            'image/jpeg',
            'image/pjpeg',
            'image/png',
            'image/svg+xml',
            'image/tiff',
            'image/vnd.microsoft.icon',
            'image/vnd.wap.wbmp',
            ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER':5,
        'AUTO_UPLOAD': True,
    },
    'video':{
        'FILE_TYPES' : ['flv', 'mpg', 'mpeg', 'mp4' ,'avi', 'mkv', 'ogg', 'wmv', 'mov', 'webm' ],
        'CONTENT_TYPES' : [
            'video/mpeg',
            'video/mp4',
            'video/ogg',
            'video/quicktime',
            'video/webm',
            'video/x-ms-wmv',
            'video/x-flv',
            ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER':5,
        'AUTO_UPLOAD': True,
    },
    'audio':{
        'FILE_TYPES' : ['mp3', 'mp4', 'ogg', 'wma', 'wax', 'wav', 'webm' ],
        'CONTENT_TYPES' : [
            'audio/basic',
            'audio/L24',
            'audio/mp4',
            'audio/mpeg',
            'audio/ogg',
            'audio/vorbis',
            'audio/x-ms-wma',
            'audio/x-ms-wax',
            'audio/vnd.rn-realaudio',
            'audio/vnd.wave',
            'audio/webm'
            ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True,
    }
}

MEDIA_TREE_UPLOAD_SUBDIR = 'uploads'


SPHINX_API_VERSION = 0x116
SPHINX_PORT = 9312
SPHINX_SERVER = '127.0.0.1'

SPHINX_ROOT = '/var/sphinx-search/'

SPHINX_CONFIG_TEMPLATE = 'conf/sphinx.html'
DATABASE_ENGINE = 'mysql'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
DATABASE_NAME = 'base_for_api'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
from decouple import config
import dj_database_url
from unipath import Path
from django.utils.translation import ugettext as _
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


PROJECT_DIR = Path(__file__).parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': dj_database_url.config(
      default=config('DATABASE_URL'))
}

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = (
                  'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'south',
    'aefat.activities',
    'aefat.articles',
    'aefat.auth',
    'aefat.core',
    'aefat.feeds',
    'aefat.messages',
    'aefat.questions',
    'aefat.search',
    'aefat.aefat_pages',
    'autofixture',
    'endless_pagination',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aefat.urls'

WSGI_APPLICATION = 'aefat.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr' #default language

TIME_ZONE = 'Europe/Paris'
LANGUAGES = (
    ('fr', 'French'),
    ('en', 'English'),
)

USE_I18N = True

USE_L10N = True

USE_TZ = True
SITE_ID = 2

LOCALE_PATHS = (PROJECT_DIR.child('locale'),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = PROJECT_DIR.parent.child('staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.child('media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/feeds/'

ALLOWED_SIGNUP_DOMAINS = ['*']

FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0644
# one month
SESSION_COOKIE_AGE = 3600*24*30


TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

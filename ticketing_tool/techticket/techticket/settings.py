"""
Django settings for techticket project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--^4)h92%2ukfiq0+ib44w=%gxq^p4@%n4xs5yca4h88#bw0kyn"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'tool.adminuser' # new
# Application definition

INSTALLED_APPS = [
    "django_crontab",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'tool',
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "techticket.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "techticket.wsgi.application"

CRONJOBS = [
    ('*/5 * * * *', 'myapp.cron.my_code')
]


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
    
#    'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'itsm',
#     'USER': 'root',
#     'PASSWORD': 'Admin123',
#     'HOST': '127.0.0.1',
#     'PORT': '3306',
#     'OPTIONS': {
#         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#         }
#    }
# }



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS=[ 
    os.path.join(BASE_DIR, 'static')
]



MEDIA_URL = '/attachments/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'tool/attachments')



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Flag to expire session on browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# #default parameter for mail
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST='smtp.gmail.com'
# EMAIL_HOST_USER = 'securesally@gmail.com'
# EMAIL_HOST_PASSWORD = 'uylgaixacmdwdguc'
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_USE_SSL=False



#default parameter for olateh web server
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


EMAIL_PORT = 465
EMAIL_HOST = 'mail.supremecluster.com'
EMAIL_HOST_USER = 'ankush.n@olatechs.com'
EMAIL_HOST_PASSWORD = '******'
EMAIL_USE_SSL=True

# CRONJOBS = [
#     ('*/1 * * * * ', 'tool.views.home')
# ]

# CRONTAB_COMMAND_SUFFIX = '2>&1'


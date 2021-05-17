"""
Django settings for DjangoV2Demo project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR再嵌套一层会出错
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6zn0+gtyc4r-)5*zzu*#@xc8ct$+-x896zq3#&#7z824m_*xo9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'demo.apps.SuitConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo.apps.DemoConfig',
    'social_django',
    'rest_framework',
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

ROOT_URLCONF = 'DjangoV2Demo.urls'

# JWT
import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10),  # 状态保持10天
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
# 第三方
AUTHENTICATION_BACKENDS = (
    'social_core.backends.weibo.WeiboOAuth2',  # 微博
    'social_core.backends.qq.QQOAuth2',  # QQ
    'social_core.backends.weixin.WeixinOAuth2',  # 微信
    'django.contrib.auth.backends.ModelBackend',
)

# 第三方登录，里面的值是你的开放平台对应的值
SOCIAL_AUTH_WEIBO_KEY = '16839985xx'
SOCIAL_AUTH_WEIBO_SECRET = 'db8252fdcd9b25d007b7ecb637c6adxx'

SOCIAL_AUTH_QQ_KEY = 'xxxxxxx'
SOCIAL_AUTH_QQ_SECRET = 'xxxxxxx'

SOCIAL_AUTH_WEIXIN_KEY = 'xxxxxxx'
SOCIAL_AUTH_WEIXIN_SECRET = 'xxxxxxx'

# 登录成功后跳转到首页
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # social_django
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoV2Demo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 第三方支付

# 支付宝相关配置
ALIPAY_APPID = "20161013006744xx"  # appid
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"  # 沙箱环境,正式环境为alipay
ALIPAY_DEBUG = True  # DEBUG模式
# 应用私钥文件路径
APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'apps/demo/keys/private_2048.txt')
# 支付宝公钥文件路径
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'apps/demo/keys/ali_pay_key_2048.txt')


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
os.makedirs(STATIC_ROOT, exist_ok=True)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
os.makedirs(MEDIA_ROOT, exist_ok=True)

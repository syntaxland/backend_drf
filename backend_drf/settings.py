"""
Django settings for backend_drf project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
# Adding dotenv 
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

#--------------------------------------------------------------------------------------------------
""" 
# AWS Secrets Manager for S3 Media Storages, Secret Keys, DB Env...
import json
import boto3
import base64
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    environment  = event['env']
    secret_name = 'mcdof/store/%s/keys' % environment
    region_name = "us-east-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        if 'SecretString' in secret_value_response:
            secret = json.loads(secret_value_response['SecretString'])
            return secret
        else:
            decode_binary_secret = base64.base64decode(secret_value_response['SecretBinary'])
            return decode_binary_secret
"""
# OR
"""
import os
import json
import boto3
from django.core.exceptions import ImproperlyConfigured

# Helper function to get environment variables or raise an error
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Environment variable '{var_name}' not set"
        raise ImproperlyConfigured(error_msg)

# Load Secrets Manager secrets
def load_secrets():
    secret_name = "your-secret-name"  
    region_name = "your-aws-region"  

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    response = client.get_secret_value(SecretId=secret_name)

    if 'SecretString' in response:
        secret = response['SecretString']
    else:
        secret = json.loads(response['SecretBinary'])

    return json.loads(secret)

# Load secrets from AWS Secrets Manager
secrets = load_secrets()

# Django Secret Key
SECRET_KEY = get_env_variable('SECRET_KEY') or secrets.get('SECRET_KEY')
"""
#--------------------------------------------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# SECRET_KEY = 'django-insecure-_#gopr9mlt-y5v4bi*7shrfhau)&5kyznb9!yjh)9m+t16-0q+'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# ALLOWED_HOSTS = ['localhost', 
#                  'localhost:8000', 
#                  '127.0.0.1', 
#                  '127.0.0.1:8000', 
#                  '54.34.229.79.247', 
#                  'ec2-18-212-11-87.compute-1.amazonaws.com', 
#                  'mcdofglobal.s3-website-us-east-1.amazonaws.com'
#                  ]
ALLOWED_HOSTS = ["*"]

# Application definition 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'whitenoise.runserver_nostatic',  # whitenoise added
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Myapps 
    'app.apps.AppConfig', 
    'payment',
    'user_profile', 
    'send_email_otp',
    'send_reset_password_email',
    'credit_point',  
    'send_email_message',
    'send_message_inbox', 

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    # 'rest_framework_simplejwt.token_blacklist',

    # Google Login Config
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'corsheaders',
    'storages',
]

# Adding JWT Auth
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',  
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=900),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    # 'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=180),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
    # "TOKEN_OBTAIN_SERIALIZER": "app.serializers.MyTokenObtainPairSerializer",
    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
}
  
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",  # Adding third-part corsheaders middleware
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # whitenoise middleware added
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'backend_drf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'backend_drf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

# DATABASES = {
#      'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': int(os.getenv('DB_PORT')),
#      }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': int(os.getenv('DB_PORT')),
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': os.getenv('MONGODB_NAME'),
#         'ENFORCE_SCHEMA': False,
#         'CLIENT': {
#             'host': os.getenv('MONGODB_HOST'),
#             'port': int(os.getenv('MONGODB_PORT')),
#             'username': os.getenv('MONGODB_USER'),
#             'password': os.getenv('MONGODB_PASS'),
#             'authSource': 'admin',
#             # 'authMechanism': 'SCRAM-SHA-1',
#         },
#     },
# }

# AWS RDS (prod)
# Using .env
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': int(os.getenv('DB_PORT')),
#     }
# }

# For AWS Secret Manager
# DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.postgresql',
#            'NAME': secrets.get('DB_NAME'),
#            'USER': secrets.get('DB_USER'),
#            'PASSWORD': secrets.get('DB_PASSWORD'),
#            'HOST': secrets.get('DB_HOST'),
#            'PORT': secrets.get('DB_PORT', '5432'),
#        }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': os.getenv('MONGODB_NAME'),
#         'ENFORCE_SCHEMA': False,
#         'CLIENT': {
#             'host': secrets.get('MONGODB_HOST'),
#             'port': int(secrets.get('MONGODB_PORT')),
#             'username': secrets.get('MONGODB_USER'),
#             'password': secrets.get('MONGODB_PASS'),
#             'authSource': 'admin',
#             # 'authMechanism': 'SCRAM-SHA-1',
#         },
#     },
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') 

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS_ALLOWED_ORIGINS = [
#     "https://mcdofglobal.com",
#     "https://store.mcdofglobal.com",
#     "http://localhost:8000",
#     "http://127.0.0.1:3000",
#     "http://localhost:3000",
#     "http://127.0.0.1:8000",
# ]

CORS_ALLOW_ALL_ORIGINS = True

# setting up s3 storages for media and static  
# from storages.backends.s3boto3 import S3Boto3Storage
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# for sms otp
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

MY_PHONE_NUMBER  = os.getenv('MY_PHONE_NUMBER')

# for captcha
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = os.getenv('RECAPTCHA_REQUIRED_SCORE')

# for email otp
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_SENDER_NAME = os.getenv('EMAIL_SENDER_NAME')

# for email otp api key
SENDINBLUE_API_KEY = os.getenv('SENDINBLUE_API_KEY')
# AWS SNS ARN
AWS_SNS_EMAIL_TOPIC_ARN = os.getenv('SENDINBLUE_API_KEY')
AWS_SNS_REGION = 'us-east-1'
AWS_REGION = 'us-east-1'


PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_PAYMENT_URL = os.getenv('PAYSTACK_PAYMENT_URL')
CALLBACK_URL = os.getenv('CALLBACK_URL')

# for google login option
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', 
    'allauth.account.auth_backends.AuthenticationBackend',
]  
  
# SITE_ID = 1 

# Google OAuth2 settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_OAUTH2_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET'),
            'key': ''
        }
    }
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'YOUR_GOOGLE_CLIENT_ID',
            'secret': 'YOUR_GOOGLE_CLIENT_SECRET',
            'key': ''
        }
    }
}

# Redirect URL after Google login
LOGIN_REDIRECT_URL = '/'  # Replace with your desired URL
# Logout URL
LOGOUT_REDIRECT_URL = '/login'


AUTH_USER_MODEL = 'user_profile.User' 


import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/'.env')
DEBUG=os.getenv('DJANGO_DEBUG','1')=='1'
SECRET_KEY=os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError('DJANGO_SECRET_KEY must be configured when DEBUG is disabled.')
    SECRET_KEY='dev-only-insecure-change-before-deploy'
ALLOWED_HOSTS=[x.strip() for x in os.getenv('DJANGO_ALLOWED_HOSTS','127.0.0.1,localhost').split(',') if x.strip()]
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','boutique','analytics']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='smartshop.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages','boutique.context_processors.cart_count']}}]
WSGI_APPLICATION='smartshop.wsgi.application'
DATABASES={
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='fr-fr'
TIME_ZONE='Africa/Dakar'
USE_I18N=True
USE_TZ=True
STATIC_URL='static/'
STATICFILES_DIRS=[BASE_DIR/'static']
STATIC_ROOT=BASE_DIR/'staticfiles'
STORAGES={
    'default': {'BACKEND':'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND':'whitenoise.storage.CompressedStaticFilesStorage'},
}
MEDIA_URL='media/'
MEDIA_ROOT=BASE_DIR/'media'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='connexion'
LOGIN_REDIRECT_URL='accueil'
LOGOUT_REDIRECT_URL='accueil'
CSRF_COOKIE_SECURE=not DEBUG
SESSION_COOKIE_SECURE=not DEBUG
SECURE_SSL_REDIRECT=not DEBUG
SECURE_HSTS_SECONDS=31536000 if not DEBUG else 0
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
SMARTCUSTOMER_API_URL=os.getenv('SMARTCUSTOMER_API_URL','https://smartcustomer-analytics.onrender.com/api/smartshop/evenements/').strip()
SMARTCUSTOMER_API_TOKEN=os.getenv('SMARTCUSTOMER_API_TOKEN','').strip()
SMARTCUSTOMER_TIMEOUT=int(os.getenv('SMARTCUSTOMER_TIMEOUT','8'))

from config.settings.base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["weddit.eba-be3gdpu7.ap-northeast-2.elasticbeanstalk.com"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.environ["RDS_USERNAME"],
        "PASSWORD": os.environ["RDS_PASSWORD"],
        "HOST": os.environ["RDS_HOSTNAME"],
        "NAME": os.environ["RDS_DB_NAME"],
        "PORT": os.environ["RDS_PORT"],
    }
}


sentry_sdk.init(
    dsn=os.environ["SENTRY_URL"],
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)


# Amazo S3 Setting
DEFAULT_FILE_STORAGE = "config.settings.custom_storages.MediaStorage"
STATICFILES_STORAGE = "config.settings.custom_storages.StaticStorage"
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com"


STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

STATIC_ROOT = "static"

# Media files

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

MEDIA_ROOT = "media"

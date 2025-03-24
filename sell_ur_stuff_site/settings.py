from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url  # For Heroku deployment

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Key for the Stripe API
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# Media storage configuration
print("Loading settings.py")
try:
    DEFAULT_FILE_STORAGE = "sell_ur_stuff_site.storage.CustomS3Boto3Storage"
    print(f"DEFAULT_FILE_STORAGE set to: {DEFAULT_FILE_STORAGE}")
    # Force import and instantiation to catch errors
    from sell_ur_stuff_site.storage import CustomS3Boto3Storage

    print("Successfully imported CustomS3Boto3Storage")
    # Force instantiation
    custom_storage = CustomS3Boto3Storage()
    print("Successfully instantiated CustomS3Boto3Storage")
    # Check default_storage
    from django.core.files.storage import default_storage

    print(f"Storage backend at startup: {default_storage.__class__.__name__}")
except Exception as e:
    print(f"Failed to initialize storage backend: {e}")
    raise
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = "sellyourtuff.s3.amazonaws.com"
MEDIA_URL = "https://sellyourtuff.s3.amazonaws.com/"
print("Finished loading settings.py")

# Manually override default_storage
try:
    from django.core.files.storage import default_storage as default_storage_original
    from sell_ur_stuff_site.storage import CustomS3Boto3Storage

    default_storage = CustomS3Boto3Storage()
    print(f"Manually set default_storage to: {default_storage.__class__.__name__}")
except Exception as e:
    print(f"Failed to manually set default_storage: {e}")
    raise

# Debug settings
DEBUG = (
    os.getenv("DEBUG", "False") == "True" if "DATABASE_URL" not in os.environ else False
)

# Database configuration
if "DATABASE_URL" in os.environ:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
            default="postgres://localhost",
        )
    }
    DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Application definition
ALLOWED_HOSTS = [
    ".herokuapp.com",
    "localhost",
    "127.0.0.1",
]

# Logging configuration for Heroku deployment
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "ERROR",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# This is the URL where the user will be redirected after logging in.
CSRF_TRUSTED_ORIGINS = ["https://sell-ur-stuff-19632c616966.herokuapp.com"]

# Application definition
INSTALLED_APPS = [
    # Custom apps
    "home",
    "sales",
    "market",
    "profiles",
    "contact",
    "widget_tweaks",
    # Third-party apps
    "storages",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Allauth apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers",
]

# Allauth settings for email verification
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Default backend
    "allauth.account.auth_backends.AuthenticationBackend",  # Allauth backend
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "sell_ur_stuff_site.urls"
WSGI_APPLICATION = "sell_ur_stuff_site.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sell_ur_stuff_site.context_processors.unread_notifications",
            ],
        },
    },
]

SITE_ID = 1  # Required by allauth

ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"  # Change to 'mandatory' after testing
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# Use local storage in development
# MEDIA_ROOT = BASE_DIR / "media"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

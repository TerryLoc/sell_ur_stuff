from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url  # For Heroku deployment
import stripe  # For Stripe API

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Key for the Stripe API
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY
    print("Stripe API key configured for production/Heroku.") # This will show in Heroku logs
else:
    # This case should ideally not happen in Heroku if the Config Var is set
    print("CRITICAL: STRIPE_SECRET_KEY is not set in the environment!")

# Manually override default_storage and ensure it persists
try:
    from django.core.files.storage import default_storage as default_storage_original
    from sell_ur_stuff_site.storage import CustomS3Boto3Storage

    # Create a new instance
    new_storage = CustomS3Boto3Storage()
    # Patch the lazy object to use the new instance
    default_storage_original._wrapped = new_storage
    print(
        f"Manually set default_storage to: {default_storage_original.__class__.__name__}"
    )
    # Verify the override
    from django.core.files.storage import default_storage

    print(f"Storage backend after override: {default_storage.__class__.__name__}")
except Exception as e:
    print(f"Failed to manually set default_storage: {e}")
    raise

# Debug settings
LOCAL_DEV = "DATABASE_URL" not in os.environ
DEBUG = os.getenv("DEBUG", "False") == "True" if LOCAL_DEV else False

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
if DEBUG:
    ALLOWED_HOSTS.append('*') # Allow all hosts in debug mode

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
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

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

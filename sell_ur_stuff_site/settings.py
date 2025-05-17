from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# --- Environment-dependent settings ---
# LOCAL_DEV is True if DATABASE_URL is NOT set in the environment.
LOCAL_DEV = "DATABASE_URL" not in os.environ

# DEBUG is True if DEBUG=True in .env AND we are in LOCAL_DEV.
# If DATABASE_URL is set (production/staging), DEBUG is False.
DEBUG = os.getenv("DEBUG", "False").lower() == "true" if LOCAL_DEV else False

print(f"--- Environment Status ---")
print(f"LOCAL_DEV: {LOCAL_DEV}")
print(f"DEBUG: {DEBUG}")
print(f"--- End Environment Status ---")

# --- Database Configuration ---
if not LOCAL_DEV:  # Production or staging with DATABASE_URL
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,  # Common for Heroku Postgres
            default=os.getenv("DATABASE_URL"), # Use DATABASE_URL directly
        )
    }
    # dj_database_url usually infers the engine, but you can be explicit if needed:
    # DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"
    print("Using PostgreSQL database (production/staging).")
else:  # Local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    print("Using SQLite database (local development).")


# --- Storage Configuration ---
if not DEBUG:  # Production settings (S3 for media)
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "eu-west-1") # Example default
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None # Or 'public-read' if media files should be public by default
    AWS_S3_VERIFY = True

    # Default storage for media files in production
    # Ensure 'sell_ur_stuff_site.storage.CustomS3Boto3Storage' is correctly implemented
    # and configured to use the AWS environment variables.
    DEFAULT_FILE_STORAGE = "sell_ur_stuff_site.storage.CustomS3Boto3Storage"

    # Static files storage for production (WhiteNoise handles serving after collectstatic)
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    print("Production Storage: S3 for media (via CustomS3Boto3Storage), WhiteNoise for static files.")

else:  # Local development settings
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
    # Ensure the 'media' directory exists at root for local development

    # WhiteNoise can serve local static files effectively during development
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    print("Development Storage: Local filesystem for media, WhiteNoise for static files.")


# --- General Settings ---
ALLOWED_HOSTS = []
HEROKU_APP_HOSTNAME = os.getenv("sell-ur-stuff-19632c616966.herokuapp.com") 

if not DEBUG:
    if HEROKU_APP_HOSTNAME:
        ALLOWED_HOSTS.append(HEROKU_APP_HOSTNAME)
    # Add any other production domains here
    # ALLOWED_HOSTS.append("yourcustomdomain.com")
    if not ALLOWED_HOSTS: # Fallback if HEROKU_HOSTNAME is not set
        ALLOWED_HOSTS.append("sell-ur-stuff-19632c616966.herokuapp.com") # Hardcode as a last resort
else:
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1", "*"]) # '*' is convenient for local dev

if not DEBUG and not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS cannot be empty in production if HEROKU_HOSTNAME is not set.")


# Logging configuration (Your existing config seems fine for Heroku)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "ERROR"},
    "loggers": {"django": {"handlers": ["console"], "level": "ERROR", "propagate": False}},
}

CSRF_TRUSTED_ORIGINS = []
if not DEBUG and HEROKU_APP_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{HEROKU_APP_HOSTNAME}")
elif not DEBUG: # Fallback if HEROKU_HOSTNAME is not set
     CSRF_TRUSTED_ORIGINS.append("https://sell-ur-stuff-19632c616966.herokuapp.com")


INSTALLED_APPS = [
    "home.apps.HomeConfig",
    "sales.apps.SalesConfig",
    "market.apps.MarketConfig",
    "profiles.apps.ProfilesConfig",
    "contact.apps.ContactConfig",
    "widget_tweaks",
    "storages", # For S3Boto3Storage and other storage backends
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "allauth.socialaccount.providers.google", # Example: only add providers you use
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # Should be high up, after SecurityMiddleware
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
                "sell_ur_stuff_site.context_processors.unread_notifications", # Your custom processor
                # "market.context_processors.categories", # Example if you have other context processors
            ],
        },
    },
]

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Static files (CSS, JavaScript, Images) - Common settings
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")] # For project-wide static files
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") # For collectstatic

# Media files - MEDIA_URL and MEDIA_ROOT are set conditionally earlier based on DEBUG

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
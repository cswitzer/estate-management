from pathlib import Path
from os import path, getenv
import cloudinary
from datetime import timedelta

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

# This is where all our django apps will be stored
APPS_DIR = BASE_DIR / "core_apps"

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
    "phonenumber_field",
    "drf_yasg",
    "djoser",
    "social_django",
    "taggit",
    "django_filters",
    "djcelery_email",
    "cloudinary",
    "django_celery_beat",
]

LOCAL_APPS = [
    "core_apps.issues",
    "core_apps.users",
    "core_apps.common",
    "core_apps.profiles",
    "core_apps.ratings",
    "core_apps.posts",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST"),
        "PORT": getenv("POSTGRES_PORT"),
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"  # absolute path from root

STATIC_ROOT = str(BASE_DIR / "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TAGGIT_CASE_INSENSITIVE = True

AUTH_USER_MODEL = "users.User"

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 10

# Send 'sent' event when a task is sent to the broker
CELERY_TASK_SEND_SENT_EVENT = True

# Enables richer insight into the results of tasks, like worker's hostnames and timestamps
CELERY_RESULT_EXTENDED = True

# Always retry to connect to the result backend (broker) up to 'CELERY_RESULT_BACKEND_MAX_RETRIES' times.
# Connections can fail for a number of reasons, such as network issues, broker downtime, etc.
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True

# Triggers warning if task exceeds a minute, and kills it after 5 minutes
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60

# Used to store periodic tasks in the database. Like cron jobs, but more flexible
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Integration with flower. Sends task events like starting, finishing, etc.
CELERY_WORKER_SEND_TASK_EVENTS = True

CLOUDINARY_CLOUD_NAME = getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)

COOKIE_NAME = "access"
COOKIE_SAMESITE = "Lax"
# The cookie will be sent to any path
# Could have defined it as /supersecret/, then only requests to /supersecret/ would have access to the cookie
COOKIE_PATH = "/"
# Prevents JavaScript from accessing the cookie
COOKIE_HTTPONLY = True
# Sent only over HTTPS
COOKIE_SECURE = getenv("COOKIE_SECURE", "True") == "True"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "core_apps.common.cookie_auth.CookieAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": ("rest_framework.pagination.PageNumberPagination",),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "Default_THROTTLE_RATES": {"anon": "200/day", "user": "500/day"},
}

SIMPLE_JWT = {
    "SIGNING_KEY": getenv("SIGNING_KEY"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    # Used in generated tokens to identify the user
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

DJOSER = {
    "USER_ID_FIELD": "id",
    "LOGIN_FIELD": "email",
    "TOKEN_MODEL": None,
    # Make user pass re_password to /users/
    "USER_CREATE_PASSWORD_RETYPE": True,
    # Send an activation email when a user signs up
    "SEND_ACTIVATION_EMAIL": True,
    # Send a password confirmation email when a user wants to change their password
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    # Make user pass re_new_password to /users/reset_password_confirm/
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    # URL to the frontend activation page where the user can activate their account. Must pass uid and token to djoser
    "ACTIVATION_URL": "activate/{uid}/{token}",
    # URL to the frontend password reset page where the user can reset their password
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",
    # URIs for redirecting back to our website after social authentication
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": getenv("REDIRECT_URIS", "").split(","),
    "SERIALIZERS": {
        "user_create": "core_apps.users.serializers.CreateUserSerializer",
        "current_user": "core_apps.users.serializers.CustomUserSerializer",
    },
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = getenv("GOOGLE_CLIENT_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
# In addition to email and profile, we also want to get the user's first and last name
# This is necessary to create a user in our database
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ["first_name", "last_name"]

AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

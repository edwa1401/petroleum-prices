from petroleum_prices.settings import *

DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'

import os
import shutil
import sys
import coverage

import django
from django.conf import settings
from django.core.management import call_command


def runtests():
    if not settings.configured:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "django_auto_actions",
                "USER": "django",
                "PASSWORD": "django",
                "HOST": "localhost",
                "PORT": "5432",
            }
        }

        settings.configure(
            DATABASES=DATABASES,
            INSTALLED_APPS=(
                "django.contrib.contenttypes",
                "django.contrib.auth",
                "django.contrib.sites",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.admin.apps.SimpleAdminConfig",
                "django.contrib.staticfiles",
                "django_auto_actions",
            ),
            ROOT_URLCONF="",
            MIDDLEWARE=[
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
            ],
            TEMPLATES=[
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
            ],
            DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
            MESSAGE_STORAGE='django.contrib.messages.storage.cookie.CookieStorage',
            SECRET_KEY="super_secret",
        )

    django.setup()

    cov = coverage.Coverage(omit=["*/tests/*", "*/migrations/*"])
    cov.start()

    failures = call_command(
        "test", "django_auto_actions", interactive=False, failfast=False, verbosity=2
    )

    cov.stop()
    cov.save()
    cov.report()

    # Delete the generated migrations folder
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder = os.path.join(BASE_DIR, "migrations")
    shutil.rmtree(folder)

    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests()
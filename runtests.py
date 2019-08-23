import sys

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="django_telegrambot.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "django_telegrambot",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        DJANGO_TELEGRAMBOT={
            'MODE': 'POLLING',  # (Optional [str]) # The default value is WEBHOOK,
            # otherwise you may use 'POLLING'
            # NB: if use polling you must provide to run
            # a management command that starts a worker
            'BOTS': [
                {
                    'TOKEN': '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11',  # Your bot token.
                },
            ],
        },
    )

    try:
        import django

        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback

    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])

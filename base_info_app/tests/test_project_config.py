from importlib import reload
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

import core.settings as project_settings
import core.urls as project_urls
import manage

POSTGRES_ENV = {
    "USE_POSTGRES": "True",
    "POSTGRES_DB": "coderr_test",
    "POSTGRES_USER": "coderr_user",
    "POSTGRES_PASSWORD": "test-password",
    "POSTGRES_HOST": "db",
    "POSTGRES_PORT": "5432",
}


class ProjectConfigTests(SimpleTestCase):
    @override_settings(DEBUG=True)
    def test_media_urls_are_added_in_debug_mode(self):
        self.addCleanup(reload, project_urls)
        urls = reload(project_urls)

        has_media_url = any(
            "media" in str(pattern.pattern)
            for pattern in urls.urlpatterns
        )
        self.assertTrue(has_media_url)

    def test_postgres_database_uses_environment(self):
        settings = self._reload_settings(POSTGRES_ENV)
        database = settings.DATABASES["default"]

        self.assertEqual(database["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(database["NAME"], "coderr_test")
        self.assertEqual(database["HOST"], "db")

    def test_production_mailer_uses_smtp(self):
        settings = self._reload_settings({"DEBUG": "False"})
        backend = settings.MAILERS["default"]["BACKEND"]

        self.assertEqual(
            backend,
            "django.core.mail.backends.smtp.EmailBackend",
        )

    def test_manage_raises_clear_error_without_django(self):
        with patch(
            "builtins.__import__",
            side_effect=ImportError("Django unavailable"),
        ):
            with self.assertRaisesRegex(
                ImportError,
                "Couldn't import Django",
            ):
                manage.main()

    def _reload_settings(self, environment):
        self.addCleanup(reload, project_settings)
        with patch.dict("os.environ", environment):
            return reload(project_settings)

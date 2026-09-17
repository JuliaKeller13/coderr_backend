from importlib import reload
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

import coderr.urls as project_urls
import manage


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
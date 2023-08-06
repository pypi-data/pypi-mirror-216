# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test the UTF-8 locale detection class."""

from __future__ import annotations

from typing import Iterable

import utf8_locale

from . import test_detect


def test_utf8_env() -> None:
    """Test get_utf8_env() and, indirectly, detect_utf8_locale()."""
    env = utf8_locale.UTF8Detect().detect().env
    test_detect.check_env(env)

    mod_env = test_detect.get_mod_env()
    env2 = utf8_locale.UTF8Detect(env=mod_env).detect().env
    test_detect.check_mod_env(env, mod_env, env2)


class TestLanguages(test_detect.TestLanguages):
    """Run the same tests using the UTF8Detect object."""

    @staticmethod
    def detect_locale(languages: Iterable[str]) -> str:
        """Get the locale name using the appropriate mechanism."""
        with test_detect.mock_locale():
            return utf8_locale.UTF8Detect(languages=languages).detect().locale

    @staticmethod
    def get_vars(languages: Iterable[str]) -> dict[str, str]:
        """Get the variables dict using the appropriate mechanism."""
        with test_detect.mock_locale():
            return utf8_locale.UTF8Detect(languages=languages).detect().env_vars

    @staticmethod
    def get_langs(env: dict[str, str]) -> list[str]:
        """Get the preferred languages using the appropriate mechanism."""
        return utf8_locale.LanguagesDetect(env=env).detect()

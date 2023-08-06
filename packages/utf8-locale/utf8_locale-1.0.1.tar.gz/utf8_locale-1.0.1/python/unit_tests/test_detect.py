# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test the UTF-8 locale detection functions."""

from __future__ import annotations

import functools
import json
import os
import pathlib
import subprocess
from typing import Iterable, NamedTuple
from unittest import mock

import pytest

import utf8_locale


class TLangData(NamedTuple):
    """The test data for a single preferred languages test case."""

    env: dict[str, str]
    expected: list[str]


class TData(NamedTuple):
    """The test data loaded from the JSON definitions file."""

    locales: list[str]
    languages: list[TLangData]


@functools.lru_cache
def load_test_data() -> TData:
    """Load the test data from the JSON definitions file."""
    raw = json.loads(
        (pathlib.Path(__file__).absolute().parent.parent.parent / "tests/data.json").read_text(
            encoding="UTF-8"
        )
    )
    assert raw["format"]["version"] == {"major": 0, "minor": 1}

    return TData(
        locales=raw["locales"],
        languages=[
            TLangData(env=item["env"], expected=item["expected"]) for item in raw["languages"]
        ],
    )


LANG_KEYS = {"LC_ALL", "LANGUAGE"}

LANG_EXPECTED = [
    (["C", "en"], "C.UTF-8"),
    (["en", "C"], "en_XX.UTF-8"),
    (["es", "bg", "*"], "it_IT.UTF-8"),
    (["en", "bg", "*"], "en_XX.UTF-8"),
    (["es", "*", "en"], "it_IT.UTF-8"),
    (["es", "*", "it"], "de_DE.UTF-8"),
    (["en", "bg", "en"], "en_XX.UTF-8"),
    (["it", "en", "it"], "it_IT.UTF-8"),
    (["xy", "yz", "xy", "en"], "en_XX.UTF-8"),
]


def check_env(env: dict[str, str]) -> None:
    """Make sure a UTF8-capable environment was setup correctly."""
    # Everything except LANG_KEYS is the same as in os.environ
    assert {key: value for key, value in env.items() if key not in LANG_KEYS} == {
        key: value for key, value in os.environ.items() if key not in LANG_KEYS
    }

    # The rest of this function makes sure that locale(1) and date(1), when
    # run in this environment, output reasonable values
    loc = {
        fields[0]: fields[1].strip('"')
        for fields in (
            line.split("=", 1)
            for line in subprocess.check_output(
                ["locale"], shell=False, env=env, encoding="UTF-8"
            ).splitlines()
        )
    }
    non_lc = {name for name in loc if not name.startswith("LC_")}
    assert non_lc.issubset({"LANG", "LANGUAGE"})
    loc = {name: value for name, value in loc.items() if name.startswith("LC_")}
    values = list(set(loc.values()))
    assert len(values) == 1, values
    assert values[0].lower().endswith(".utf8") or values[0].lower().endswith(".utf-8")

    utc_env = dict(env)
    utc_env["TZ"] = "UTC"
    lines = subprocess.check_output(
        ["date", "-d", "@1000000000", "+%A"],
        shell=False,
        env=utc_env,
        encoding="UTF-8",
    ).splitlines()
    assert lines in [["Sunday"], ["Sonntag"], ["domenica"], ["domingo"]]


def get_mod_env() -> dict[str, str]:
    """Get a slightly modified copy of os.environ for test purposes."""
    mod_env = {
        key: value
        for key, value in os.environ.items()
        if key not in ("HOME", "USER", "PS1", "PATH")
    }
    mod_env["TEST_KEY"] = "test value"
    return mod_env


def check_mod_env(env: dict[str, str], mod_env: dict[str, str], env2: dict[str, str]) -> None:
    """Make sure very little has changed in the prepared environment."""
    # Nothing besides LANG_KEYS has changed
    assert {key: value for key, value in env2.items() if key not in LANG_KEYS} == {
        key: value for key, value in mod_env.items() if key not in LANG_KEYS
    }

    # LANG_KEYS have changed in the same way as before
    assert {key: value for key, value in env2.items() if key in LANG_KEYS} == {
        key: value for key, value in env.items() if key in LANG_KEYS
    }


def test_utf8_env() -> None:
    """Test get_utf8_env() and, indirectly, detect_utf8_locale()."""
    env = utf8_locale.get_utf8_env()
    check_env(env)

    mod_env = get_mod_env()
    env2 = utf8_locale.get_utf8_env(mod_env)
    check_mod_env(env, mod_env, env2)


def mock_locale() -> mock._patch[mock.Mock]:  # noqa: SLF001
    """Mock subprocess.check_output("locale -a")."""
    locales = load_test_data().locales
    mock_check_output = mock.Mock(spec=["__call__"])
    mock_check_output.return_value = "".join(item + "\n" for item in locales)
    return mock.patch("subprocess.check_output", new=mock_check_output)


class TestLanguages:
    """Test the language preference handling of detect_utf8_locale()."""

    @staticmethod
    def detect_locale(languages: Iterable[str]) -> str:
        """Get the locale name using the appropriate mechanism."""
        with mock_locale():
            return utf8_locale.detect_utf8_locale(languages=languages)

    @staticmethod
    def get_vars(languages: Iterable[str]) -> dict[str, str]:
        """Get the variables dict using the appropriate mechanism."""
        with mock_locale():
            return utf8_locale.get_utf8_vars(languages=languages)

    @staticmethod
    def get_langs(env: dict[str, str]) -> list[str]:
        """Get the preferred languages using the appropriate mechanism."""
        return utf8_locale.get_preferred_languages(env)

    @pytest.mark.parametrize(("languages", "result"), LANG_EXPECTED)
    def test_language(self, languages: list[str], result: str) -> None:
        """Test detect_utf8_locale() with some languages specified."""
        assert self.detect_locale(iter(languages)) == result

    @pytest.mark.parametrize(("languages", "result"), LANG_EXPECTED)
    def test_language_vars(self, languages: list[str], result: str) -> None:
        """Test detect_utf8_locale() with some languages specified."""
        assert self.get_vars(iter(languages)) == {
            "LC_ALL": result,
            "LANGUAGE": "",
        }

    def test_no_languages(self) -> None:
        """Test detect_utf8_locale() with no languages specified."""
        with pytest.raises(utf8_locale.NoLanguagesError):
            self.detect_locale(languages=iter([]))

    @pytest.mark.parametrize("tcase", load_test_data().languages)
    def test_preferred(self, tcase: TLangData) -> None:
        """Test get_preferred_languages() with the specified environment."""
        assert self.get_langs(tcase.env) == tcase.expected

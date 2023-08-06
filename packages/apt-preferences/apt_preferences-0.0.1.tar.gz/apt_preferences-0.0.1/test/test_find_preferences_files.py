from pathlib import Path
from test.utils import process_files_map
from unittest import mock

import pytest

from apt_preferences.find_preferences_files import find_preferences_files
from apt_preferences.find_preferences_files import is_preference_path


def test_find_preferences_files_no_default_preference_file():
    """Default preference file is required."""

    not_existing_path = "/not/existing/path"

    with mock.patch(
        "apt_preferences.find_preferences_files._APT_PREF_FILE_PATH_S",
        not_existing_path,
    ):
        with pytest.raises(FileNotFoundError):
            find_preferences_files()


def test_find_preferences_files_no_default_preference_dir(tmpdir):
    """Default preference dir is not required."""
    default_pref_file = tmpdir.join("preferences")

    Path(default_pref_file).touch()

    with mock.patch(
        "apt_preferences.find_preferences_files._APT_PREF_FILE_PATH_S",
        default_pref_file,
    ):
        find_preferences_files()


@pytest.mark.parametrize(
    ("file_name", "expected_result"),
    [
        pytest.param(
            "hello.txt",
            False,
            id="wrong extension",
        ),
        pytest.param(
            "hello.pref",
            True,
            id="good extension",
        ),
        pytest.param(
            "hello",
            True,
            id="no extension",
        ),
    ],
)
def test_is_preference_path_pref_extension(tmpdir, file_name, expected_result):
    file_p = Path(tmpdir.join(file_name))

    with mock.patch.object(Path, "read_text") as read_text_mock:
        read_text_mock.return_value = ""

        assert is_preference_path(file_p) is expected_result


@pytest.mark.parametrize(
    ("file_name", "expected_result"),
    [
        pytest.param(
            "hello.",
            True,
            id="allow dot",
        ),
        pytest.param(
            "hello_abc",
            True,
            id="allow underscore",
        ),
        pytest.param(
            "hello-abc",
            True,
            id="allow hyphen",
        ),
        pytest.param(
            "hello~abc",
            False,
            id="forbid tild",
        ),
    ],
)
def test_is_preference_path_allowed_chars(tmpdir, file_name, expected_result):
    file_p = Path(tmpdir.join(file_name))

    with mock.patch.object(Path, "read_text") as read_text_mock:
        read_text_mock.return_value = ""

        assert is_preference_path(file_p) is expected_result


@pytest.mark.parametrize(
    ("files_map", "expected_prefs_files_len"),
    [
        pytest.param(
            {
                "preferences": "",
                "preferences.d/no_extension": "",
                "preferences.d/good_extension": "",
            },
            3,
            id="Preferences files only",
        ),
        pytest.param(
            {
                "preferences": "",
                "preferences_1": "",
                "preferencesButLonger": "",
            },
            1,
            id="Only one preference file",
        ),
        pytest.param(
            {
                "preferences": "@#$(*&(^*%^&%^))",
                "preferences.d/no_extension": "%^&",
                "preferences.d/good_extension": ",.:}{}+_/*-+",
            },
            3,
            id="Wrong content but good names",
        ),
        pytest.param(
            {
                "preferences": "",
                "preferences.d/no_extension.conf": "",
                "preferences.d/good_extension.txt": "",
            },
            1,
            id="Wrong extensions",
        ),
    ],
)
def test_find_preferences_files(tmpdir, files_map, expected_prefs_files_len):
    # prepare testfiles
    process_files_map(files_map, tmpdir)

    # process data
    with mock.patch(
        "apt_preferences.find_preferences_files._get_default_pref_file_path",
        lambda: Path(tmpdir.join("preferences")),
    ):
        # process data
        with mock.patch(
            "apt_preferences.find_preferences_files._get_default_pref_dir_path",
            lambda: Path(tmpdir.join("preferences.d")),
        ):
            received_paths_l = find_preferences_files()

    received_paths_l_len = len(received_paths_l)

    # check results
    assert received_paths_l_len == expected_prefs_files_len

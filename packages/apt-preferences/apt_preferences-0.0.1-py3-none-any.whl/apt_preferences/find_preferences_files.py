"""

   Find paths to all preference files.

"""
import string
import typing
from pathlib import Path

_APT_PREF_FILE_PATH_S: str = "/etc/apt/preferences"

_APT_PREF_DIR_PATH_S: str = _APT_PREF_FILE_PATH_S + ".d"


def find_preferences_files() -> typing.List[Path]:
    """Find paths to files used by APT to set up preferences."""

    pref_files_paths: typing.List[Path] = []

    for file_name in _list_possible_pref_files():
        file_path = Path(file_name)

        if is_preference_path(file_path) is True:
            pref_files_paths.append(file_path)

    return pref_files_paths


def _list_possible_pref_files():
    all_preferences_d_files = list(_get_default_pref_dir_path().rglob("*"))

    return all_preferences_d_files + [_get_default_pref_file_path()]


def _get_default_pref_file_path() -> Path:
    """The APT preferences file '/etc/apt/preferences'."""
    default_pref_file = Path(_APT_PREF_FILE_PATH_S)

    if default_pref_file.exists() is False:
        raise FileNotFoundError(default_pref_file)

    return default_pref_file


def _get_default_pref_dir_path() -> Path:
    """The APT preferences fragment files in the '/etc/apt/preferences.d/'."""
    return Path(_APT_PREF_DIR_PATH_S)


def is_preference_path(path: Path) -> bool:
    """According docs:
    `The files have either no or "pref" as filename extension and only
    contain alphanumeric, hyphen (-), underscore (_) and period (.) characters.`
    """
    allowed_extensions, allowed_characters = ["", ".pref"], [
        *string.ascii_letters,
        *string.digits,
        "-",
        "_",
        ".",
    ]

    file_extension, file_name = path.suffix, path.name

    file_name = file_name.replace(file_extension, "")

    if len(file_name) == 0:
        return False

    if file_extension not in allowed_extensions:
        return False

    for character in file_name:
        if character not in allowed_characters:
            return False

    return True

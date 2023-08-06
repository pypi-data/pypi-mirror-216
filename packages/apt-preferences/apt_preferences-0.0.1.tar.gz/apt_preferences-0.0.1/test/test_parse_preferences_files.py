from pathlib import Path
from test.utils import process_files_map
from unittest import mock

import pytest

from apt_preferences.data_structures import AptPreference
from apt_preferences.errors import NoPreferencesFound
from apt_preferences.parse_preferences_files import parse_preferences_files
from apt_preferences.parse_preferences_files import parse_preferences_path

PREFERENCE_EXAMPLE = AptPreference(
    package="my-custom-package",
    pin="origin my.custom.repo.url",
    pin_priority=1,
)

_PARENT_DIR_PATH = Path(__file__).parent


@pytest.mark.parametrize(
    "str_to_parse",
    [
        pytest.param(
            """Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """,
            id="Package,Pin,Priority",
        ),
        pytest.param(
            """Package: my-custom-package
               Pin-Priority: 1
               Pin: origin my.custom.repo.url
            """,
            id="Package,Priority,Pin",
        ),
        pytest.param(
            """Pin-Priority: 1
               Package: my-custom-package
               Pin: origin my.custom.repo.url
            """,
            id="Priority,Package,Pin",
        ),
        pytest.param(
            """Pin-Priority: 1
               Pin: origin my.custom.repo.url
               Package: my-custom-package
            """,
            id="Priority,Pin,Package",
        ),
        pytest.param(
            """Pin: origin my.custom.repo.url
               Pin-Priority: 1
               Package: my-custom-package
            """,
            id="Pin,Priority,Package",
        ),
        pytest.param(
            """Pin: origin my.custom.repo.url
               Package: my-custom-package
               Pin-Priority: 1
            """,
            id="Pin,Package,Priority",
        ),
    ],
)
def test_parse_apt_preference_order_no_error(tmp_path, str_to_parse):
    pref_file_p: Path = _create_apt_preferences_file(tmp_path, str_to_parse)
    # parsed without error
    parse_preferences_path(pref_file_p)


@pytest.mark.parametrize(
    ("str_to_parse", "expected_obj"),
    [
        pytest.param(
            """Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """,
            PREFERENCE_EXAMPLE,
            id="Package,Pin,Priority",
        ),
        pytest.param(
            """Package: my-custom-package
               Pin-Priority: 1
               Pin: origin my.custom.repo.url
            """,
            PREFERENCE_EXAMPLE,
            id="Package,Priority,Pin",
        ),
        pytest.param(
            """Pin-Priority: 1
               Package: my-custom-package
               Pin: origin my.custom.repo.url
            """,
            PREFERENCE_EXAMPLE,
            id="Priority,Package,Pin",
        ),
        pytest.param(
            """Pin-Priority: 1
               Pin: origin my.custom.repo.url
               Package: my-custom-package
            """,
            PREFERENCE_EXAMPLE,
            id="Priority,Pin,Package",
        ),
        pytest.param(
            """Pin: origin my.custom.repo.url
               Pin-Priority: 1
               Package: my-custom-package
            """,
            PREFERENCE_EXAMPLE,
            id="Pin,Priority,Package",
        ),
        pytest.param(
            """Pin: origin my.custom.repo.url
               Package: my-custom-package
               Pin-Priority: 1
            """,
            PREFERENCE_EXAMPLE,
            id="Pin,Package,Priority",
        ),
    ],
)
def test_parse_apt_preference_order_content(tmp_path, str_to_parse, expected_obj):
    expected_result = [expected_obj]

    pref_file_p: Path = _create_apt_preferences_file(tmp_path, str_to_parse)

    received_result = parse_preferences_path(pref_file_p)

    for pref in expected_result:
        pref.file_path = pref_file_p

    assert received_result == expected_result


def test_parse_apt_preference_empty_content(tmp_path):
    str_to_parse = """
    """

    pref_file_p: Path = _create_apt_preferences_file(tmp_path, str_to_parse)

    with pytest.raises(NoPreferencesFound):
        parse_preferences_path(pref_file_p)


def _create_apt_preferences_file(tmp_path, file_content: str) -> Path:
    pref_file = tmp_path.joinpath("file.pref")

    pref_file.write_text(file_content)

    return Path(pref_file)


@pytest.mark.parametrize(
    ("str_to_parse", "expected_objs"),
    [
        pytest.param(
            """Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """
            + """Package: my-custom-package
               Pin-Priority: 1
               Pin: origin my.custom.repo.url
            """,
            [PREFERENCE_EXAMPLE] * 2,
            id="Two preferences",
        ),
        pytest.param(
            """Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """
            + """Package: my-custom-package
               Pin-Priority: 1
               Pin: origin my.custom.repo.url
            """
            + """Pin-Priority: 1
               Package: my-custom-package
               Pin: origin my.custom.repo.url
            """,
            [PREFERENCE_EXAMPLE] * 3,
            id="Three preferences",
        ),
        pytest.param(
            """Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """
            + """Package: my-custom-package
               Pin-Priority: 1
               Pin: origin my.custom.repo.url
            """
            + """Pin-Priority: 1
               Package: my-custom-package
               Pin: origin my.custom.repo.url
            """
            + """Pin-Priority: 1
               Pin: origin my.custom.repo.url
               Package: my-custom-package
            """,
            [PREFERENCE_EXAMPLE] * 4,
            id="Four preferences no. 0",
        ),
        pytest.param(
            """Pin-Priority: 1
               Pin: origin my.custom.repo.url
               Package: my-custom-package
            """
            + """Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """
            + """Package: my-custom-package
               Pin-Priority: 1
               Pin: origin my.custom.repo.url
            """
            + """Pin-Priority: 1
               Package: my-custom-package
               Pin: origin my.custom.repo.url
            """,
            [PREFERENCE_EXAMPLE] * 4,
            id="Four prefererences no. 1",
        ),
    ],
)
def test_parse_apt_preference_multiple(tmp_path, str_to_parse, expected_objs):
    pref_file_p: Path = _create_apt_preferences_file(tmp_path, str_to_parse)

    for pref in expected_objs:
        pref.file_path = pref_file_p

    received_objs = parse_preferences_path(pref_file_p)

    assert received_objs == expected_objs


def test_parse_apt_preference_e2e_multiple(e2e_multiple_entries):
    pref_file_p: Path = e2e_multiple_entries

    expected_objs = [
        AptPreference(
            package="*",
            pin="origin my.custom.repo.url",
            pin_priority=1,
            file_path=pref_file_p,
        ),
        AptPreference(
            package="my-specific-software",
            pin="origin my.custom.repo.url",
            pin_priority=500,
            file_path=pref_file_p,
        ),
    ]

    received_objs = parse_preferences_path(pref_file_p)

    assert received_objs == expected_objs


def test_parse_apt_preference_e2e_single(e2e_single_entry):
    pref_file_p: Path = e2e_single_entry

    expected_objs = [
        AptPreference(
            package="my-custom-package",
            pin="origin my.custom.repo.url",
            pin_priority=1,
            file_path=e2e_single_entry,
        )
    ]

    received_objs = parse_preferences_path(pref_file_p)

    assert received_objs == expected_objs


@pytest.mark.parametrize(
    ("files_map", "expected_prefs_files_l"),
    [
        pytest.param(
            {
                "preferences": """
                        Package: my-custom-package
                        Pin: origin my.custom.repo.url
                        Pin-Priority: 1

                        Pin-Priority: 1
                        Pin: origin my.custom.repo.url
                        Package: my-custom-package
                        """,
                "preferences.d/no_extension": """
                        Package: my-custom-package
                        Pin-Priority: 1
                        Pin: origin my.custom.repo.url

                        Pin: origin my.custom.repo.url
                        Pin-Priority: 1
                        Package: my-custom-package
                        """,
                "preferences.d/good_extension.pref": """
                        Pin-Priority: 1
                        Package: my-custom-package
                        Pin: origin my.custom.repo.url

                        Pin: origin my.custom.repo.url
                        Package: my-custom-package
                        Pin-Priority: 1
                        """,
            },
            [
                "preferences",
                "no_extension",
                "good_extension.pref",
            ],
            id="Preferences files only",
        ),
        pytest.param(
            {
                "preferences": """
                        Package: my-custom-package
                        Pin: origin my.custom.repo.url
                        Pin-Priority: 1

                        Pin-Priority: 1
                        Pin: origin my.custom.repo.url
                        Package: my-custom-package
                        """,
                "preferences.d/bad_extension.conf": """
                        [apt]
                        frontend=pager
                        which=news
                        email_address=root
                        email_format=text
                        confirm=false
                        headers=false
                        reverse=false
                        save_seen=/var/lib/apt/listchanges.db
                        """,
                "preferences.d/good_extension.pref": """
                        Pin-Priority: 1
                        Package: my-custom-package
                        Pin: origin my.custom.repo.url

                        Pin: origin my.custom.repo.url
                        Package: my-custom-package
                        Pin-Priority: 1
                        """,
            },
            ["preferences", "good_extension.pref"],
            id="Recognize extension",
        ),
    ],
)
def test_find_preferences_files(tmpdir, files_map, expected_prefs_files_l):
    def _is_expected(path_to_check) -> bool:
        name_to_check = Path(path_to_check).name
        return name_to_check in expected_prefs_files_l

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
            received_results = parse_preferences_files()

    received_paths = set()

    for preference in received_results:
        if (is_expected := _is_expected(preference.file_path)) is True:
            received_paths.add(preference.file_path)

        assert is_expected is True

    assert len(expected_prefs_files_l) == len(received_paths)


@pytest.mark.parametrize(
    ("str_to_parse", "expected_obj"),
    [
        pytest.param(
            """# Some comment
               Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """,
            PREFERENCE_EXAMPLE,
            id="single comment",
        ),
        pytest.param(
            """Package: my-custom-package
               # Some comment
               # Some comment
               Pin-Priority: 1
               # Some comment
               Pin: origin my.custom.repo.url
            """,
            PREFERENCE_EXAMPLE,
            id="multiple comment",
        ),
    ],
)
def test_parse_apt_preference_comments(tmp_path, str_to_parse, expected_obj):
    expected_result = [expected_obj]

    pref_file_p: Path = _create_apt_preferences_file(tmp_path, str_to_parse)

    received_result = parse_preferences_path(pref_file_p)

    for pref in expected_result:
        pref.file_path = pref_file_p

    assert received_result == expected_result


@pytest.mark.parametrize(
    ("str_to_parse", "expected_objs_l"),
    [
        # `do not inject tests between` start
        pytest.param(
            """Explanation: dadada nananana
               Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """,
            [
                AptPreference(
                    package="my-custom-package",
                    pin="origin my.custom.repo.url",
                    pin_priority=1,
                    explanations={"package": ["dadada nananana"]},
                )
            ],
            id="single explanation",
        ),
        pytest.param(
            """Explanation: dadada nananana
               Package: my-custom-package
               Explanation: banana marianna
               Explanation: arkana sawanna
               Pin: origin my.custom.repo.url
               Explanation: alaaaabaaama song
               Pin-Priority: 1
            """,
            [
                AptPreference(
                    package="my-custom-package",
                    pin="origin my.custom.repo.url",
                    pin_priority=1,
                    explanations={
                        "package": ["dadada nananana"],
                        "pin": ["banana marianna", "arkana sawanna"],
                        "pin_priority": ["alaaaabaaama song"],
                    },
                ),
            ],
            id="multiple explanation",
        ),
        pytest.param(
            """Explanation: dadada nananana
               Package: my-custom-package
               Pin: origin my.custom.repo.url
               Pin-Priority: 1
            """
            + """Explanation: dadada nananana
               Package: my-custom-package
               Explanation: banana marianna
               Explanation: arkana sawanna
               Pin: origin my.custom.repo.url
               Explanation: alaaaabaaama song
               Pin-Priority: 1
            """,
            [
                AptPreference(
                    package="my-custom-package",
                    pin="origin my.custom.repo.url",
                    pin_priority=1,
                    explanations={"package": ["dadada nananana"]},
                ),
                AptPreference(
                    package="my-custom-package",
                    pin="origin my.custom.repo.url",
                    pin_priority=1,
                    explanations={
                        "package": ["dadada nananana"],
                        "pin": ["banana marianna", "arkana sawanna"],
                        "pin_priority": ["alaaaabaaama song"],
                    },
                ),
            ],
            id="previous examples combined",
        ),
        # `do not inject tests between` end
    ],
)
def test_parse_apt_preference_explanation(tmp_path, str_to_parse, expected_objs_l):
    expected_result = expected_objs_l

    pref_file_p: Path = _create_apt_preferences_file(tmp_path, str_to_parse)

    received_result = parse_preferences_path(pref_file_p)

    for pref in expected_result:
        pref.file_path = pref_file_p

    assert received_result == expected_result

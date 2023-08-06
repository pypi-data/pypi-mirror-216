from pathlib import Path

import pytest

from apt_preferences.data_structures import AptPreference
from apt_preferences.render_preferences_files import _render_field_with_explanation
from apt_preferences.render_preferences_files import render_preference
from apt_preferences.render_preferences_files import render_preferences_files


@pytest.fixture
def preference_example(tmpdir):
    return AptPreference(
        package="my-custom-package",
        pin="origin my.custom.repo.url",
        pin_priority=1,
        file_path=Path(tmpdir.join("preference")),
    )


@pytest.fixture
def preference_example_with_explanation(tmpdir):
    return AptPreference(
        package="my-custom-package",
        pin="origin my.custom.repo.url",
        pin_priority=1,
        file_path=Path(tmpdir.join("preference")),
        explanations={
            "package": [
                "this is very important explanation",
                "this is not important explanation",
            ],
            "pin_priority": [
                "this is a little important explanation",
                "this is not so much important explanation",
            ],
            "pin": [
                "OMG! this the most important explanation",
            ],
        },
    )


def test_render_package(preference_example):
    print(preference_example)

    received_s: str = _render_field_with_explanation(preference_example, "package")

    expected_s: str = "Package: my-custom-package"

    assert received_s == expected_s


def aaa_test_render_package_with_explanation(preference_example_with_explanation):
    received_s: str = _render_field_with_explanation(
        preference_example_with_explanation, "package"
    )

    expected_s: str = (
        "Explanation: this is very important explanation\n"
        "Explanation: this is not important explanation\n"
        "Package: my-custom-package"
    )

    assert received_s == expected_s


def test_render_pin(preference_example):
    received_s: str = _render_field_with_explanation(preference_example, "pin")

    expected_s: str = "Pin: origin my.custom.repo.url"

    assert received_s == expected_s


def test_render_pin_with_explanation(preference_example_with_explanation):
    received_s: str = _render_field_with_explanation(
        preference_example_with_explanation, "pin"
    )

    expected_s: str = (
        "Explanation: OMG! this the most important explanation\n"
        "Pin: origin my.custom.repo.url"
    )

    assert received_s == expected_s


def test_render_pin_priority(preference_example):
    received_s: str = _render_field_with_explanation(preference_example, "pin_priority")

    expected_s: str = "Pin priority: 1"

    assert received_s == expected_s


def test_render_pin_priority_with_explanation(preference_example_with_explanation):
    received_s: str = _render_field_with_explanation(
        preference_example_with_explanation, "pin_priority"
    )

    expected_s: str = (
        "Explanation: this is a little important explanation\n"
        "Explanation: this is not so much important explanation\n"
        "Pin priority: 1"
    )

    assert received_s == expected_s


def test_render_preference(preference_example):
    received_s: str = render_preference(preference_example)

    expected_s: str = (
        "Package: my-custom-package\n"
        "Pin: origin my.custom.repo.url\n"
        "Pin priority: 1"
    )

    assert received_s == expected_s


def test_render_preference_with_explanation(preference_example_with_explanation):
    received_s: str = render_preference(preference_example_with_explanation)

    expected_s: str = (
        "Explanation: this is very important explanation\n"
        "Explanation: this is not important explanation\n"
        "Package: my-custom-package\n"
        "Explanation: OMG! this the most important explanation\n"
        "Pin: origin my.custom.repo.url\n"
        "Explanation: this is a little important explanation\n"
        "Explanation: this is not so much important explanation\n"
        "Pin priority: 1"
    )

    assert received_s == expected_s


def test_render_preferences_files_single_file(
    preference_example, preference_example_with_explanation
):
    preferences_l = [preference_example, preference_example_with_explanation]

    file_to_snippet_map = render_preferences_files(preferences_l)

    assert len(file_to_snippet_map) == 1

    for file_content in file_to_snippet_map.values():
        assert file_content == (
            "Package: my-custom-package\n"
            "Pin: origin my.custom.repo.url\n"
            "Pin priority: 1\n"
            "Explanation: this is very important explanation\n"
            "Explanation: this is not important explanation\n"
            "Package: my-custom-package\n"
            "Explanation: OMG! this the most important explanation\n"
            "Pin: origin my.custom.repo.url\n"
            "Explanation: this is a little important explanation\n"
            "Explanation: this is not so much important explanation\n"
            "Pin priority: 1"
        )


def test_render_preferences_files_multiple_files(
    preference_example, preference_example_with_explanation, tmpdir
):
    preferences_l = [preference_example, preference_example_with_explanation]
    for i, preference in enumerate(preferences_l):
        preference.file_path = Path(tmpdir.join(f"{i}.pref"))

    expected_map = {
        str(preference_example.file_path.absolute()): (
            "Package: my-custom-package\n"
            "Pin: origin my.custom.repo.url\n"
            "Pin priority: 1"
        ),
        str(preference_example_with_explanation.file_path.absolute()): (
            "Explanation: this is very important explanation\n"
            "Explanation: this is not important explanation\n"
            "Package: my-custom-package\n"
            "Explanation: OMG! this the most important explanation\n"
            "Pin: origin my.custom.repo.url\n"
            "Explanation: this is a little important explanation\n"
            "Explanation: this is not so much important explanation\n"
            "Pin priority: 1"
        ),
    }

    file_to_snippet_map = render_preferences_files(preferences_l)

    assert len(file_to_snippet_map) == len(expected_map)

    for key in expected_map:
        assert file_to_snippet_map[key] == expected_map[key]

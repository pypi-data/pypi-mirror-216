from pathlib import Path

from apt_preferences._utils import copy_obj
from apt_preferences._utils import get_function_name
from apt_preferences._utils import read_file
from apt_preferences.data_structures import AptPreference


def test_read_file(tmp_path):
    expected_content, file_ = "abcxyz123@#$", tmp_path.joinpath("test_file")

    file_.write_text(expected_content)

    file_path = Path(file_.absolute())

    received_content = read_file(file_path)

    assert received_content == expected_content


def test_copy_obj(tmp_path):
    expected_package, expected_pin, expected_priority, expected_path = (
        "my-package",
        "*",
        5,
        Path(tmp_path.joinpath("test_file").absolute()),
    )

    obj_to_copy = AptPreference(
        package=expected_package,
        pin=expected_pin,
        pin_priority=expected_priority,
        file_path=expected_path,
    )

    new_obj = copy_obj(obj_to_copy)

    assert new_obj.package == expected_package
    assert new_obj.pin == expected_pin
    assert new_obj.pin_priority == expected_priority
    assert new_obj.file_path == expected_path


def test_get_function_name_def():
    def my_function():
        received_name = get_function_name()
        return received_name

    expected_function_name = "my_function"

    received_function_name = my_function()

    assert received_function_name == expected_function_name


def test_get_function_name_class():
    class MyClass:
        def my_method(self):
            received_name = get_function_name()
            return received_name

    expected_method_name = "my_method"

    received_method_name = MyClass().my_method()

    assert received_method_name == expected_method_name

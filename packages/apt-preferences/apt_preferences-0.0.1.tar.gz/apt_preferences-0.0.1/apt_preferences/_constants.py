from pathlib import Path

from apt_preferences._utils import read_file

EXPLANATIONS_FIELD_NAME = "explanations"

_PARENT_DIR_PATH = Path(__file__).parent

LARK_GRAMMAR_PATH = _PARENT_DIR_PATH.joinpath("apt_preferences.lark")

LARK_GRAMMAR = read_file(LARK_GRAMMAR_PATH)

FIELD_TO_SNIPPET_MAP = {
    "package": "Package: {value}",
    "pin": "Pin: {value}",
    "pin_priority": "Pin-Priority: {value}",
    EXPLANATIONS_FIELD_NAME: "Explanation: {value}",
}

DELIMETER = "\n"

FIELDS_NOT_TO_RENDER = [EXPLANATIONS_FIELD_NAME]

FIELDS_TO_RENDER = [
    field_name
    for field_name in FIELD_TO_SNIPPET_MAP
    if field_name not in FIELDS_NOT_TO_RENDER
]

assert set(FIELDS_NOT_TO_RENDER + FIELDS_TO_RENDER) == set(FIELD_TO_SNIPPET_MAP)

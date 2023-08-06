import functools
import typing
from pathlib import Path

from lark import Lark
from lark import Transformer
from lark import v_args

from apt_preferences._constants import \
    EXPLANATIONS_FIELD_NAME as _EXPLANATIONS_FIELD_NAME
from apt_preferences._constants import LARK_GRAMMAR as _LARK_GRAMMAR
from apt_preferences._utils import copy_obj as _copy_obj
from apt_preferences._utils import get_function_name as _get_function_name
from apt_preferences._utils import \
    get_function_parameters_names as _get_function_parameters_names
from apt_preferences._utils import read_file as _read_file
from apt_preferences.data_structures import AptPreference
from apt_preferences.errors import NoPreferencesFound
from apt_preferences.find_preferences_files import find_preferences_files


def parse_preferences_files() -> typing.List[AptPreference]:
    """Find preference files.
    Transform each preference file into AptPreferences' list.
    Merge lists (info about source file is kept as AptPreference.file_path).
    """
    all_preferences_l: typing.List[AptPreference] = []

    for file_path in find_preferences_files():
        try:
            local_preferences_l: typing.List[AptPreference] = parse_preferences_path(
                file_path
            )
        except NoPreferencesFound:
            continue

        all_preferences_l.extend(local_preferences_l)

    return all_preferences_l


def parse_preferences_path(
    pref_file_path: Path,
) -> typing.List[AptPreference]:
    """Transforms preference file into AptPreferences' list."""

    pref_file_content: str = _read_file(pref_file_path)

    try:
        preferences_l = parse_preference(pref_file_content)
    except NoPreferencesFound as err:
        raise NoPreferencesFound(pref_file_path) from err

    _populate_preferences_paths(preferences_l, pref_file_path)

    return preferences_l


def parse_preference(preference_content_s: str) -> typing.List[AptPreference]:
    return _parser.parse(preference_content_s)


def _populate_preferences_paths(preferences_l, file_path):
    for preference in preferences_l:
        preference.file_path = _copy_obj(file_path)


def _add_explanations_to_rule(func):
    @functools.wraps(func)
    def wrapped_func(_, rule_l) -> dict:
        explanations_exist, rule_is_valid = _explanations_exist(rule_l), _rule_is_valid(
            rule_l
        )

        if rule_is_valid is False:
            raise ValueError(rule_l)

        rule_value = rule_l.pop()

        func_result: dict = func(_, rule_value)

        if explanations_exist is True:
            func_result[_EXPLANATIONS_FIELD_NAME] = rule_l.pop()

        return func_result

    return wrapped_func


def _explanations_exist(rule_l) -> bool:
    return len(rule_l) == 2


def _rule_is_valid(rule_l) -> bool:
    return len(rule_l) == 1 or _explanations_exist(rule_l)


def _add_explanations_to_preference(func):
    @functools.wraps(func)
    def wrapped_func(_, fields_l) -> AptPreference:
        explanations = {}

        for field_d in fields_l:
            field_name: str = _find_field_name(field_d)

            explanation_exist = field_d.get(_EXPLANATIONS_FIELD_NAME) is not None

            if explanation_exist:
                explanations[field_name] = field_d.pop(_EXPLANATIONS_FIELD_NAME)

        explanations_exist = len(explanations) > 0

        if explanations_exist and _kwargs_are_valid(explanations) is False:
            raise ValueError(fields_l, explanations)

        preference: AptPreference = func(_, fields_l)

        setattr(preference, _EXPLANATIONS_FIELD_NAME, explanations)

        return preference

    return wrapped_func


def _find_field_name(value_d):
    for field in value_d.keys():
        if field != _EXPLANATIONS_FIELD_NAME:
            return field
    raise NotImplementedError(value_d)


def _kwargs_are_valid(kwargs) -> bool:
    not_mapped_fields_names = set(["self", "file_path"])

    mapped_fields_names: set = _get_function_parameters_names(
        AptPreference.__init__
    ).difference(not_mapped_fields_names)

    for kwarg_key in kwargs:
        if kwarg_key in mapped_fields_names:
            return True
    return False


class PreferencesTreeTransformer(Transformer):
    string = v_args(inline=True)(str)
    integer = v_args(inline=True)(int)
    explanation = v_args(inline=True)(str)

    preferences_l = list
    explanations_l = list

    @_add_explanations_to_rule
    def pin(self, s) -> typing.Dict[str, str]:
        return {_get_function_name(): s}

    @_add_explanations_to_rule
    def package(self, s) -> typing.Dict[str, str]:
        return {_get_function_name(): s}

    @_add_explanations_to_rule
    def pin_priority(self, i) -> typing.Dict[str, int]:
        return {_get_function_name(): i}

    # While order is unimportant for apt, Transformer
    #   creates python list for each rule (for which
    #   order is important). To distinguish values
    #   from each other, methods names are mapped to
    #   AptPreferences.__init__ kwargs.

    @_add_explanations_to_preference
    def preference(self, rule_l) -> AptPreference:
        if len(rule_l) == 0:
            raise NoPreferencesFound()

        kwargs = {}

        for value_d in rule_l:
            field_name = _find_field_name(value_d)

            kwargs[field_name] = value_d[field_name]

        if _kwargs_are_valid(kwargs) is False:
            raise ValueError(rule_l, kwargs)

        return AptPreference(**kwargs)


def _create_lark_parser():
    return Lark(
        _LARK_GRAMMAR,
        parser="lalr",
        lexer="contextual",  # <- contextual lexer is required to resolve priorities
        propagate_positions=False,  # <- improve speed
        maybe_placeholders=False,  # <- improve speed
        transformer=PreferencesTreeTransformer(),  # <- improve speed
    )


_parser = _create_lark_parser()

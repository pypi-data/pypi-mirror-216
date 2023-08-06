import copy
import inspect
import typing
from pathlib import Path


def read_file(path: Path) -> str:
    with open(path.absolute(), "r", encoding="utf-8") as _fp:
        return _fp.read()


def copy_obj(obj_: typing.Any) -> typing.Any:
    return copy.deepcopy(obj_)


def get_function_name():
    current_stack = inspect.stack()

    if len(current_stack) <= 1:
        raise ValueError(current_stack)

    current_stack = current_stack[1]

    if len(current_stack) <= 3:
        raise ValueError(current_stack)

    return current_stack[3]


def get_function_parameters_names(function) -> set:
    function_signature = inspect.signature(function)
    function_parameters = function_signature.parameters
    return set(function_parameters)

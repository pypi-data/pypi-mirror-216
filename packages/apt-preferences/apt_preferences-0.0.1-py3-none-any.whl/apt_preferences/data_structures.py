import typing
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path


@dataclass
class AptPreference:
    """Represents preference entry."""

    FILE_PATH_NONE_FIELD_NAME = "no path"

    package: str
    pin: str
    pin_priority: int
    explanations: typing.Dict[str, typing.List[str]] = field(default_factory=dict)
    file_path: typing.Optional[Path] = None

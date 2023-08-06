from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class Property:
    label: str
    datatype: Type

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Register:
    """Represents a single Modbus register."""

    sheet: str
    group: str

    address: int
    address_hex: str

    name: str

    access: str

    datatype: str

    unit: str

    description_cn: str

    description_en: str = ""

    usage: str = ""

    minimum: Any = None

    maximum: Any = None
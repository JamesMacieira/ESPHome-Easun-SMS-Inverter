from dataclasses import dataclass, field


@dataclass
class Register:
    """
    Represents a single Modbus register.
    """

    # Register information
    index: int

    sheet: str
    group: str

    address: int
    address_hex: str

    # Modbus
    datatype: str
    access: str

    # Description
    variable: str
    description_cn: str
    description_en: str

    # Scaling
    unit: str
    scale: float

    # Limits
    minimum: str
    maximum: str

    # Raw usage text from Excel
    usage: str

    # Parsed enum values
    #
    # Example:
    #
    # {
    #     0: "APP Mode",
    #     1: "UPS Mode",
    #     2: "GEN Mode"
    # }
    #
    enum: dict[int, str] = field(default_factory=dict)

    # Reserved register (empty description)
    reserved: bool = False

    def has_enum(self) -> bool:
        return len(self.enum) > 0

    def is_switch(self) -> bool:

        if not self.has_enum():
            return False

        values = [v.lower() for v in self.enum.values()]

        if len(values) != 2:
            return False

        pair1 = {"enable", "disable"}
        pair2 = {"enabled", "disabled"}
        pair3 = {"on", "off"}

        return (
            set(values) == pair1
            or set(values) == pair2
            or set(values) == pair3
        )

    def is_select(self) -> bool:

        return self.has_enum() and not self.is_switch()

    def is_number(self) -> bool:

        return (
            self.access == "RW"
            and not self.has_enum()
        )

    def is_sensor(self) -> bool:

        return self.access == "RO"

    def to_dict(self):

        return {

            "sheet": self.sheet,
            "group": self.group,

            "index": self.index,

            "address": self.address,
            "hex": self.address_hex,

            "datatype": self.datatype,
            "access": self.access,

            "variable": self.variable,

            "description_cn": self.description_cn,
            "description_en": self.description_en,

            "unit": self.unit,
            "scale": self.scale,

            "minimum": self.minimum,
            "maximum": self.maximum,

            "usage": self.usage,

            "enum": self.enum,

            "reserved": self.reserved
        }

    def __str__(self):

        name = self.description_en

        if name == "":
            name = self.description_cn

        return (
            f"[{self.address_hex}] "
            f"{name} "
            f"({self.datatype})"
        )
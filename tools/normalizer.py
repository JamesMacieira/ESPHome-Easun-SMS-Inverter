import re


#
# Access rights
#

ACCESS = {

    "只读": "RO",

    "读写": "RW",

    "": ""

}


#
# Datatypes
#

DATATYPE = {

    "uint16_t": "uint16",

    "int16_t": "int16",

    "uint32_t": "uint32",

    "int32_t": "int32",

    "float": "float",

    "": ""

}


#
# Common units
#

UNITS = {

    "%": "%",

    "V": "V",

    "A": "A",

    "W": "W",

    "Hz": "Hz",

    "℃": "°C",

    "min": "min",

    "ms": "ms"

}


def normalize_access(value):

    value = str(value or "").strip()

    return ACCESS.get(value, value)


def normalize_datatype(value):

    value = str(value or "").strip()

    return DATATYPE.get(value, value)


def normalize_unit(value):

    """
    Examples

    0.1V
    1%
    0.01Hz
    ℃
    """

    value = str(value or "").strip()

    if value == "":
        return "", 1.0

    #
    # only unit
    #

    if value in UNITS:

        return UNITS[value], 1.0

    #
    # scale + unit
    #

    match = re.match(r"([0-9.]+)(.*)", value)

    if match:

        scale = float(match.group(1))

        unit = match.group(2).strip()

        unit = UNITS.get(unit, unit)

        return unit, scale

    return value, 1.0


def normalize_description(value):

    return str(value or "").strip()


def normalize_variable(value):

    return str(value or "").strip()


def normalize_limits(value):

    if value is None:

        return ""

    return str(value).strip()


def is_reserved(description):

    """
    Register exists but has no meaning.

    Example

    0151

    description = ""

    """

    return description.strip() == ""
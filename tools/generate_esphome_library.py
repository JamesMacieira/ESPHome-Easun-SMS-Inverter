#!/usr/bin/env python3
"""Build the ESPHome package library from the CVTE Modbus workbook.

The Excel workbook is the source of truth.  Generated files are committed so
that users do not need Python or Excel to use the integration.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import openpyxl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "modbus/original/CVTE_Modbus_v1.20 - simplex.xlsx"
OUTPUT = ROOT / "esphome/packages/easun_sms"

# These worksheets are runtime telemetry.  Factory, calibration, OTA and
# administrative pages are intentionally not exposed by an automation package.
TELEMETRY_SHEETS = (
    "WF_Simplify", "WF_WorkMode", "WF_BAT", "WF_BMS", "WF_OP", "WF_PV",
    "WF_INV", "WF_FAN", "WF_NTC",
)

VALUE_TYPES = {
    "int16": "S_WORD", "uint16": "U_WORD",
    "int16_t": "S_WORD", "uint16_t": "U_WORD",
}
UNIT_RE = re.compile(r"^([0-9.]+)\s*(.*)$")
ENUM_RE = re.compile(r"(?:^|\n)\s*(?:0x)?([0-9A-Fa-f]+)\s*:\s*([^\n]+)")
UNIT_ALIASES = {
    "%": "%", "V": "V", "mV": "mV", "A": "A", "W": "W", "Wh": "Wh",
    "kWh": "kWh", "Hz": "Hz", "°C": "°C", "min": "min", "ms": "ms",
    "mAH": "mAh", "mAh": "mAh",
}


def clean(value: object) -> str:
    return str(value or "").strip()


def yaml_string(value: str) -> str:
    """Quote a YAML scalar without relying on a YAML emitter."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def make_id(sheet: str, address: int, description: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "_", description.lower()).strip("_")
    return f"{sheet[3:].lower()}_{address:04x}_{text}"[:120]


def parse_unit(value: object) -> tuple[str, float]:
    text = clean(value).replace("℃", "°C")
    if not text or text == "/":
        return "", 1.0
    match = UNIT_RE.match(text)
    if not match:
        return UNIT_ALIASES.get(text, ""), 1.0
    unit = UNIT_ALIASES.get(match.group(2).strip(), "")
    # Some cells in the workbook use the Unit column for bit definitions or
    # notes.  They are documentation, not a Home Assistant unit.
    return unit, float(match.group(1)) if unit else 1.0


def device_metadata(description: str, unit: str) -> list[str]:
    lower = description.lower()
    if unit == "V":
        return ["    device_class: voltage", "    state_class: measurement"]
    if unit == "A":
        return ["    device_class: current", "    state_class: measurement"]
    if unit == "W":
        return ["    device_class: power", "    state_class: measurement"]
    if unit == "Hz":
        return ["    device_class: frequency", "    state_class: measurement"]
    if unit == "°C":
        return ["    device_class: temperature", "    state_class: measurement"]
    if unit == "%":
        return ["    device_class: battery", "    state_class: measurement"] if "soc" in lower or "battery" in lower else ["    state_class: measurement"]
    if unit in {"Wh", "kWh"}:
        return ["    device_class: energy", "    state_class: total_increasing"]
    return []


def accuracy(scale: float) -> int:
    value = f"{scale:.8f}".rstrip("0")
    return len(value.split(".")[1]) if "." in value else 0


def telemetry_rows(workbook: openpyxl.Workbook):
    for sheet_name in TELEMETRY_SHEETS:
        sheet = workbook[sheet_name]
        for row in sheet.iter_rows(min_row=2, values_only=True):
            address, permission, description = row[1], clean(row[4]), clean(row[5])
            if not isinstance(address, (int, float)) or permission not in {"RO", "Read Only"}:
                continue
            if not description or description.lower() == "reserved":
                continue
            yield sheet_name, int(address), description, clean(row[6]), row[7], clean(row[8])


def write_telemetry(workbook: openpyxl.Workbook, source_name: str) -> int:
    target = OUTPUT / "telemetry"
    target.mkdir(parents=True, exist_ok=True)
    count = 0
    for sheet_name in TELEMETRY_SHEETS:
        lines = [
            f"# Generated from {source_name}. Do not edit by hand.",
            f"# Source worksheet: {sheet_name}",
            "sensor:",
        ]
        rows = [item for item in telemetry_rows(workbook) if item[0] == sheet_name]
        for _, address, description, datatype, raw_unit, usage in rows:
            unit, scale = parse_unit(raw_unit)
            value_type = VALUE_TYPES.get(datatype, "U_WORD")
            lines.extend([
                "  - platform: modbus_controller",
                "    modbus_controller_id: easun_sms",
                f"    id: {make_id(sheet_name, address, description)}",
                f"    name: {yaml_string('${friendly_name} ' + description)}",
                f"    address: 0x{address:04X}",
                "    register_type: holding",
                f"    value_type: {value_type}",
                "    entity_category: diagnostic" if not unit else "",
            ])
            if unit:
                lines.append(f"    unit_of_measurement: {yaml_string(unit)}")
                lines.extend(device_metadata(description, unit))
                lines.append(f"    accuracy_decimals: {accuracy(scale)}")
                if scale != 1:
                    lines.extend(["    filters:", f"      - multiply: {scale}"])
            if usage:
                lines.append(f"    # {usage.splitlines()[0]}")
            lines.extend(["", ""])
            count += 1
        (target / f"{sheet_name[3:].lower()}.yaml").write_text("\n".join(line for line in lines if line != "") + "\n", encoding="utf-8")
    return count


def write_base() -> None:
    (OUTPUT / "base.yaml").write_text("""# Core transport for the Easun SMS / CVTE inverter family.\n# Include this package and the telemetry package from your device configuration.\nsubstitutions:\n  easun_modbus_address: \"0x01\"\n  easun_update_interval: 5s\n\nuart:\n  id: easun_uart\n  tx_pin: ${tx_pin}\n  rx_pin: ${rx_pin}\n  baud_rate: 9600\n  data_bits: 8\n  parity: NONE\n  stop_bits: 1\n\nmodbus:\n  id: easun_modbus\n  uart_id: easun_uart\n  send_wait_time: 250ms\n\nmodbus_controller:\n  - id: easun_sms\n    address: ${easun_modbus_address}\n    modbus_id: easun_modbus\n    command_throttle: 50ms\n    update_interval: ${easun_update_interval}\n""", encoding="utf-8")


def write_telemetry_index() -> None:
    includes = "\n".join(
        f"  {name[3:].lower()}: !include telemetry/{name[3:].lower()}.yaml"
        for name in TELEMETRY_SHEETS
    )
    (OUTPUT / "telemetry.yaml").write_text(
        "# Complete safe read-only register map.\npackages:\n" + includes + "\n",
        encoding="utf-8",
    )


def write_readme(count: int, source_name: str) -> None:
    (OUTPUT / "README.md").write_text(f"""# Easun SMS ESPHome package\n\nThis package was generated from `modbus/original/{source_name}`.\nIt exposes **{count} documented read-only telemetry registers** from the runtime worksheets.\n\nUse it from an ESPHome device configuration:\n\n```yaml\nsubstitutions:\n  friendly_name: Easun SMS\n  tx_pin: GPIO16\n  rx_pin: GPIO17\n\npackages:\n  transport: !include base.yaml\n  telemetry: !include telemetry.yaml\n```\n\n`base.yaml` requires the ESPHome `uart`, `modbus`, and `modbus_controller` components; it does not create Wi-Fi, API, OTA, or logger configuration.\n\nThe package deliberately excludes writable settings and factory-control pages. Those controls can reset, calibrate, drive power electronics, or overwrite firmware and are not safe to publish automatically.\n\nRegenerate after replacing the source workbook:\n\n```sh\npython3 tools/generate_esphome_library.py\n```\n""", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    workbook = openpyxl.load_workbook(args.source, read_only=True, data_only=True)
    count = write_telemetry(workbook, args.source.name)
    write_base()
    write_telemetry_index()
    write_readme(count, args.source.name)
    print(f"Generated {count} telemetry entities in {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

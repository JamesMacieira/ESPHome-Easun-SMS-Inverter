# ESPHome Easun SMS Inverter

![Easun SMS](images/Easun%20SMS%206.5KP.jpg)

An open-source ESPHome integration for Easun SMS Hybrid Inverters.

This project aims to provide a complete Modbus implementation for the new Easun SMS inverter platform, including documentation, ESPHome configuration, Home Assistant integration and protocol reverse engineering.

## Current Status

🚧 Early development

The project is currently focused on:

- Translating the official Modbus documentation
- Mapping every register
- Building a native ESPHome configuration
- Testing on real hardware

## Supported Models

Currently tested:

- Easun SMS-6.2KP-W

Planned:

- SMS-6.5KP-W-E
- Other CVTE based models

## Repository Structure

- `docs/` — official Modbus workbooks; `CVTE_Modbus_v1.20 - simplex.xlsx` is the clean reference.
- `modules/` — ESPHome telemetry modules.
- `easun_sms.yaml` — package that combines the available, read-only modules.
- `examples/` — complete device configurations.
- `tools/` — conversion and generation utilities.

## Goals

✔ Complete Modbus register map

✔ ESPHome native integration

✔ Home Assistant ready

✔ Alarm decoding

✔ Configuration registers

✔ Community documentation

## Install the ESPHome package

The safe, read-only telemetry modules are derived from
`docs/CVTE_Modbus_v1.20 - simplex.xlsx`.

Add this package to a device configuration that already defines the `uart`,
`modbus`, and `modbus_controller` IDs used by the package (`uart_0`,
`modbus_0`, and `sms_0`):

```yaml
packages:
  easun_sms: github://JamesMacieira/ESPHome-Easun-SMS-Inverter/easun_sms.yaml@main
```

With 285 Sensors

See `examples/easun-65kp.yaml` for a complete starting configuration.
Factory, calibration, drive-test, OTA, and writable user-setting registers are
intentionally not published as Home Assistant controls until validated on real
hardware.

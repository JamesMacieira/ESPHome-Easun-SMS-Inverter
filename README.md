# ESPHome Easun SMS Inverter

![Easun SMS](image/Easun_SMS_6.5KP.jpg)

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

/docs
Technical documentation

/modbus
Official Modbus documentation and translated register database

/esphome
ESPHome packages

/research
Notes, firmware information and protocol analysis

/tools
Utilities used during development

/esphome/packages/easun_sms
Generated, reusable ESPHome Modbus package

## Goals

✔ Complete Modbus register map

✔ ESPHome native integration

✔ Home Assistant ready

✔ Alarm decoding

✔ Configuration registers

✔ Community documentation

## ESPHome package generated from the Excel map

The complete safe read-only map is generated directly from
`modbus/original/CVTE_Modbus_v1.20 - simplex.xlsx`, the cleaned version of
the original protocol workbook. It provides the documented runtime entities,
grouped by the worksheet that defines them.

Add the package to an ESPHome configuration:

```yaml
substitutions:
  friendly_name: Easun SMS
  tx_pin: GPIO16
  rx_pin: GPIO17

packages:
  transport: !include esphome/packages/easun_sms/base.yaml
  telemetry: !include esphome/packages/easun_sms/telemetry.yaml
```

See `esphome/packages/easun_sms/README.md` for scope and regeneration
instructions. Factory, calibration, drive-test and firmware-update registers
are intentionally not published as Home Assistant controls.

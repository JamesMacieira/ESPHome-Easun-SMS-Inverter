# ESPHome Easun SMS Inverter

![Easun SMS](images/Easun%20SMS%206.5KP.jpg)

An open-source ESPHome integration for Easun SMS Hybrid Inverters.

This project provides a native ESPHome implementation of the Easun SMS Modbus protocol, based on the official manufacturer Modbus register map and validated on real hardware.

It includes complete telemetry, writable configuration registers, Home Assistant integration and ongoing protocol documentation.

## Current Status

🟢 Active Development

Current implementation includes:

* Complete Modbus register map
* Native ESPHome integration
* Home Assistant entities
* Read and write Modbus support
* Alarm and fault decoding
* Real hardware validation

Available Packages

easun_sms.yaml (Full)

Complete implementation of the official Modbus register map.

Includes:

* Approximately 285 entities
* All readable registers
* All writable registers
* Advanced diagnostic registers
* Factory and engineering configuration

Recommended for:

* Developers
* Reverse engineering
* Advanced users
* Complete inverter control

⸻

easun_sms_lite.yaml (Lite)

Optimized package for a standalone inverter installation.

Includes approximately 60 carefully selected entities covering:

* PV
* Battery
* Grid
* Load
* Inverter
* Temperatures
* Alarms
* Daily operation

Also includes the most commonly used writable settings while intentionally excluding factory, calibration and potentially destructive parameters.

Recommended for:

* Home Assistant
* Everyday monitoring
* Most users



## Supported Models

Validated

* ✅ Easun SMS-6.2KP-W

Under Validation

* Easun SMS-6.5KP-W-E

Other CVTE-based models may also be compatible but have not yet been validated.

## Repository Structure

ESPHome-Easun-SMS-Inverter/
│
├── docs/
│   Official Modbus documentation
│
├── modules/
│   ESPHome telemetry modules
│
├── examples/
│   Complete ESPHome configurations
│
├── tools/
│   Register conversion utilities
│
├── easun_sms.yaml
│   Complete package
│
└── easun_sms_lite.yaml
    Optimized package

Features

* ✅ Complete Modbus register map
* ✅ Native ESPHome integration
* ✅ Home Assistant ready
* ✅ Alarm decoding
* ✅ Fault decoding
* ✅ Read registers
* ✅ Write registers
* ✅ Full engineering package
* ✅ Optimized Lite package
* 🚧 Continuous validation and improvements

## Install the ESPHome package

The safe, read-only telemetry modules are derived from
`docs/CVTE_Modbus_v1.20 - simplex.xlsx`.

Add this package to a device configuration that already defines the `uart`,
`modbus`, and `modbus_controller` IDs used by the package (`uart_0`,
`modbus_0`, and `sms_0`):

Full Package

```yaml
packages:
  easun_sms: github://JamesMacieira/ESPHome-Easun-SMS-Inverter/easun_sms.yaml@main
```
Lite Package
```yaml
packages:
  easun_sms: github://JamesMacieira/ESPHome-Easun-SMS-Inverter/easun_sms_lite.yaml@main
```
Example Configuration

A complete ESPHome configuration is available at:

examples/easun-65kp.yaml (Full Version)
examples/easun-65kp-lite.yaml (Lite Version)



Safety Notice

The Full package exposes every writable register documented by the manufacturer.

Some registers may modify inverter behaviour, operating parameters, calibration or factory settings.

Only change writable registers if you fully understand their function.

The Lite package exposes only commonly used, non-destructive settings intended for normal day-to-day operation.

⸻

Project Goals

* Maintain the most complete open-source Modbus implementation for Easun SMS Hybrid Inverters.
* Keep compatibility with native ESPHome and Home Assistant.
* Document the complete manufacturer register map.
* Validate registers on real hardware.
* Provide a safe Lite package for everyday users and a complete Full package for advanced users and development.

⸻

Contributing

Contributions, testing, bug reports and improvements are welcome.

If you own a compatible Easun SMS inverter, feedback and validation of additional models are highly appreciated.
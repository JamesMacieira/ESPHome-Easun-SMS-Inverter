# Easun SMS ESPHome package

This package was generated from `modbus/original/CVTE_Modbus_v1.20 - simplex.xlsx`.
It exposes **267 documented read-only telemetry registers** from the runtime worksheets.

Use it from an ESPHome device configuration:

```yaml
substitutions:
  friendly_name: Easun SMS
  tx_pin: GPIO16
  rx_pin: GPIO17

packages:
  transport: !include base.yaml
  telemetry: !include telemetry.yaml
```

`base.yaml` requires the ESPHome `uart`, `modbus`, and `modbus_controller` components; it does not create Wi-Fi, API, OTA, or logger configuration.

The package deliberately excludes writable settings and factory-control pages. Those controls can reset, calibrate, drive power electronics, or overwrite firmware and are not safe to publish automatically.

Regenerate after replacing the source workbook:

```sh
python3 tools/generate_esphome_library.py
```

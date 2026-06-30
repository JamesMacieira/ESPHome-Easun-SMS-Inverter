# ESPHome Easun SMS Inverter

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

## Goals

✔ Complete Modbus register map

✔ ESPHome native integration

✔ Home Assistant ready

✔ Alarm decoding

✔ Configuration registers

✔ Community documentation

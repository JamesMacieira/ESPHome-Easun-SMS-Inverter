#pragma once

#include "esphome/components/modbus_controller/modbus_controller.h"

namespace easun_sms {

// Write one holding register with FC16, then immediately read it back with FC3.
// The entity state is published only when the inverter returns the exact value
// that was requested. Normal periodic polling remains controlled by
// skip_updates in setup.yaml.
template<typename Entity, typename Value> void write_and_verify(
    esphome::modbus_controller::ModbusController *controller, Entity *entity, uint16_t address, uint16_t requested,
    Value requested_state) {
  using namespace esphome::modbus_controller;

  auto write_command = ModbusCommandItem::create_write_multiple_command(
      controller, address, 1, std::vector<uint16_t>{requested});

  write_command.on_data_func = [controller, entity, requested, requested_state](
                                   ModbusRegisterType register_type, uint16_t start_address,
                                   const std::vector<uint8_t> &data) {
    controller->on_write_register_response(register_type, start_address, data);

    auto read_command = ModbusCommandItem::create_read_command(
        controller, ModbusRegisterType::HOLDING, start_address, 1,
        [entity, requested, requested_state](ModbusRegisterType, uint16_t read_address,
                                             const std::vector<uint8_t> &response) {
          if (response.size() < 2) {
            ESP_LOGE("easun_sms", "Readback failed for register 0x%04X: response too short", read_address);
            return;
          }

          const uint16_t actual = (static_cast<uint16_t>(response[0]) << 8) | response[1];
          if (actual != requested) {
            ESP_LOGE("easun_sms", "Readback mismatch for register 0x%04X: requested %u, got %u", read_address,
                     requested, actual);
            return;
          }

          entity->publish_state(requested_state);
          ESP_LOGI("easun_sms", "Write confirmed by inverter for register 0x%04X", read_address);
        });
    controller->queue_command(read_command);
  };

  controller->queue_command(write_command);
}

}  // namespace easun_sms

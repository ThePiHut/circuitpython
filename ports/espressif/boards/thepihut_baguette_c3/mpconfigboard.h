// This file is part of the CircuitPython project: https://circuitpython.org
//
// SPDX-License-Identifier: MIT

#pragma once

// Board setup
#define MICROPY_HW_BOARD_NAME       "ThePiHut Baguette C3"
#define MICROPY_HW_MCU_NAME         "ESP32-C3-MINI-1-H4"

// Status LED (GPIO8)
#define MICROPY_HW_NEOPIXEL         (&pin_GPIO8)

// I2C (Qwiic connector)
#define CIRCUITPY_BOARD_I2C         (1)
#define CIRCUITPY_BOARD_I2C_PIN     {{.scl = &pin_GPIO6, .sda = &pin_GPIO5}}

// UART
#define CIRCUITPY_BOARD_UART        (1)
#define CIRCUITPY_BOARD_UART_PIN    {{.tx = &pin_GPIO21, .rx = &pin_GPIO20}}

// For entering safe mode
#define CIRCUITPY_BOOT_BUTTON       (&pin_GPIO9)
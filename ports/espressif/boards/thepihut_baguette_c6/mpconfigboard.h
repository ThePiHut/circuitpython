// This file is part of the CircuitPython project: https://circuitpython.org
//
// SPDX-License-Identifier: MIT

#pragma once

// Board setup
#define MICROPY_HW_BOARD_NAME       "ThePiHut Baguette C6"
#define MICROPY_HW_MCU_NAME         "ESP32-C6-MINI-1-N4"

// RGB LED (GPIO8)
#define MICROPY_HW_NEOPIXEL         (&pin_GPIO8)

// I2C (Qwiic connector)
#define CIRCUITPY_BOARD_I2C         (1)
#define CIRCUITPY_BOARD_I2C_PIN     {{.scl = &pin_GPIO6, .sda = &pin_GPIO5}}

// SD Card (using standard SPI pins)
#define CIRCUITPY_BOARD_SPI         (1)
#define CIRCUITPY_BOARD_SPI_PIN     {{.clock = &pin_GPIO21, .mosi = &pin_GPIO19, .miso = &pin_GPIO20}}

// UART
#define CIRCUITPY_BOARD_UART        (1)
#define CIRCUITPY_BOARD_UART_PIN    {{.tx = &pin_GPIO16, .rx = &pin_GPIO17}}

// For entering safe mode
#define CIRCUITPY_BOOT_BUTTON       (&pin_GPIO9)

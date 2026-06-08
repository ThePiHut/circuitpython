// This file is part of the CircuitPython project: https://circuitpython.org
//
// SPDX-FileCopyrightText: Copyright (c) 2019 Scott Shawcroft for Adafruit Industries
//
// SPDX-License-Identifier: MIT

#pragma once

// Board setup
#define MICROPY_HW_BOARD_NAME       "ThePiHut Baguette S3"
#define MICROPY_HW_MCU_NAME         "ESP32-S3-MINI-1-N8"

// Status LED (GPIO8)
#define MICROPY_HW_NEOPIXEL         (&pin_GPIO8)

// I2C (Qwiic connector)
#define CIRCUITPY_BOARD_I2C         (1)
#define CIRCUITPY_BOARD_I2C_PIN     {{.scl = &pin_GPIO48, .sda = &pin_GPIO47}}

// UART
#define CIRCUITPY_BOARD_UART        (1)
#define CIRCUITPY_BOARD_UART_PIN    {{.tx = &pin_GPIO44, .rx = &pin_GPIO43}}

// For entering safe mode
#define CIRCUITPY_BOOT_BUTTON       (&pin_GPIO0)


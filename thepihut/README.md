# ThePiHut Baguette Board Development Files

This folder contains internal development and testing files for the Baguette CircuitPython board definitions (C3, S3, C6). These files are **not** part of any upstream repository submissions.

## Contents

- **testing.md** - Build and flash instructions for all three boards
- **TEST_GUIDE.md** - Comprehensive testing guide with expected outputs
- **test_pins.py** - GPIO pin verification script
- **test_wifi.py** - WiFi connectivity test script
- **test_i2c.py** - I2C/Qwiic bus test script
- **test_sdcard.py** - SD card read/write test (S3 only)

## Quick Start

1. Build firmware for your board (see `testing.md`)
2. Flash to the board using esptool.py (see `testing.md`)
3. Connect board to USB in Thonny
4. Run test scripts one at a time (see `TEST_GUIDE.md`)

## Boards Supported

- **C3** - ESP32-C3-MINI (16-pin breadboard)
- **S3** - ESP32-S3-MINI (30-pin breadboard)
- **C6** - ESP32-C6-MINI (pending hardware revision - excluded from testing)

## Testing Status

### C3
- GPIO Pins: ✓
- WiFi: ✓
- I2C/Qwiic: ✓
- LED (GPIO8 NeoPixel): ✓

### S3
- GPIO Pins: ✓
- WiFi: ✓
- I2C/Qwiic: ✓
- LED (GPIO8 NeoPixel): ✓
- SD Card: (to be tested)

### C6
- LED (GPIO8 NeoPixel): ✓
- Status LED (GPIO23): ⚠️ Hardware issue
- Pending hardware revision

## Not for Submission

These files are internal development tools and should **not** be included in any pull requests to upstream repositories. They're kept here for reference and future development work.

## Notes

- Test scripts are designed to be run in Thonny IDE
- Some tests are optional (like WiFi if network not available)
- SD card test (S3) requires formatted micro SD card inserted
- I2C test reports success even if no devices are connected (expected)

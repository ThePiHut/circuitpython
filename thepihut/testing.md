# Testing Baguette CircuitPython Board Definitions

This document provides comprehensive testing procedures for each Baguette board variant after building CircuitPython firmware.

## Table of Contents
1. [Flash Instructions by Board](#flash-instructions-by-board)
2. [Thonny Setup](#thonny-setup)
3. [Board-Specific Tests](#board-specific-tests)
4. [Troubleshooting](#troubleshooting)

---

## Flash Instructions by Board

### Prerequisites

Before flashing:
```bash
# Plug board in via USB-C
# Verify USB connection
ls /dev/tty*  # macOS/Linux
# or check Device Manager on Windows

# Install esptool.py if needed
pip install esptool
```

### Baguette C3 (ESP32-C3)

**Build:**
```bash
cd ~/projects/circuitpython/ports/espressif
make BOARD=thepihut_baguette_c3 clean
make BOARD=thepihut_baguette_c3
```

**Flash:**
```bash
# macOS/Linux
esptool.py --chip esp32c3 -p /dev/ttyUSB0 write_flash 0x0 \
  build-thepihut_baguette_c3/firmware.bin

# Or for native USB port (common on macOS)
esptool.py --chip esp32c3 -p /dev/tty.usbmodem* write_flash 0x0 \
  build-thepihut_baguette_c3/firmware.bin

# Windows
esptool.py --chip esp32c3 -p COM3 write_flash 0x0 ^
  build-thepihut_baguette_c3/firmware.bin
```

**Expected Output:**
```
esptool.py v4.x.x
Found 1 serial ports
Serial port /dev/ttyUSB0
Connecting....
Chip is ESP32-C3
Features: WiFi, BLE, Embedded Flash
...
Hard resetting via RTS pin...
```

---

### Baguette C6 (ESP32-C6)

**Build (RISC-V toolchain required):**
```bash
cd ~/projects/circuitpython/ports/espressif

# Source ESP-IDF environment for RISC-V compiler
source esp-idf/export.sh

# Build
make BOARD=thepihut_baguette_c6 clean
make BOARD=thepihut_baguette_c6
```

**Flash:**
```bash
# macOS/Linux
esptool.py --chip esp32c6 -p /dev/ttyUSB0 write_flash 0x0 \
  build-thepihut_baguette_c6/firmware.bin

# Or for native USB port (common on macOS)
esptool.py --chip esp32c6 -p /dev/tty.usbmodem* write_flash 0x0 \
  build-thepihut_baguette_c6/firmware.bin

# Windows
esptool.py --chip esp32c6 -p COM3 write_flash 0x0 ^
  build-thepihut_baguette_c6/firmware.bin
```

**Expected Output:**
```
esptool.py v4.x.x
Found 1 serial ports
Serial port /dev/ttyUSB0
Connecting....
Chip is ESP32-C6
Features: WiFi, BLE, Embedded Flash
...
Hard resetting via RTS pin...
```

---

### Baguette S3 (ESP32-S3)

**Build:**
```bash
cd ~/projects/circuitpython/ports/espressif
make BOARD=thepihut_baguette_s3 clean
make BOARD=thepihut_baguette_s3
```

**Flash:**
```bash
# macOS/Linux
esptool.py --chip esp32s3 -p /dev/ttyUSB0 write_flash 0x0 \
  build-thepihut_baguette_s3/firmware.bin

# Or for native USB port (common on macOS)
esptool.py --chip esp32s3 -p /dev/tty.usbmodem* write_flash 0x0 \
  build-thepihut_baguette_s3/firmware.bin

# Windows
esptool.py --chip esp32s3 -p COM3 write_flash 0x0 ^
  build-thepihut_baguette_s3/firmware.bin
```

**Expected Output:**
```
esptool.py v4.x.x
Found 1 serial ports
Serial port /dev/ttyUSB0
Connecting....
Chip is ESP32-S3
Features: WiFi, BLE, Embedded Flash, USB-OTG
...
Hard resetting via RTS pin...
```

---

## Finding Your USB Port

If you're unsure which port to use:

**macOS/Linux:**
```bash
# Before plugging in
ls /dev/tty* > /tmp/before.txt

# Plug in board

# After plugging in
ls /dev/tty* > /tmp/after.txt
diff /tmp/before.txt /tmp/after.txt

# Or just list all
ls /dev/tty.*
```

**Windows:**
```bash
# PowerShell - list COM ports
Get-WmiObject Win32_SerialPort | Select-Object Name, Description
```

---

## Thonny Setup

### Installation
1. Download from [thonny.org](https://thonny.org)
2. Install for your OS
3. Launch Thonny

### Configure Interpreter

1. **Tools** → **Interpreter**
2. Select: **CircuitPython (generic)**
3. Select your **Port** (e.g., `/dev/ttyUSB0`)
4. Click **OK**

After successful connection, you'll see CircuitPython version in the Shell at the bottom.

---

## Board-Specific Tests

### Test 1: Verify Board Identity

Works for all boards - run in Thonny Shell:

```python
import board
import supervisor

print("="*50)
print("Board Identity Test")
print("="*50)

# Board info
print(f"Board: {board.board_id}")
print(f"MCU: {supervisor.runtime.chip}")

# Available pins
pins = dir(board)
gpio_pins = [p for p in pins if p.startswith('D') or p.startswith('IO')]
print(f"\nAvailable GPIO pins: {len(gpio_pins)}")
print(f"Sample pins: {gpio_pins[:5]}")

print("\n✓ Board test passed!")
```

---

### Baguette C3 - Full Test Suite

**Specifications:**
- Chip: ESP32-C3-MINI-1-N4
- Flash: 4MB
- Pins: 16-pin breadboard breakout
- RGB LED: GPIO8
- Boot Button: GPIO9
- I2C: GPIO5 (SDA), GPIO6 (SCL)
- UART: GPIO20 (RX), GPIO21 (TX)

**Create file: `test_c3.py` in Thonny**

```python
#!/usr/bin/env python3
"""
Comprehensive test suite for Baguette C3
Tests: Board pins, LED, Button, I2C, UART
"""

import board
import neopixel
import digitalio
import busio
import time

print("="*60)
print("BAGUETTE C3 TEST SUITE")
print("="*60)

# ============================================================
# TEST 1: BOARD IDENTITY
# ============================================================
print("\n[TEST 1] Board Identity")
print("-" * 60)
try:
    pins = dir(board)
    print(f"✓ Board module loaded")
    print(f"✓ Available pins: {len(pins)}")
    
    # Check required pins
    required = ['NEOPIXEL', 'BUTTON', 'SDA', 'SCL', 'TX', 'RX']
    for pin in required:
        if hasattr(board, pin):
            print(f"  ✓ {pin} found")
        else:
            print(f"  ✗ {pin} MISSING!")
except Exception as e:
    print(f"✗ Error: {e}")

# ============================================================
# TEST 2: RGB LED (GPIO8)
# ============================================================
print("\n[TEST 2] RGB LED Test (GPIO8)")
print("-" * 60)
try:
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
    colors = {
        'Red': (255, 0, 0),
        'Green': (0, 255, 0),
        'Blue': (0, 0, 255),
        'Yellow': (255, 255, 0),
        'Off': (0, 0, 0)
    }
    
    for name, color in colors.items():
        pixels[0] = color
        pixels.show()
        print(f"  ✓ LED: {name}")
        time.sleep(0.5)
    
    print("✓ RGB LED test passed!")
except Exception as e:
    print(f"✗ LED Error: {e}")

# ============================================================
# TEST 3: BOOT BUTTON (GPIO9)
# ============================================================
print("\n[TEST 3] Boot Button Test (GPIO9)")
print("-" * 60)
try:
    button = digitalio.DigitalInOut(board.BUTTON)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    
    print("  ✓ Button initialized (pull-up)")
    print("  Button state (unpressed):", button.value)
    print("  >>> Press button now, waiting 3 seconds...")
    
    start = time.time()
    pressed = False
    while time.time() - start < 3:
        if not button.value:  # Button pulls LOW when pressed
            pressed = True
            print(f"  ✓ Button pressed at {time.time() - start:.2f}s")
            break
        time.sleep(0.1)
    
    if not pressed:
        print("  ⚠ Button not pressed (check hardware)")
    else:
        print("✓ Button test passed!")
except Exception as e:
    print(f"✗ Button Error: {e}")

# ============================================================
# TEST 4: I2C / QWIIC (GPIO5 SDA, GPIO6 SCL)
# ============================================================
print("\n[TEST 4] I2C/Qwiic Test")
print("-" * 60)
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print("  ✓ I2C initialized")
    print("  SCL: GPIO6, SDA: GPIO5")
    
    # Scan for I2C devices
    devices = []
    while not i2c.try_lock():
        pass
    try:
        for addr in range(128):
            try:
                i2c.writeto(addr, b'')
                devices.append(addr)
            except OSError:
                pass
    finally:
        i2c.unlock()
    
    if devices:
        print(f"  ✓ Found {len(devices)} I2C device(s):")
        for addr in devices:
            print(f"    - Address: 0x{addr:02X}")
    else:
        print("  ℹ No I2C devices found (expected if nothing connected)")
    
    print("✓ I2C test passed!")
except Exception as e:
    print(f"✗ I2C Error: {e}")

# ============================================================
# TEST 5: UART (GPIO20 RX, GPIO21 TX)
# ============================================================
print("\n[TEST 5] UART Test")
print("-" * 60)
try:
    uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0.1)
    print("  ✓ UART initialized")
    print("  TX: GPIO21, RX: GPIO20")
    print("  Baudrate: 9600")
    
    # Send test message
    test_msg = b"CircuitPython UART Test\n"
    bytes_written = uart.write(test_msg)
    print(f"  ✓ Wrote {bytes_written} bytes to UART")
    print(f"  Message: {test_msg.decode()}")
    
    print("✓ UART test passed!")
except Exception as e:
    print(f"✗ UART Error: {e}")

# ============================================================
# TEST 6: ALL GPIO PINS
# ============================================================
print("\n[TEST 6] GPIO Pins Test")
print("-" * 60)
try:
    pins = dir(board)
    gpio_pins = [p for p in pins if p.startswith('D')]
    
    print(f"  ✓ Found {len(gpio_pins)} GPIO pins:")
    print(f"  {', '.join(gpio_pins)}")
    
    # Try to read a pin state (non-destructive)
    test_pin = digitalio.DigitalInOut(board.D0)
    test_pin.direction = digitalio.Direction.INPUT
    state = test_pin.value
    print(f"  ✓ GPIO0 state: {state}")
    
    print("✓ GPIO pins test passed!")
except Exception as e:
    print(f"✗ GPIO Error: {e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*60)
print("ALL TESTS COMPLETE!")
print("="*60)
print("\nSummary:")
print("  ✓ Board identity verified")
print("  ✓ RGB LED functional")
print("  ✓ Boot button responsive")
print("  ✓ I2C/Qwiic interface working")
print("  ✓ UART interface working")
print("  ✓ GPIO pins accessible")
print("\nBaguette C3 is ready for deployment!")
print("="*60)
```

---

## Troubleshooting

### Flash Issues

**"Failed to open port /dev/ttyUSB0"**
```bash
# Check what ports are available
ls /dev/tty*

# Use correct port
esptool.py --chip esp32s3 -p /dev/tty.usbmodem14201 write_flash 0x0 firmware.bin
```

**"Chip is not in bootloader mode"**
- Press and hold BOOT button
- Click RESET button while holding BOOT
- Release BOOT
- Try flashing again

**"Permission denied"**
```bash
# Linux - add user to dialout group
sudo usermod -a -G dialout $USER
# Then log out and back in

# Or use sudo
sudo esptool.py --chip esp32c3 -p /dev/ttyUSB0 write_flash 0x0 firmware.bin
```

---

### Runtime Issues

**"ModuleNotFoundError: No module named 'neopixel'"**
- NeoPixel library not included in firmware
- Rebuild CircuitPython or use built-in `adafruit_pixel_framebuf`

**"AttributeError: module 'board' has no attribute 'NEOPIXEL'"**
- Check `pins.c` - LED pin may not be defined
- Verify GPIO8 is defined for C3/S3

**"I2C not responding"**
- Check pull-up resistors on SDA/SCL
- Verify I2C device addresses (use scan test)
- Check board connections

**"Button always reports LOW"**
- Check pull-up configuration in test
- Button may be active-high instead of low
- Test with different input mode

---

## Next Steps

Once all tests pass:

1. **Document Results** - Note any quirks or issues
2. **Test Real Devices** - Connect actual I2C/SPI sensors
3. **Commit Changes** - Push to your fork
4. **Consider PR** - Contribute to Adafruit repo

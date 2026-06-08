# Baguette Board Testing Guide

This guide covers comprehensive testing of the Baguette C3 and S3 boards using CircuitPython.

## Overview

Four test scripts are provided:
- **test_pins.py** - GPIO pin verification
- **test_wifi.py** - WiFi connectivity
- **test_i2c.py** - I2C/Qwiic connector
- **test_sdcard.py** - SD card read/write (S3 only)

## Prerequisites

1. **Board flashed with CircuitPython firmware** (see `testing.md`)
2. **Thonny IDE** installed on your computer
3. **USB cable** connected to the board
4. **WiFi credentials** (for WiFi test)
5. **Optional**: I2C/Qwiic device for full I2C testing
6. **Optional**: Micro SD card in slot (for S3 SD card test)

## Running Tests

### Setup in Thonny

1. Connect your board to USB
2. Open Thonny
3. Go to **Tools → Options → Interpreter**
4. Select **CircuitPython** as interpreter
5. Select your board from the device list
6. Click **OK**

### Test 1: GPIO Pins (All Boards)

**File:** `test_pins.py`

This test verifies all GPIO pins are accessible and can toggle.

```bash
# In Thonny Shell or File → Run
run test_pins.py
```

**Expected Output:**
- Lists all available GPIO pins (D0, D1, etc.)
- Shows ✓ for each pin that works
- Shows final pass/fail count
- ✅ All pins should pass

**What it tests:**
- Initializing each pin as digital output
- Setting pin high/low
- Cleaning up properly

---

### Test 2: WiFi (C3 and S3)

**File:** `test_wifi.py`

This test verifies WiFi scanning, connection, and HTTP requests.

**Before running:**
1. Open `test_wifi.py` in Thonny
2. Edit lines 12-14:
   ```python
   WIFI_SSID = "YOUR_SSID"
   WIFI_PASSWORD = "YOUR_PASSWORD"
   ```
3. Save the file
4. Run it

**Expected Output:**
```
[1/4] Scanning for WiFi networks...
  Found: YourNetwork (RSSI: -50)
  ✓ Found 3 networks

[2/4] Connecting to WiFi...
  ✓ Connected to YourNetwork
  IP Address: 192.168.1.100

[3/4] Checking connection status...
  ✓ WiFi is connected
  Signal strength: -50

[4/4] Testing HTTP request...
  ✓ HTTP request successful (Status: 200)
```

**What it tests:**
- WiFi network scanning
- WiFi connection and authentication
- IP address assignment
- Signal strength reporting
- HTTP client functionality

**Troubleshooting:**
- If connection fails: Check SSID/password
- If HTTP fails: Check internet connectivity
- If scan fails: WiFi radio may need restart

---

### Test 3: I2C/Qwiic (C3 and S3)

**File:** `test_i2c.py`

This test verifies I2C bus initialization and device scanning.

```bash
run test_i2c.py
```

**Expected Output (without device):**
```
[1/3] Initializing I2C bus...
  ✓ I2C initialized
  SCL Pin: board.D6
  SDA Pin: board.D5

[2/3] Scanning for I2C devices...
  ℹ️  No I2C devices found (expected if nothing plugged in)

[3/3] Testing I2C read/write capability...
  ℹ️  No device at test address (expected if nothing connected)
```

**Expected Output (with device, e.g., 0x68 address):**
```
[2/3] Scanning for I2C devices...
  ✓ Found 1 device(s):
    - Address: 0x68

[3/3] Testing I2C read/write capability...
  ✓ I2C bus is responsive
```

**What it tests:**
- I2C bus initialization on SCL/SDA pins
- Device address scanning (0x00-0x7F)
- Read/write communication

**Troubleshooting:**
- If I2C fails to initialize: Check pin definitions
- If no devices found: Verify Qwiic device is connected
- If address mismatch: Verify device I2C address

---

### Test 4: SD Card (S3 Only)

**File:** `test_sdcard.py`

This test verifies SD card detection, mounting, and read/write.

**Before running:**
- Insert a formatted micro SD card into the S3 slot
- Run the test

```bash
run test_sdcard.py
```

**Expected Output:**
```
[1/4] Initializing SD card...
  ✓ SPI initialized
  Clock: GPIO21, MOSI: GPIO19, MISO: GPIO20, CS: GPIO18

[2/4] Detecting SD card...
  ✓ SD card detected and mounted at /sd

[3/4] Reading SD card info...
  ✓ SD card info:
    Total: 7872000 KB
    Used: 16384 KB
    Free: 7855616 KB

[4/4] Testing read/write...
  ✓ File written: /sd/circuitpython_test.txt
  ✓ File read successful (data matches)
  ✓ Test file cleaned up
```

**What it tests:**
- SD card SPI bus initialization
- Card detection and mounting
- Storage capacity reporting
- File write/read operations
- File deletion

**Troubleshooting:**
- If SPI fails: Check pin definitions
- If card not detected: Try reinserting card
- If card is corrupted: Format on computer first
- If read/write fails: Card may be write-protected

---

## Test Results Summary

After running all tests, you should have:

### C3 Board ✓
- [ ] All GPIO pins accessible
- [ ] WiFi scanning works
- [ ] WiFi connection successful (if credentials set)
- [ ] I2C bus operational
- [ ] HTTP requests working

### S3 Board ✓
- [ ] All GPIO pins accessible
- [ ] WiFi scanning works
- [ ] WiFi connection successful (if credentials set)
- [ ] I2C bus operational
- [ ] SD card detection and read/write working
- [ ] HTTP requests working

---

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "pin already in use" | Pin used by another test | Restart board |
| I2C fails immediately | Wrong pins in board definition | Check pins.c |
| WiFi won't connect | Credentials wrong or network down | Verify SSID/password |
| SD card not found | Card not inserted or not formatted | Reinsert/reformat card |
| USB connection drops | Firmware issue or bad cable | Try different cable/USB port |

---

## Next Steps

1. **Fix any failing tests** by investigating the specific pin/feature
2. **Document results** with notes on any issues
3. **For passing boards**, proceed to commit:
   ```bash
   git add -A
   git commit -m "Add Baguette C3 and S3 board definitions with tests passing"
   ```

---

## Test Script Details

### test_pins.py
- Uses `digitalio.DigitalInOut` to test each pin
- Tests by toggling HIGH/LOW
- Reports pass/fail for each pin
- Good for finding broken GPIO pins

### test_wifi.py
- Scans available networks (shows signal strength)
- Connects to configured network
- Reports IP address and signal
- Tests HTTP client capability
- Requires credentials to be set

### test_i2c.py
- Initializes I2C on board's SCL/SDA pins
- Scans addresses 0x00-0x7F
- Attempts read/write to test bus
- Gracefully handles no devices found

### test_sdcard.py
- Initializes SPI for SD card
- Mounts card as `/sd` filesystem
- Reports storage stats
- Writes/reads test file
- S3 only (C3 has no SD slot)

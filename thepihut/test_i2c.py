"""
Test I2C/Qwiic connector on Baguette boards
Run in Thonny on C3 or S3
"""

import board
import busio
import time

print("=" * 60)
print("BAGUETTE BOARD I2C/QWIIC TEST")
print("=" * 60)

# Test 1: Initialize I2C bus
print("\n[1/3] Initializing I2C bus...")
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print(f"  ✓ I2C initialized")
    print(f"  SCL Pin: {board.SCL}")
    print(f"  SDA Pin: {board.SDA}")
except Exception as e:
    print(f"  ✗ I2C initialization failed: {e}")
    exit()

# Test 2: Scan for I2C devices
print("\n[2/3] Scanning for I2C devices on Qwiic connector...")
try:
    devices = []
    while not i2c.try_lock():
        pass

    try:
        for addr in range(128):
            try:
                # Try to read 1 byte from the device
                # This is more reliable than writeto with empty data
                result = bytearray(1)
                i2c.writeto_then_readfrom(addr, b'\x00', result)
                devices.append(addr)
            except OSError:
                pass
    finally:
        i2c.unlock()

    if devices:
        print(f"  ✓ Found {len(devices)} device(s):")
        for addr in devices:
            print(f"    - Address: 0x{addr:02X}")
    else:
        print("  ℹ️  No I2C devices found (expected if nothing plugged in)")

except Exception as e:
    print(f"  ✗ I2C scan failed: {e}")

# Test 3: Test I2C read/write
print("\n[3/3] Testing I2C read/write capability...")
try:
    # This tests if we can communicate with the bus
    # It will fail if no device is present, but that's OK
    test_addr = 0x50  # Common EEPROM address

    while not i2c.try_lock():
        pass

    try:
        # Try to read from a standard address
        i2c.writeto(test_addr, b'\x00')
        i2c.readfrom_into(test_addr, bytearray(1))
        print(f"  ✓ I2C bus is responsive")
    except OSError:
        print(f"  ℹ️  No device at test address (expected if nothing connected)")
    finally:
        i2c.unlock()

except Exception as e:
    print(f"  ✗ I2C read/write test failed: {e}")

# Cleanup
try:
    i2c.deinit()
except:
    pass

print("\n" + "=" * 60)
print("I2C TEST COMPLETE")
print("=" * 60)
print("\nTip: Connect a Qwiic device (sensor, display, etc.) to test")
print("     with actual I2C communication")

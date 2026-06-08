"""
Test I2C using board.I2C object instead of busio.I2C
"""

import board
import time

print("=" * 60)
print("I2C TEST - Using board.I2C()")
print("=" * 60)

# Try Method 1: Use board.I2C directly
print("\n[1] Attempting to use board.I2C()...")
try:
    i2c = board.I2C()
    print(f"  ✓ board.I2C() created: {i2c}")
    print(f"  I2C object type: {type(i2c)}")
except Exception as e:
    print(f"  ✗ board.I2C() failed: {e}")
    print(f"  Error type: {type(e)}")
    i2c = None

# If board.I2C works, try scanning
if i2c:
    print("\n[2] Scanning for devices with board.I2C()...")
    try:
        devices = []
        while not i2c.try_lock():
            pass

        try:
            for addr in range(128):
                try:
                    i2c.writeto(addr, b'')
                    devices.append(addr)
                    print(f"  ✓ Device found at 0x{addr:02X}")
                except OSError:
                    pass
        finally:
            i2c.unlock()

        if devices:
            print(f"\n  ✓ Found {len(devices)} device(s)!")
        else:
            print(f"\n  ✗ No devices found")

    except Exception as e:
        print(f"  ✗ Scan failed: {e}")
        print(f"  Error type: {type(e)}")

    # Cleanup
    try:
        i2c.deinit()
    except:
        pass

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

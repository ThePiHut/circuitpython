"""
Test I2C by reading directly from known device addresses
"""

import board
import busio
import time

print("=" * 60)
print("I2C DIRECT READ TEST")
print("=" * 60)

# Initialize I2C
print("\n[1] Initializing I2C on GPIO5/6...")
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print(f"  ✓ I2C initialized")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    exit()

# Try to read from BME280 at 0x77
print("\n[2] Attempting to read from BME280 (0x77)...")
try:
    while not i2c.try_lock():
        pass

    try:
        # BME280 has ID register at 0xD0
        result = bytearray(1)
        i2c.writeto_then_readfrom(0x77, b'\xD0', result)
        print(f"  ✓ Successfully read from 0x77!")
        print(f"  Register 0xD0 value: 0x{result[0]:02X}")

        # BME280 ID should be 0x60
        if result[0] == 0x60:
            print(f"  ✓✓ This is a BME280! (ID matches)")
        else:
            print(f"  ⚠️  Device responds but ID doesn't match BME280")
    except OSError as e:
        print(f"  ✗ No response at 0x77: {e}")
    finally:
        i2c.unlock()
except Exception as e:
    print(f"  ✗ Error: {e}")

# Try to read from VL6180 at 0x29
print("\n[3] Attempting to read from VL6180 (0x29)...")
try:
    while not i2c.try_lock():
        pass

    try:
        # VL6180 has model ID at 0x00E4
        result = bytearray(1)
        i2c.writeto_then_readfrom(0x29, b'\x00\xE4', result)
        print(f"  ✓ Successfully read from 0x29!")
        print(f"  Register 0x00E4 value: 0x{result[0]:02X}")

        # VL6180 model ID should be 0xB4
        if result[0] == 0xB4:
            print(f"  ✓✓ This is a VL6180! (ID matches)")
        else:
            print(f"  ⚠️  Device responds but ID doesn't match VL6180")
    except OSError as e:
        print(f"  ✗ No response at 0x29: {e}")
    finally:
        i2c.unlock()
except Exception as e:
    print(f"  ✗ Error: {e}")

# Cleanup
try:
    i2c.deinit()
except:
    pass

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nIf devices respond, the I2C bus is working!")
print("If not, there may be a hardware/configuration issue.")

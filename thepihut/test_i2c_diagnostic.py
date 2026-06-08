"""
Diagnostic I2C test for Baguette boards
Helps identify I2C bus issues
"""

import board
import busio
import time

print("=" * 60)
print("I2C DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Check pin objects exist
print("\n[1/4] Checking pin objects...")
try:
    scl_pin = board.SCL
    sda_pin = board.SDA
    print(f"  ✓ SCL pin object: {scl_pin}")
    print(f"  ✓ SDA pin object: {sda_pin}")
except Exception as e:
    print(f"  ✗ Pin objects missing: {e}")
    exit()

# Test 2: Try to initialize I2C with different speeds
print("\n[2/4] Trying I2C initialization at different speeds...")
i2c = None
speeds = [100000, 200000, 400000]

for speed in speeds:
    try:
        i2c = busio.I2C(board.SCL, board.SDA, frequency=speed)
        print(f"  ✓ I2C initialized at {speed} Hz")
        break
    except Exception as e:
        print(f"  ✗ Failed at {speed} Hz: {e}")

if i2c is None:
    print("\n  ✗ Could not initialize I2C at any speed - BUS ISSUE!")
    exit()

# Test 3: Try locking/unlocking (tests if bus is responsive)
print("\n[3/4] Testing bus responsiveness...")
try:
    lock_acquired = False
    for attempt in range(5):
        if i2c.try_lock():
            lock_acquired = True
            print(f"  ✓ Bus lock acquired (attempt {attempt + 1})")
            i2c.unlock()
            break
        else:
            print(f"  • Attempt {attempt + 1}: Lock busy (bus might be stuck)")
            time.sleep(0.1)

    if not lock_acquired:
        print("  ✗ Could not acquire I2C lock - BUS LIKELY STUCK")
except Exception as e:
    print(f"  ✗ Lock test failed: {e}")

# Test 4: Scan with detailed diagnostics
print("\n[4/4] Detailed address scan (this may take a moment)...")
try:
    devices = []
    errors = {}

    while not i2c.try_lock():
        time.sleep(0.01)

    try:
        for addr in range(128):
            try:
                # Try to write single byte
                i2c.writeto(addr, b'\x00')
                devices.append(addr)
                print(f"  ✓ Device found at 0x{addr:02X}")
            except OSError as e:
                # Capture which addresses give which errors
                error_code = str(e)
                if error_code not in errors:
                    errors[error_code] = []
                errors[error_code].append(addr)
            except Exception as e:
                print(f"  ✗ Unexpected error at 0x{addr:02X}: {e}")
    finally:
        i2c.unlock()

    print(f"\n  Summary: Found {len(devices)} device(s)")

    if not devices:
        print("\n  ℹ️  No devices found. Checking for common Adafruit devices:")
        print("     BME280: Should be at 0x76 or 0x77")
        print("     VL6180: Should be at 0x29")
        print("     If not found, check:")
        print("     • I2C pull-up resistors (4.7kΩ on SDA/SCL)")
        print("     • Wire connections (no loose wires)")
        print("     • Device power (3.3V)")
        print("     • Device GND connection")

except Exception as e:
    print(f"  ✗ Scan failed: {e}")

# Cleanup
try:
    i2c.deinit()
except:
    pass

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)

"""
Test SD card on Baguette S3
Run in Thonny on S3 only

Note: C3 does not have SD card, so this test is S3-only
"""

import board
import busio
import digitalio
import storage
import os
import time

print("=" * 60)
print("BAGUETTE S3 SD CARD TEST")
print("=" * 60)

# Test 1: Initialize SPI and SD card
print("\n[1/4] Initializing SD card...")
try:
    # S3 SD card pins: SCLK=GPIO9, MOSI=GPIO10, MISO=GPIO11, CS=GPIO7
    spi = busio.SPI(board.D9, board.D10, board.D11)  # SCLK, MOSI, MISO
    cs_pin = board.D7  # CS pin as raw Pin object (not DigitalInOut)

    print(f"  ✓ SPI initialized")
    print(f"  SCLK: GPIO9, MOSI: GPIO10, MISO: GPIO11, CS: GPIO7")

except Exception as e:
    print(f"  ✗ SPI initialization failed: {e}")
    exit()

# Test 2: Try to detect SD card
print("\n[2/4] Detecting SD card...")
try:
    import sdcardio

    sd_card = sdcardio.SDCard(spi, cs_pin)
    vfs = storage.VfsFat(sd_card)
    storage.mount(vfs, "/sd")

    print(f"  ✓ SD card detected and mounted at /sd")

except Exception as e:
    print(f"  ✗ SD card detection failed: {e}")
    print(f"     (SD card might not be inserted or could be corrupted)")
    exit()

# Test 3: Read SD card information
print("\n[3/4] Reading SD card info...")
try:
    stats = os.statvfs("/sd")
    total_space = stats[0] * stats[2]
    free_space = stats[0] * stats[3]
    used_space = total_space - free_space

    print(f"  ✓ SD card info:")
    print(f"    Total: {total_space // 1024} KB")
    print(f"    Used: {used_space // 1024} KB")
    print(f"    Free: {free_space // 1024} KB")

except Exception as e:
    print(f"  ✗ Could not read SD card info: {e}")

# Test 4: Write and read test file
print("\n[4/4] Testing read/write...")
try:
    test_file = "/sd/circuitpython_test.txt"
    test_data = "CircuitPython SD Card Test - " + str(time.time())

    # Write test
    with open(test_file, "w") as f:
        f.write(test_data)
    print(f"  ✓ File written: {test_file}")

    # Read test
    with open(test_file, "r") as f:
        read_data = f.read()

    if read_data == test_data:
        print(f"  ✓ File read successful (data matches)")
    else:
        print(f"  ✗ File read mismatch")

    # Clean up
    os.remove(test_file)
    print(f"  ✓ Test file cleaned up")

except Exception as e:
    print(f"  ✗ Read/write test failed: {e}")

# Cleanup
try:
    storage.umount("/sd")
    print("\n  ✓ SD card unmounted")
except:
    pass

try:
    spi.deinit()
except:
    pass

print("\n" + "=" * 60)
print("SD CARD TEST COMPLETE")
print("=" * 60)
print("\nNote: This test is for S3 only. C3 does not have SD card.")

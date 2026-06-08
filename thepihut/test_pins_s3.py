"""
Test GPIO pins on Baguette S3 (30-pin breakout)
Run in Thonny on S3 only
"""

import board
import digitalio
import time

print("=" * 60)
print("BAGUETTE S3 GPIO PIN TEST (30-pin breakout)")
print("=" * 60)

# S3 specific pins: exposed on the 30-pin connector
# Internal/special pins (D0, D1, D7, D8, D9, D10, D11, D32) are excluded
s3_pins = [
    'D2', 'D3', 'D4', 'D5', 'D6',           # GPIO2-6
    'D12', 'D13', 'D14', 'D15', 'D16',     # GPIO12-16
    'D17', 'D18',                           # GPIO17-18
    'D21',                                  # GPIO21
    'D33', 'D34', 'D35', 'D36', 'D37',     # GPIO33-37
    'D38', 'D39', 'D40', 'D41', 'D42',     # GPIO38-42
    'D43', 'D44', 'D47', 'D48',            # GPIO43-44 (UART), GPIO47-48 (I2C)
]

print(f"\nFound {len(s3_pins)} exposed GPIO pins on S3")
print(f"Pins: {', '.join(s3_pins)}")
print("\nTesting each pin as digital output...")

tested = 0
passed = 0
failed = 0
errors = []

for pin_name in s3_pins:
    try:
        pin_obj = getattr(board, pin_name)
        io = digitalio.DigitalInOut(pin_obj)
        io.direction = digitalio.Direction.OUTPUT

        # Test write
        io.value = True
        time.sleep(0.01)
        io.value = False
        time.sleep(0.01)

        io.deinit()
        tested += 1
        passed += 1
        print(f"  ✓ {pin_name}")

    except Exception as e:
        tested += 1
        failed += 1
        error_msg = f"  ✗ {pin_name}: {str(e)}"
        print(error_msg)
        errors.append(error_msg)

print("\n" + "=" * 60)
print(f"PIN TEST RESULTS: {passed}/{tested} passed")
print("=" * 60)

if failed > 0:
    print(f"\n⚠️  {failed} pin(s) failed:")
    for error in errors:
        print(error)
else:
    print("\n✅ All S3 GPIO pins tested successfully!")

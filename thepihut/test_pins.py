"""
Test all GPIO pins on Baguette boards
Run in Thonny on C3 or S3
"""

import board
import digitalio
import time

print("=" * 60)
print("BAGUETTE BOARD GPIO PIN TEST")
print("=" * 60)

# Get all available pins from board module
all_pins = dir(board)

# Filter only GPIO pins (D0-D42, exclude buses and special)
# Also exclude internal pins: D0, D1, D7 (SD CS), D8 (LED), D9/D10/D11 (SD SPI), D32 (internal)
internal_pins = {'D0', 'D1', 'D7', 'D8', 'D9', 'D10', 'D11', 'D32'}
gpio_pins = [p for p in all_pins if p.startswith('D') and p[1:].isdigit() and p not in internal_pins]
gpio_pins.sort(key=lambda x: int(x[1:]))

print(f"\nFound {len(gpio_pins)} GPIO pins to test")
print(f"Pins: {', '.join(gpio_pins)}")
print("\nTesting each pin as digital output...")

tested = 0
passed = 0
failed = 0
errors = []

for pin_name in gpio_pins:
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
    print("\n✅ All pins tested successfully!")

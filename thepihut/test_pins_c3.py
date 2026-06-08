"""
Test GPIO pins on Baguette C3 (16-pin breadboard breakout)
Run in Thonny on C3 only
"""

import board
import digitalio
import time

print("=" * 60)
print("BAGUETTE C3 GPIO PIN TEST (16-pin breakout)")
print("=" * 60)

# C3 specific pins: exposed on the 16-pin breadboard connector
c3_pins = [
    'D0', 'D1', 'D2', 'D3',                # GPIO0-3
    'D4',                                   # GPIO4
    'D5', 'D6',                            # GPIO5-6 (I2C: SDA, SCL)
    'D7',                                   # GPIO7
    'D8',                                   # GPIO8 (also RGB LED)
    'D9',                                   # GPIO9 (also Boot Button)
    'D10',                                  # GPIO10 (shared)
    'D20', 'D21',                          # GPIO20-21 (UART: RX, TX)
]

print(f"\nFound {len(c3_pins)} exposed GPIO pins on C3")
print(f"Pins: {', '.join(c3_pins)}")
print("\nNote:")
print("  D8  = RGB LED (NeoPixel)")
print("  D9  = Boot Button")
print("  D10 = Shared function")
print("\nTesting each pin as digital output...")

tested = 0
passed = 0
failed = 0
errors = []

for pin_name in c3_pins:
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
    print("\n✅ All C3 GPIO pins tested successfully!")

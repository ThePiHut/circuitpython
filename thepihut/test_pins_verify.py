"""
Verify actual pin mappings on Baguette C3
"""

import board
import digitalio
import time

print("=" * 60)
print("PIN MAPPING VERIFICATION")
print("=" * 60)

# Check what the board thinks SDA/SCL are
print("\n[1] I2C Pin Definitions:")
print(f"  board.SDA = {board.SDA}")
print(f"  board.SCL = {board.SCL}")

# Try to test each pin individually
print("\n[2] Testing GPIO5 as digital output:")
try:
    pin5 = board.D5
    io5 = digitalio.DigitalInOut(pin5)
    io5.direction = digitalio.Direction.OUTPUT
    io5.value = True
    print(f"  ✓ GPIO5 (D5) is working: {pin5}")
    io5.deinit()
except Exception as e:
    print(f"  ✗ GPIO5 failed: {e}")

print("\n[3] Testing GPIO6 as digital output:")
try:
    pin6 = board.D6
    io6 = digitalio.DigitalInOut(pin6)
    io6.direction = digitalio.Direction.OUTPUT
    io6.value = True
    print(f"  ✓ GPIO6 (D6) is working: {pin6}")
    io6.deinit()
except Exception as e:
    print(f"  ✗ GPIO6 failed: {e}")

# Print all available pins
print("\n[4] All available board pins:")
pins = dir(board)
gpio_pins = sorted([p for p in pins if p.startswith('D')])
print(f"  GPIO pins: {', '.join(gpio_pins)}")

# Check if I2C and board.I2C exist
print("\n[5] I2C Objects:")
if hasattr(board, 'I2C'):
    print(f"  ✓ board.I2C exists: {board.I2C}")
else:
    print(f"  ✗ board.I2C does NOT exist")

# Check SDA/SCL in pins
if hasattr(board, 'SDA'):
    print(f"  ✓ board.SDA exists")
else:
    print(f"  ✗ board.SDA does NOT exist")

if hasattr(board, 'SCL'):
    print(f"  ✓ board.SCL exists")
else:
    print(f"  ✗ board.SCL does NOT exist")

print("\n" + "=" * 60)

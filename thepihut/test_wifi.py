"""
Test WiFi connectivity on Baguette boards
Run in Thonny on C3 or S3

Set SSID and PASSWORD below before running
"""

import wifi
import ipaddress
import time

# ===== CONFIGURE THESE =====
WIFI_SSID = "ssid"
WIFI_PASSWORD = "password"
# ==========================

print("=" * 60)
print("BAGUETTE BOARD WIFI TEST")
print("=" * 60)

# Test 1: Scan for networks
print("\n[1/4] Scanning for WiFi networks...")
try:
    networks = wifi.radio.start_scanning_networks()
    num_networks = 0
    for network in networks:
        num_networks += 1
        if num_networks <= 5:  # Show first 5
            print(f"  Found: {network.ssid} (RSSI: {network.rssi})")
    print(f"  ✓ Found {num_networks} networks")
    wifi.radio.stop_scanning_networks()
except Exception as e:
    print(f"  ✗ Scan failed: {e}")

# Test 2: Connect to WiFi
print("\n[2/4] Connecting to WiFi...")
if WIFI_SSID == "YOUR_SSID":
    print("  ⚠️  Please set WIFI_SSID and WIFI_PASSWORD at the top of this script")
else:
    try:
        wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
        print(f"  ✓ Connected to {WIFI_SSID}")
        print(f"  IP Address: {wifi.radio.ipv4_address}")
    except Exception as e:
        print(f"  ✗ Connection failed: {e}")

# Test 3: Check connection status
print("\n[3/4] Checking connection status...")
try:
    if wifi.radio.connected:
        print("  ✓ WiFi is connected")
        # Try to get signal strength if available
        try:
            rssi = wifi.radio.signal_strength
            print(f"  Signal strength: {rssi} dBm")
        except AttributeError:
            print("  (Signal strength not available on this firmware)")
    else:
        print("  ✗ WiFi is not connected")
except Exception as e:
    print(f"  ✗ Status check failed: {e}")

# Test 4: Simple HTTP request (optional - requires adafruit_requests)
print("\n[4/4] Testing HTTP request (optional)...")
try:
    import adafruit_requests
    socket = wifi.socket.socket()
    requests = adafruit_requests.Session(socket)

    response = requests.get("http://www.example.com", timeout=10)
    if response.status_code == 200:
        print(f"  ✓ HTTP request successful (Status: {response.status_code})")
    else:
        print(f"  ✗ HTTP request returned: {response.status_code}")
    response.close()

except ImportError:
    print("  ℹ️  adafruit_requests not installed")
    print("     (Optional - only needed for HTTP client functionality)")
    print("     To enable: Add adafruit-circuitpython-requests to lib folder")
except Exception as e:
    print(f"  ✗ HTTP request failed: {e}")

print("\n" + "=" * 60)
print("WIFI TEST COMPLETE")
print("=" * 60)

# Write your code here :-)
# SPDX-FileCopyrightText: 2020 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Connect to an "eval()" service over BLE UART.
import time
from ble_data_sender import BLEMonitor
from seeed_xiao_nrf52840 import Battery

# update interval in seconds
update_interval = 5

battery = Battery()

def get_measurements():
    bat_voltage = battery.voltage
    bat_percent = get_battery_percent(bat_voltage)

    return {"temperature":34.5, "moisture":7, "battery" : {"voltage":bat_voltage, "percent":bat_percent}}


ble = BLEMonitor()

# Simple example, not precise for non-linear discharge
def get_battery_percent(voltage):
    if voltage > 3.7:
        return 100
    elif voltage < 3.2:
        return 0
    else:
        # Linear interpolation between 3.2V (0%) and 3.7V (100%)
        return (voltage - 3.2) / (3.7 - 3.2) * 100
    
# need to change this to True ********
while True:
#    print("WAITING...")
    # Advertise when not connected.
    ble.connect()
#    print("CONNECTED")
    
    # Loop and send status update
    while ble.is_connected():
        time.sleep(update_interval)
        ble.send_monitoring_update(get_measurements())

# Write your code here :-)
# SPDX-FileCopyrightText: 2020 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Connect to an "eval()" service over BLE UART.
import time
from ble_data_sender import BLEMonitor
from sensors import Sensors

# update interval in seconds
update_interval = 5

sensors = Sensors()
ble = BLEMonitor()
    
# need to change this to True ********
while True:
#    print("WAITING...")
    # Advertise when not connected.
    ble.connect()
#    print("CONNECTED")
    
    # Loop and send status update
    while ble.is_connected():
        time.sleep(update_interval)
        ble.send_monitoring_update(sensors.get_measurements())

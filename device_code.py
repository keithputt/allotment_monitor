import time
from ble_data_sender import BLEMonitor
from sensors import Sensors

# update interval in seconds
update_interval = 5

sensors = Sensors()
ble = BLEMonitor()
    
# need to change this to True ********
while True:
    # Wait for a connection
    ble.connect()
    # Loop and send status update
    while ble.is_connected():
        time.sleep(update_interval)
        ble.send_monitoring_update(sensors.get_measurements())

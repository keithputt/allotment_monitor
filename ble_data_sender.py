# create a python class that sends monitoring data using the BLERadio
import json
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


class BLEMonitor:


    def __init__(self):
        # mapping of ble address to unique name
        device_map = {"<Address d6:95:f4:1e:2b:d8>":"Allotment_z1"}

        self.ble = BLERadio()
        adapter_address = str(self.ble._adapter.address)
        if adapter_address in device_map:
            self.name = device_map[adapter_address]
        else:
            self.name = "Unknown device"
        
        print("Started BLEMonitor: " + self.name)
        self.ble.name = self.name
        self.uart_service = UARTService() 
        self.advertisement = ProvideServicesAdvertisement(self.uart_service)
        self.connection = None

    # create a method that starts advertising, connects and then writes a status update message using UART
    def connect(self):
        self.ble.start_advertising(self.advertisement)
        while not self.ble.connected:
            pass
        self.connection = self.ble.connections[0]
        self.ble.stop_advertising()

    def is_connected(self):
        return self.ble.connected
    
    
    def get_ble_adapter_address(self):
        return 
    
    def get_device_name(self):
        return self.name

    # create a method that sends a status update message using UART
    def send_monitoring_update(self, measurements):
        update_dict = {"device" : self.get_device_name(), "measurements":measurements}
        update = json.dumps(update_dict)#'{"device":"' + self.get_device_name() + '", "measurements" : ' + measurements_json + '}\n'
        self.uart_service.write(update.encode())

    # create a method to disconnect
    def disconnect(self):
        if self.connection:
            self.connection.disconnect()
            self.connection = None
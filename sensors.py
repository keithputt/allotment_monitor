import adafruit_dht 
import board
from analogio import AnalogIn
from seeed_xiao_nrf52840 import Battery

class Sensors:
    def __init__(self):
        self.dht = adafruit_dht.DHT11(board.D4)
        self.moisture = AnalogIn(board.A0)
        self.battery = Battery()
        self.battery.charge_current = self.battery.CHARGE_100MA

    def get_measurements(self):
        try:
            self.dht.measure()
        except RuntimeError:
            print("DHT11 not connected")
            return {"message":"DHT11 not connected"}

        measurements = {"temperature":self.get_temperature(), 
                        "humidity"   :self.get_humidity(), 
                        "moisture"   :self.get_moisture(), 
                        "battery"    :self.get_battery_status()}
        return measurements

    def get_temperature(self):
        return self.dht.temperature
    
    def get_humidity(self):
        return self.dht.humidity

    def get_moisture(self):
        return self.moisture.value / 65536
    
    def get_battery_voltage(self):
        return self.battery.voltage
    
    def get_battery_charge_status(self):
        return self.battery.charge_status
    
    def get_battery_charge_current(self):
        return self.battery.charge_current

    # Simple example, not precise for non-linear discharge
    def get_battery_percent(self):
        voltage = self.battery.voltage
        if voltage > 4.2:
            return 100
        elif voltage < 3.2:
            return 0
        else:
            # Linear interpolation between 3.2V (0%) and 4.2V (100%)
            return (voltage - 3.2) / (4.2 - 3.2) * 100

    def get_battery_status(self):
        return {"charging":self.get_battery_charge_status(),
                "voltage":self.get_battery_voltage(), 
                "percent":self.get_battery_percent(),
                "charge_current":self.get_battery_charge_current()}

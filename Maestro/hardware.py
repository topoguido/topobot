import machine 
import dht

class sensor:
    
    def __init__(self):
        self.sensor_temp = dht.DHT11(machine.Pin(1, machine.Pin.IN))
    
    def update_values(self):
        self.sensor_temp.measure()
    
    def get_temp(self):
        return self.sensor_temp.temperature()
    
    def get_hum(self):
        return self.sensor_temp.humidity()
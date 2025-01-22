import machine 
import dht
from time import sleep

class sensor:
    
    def __init__(self):
        self.sensor_temp = dht.DHT11(machine.Pin(1, machine.Pin.IN))
    
    def update_values(self):
        self.sensor_temp.measure()
    
    def get_temp(self):
        return self.sensor_temp.temperature()
    
    def get_hum(self):
        return self.sensor_temp.humidity()
    
class rele:
    def __init__(self):
        self.rele = machine.Pin(2, machine.Pin.OUT)

    def shutdown(self):
        self.rele.value(1)
        sleep(0.5)
        self.rele.value(0)
        return True
        
    
    
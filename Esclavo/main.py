import network
import espnow
import dht
from machine import Pin
from utime import sleep

# Create the sensor object using I2C
sensor = dht.DHT11(machine.Pin(0, machine.Pin.IN))


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b"\x58\xcf\x79\xd7\x2e\x7c"  # MAC address of peer's wifi interface 58cf79d72e7c
e.add_peer(peer)  # Must add_peer() before send()

while True:
    print("enviando...")
    sensor.measure()
    sleep(1)
    temp = sensor.temperature()
    hum = sensor.humidity()
    e.send(peer, "Nuevo dato")
    print(f'Temp: {temp} - Hum: {hum}')
    e.send(peer, "Temperatura: %0.2f C" % temp)
    e.send(peer, "Humedad: %0.2f %%" % hum)
    print("enviado")
    sleep(5)

import network
import espnow
import ubinascii

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
wlan_mac = sta.config("mac")
print(f'MAC: {ubinascii.hexlify(wlan_mac).decode()}')
sta.disconnect()  # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.recv()
    if msg:  # msg == None if timeout in recv()
        print(msg)

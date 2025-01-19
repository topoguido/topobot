import espnow
import dht
import machine
from utime import sleep
from config import wlan_com

sensor = dht.DHT11(machine.Pin(2, machine.Pin.IN))

e = espnow.ESPNow()
e.active(True)
master = wlan_com.get('mac_master')
e.add_peer(master)  # MAC address of peer's wifi interface

while True:
    host, msg = e.recv()
    if msg:
        print('Recibiendo mensaje')
        if msg.decode('utf-8') == 'values':
            print('Solicitud de valores')
            sensor.measure()
            sleep(1)
            temp = sensor.temperature()
            hum = sensor.humidity()
            print(f'Enviando datos - Temp: {temp}° - Hum: {hum}%')
            resp = str(temp) + ',' + str(hum)
            e.send(master, resp)
            print(f'Datos enviado: {resp}')
        else:
            print(f'Mensaje no válido - {msg.decode('utf-8')}')

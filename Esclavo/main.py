import espnow
import dht
import machine
import gc
from utime import sleep
from config import wlan_com

sensor = dht.DHT11(machine.Pin(2, machine.Pin.IN))
rele = machine.Pin(0,machine.Pin.OUT)

e = espnow.ESPNow()
e.active(True)
#master = wlan_com.get('mac_master')
master = b'\xff\xff\xff\xff\xff\xff'

while True:
    host, msg = e.recv(timeout_ms=1000)
    if msg:
        print('Recibiendo mensaje')
        if msg.decode('utf-8') == 'values':
            print('Solicitud de valores')
            sensor.measure()
            #sleep(1)
            temp = sensor.temperature()
            hum = sensor.humidity()
            print(f'Enviando datos - Temp: {temp}° - Hum: {hum}%')
            resp = str(temp) + ',' + str(hum)
            e.send(master, resp)
            print(f'Datos enviado: {resp}')
        else:
            print(f'Mensaje no válido - {msg.decode('utf-8')}')
    print('Rele a cero')
    rele.value(0)
    sleep(2)
    print('Rele a uno')
    rele.value(1)
    sleep(2)
    gc.collect()
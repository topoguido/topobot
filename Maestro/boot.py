from config import wifi_config
from config import update_params
from machine import reset
import network
import ubinascii
import senko

wlan = network.WLAN(network.WLAN.IF_STA)
if not wlan.isconnected():
    wlan.active(True)
    wlan.config(channel=8, pm=wlan.PM_NONE)
    wlan.connect(wifi_config['ssid'], wifi_config['password'])
    wlan_mac = wlan.config("mac")
    print(f'Mi MAC es: {ubinascii.hexlify(wlan_mac).decode()}')
    print(f'Esperando red - Parametros: SSID: {wifi_config['ssid']} Pass: {wifi_config['password']}')
    while not wlan.isconnected():
        pass
    if wlan.isconnected():
        print(f'conectado a red con IP {wlan.ipconfig("addr4")}')

        OTA = senko.Senko(user = update_params.get('user'), 
                          repo = update_params.get('repo'),
                          branch = update_params.get('branch'), 
                          files = update_params.get('files'),
                          working_dir = 'Maestro'
                          )
        
        if OTA.update():
            print('Nueva version de soft')
            reset()
        else:
            print('Soft al dia')

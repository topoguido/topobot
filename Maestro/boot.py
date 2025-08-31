import json

try:
    with open("config.json", "r") as f:
        config = json.load(f)

except json.JSONDecodeError as e:
        print(f"Error: El archivo no tiene un formato JSON válido.")
        print("Detalles:", e)


from machine import reset
import network
import ubinascii
import senko

wlan = network.WLAN(network.WLAN.IF_STA)
if not wlan.isconnected():
    wlan.active(True)
    wlan.config(channel=8, pm=wlan.PM_NONE)
    wlan.connect(config['wifi_config']['ssid'], config['wifi_config']['password'])
    wlan_mac = wlan.config("mac")
    print(f'Mi MAC es: {ubinascii.hexlify(wlan_mac).decode()}')
    print(f'Esperando red - Parametros: SSID: {config['wifi_config']['ssid']} Pass: {config['wifi_config']['password']}')
    while not wlan.isconnected():
        pass
    if wlan.isconnected():
        print(f'conectado a red con IP {wlan.ipconfig("addr4")}')

        OTA = senko.Senko( config['update_params']['user'], 
                          config['update_params']['repo'],
                          config['update_params']['branch'], 
                          config['update_params']['files'],
                          config['update_params']['working_dir']
                          )
        
        if config['update_params']['status']:
            if OTA.update():
                print('Nueva version de soft')
                reset()
            else:
                print('Soft al dia')
        
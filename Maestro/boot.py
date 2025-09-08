from machine import reset
import network
import ubinascii
import senko
from Configurations import Configurations

configs = Configurations("boot")

wlan = network.WLAN(network.WLAN.IF_STA)
if not wlan.isconnected():
    wlan.active(True)
    wlan.config(channel=8, pm=wlan.PM_NONE)
    wlan.connect(configs.wifi_ssid, configs.wifi_password)
    wlan_mac = wlan.config("mac")
    print(f'Mi MAC es: {ubinascii.hexlify(wlan_mac).decode()}')
    print(f'Esperando red - Parametros: SSID: {configs.wifi_ssid} Pass: {configs.wifi_password}')
    while not wlan.isconnected():
        pass
    if wlan.isconnected():
        print(f'conectado a red con IP {wlan.ipconfig("addr4")}')

        OTA = senko.Senko(configs.update_user,
                          configs.update_repo,
                          configs.update_branch, 
                          configs.update_files,
                          configs.update_working_dir
                          )
        
        if configs.update_status:
            if OTA.update():
                print('Nueva version de soft')
                reset()
            else:
                print('Soft al dia')
        
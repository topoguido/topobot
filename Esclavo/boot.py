import network
import ubinascii

print('Iniciando')
sta = network.WLAN(network.STA_IF)
sta.active(True)
wlan_mac = sta.config("mac")
print(f'Mi MAC: {ubinascii.hexlify(wlan_mac).decode()} - {wlan_mac}')
#sta.disconnect()  
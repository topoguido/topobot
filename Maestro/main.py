import json

try:
    with open("config.json", "r") as f:
        config = json.load(f)

except json.JSONDecodeError as e:
        print(f"Error: El archivo no tiene un formato JSON válido.")
        print("Detalles:", e)

from machine import reset
import utelegram
import time
import gc
import hardware
import espnow
import os

print('Iniciando bot')
bot = utelegram.ubot(config['utelegram_config']['token'], bool(config['utelegram_config']['debug']))
bot.saluda(config['utelegram_config']['chat_id_default'])
rele = hardware.rele() # relé utilizado para hacer saltar al diferencial
sensor_st = hardware.sensor()  # sensor del estudio
dir_sensor_tx = bytes.fromhex(config['wlan_com']['mac_sensortx'])
e = espnow.ESPNow()
e.active(True)
e.add_peer(dir_sensor_tx)

while True:
    print('bot en escucha')
    if bot.read_once():

        # Analiza el comando recibido y responde
        if bot.command == '/ping':
            bot.reply_ping(bot.chat_id)

        elif bot.command == '/temp':
            # Obtiene los valores de temperatura y humedad del sensor cableado (estudio)
            sensor_st.update_values()
            bot.send(bot.chat_id, f'Estudio: Temp: {sensor_st.get_temp()}° - Humedad: {sensor_st.get_hum()}%')
            
            # Se solicitan al dispositivo ESP01 por wifi que devuelva los datos del sensor
            # ubicados en la planta transmisora.
            print("Solicitando datos al sensor del transmisor")
            e.send(dir_sensor_tx, "values")
            host, msg = e.recv(timeout_ms=3000)
            if msg:
                data = msg.decode('utf-8').split(',')
                print(f'Datos recibidos de sensor del transmisor {data}')
                temp = data[0]
                hum = data[1]
                fan = data[2]
                if fan == '1':
                    fan_status = 'Encendido'
                elif fan == '0':
                    fan_status = 'Apagado'
                else:
                    fan_status = 'sin datos'
                bot.send(bot.chat_id, f'Transmisor: Temp: {temp}° - Humedad: {hum}% - Ventilador: {fan_status}')
            else:
                print('No hay comunicacion con sensor de transmisor')
                print(e.stats())
                bot.send(bot.chat_id, "No puedo obtener los datos del transmisor")
    
        elif bot.command == '/apagar':
            # se activa relé que pone a tierra el vivo de la red de 220V.
            print('Ejecutando apagado de emergencia')
            bot.send(bot.chat_id, "Ok, vamos a cortar la energía")
            if rele.shutdown():
                bot.send(bot.chat_id, "Se ha cortado la energía")
            else:
                bot.send(bot.chat_id, "Parece que no lo he logrado")

        elif bot.command == '/saluda':
            print('Saludando a pedido')
            bot.send(bot.chat_id, f'Hola {bot.chat_name}, saludos!')

        elif bot.command == '/reset':
            print('Reinicio de dispositivo')
            delay = config['disp_conf']['reset_delay']
            bot.send(bot.chat_id, f'Ok, voy a reiniciarme en {delay} segundos.')
            time.sleep(delay)
            reset()

    time.sleep(3)
    gc.collect()

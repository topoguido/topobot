wifi_config = {
    'ssid':'manzanita',
    'password':'benito123'
}

utelegram_config = {
    'token': '6155203747:AAHXbcoaD_Axnoor4fBVeJQW1fVG4BXjOmk',
    'chat_id_default': '',
    'debug': True
}

wlan_com = {
    'mac_sensortx': bytes.fromhex('8ece4ee97325')
}

disp_conf = {
    'reset_delay': int(5)
}

update_params = {
    'user' : 'topoguido', 
    'repo' : 'bot-radio',
    'branch' : 'dev',
    'files' :  ['boot.py','main.py','hardware.py','utelegram.py'] 
}

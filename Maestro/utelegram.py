import time
import gc
import urequests

class ubot:
    
    def __init__(self, token, offset, debug):
        self.url = 'https://api.telegram.org/bot' + token
        
        self.commands = self.getCommands()
        
#         self.default_handler = self.get_message
        self.default_handler = None
        self.message_offset = offset
        self.sleep_btw_updates  = offset if offset > 0 else 3
        self.command = None
        self.commandOK = False
        self.chat_id = ''
        self.debug = debug
        print(f'Lista de comandos: {self.commands}')
       
        messages = self.read_messages()
        if messages:
            if self.message_offset==0:
                self.message_offset = messages[-1]['update_id']
            else:
                for message in messages:
                    if message['update_id'] >= self.message_offset:
                        self.message_offset = message['update_id']
                        break


    def getCommands(self):
        commands = {}
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            print(f'URL: {self.url}')
            response = urequests.get(self.url + '/getMyCommands', headers=headers, timeout=20)
            if response.status_code == 200:
                response_json = response.json()
                if 'result' in response_json:
                    for item in response_json['result']:
                        command = '/' + item['command']
                        desc = item['description']
                        commands[command] = desc
                    return commands    
            else:
                print(f"Error HTTP: {response.status_code}")
                return None    
        except (ValueError):
            return None
        except (OSError):
            print("OSError: request timed out")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
        finally:
            response.close()
    
    def get_message(self, message):
        self.send(message['message']['chat']['id'], 'Procesando tu solicitud...')

    def reply_ping(self, chat_id):
        if self.debug: print('Respondiendo al ping')
        self.send(chat_id, 'pong')
    
    def saluda(self, chat_id):
        if self.debug: print('Saludando')
        self.send(int(chat_id), 'Hola, el bot se ha iniciado')
    
      
    def send(self, chat_id, text):
        data = {'chat_id': chat_id, 'text': text}
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = urequests.post(self.url + '/sendMessage', json=data, headers=headers)
            response.close()
            return True
        except:
            return False

    def read_messages(self):
        result = []
        self.query_updates = {
            'offset': self.message_offset + 1,
            'limit': 1,
            'timeout': 30,
            'allowed_updates': ['message']}
        try:
            update_messages = urequests.post(self.url + '/getUpdates', json=self.query_updates).json() 
            if 'result' in update_messages:
                if self.debug: print(f'Metodo read_messages: {update_messages}')
                for item in update_messages['result']:
                    result.append(item)
            return result
        except (ValueError):
            return None
        except (OSError):
            if self.debug: print("OSError: request timed out")
            return None

    # def listen(self):
    #     while True:
    #         return self.read_once()
                
    #         time.sleep(self.sleep_btw_updates)
    #         gc.collect()

    def read_once(self):
        messages = self.read_messages()
        if messages:
            if self.debug: print('Mensajes entrantes')
            if self.message_offset==0:
                self.message_offset = messages[-1]['update_id']
                return self.message_handler(messages[-1])
            else:
                for message in messages:
                    if message['update_id'] >= self.message_offset:
                        self.message_offset = message['update_id']
                        return self.message_handler(message)
                        #break

    # def set_default_handler(self, handler):
    #     self.default_handler = handler

    def set_sleep_btw_updates(self, sleep_time):
        self.sleep_btw_updates = sleep_time

    def message_handler(self, message):
        if 'text' in message['message']:
            parts = message['message']['text'].split(' ')
            if 'entities' in message['message']:
                for entity in message['message']['entities']:
                    if 'type' in entity and entity['type'] == 'bot_command':
                        if self.debug: print('Es comando')
                        if parts[0] in self.commands:
                            if parts[0] == '/ping':
                                self.reply_ping(message)
                            else:
                                if self.debug: print(f'Comando recibido: {parts[0]}')
                                self.command = parts[0]
                                self.commandOK = True
                                self.chat_id = message['message']['chat']['id']
                                return True
                                # if parts[0] == '/saluda':
                                #     self.saluda(message['message']['chat']['id'])
                                # elif parts[0] == '/ping':
                                #     self.reply_ping(message)
                                # elif parts[0] == '/temp':
                                #     self.return_temp(message['message']['chat']['id'])
                        else:
                            self.commandOK = False
                            self.send(message['message']['chat']['id'], 'No reconozco ese comando \U0001F611')
                            return False
                            # if self.default_handler:
                            #     self.default_handler(message)
            else:
                print(f'Es un mensaje normal con el texto: {parts}')
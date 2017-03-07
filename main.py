import cyclos_api
import telepot
import asyncio
from telepot.aio.delegate import (pave_event_space, per_chat_id,
                                  create_open)
import psycopg2
import psycopg2.extras
import config as c


class BotHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(BotHandler, self).__init__(*args, **kwargs)
        self.registered = False
        self.db_ready = False
        self.wait_username = False
        self.wait_password = False
    async def initialize_db(self):
        print('initalize_db')

        conn_string = ("host='" + c.DB_HOST
                       + "' dbname='" + c.DB_NAME
                       + "' user='" + c.DB_USER
                       + "' password='" + c.DB_PASSWORD + "'")

        print(conn_string)

        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        self.cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.db_ready = True
        print("db db_ready")

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if not self.db_ready:
            print('iniciamos db')
            await self.initialize_db()
            print('db iniciada')
        # This is only a temporary code
        print("getn message")
        if chat_id == c.CHAT_ID:

            await self.sender.sendMessage('hola ' + str(chat_id))

            self.cursor.execute('SELECT * FROM users WHERE chat_id = %s',
                                (chat_id,))
            row = self.cursor.fetchone()
            if (row is not None and
                row['username'] != None and
                    row['password'] != None):

                print(row['username'])
                await self.sender.sendMessage('Estás registrado')

            elif row is None:
                await self.sender.sendMessage('No estás registrado, vamos a'
                                              + ' solucionarlo, primero,'
                                              + ' dime tu usuario')
                # insert chatid in the database
                self.cursor.execute('INSERT INTO users (chat_id) VALUES (%s)',
                                    (chat_id,))
                self.wait_username = True

            elif (row['username'] == None and
                  self.wait_username is False):

                await self.sender.sendMessage('Necesito que me digas tu '
                                              + 'usuario para poder continuar')
                self.wait_username = True

            elif (row['username'] == None and
                  self.wait_username is True):
                # insert username in the database
                self.cursor.execute('UPDATE users SET username = %s WHERE chat_id = %s',
                                    (msg['text'], chat_id))
                await self.sender.sendMessage('Muy bien, ahora'
                                              + ' dime tu contraseña')
                self.wait_username = False
                self.wait_password = True

            elif (row['password'] == None and
                  self.wait_password is False):

                await self.sender.sendMessage('Hasta que no me digas tu'
                                              + ' contraseña no puedo'
                                              + ' ayudarte')
                self.wait_password = True

            elif (row['password'] == None and
                  self.wait_password is True):
                # insert password
                # check if works

                # if works
                await self.sender.sendMessage('Enhorabuenaa, ya puedes acceder'
                                              + ' a cyclos a través de mi')
                await self.send_help()

                # if dont works
                await self.sender.sendMessage('Vaya, parece que ha habido'
                                              + ' algún error')
                await self.sender.sendMessage('El usuario y contraseña que me'
                                              + ' has dado no funciona,'
                                              + ' ¿probamos otra vez?')

                # reset

        else:

            await self.sender.sendMessage('No estás autorizado, el bot está'
                                          + ' en desarrollo')

    async def checkRegister(self, msg):
        pass

    async def register(self):
        pass

    async def send_help():
        pass

    async def account_balance(name, password, self):
        data = cyclos_api.get_account_balance(name,
                                              password)

        await self.sender.sendMessage('Saldo: ' + data['balance'] +
                                      '\nCrédito disponible: ' +
                                      data['availableBalance'])

        print('saldo: ' + data['balance'])
        print('\n Crédito disponible: ' + data['availableBalance'])


if __name__ == "__main__":

    bot = telepot.aio.DelegatorBot(c.TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, BotHandler, timeout=100),
        ])

    loop = asyncio.get_event_loop()
    loop.create_task(bot.message_loop())
    print('Listening')

    loop.run_forever()

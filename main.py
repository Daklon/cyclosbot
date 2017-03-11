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
        self.username = None
        self.password = None

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
        # if chat_id == c.CHAT_ID:

        # await self.sender.sendMessage('hola ' + str(chat_id))

        self.cursor.execute('SELECT * FROM users WHERE chat_id = %s',
                            (chat_id,))
        row = self.cursor.fetchone()
        if (row is not None and
            row['username'] is not None and
                row['password'] is not None):

            self.username = row['username']
            self.password = row['password']

            await self.process(msg)

        elif row is None:
            await self.sender.sendMessage('No estás registrado, vamos a'
                                          + ' solucionarlo, primero,'
                                          + ' dime tu usuario')
            # insert chatid in the database
            self.cursor.execute('INSERT INTO users (chat_id) VALUES (%s)',
                                (chat_id,))
            self.wait_username = True

        elif (row['username'] is None and
              self.wait_username is False):

            await self.sender.sendMessage('Necesito que me digas tu '
                                          + 'usuario para poder continuar')
            self.wait_username = True

        elif (row['username'] is None and
              self.wait_username is True):
            # insert username in the database
            self.cursor.execute('UPDATE users SET username = %s WHERE chat_id = %s',
                                (msg['text'], chat_id))
            self.username = msg['text']
            await self.sender.sendMessage('Muy bien, ahora'
                                          + ' dime tu contraseña')
            self.wait_username = False
            self.wait_password = True

        elif (row['password'] is None and
              self.wait_password is False):

            await self.sender.sendMessage('Hasta que no me digas tu'
                                          + ' contraseña no puedo'
                                          + ' ayudarte')
            self.wait_password = True

        elif (row['password'] is None and
              self.wait_password is True):
            # insert password
            self.cursor.execute('UPDATE users SET password = %s WHERE chat_id = %s',
                                (msg['text'], chat_id))
            self.password = msg['text']
            # check if works
            if (await self.checkRegister()):
                # if works
                await self.sender.sendMessage('Enhorabuenaa, ya puedes acceder'
                                              + ' a cyclos a través de mi')
                await self.send_help()
            else:
                # if dont works
                await self.sender.sendMessage('Vaya, parece que ha habido'
                                              + ' algún error')
                await self.sender.sendMessage('El usuario y contraseña que me'
                                              + ' has dado no funciona,'
                                              + ' ¿probamos otra vez?')
                self.cursor.execute('DELETE FROM users WHERE chat_id = %s',
                                    (chat_id,))
                # reset

        # else:

        #    await self.sender.sendMessage('No estás autorizado, el bot está'
        #                                  + ' en desarrollo')

    async def checkRegister(self):
        return cyclos_api.auth(self.username, self.password)

    async def register(self):
        pass

    async def send_help(self):
        await self.sender.sendMessage('De momento solo hay un comando')
        await self.sender.sendMessage('saldo')
        await self.sender.sendMessage('Devuelve el saldo disponible')

    async def process(self, msg):
        text = msg['text']
        if 'saldo' in text.lower():
            await self.account_balance()

        else:
            await self.send_help()

    async def account_balance(self):
        data = cyclos_api.get_account_balance(self.username,
                                              self.password)

        await self.sender.sendMessage('Saldo: ' + data['balance'] +
                                      '\nCrédito disponible: ' +
                                      data['availableBalance'])


if __name__ == "__main__":

    bot = telepot.aio.DelegatorBot(c.TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, BotHandler, timeout=100),
        ])

    loop = asyncio.get_event_loop()
    loop.create_task(bot.message_loop())
    print('Listening')

    loop.run_forever()

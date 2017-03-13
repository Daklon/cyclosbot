import cyclos_api
import telepot
import asyncio
from telepot.aio.delegate import (pave_event_space, per_chat_id,
                                  create_open)
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import psycopg2
import psycopg2.extras
import config as c

import logging


class BotHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(BotHandler, self).__init__(*args, **kwargs)
        self.registered = False
        self.db_ready = False
        self.wait_username = False
        self.wait_password = False
        self.wait_category_select = False
        self.username = None
        self.password = None
        self.categories = [[]]

    async def initialize_db(self):
        logging.info('Initializing database')

        conn_string = ("host='" + c.DB_HOST
                       + "' dbname='" + c.DB_NAME
                       + "' user='" + c.DB_USER
                       + "' password='" + c.DB_PASSWORD + "'")

        logging.debug(conn_string)

        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        self.cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.db_ready = True
        logging.info("Database ready")

    # This method is called each time a new message arrives
    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if not self.db_ready:
            logging.info('Database not started')
            await self.initialize_db()
        logging.info('Received message from: %s', chat_id)
        logging.debug(msg['text'])

        self.cursor.execute('SELECT * FROM users WHERE chat_id = %s',
                            (chat_id,))
        logging.debug("Sql select")

        row = self.cursor.fetchone()
        if (row is not None and
            row['username'] is not None and
                row['password'] is not None):

            self.username = row['username']
            self.password = row['password']
            logging.debug('Processing new message: %s', chat_id)
            await self.process(msg, chat_id)

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
                await self.sender.sendMessage('Enhorabuena, ya puedes acceder'
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

    # Return true if success or false if fail
    async def checkRegister(self):
        return cyclos_api.auth(self.username, self.password)

    # Register new user in the bot db
    async def register(self):
        pass

    # Send help to the user, a list of commands
    async def send_help(self):
        await self.sender.sendMessage('De momento solo hay un comando')
        await self.sender.sendMessage('saldo: Devuelve el saldo disponible')

    # Process the answer from the user to decide what to do
    async def process(self, msg, chat_id):
        text = msg['text']
        if 'saldo' in text.lower():
            logging.debug('Received saldo command from: %s', chat_id)
            await self.account_balance(chat_id)

        elif 'anuncio' in text.lower():
            if 'nuevo' in text.lower():
                await self.new_advert()

        elif [text] in self.categories:
            await self.sender.sendMessage('ahora imprimo las subcategorías, si las hay')
        else:
            logging.debug('Sending help to: %s', chat_id)
            await self.send_help()

    # Start asking info to the user to create new advertise
    async def new_advert(self):
        data = cyclos_api.get_marketplace_info(self.username,
                                               self.password)
        # for each parent category, create new list, and append to
        # the main list, then create a keyboard using this list and
        # send it
        for parent in data['categories']:
            temps = []
            temps.append(parent['name'])
            self.categories.append(temps)

        markup = ReplyKeyboardMarkup(keyboard=self.categories, one_time_keyboard=True)
        await self.sender.sendMessage('Selecciona en que categoría'
                                      + ' deseas que aparezca el anuncio',
                                      reply_markup=markup)

    # Return the user's account balance
    async def account_balance(self, chat_id):
        logging.debug("Waiting the api answer")
        data = cyclos_api.get_account_balance(self.username,
                                              self.password)
        logging.debug("Received api answer")
        logging.info("Sending answer to: %s", chat_id)

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
    logging.basicConfig(filename=c.LOG_DIR, format='%(asctime)s - %(levelname)s:%(message)s', level=c.DEBUG_LEVEL)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # unifinished
        pass


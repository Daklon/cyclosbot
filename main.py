import cyclos_api
import telepot
import asyncio
from telepot.aio.delegate import (pave_event_space, per_chat_id,
                                  create_open)
from aiopg.sa import create_engine
import sqlalchemy as sa

import config


async def account_balance(name, password, self):
    data = cyclos_api.get_account_balance(name,
                                          password)

    await self.sender.sendMessage('Saldo: ' + data['balance'] +
                                  '\nCrédito disponible: ' +
                                  data['availableBalance'])

    print('saldo: ' + data['balance'])
    print('\n Crédito disponible: ' + data['availableBalance'])


class BotHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(BotHandler, self).__init__(*args, **kwargs)
        engine = None
        print('iniciamos db')
        self.intialize_db()
        print('db iniciada')

    async def intialize_db(args):
        global engine
        print('metadata')
        metadata = sa.MetaData()

        # set the user table config
        self.users = sa.Table('users', metadata,
                              sa.Column('chat_id', sa.Integer,
                                        primary_key=True),
                              sa.Column('username', sa.String),
                              sa.Column('password', sa.String),
                              sa.Column('token', sa.String),
                              )

        # create the engine object used to connect to the db
        async with create_engine('postgresql://' +
                                 config.DB_USER + ':' +
                                 config.DB_PASSWORD + '@' +
                                 config.DB_HOST + ':' +
                                 config.DB_PORT + '/' +
                                 config.DB_NAME
                                 ) as engine:
            return engine
        
    async def on_chat_message(self, msg,):
        global engine
        content_type, chat_type, chat_id = telepot.glance(msg)
        # This is only a temporary code
        print(chat_id)
        print(config.CHAT_ID)
        if chat_id == config.CHAT_ID:

            await self.sender.sendMessage('hola ' + str(chat_id))

            async with engine.acquire() as conn:
                s = self.users.select([self.users.c.username,
                                       self.users.c.password],
                                      self.users.c.chat_id == chat_id)
                print(str(s))
                row = conn.execute(s).fetchone()
                if row is not None and row['username'] != "" and row['password'] != "":
                    self.sender.sendMessage('Estás registrado')

                elif row['username'] == "" and self.wait_username == False:
                    self.sender.sendMessage('Necesito que me digas tu usuario para poder continuar')
                    self.wait_username = True

                elif row['username'] == "" and self.wait_username == True:
                    # insert username in the database
                    self.sender.sendMessage('Muy bien, ahora dime tu contraseña')
                    self.wait_username = False
                    self.wait_password = True

                elif row['password'] == "" and self.wait_password == False:
                    self.sender.sendMessage('Necesitas estar registrado para usar el bot, por favor dime tu contraseña')
                    self.wait_password = True

                elif row['password'] == "" and self.wait_password == True:
                    # insert password
                    # check if works

                    # if works
                        self.sender.sendMessage('Enhorabuena, ya estás registrado y puedes acceder a cyclos a través de mi')

                    # if dont works
                        self.sender.sendMessage('Vaya, parece que ha habido algún error')
                        self.sender.sendMessage('El usuario y contraseña que me has dado no funciona, ¿probamos otra vez?')

                    # reset

                else:
                    self.sender.sendMessage('No estás registrado, vamos a solucionarlo, primero, dime tu usuario')
                    # insert chatid in the database
                    self.wait_username = True

        else:

            await self.sender.sendMessage('No estás autorizado, el bot está en desarrollo')


if __name__ == "__main__":

    bot = telepot.aio.DelegatorBot(config.TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, BotHandler, timeout=100),
        ])

    loop = asyncio.get_event_loop()
    loop.create_task(bot.message_loop())
    print('Listening')

    loop.run_forever()

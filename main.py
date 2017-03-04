import cyclos_api
import telepot
import asyncio
from telepot.aio.delegate import (pave_event_space, per_chat_id,
                                  create_open)
from aiopg.sa import create_engine
import sqlachemy as sa

import config


class BotHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(BotHandler, self).__init__(*args, **kwargs)

        # set the user table config
        users = sa.Table('users', metadata,
                Column('chat_id', Integer, primary_key=True).
                Column('username', String),
                Column('password', String),
                Column('token', String),
                )

        # create the engine object used to connect to the db
        async with create_engine('postgresql://' +
                                 DB_USER + ':' +
                                 DB_PASSWORD + '@' +
                                 DB_HOST + ':' +
                                 DB_PORT + '/' +
                                 DB_NAME
                                 ) as engine

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # This is only a temporary code
        if chat_id = config.CHAT_ID {

            await self.sender.sendMessage('hola ' + str(chat_id))

            async with engine.acquire() as conn:
                s = users.select([users.c.username,users.c.password],users.c.chat_id==chat_id)
                row = s.execute().fetchone()
                if row is not None and row['username'] != "" and row['password'] != "":
                    self.sender.sendMessage('Estás registrado')
                
                else if row['username'] == "" and self.wait_username == False:
                    self.sender.sendMessage('Necesito que me digas tu usuario para poder continuar')
                    self.wait_username = True
                
                else if row['username'] == "" and self.wait_username == True:
                    # insert username in the database
                    self.sender.sendMessage('Muy bien, ahora dime tu contraseña')
                    self.wait_username = False
                    self.wait_password = True

                else if row['password'] == "" and self.wait_password == False:
                    self.sender.sendMessage('Necesitas estar registrado para usar el bot, por favor dime tu contraseña')
                    self.wait_password = True

                else if row['password'] == "" and self.wait_password == True:
                    #insert password
                    #check if works

                    #if works
                        self.sender.sendMessage('Enhorabuena, ya estás registrado y puedes acceder a cyclos a través de mi'

                    #if dont works
                        self.sender.sendMessage('Vaya, parece que ha habido algún error')
                        self.sender.sendMessage('El usuario y contraseña que me has dado no funciona, ¿probamos otra vez?')
                    
                    #reset

                else:
                    self.sender.sendMessage('No estás registrado, vamos a solucionarlo, primero, dime tu usuario')
                    #insert chatid in the database
                    self.wait_username = True

            await data = cyclos_api.get_account_balance(config.NAME,
                                                  config.PASSWORD)

            await self.sender.sendMessage('Saldo: ' + data['balance'] +
                                          '\nCrédito disponible: ' +
                                          data['availableBalance'])

            print('saldo: ' + data['balance'])
            print('\n Crédito disponible: ' + data['availableBalance'])

        } else {

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

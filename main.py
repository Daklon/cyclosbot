import cyclos_api
import telepot
import asyncio
from telepot.aio.delegate import (pave_event_space, per_chat_id,
                                  create_open)

import config


class BotHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(BotHandler, self).__init__(*args, **kwargs)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # This is only a temporary code
        if chatd_id = config.CHAT_ID {

            await self.sender.sendMessage('hola ' + str(chat_id))

            data = cyclos_api.get_account_balance(config.NAME,
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

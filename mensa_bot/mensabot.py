from telegram.ext import (Updater, CallbackQueryHandler, MessageHandler, CommandHandler, StringCommandHandler, Filters,
                          PicklePersistence)

from mensa_bot.skills.menu import MensaMenuHandler


class MensaBot:
    def __init__(self, token: str, persistence_filename: str):
        self.__pickle_persistence = PicklePersistence(filename=persistence_filename)
        self.__updater = Updater(token, persistence=self.__pickle_persistence, use_context=True)
        mmh = MensaMenuHandler("/menu")
        self.__updater.dispatcher.add_handler(
            mmh, 1
        )
        self.__updater.dispatcher.add_handler(
            CallbackQueryHandler(mmh.callback), 1
        )
        pass

    def run(self):
        self.__updater.start_polling()
        self.__updater.idle()

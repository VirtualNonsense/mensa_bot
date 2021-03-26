from telegram.ext import (Updater, MessageHandler, CommandHandler, StringCommandHandler, Filters,
                          PicklePersistence)


class MensaBot:
    def __init__(self, token: str, persistence_filename: str):
        self.__pickle_persistence = PicklePersistence(filename=persistence_filename)
        self.__updater = Updater(token, persistence=self.__pickle_persistence, use_context=True)

        pass

    def run(self):
        self.__updater.start_polling()
        self.__updater.idle()

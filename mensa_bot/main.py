import mensa_bot.mensabot as mensabot
from secret_stuff import token
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    bot = mensabot.MensaBot(token=token["bot"], persistence_filename="bot.pkl")
    bot.run()

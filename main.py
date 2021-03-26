import mensabot
from secret_stuff import token

if __name__ == '__main__':
    bot = mensabot.MensaBot(token=token["test"], persistence_filename="bot.pkl")

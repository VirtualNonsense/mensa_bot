from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler, CallbackContext)

from telegram.update import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

import datetime as dt

from mensa_bot.services.MensaWebSite import MensaWebSite


class MensaMenuHandler(ConversationHandler, CallbackQueryHandler):
    weekDays = dict(Monday="Montag",
                    Tuesday="Dienstag",
                    Wednesday="Mittwoch",
                    Thursday="Donnerstag",
                    Friday="Freitag",
                    Saturday="Samstag",
                    Sunday="Sonntag")

    def __init__(self, command):
        self.command = command
        self.callback = self.__button_callback
        self.site = MensaWebSite()

        super(MensaMenuHandler, self).__init__(

            entry_points=[MessageHandler(Filters.regex(f"^{command}"), self.__command_parser)],
            states={
            },
            fallbacks=[]
        )

    def __command_parser(self, update: Update, context):
        keyboard = []
        for l in self.site.get_locations():
            keyboard.append([InlineKeyboardButton(l.name, callback_data="{},{},{}".format(self.command, l.name, l.link))])
        update.message.reply_text("Für welche Mensa?", reply_markup=InlineKeyboardMarkup(keyboard), quote=True)

    def __button_callback(self, update: Update, context: CallbackContext):
        query = update.callback_query
        cmd, lname, llink = query.data.split(",")
        if cmd == self.command:
            foodlist = self.site.get_menu(llink)
            stri = "Mahlzeit {}\n".format(update.effective_user.first_name)
            if len(foodlist.food) < 1:
                stri += "Leider ist aktuell kein Speiseplan verfügbar"
            else:
                if foodlist.date is None:
                    stri += "Irgendwann gibt es am Standort \"{}\":\n".format(lname)
                elif foodlist.date is None or foodlist.date.date() == dt.datetime.now().date():
                    stri += "Heute gibt es am Standort \"{}\":\n".format(lname)
                else:
                    stri += "Am {} gibt es am Standort \"{}\":\n".format(self.weekDays.get(foodlist.date.strftime("%A")),
                                                                         lname)
                for f in foodlist.food:
                    stri += "{}\n\t{} {}:\n\tStud.: {:.2f}€ Bed.: {:.2f}€ Gäste:{:.2f}€".format(f.caption, f.name,
                                                                                                f.foodIcon,
                                                                                                f.priceStudent,
                                                                                                f.priceStaff,
                                                                                                f.priceVisitor) + "\n\n"
            query.edit_message_text(text="{}".format(stri))

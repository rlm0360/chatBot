#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

""""============= LIBRARIES =========================================================================================="""

"""Local Libraries"""

from weather import *
from asset_info import *


""""================= LOGGING =========================================================================================="""

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

""""============= TELGRAM BOT FUNCTIONS ==============================================================================="""

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(fr'Hi {user.mention_markdown_v2()}\, How can I be of assistance?')


def unknown(update: Update, context: CallbackContext) -> None:
    """Send a message when telegram bot doesn't understand the command or message"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand.")


def program_reinitialized(update: Update, context: CallbackContext):
    """Message Sent to Telegram each time the python program is reinitialized"""
    context.bot.send_message(chat_id=chat_id_num,text="Bot reinitialized...")

def add_ticker(update: Update, context: CallbackContext):

    context.bot.send_message(chat_id=chat_id_num, text="Ticker Added")


def main() -> None:

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
   # dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.command & Filters.text, unknown))
    ##updates Stock Prices
    dispatcher.add_handler(StringCommandHandler("reinit", program_reinitialized))
    dispatcher.add_handler(StringCommandHandler("buy_sell", Buy_Sell_Notification))
    dispatcher.add_handler(StringCommandHandler("weather", Weather_Notification))
    dispatcher.add_handler(MessageHandler(Filters.text(ticker_list), Get_Price))


    # Start the Bot5
    updater.start_polling()
    print("Bot Reinitialized...")


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    return


if __name__ == '__main__':

    main()

    select_function(updater,"reinit")

    #update notification text to send to the chat
    price_change()
    #update the weather update text to send to the chat
    Weather_Update()








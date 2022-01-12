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

import logging # Logging Library
import yfinance as yf #Fetch Data from Yahoo Finance

"""Library for Telegram Bot"""
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, StringCommandHandler, Filters, CallbackContext, Handler

""""============= LOGGING =========================================================================================="""

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

""""============= TELGRAM BOT FUNCTIONS ==============================================================================="""

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")





def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    context.bot.send_message(chat_id=5064819774,text="IT WORKS")


def Get_Price(update: Update, context: CallbackContext) -> None:
    ticker_convert={"VGX":"VGX-USD",
                    "BMY":"BMY"}

    asset = yf.Ticker(ticker_convert[update.message.text])

    asset_data = asset.info

    current_Price = round(asset_data['regularMarketPrice'], 2)
    market_Cap = round((int(asset_data['marketCap']) / 1000000), 2)

    print(current_Price)

    messages = "{} Price is now ${} with a market cap of ${} Million".format(update.message.text,current_Price, market_Cap)

    """Echo the user message."""
    update.message.reply_text(messages)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5098430589:AAHJkws6DDyv-GNoeHxSpv_svEu_a3cplz0")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    update_queue = updater.update_queue


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    ##updates Stock Prices
    dispatcher.add_handler(StringCommandHandler("stock_update", help_command))


    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    ticker_list = ["VGX", "BMY"]
    dispatcher.add_handler(MessageHandler(Filters.text(ticker_list), Get_Price))

    # Start the Bot
    updater.start_polling()
    print("test3")


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #updater.idle()

    return updater



def select_function(updater,func):
    update_queue = updater.update_queue
    update_queue.put_nowait("/{}".format(func))

if __name__ == '__main__':
    print("test1")
    updater = main()

    select_function(updater,"stock_update")




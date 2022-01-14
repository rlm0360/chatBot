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
import threading

"""Local Libraries"""
from asset_info import *

""""============= GLOBAL VARIABLES ====================================================================================="""
chat_id_num = 5064819774
ticker_dict = {"VGX": "VGX-USD",
               "BTC": "BTC-USD",
               "BMY": "BMY"}
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
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\, How can I be of assistance?'
    )

def unknown(update: Update, context: CallbackContext) -> None:
    """Send a message when telegram bot doesn't understand the command or message"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand.")



def program_reinitialized(update: Update, context: CallbackContext):
    """Message Sent to Telegram each time the python program is reinitialized"""
    context.bot.send_message(chat_id=chat_id_num,text="Bot reinitialized...")



def Get_Price(update: Update, context: CallbackContext) -> None:
    """Respond with data about a certain Ticker symbol. Supported tickers saved in List"""


    update.message.reply_text("Let me check...")

    asset = yf.Ticker(ticker_dict[update.message.text]) #fetch ticker price from Yahoo Finance

    asset_data = asset.info #Save the information about the ticker in a Dict

    current_Price = round(asset_data['regularMarketPrice'], 2)
    market_Cap = round((int(asset_data['marketCap']) / 1000000), 2)

    messages = "{} Price is now ${} with a market cap of ${} Million".format(update.message.text,current_Price, market_Cap)

    """Echo the user message."""
    update.message.reply_text(messages)

def Buy_Sell_Notification(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=chat_id_num,text=notification_text)


def main() -> None:


    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5098430589:AAHJkws6DDyv-GNoeHxSpv_svEu_a3cplz0")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    update_queue = updater.update_queue


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
   # dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.command & Filters.text, unknown))

    ##updates Stock Prices
    dispatcher.add_handler(StringCommandHandler("reinit", program_reinitialized))

    dispatcher.add_handler(StringCommandHandler("buy_sell", Buy_Sell_Notification))


    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    ticker_list = list(ticker_dict.keys())
    print(ticker_list)
    dispatcher.add_handler(MessageHandler(Filters.text(ticker_list), Get_Price))

    # Start the Bot5
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

def test():
    threading.Timer(30.0, test).start()
    print("SUCCESS")

if __name__ == '__main__':
    print("test1")
    updater = main()

    select_function(updater,"reinit")
    result = price_change()

    if result[0] < result[2]:
        notification_text = "Your asset {} has decreased to ${}. Your buy price is currently calculated at ${}".format(result[3],result[0], result[2])
        select_function(updater,"buy_sell")
    elif result[0] > result[1]:
        notification_text = "Your asset {} has increased to ${}. Your sell price is currently calculated at ${}".format(result[3], result[0], result[1])
        select_function(updater,"buy_sell")






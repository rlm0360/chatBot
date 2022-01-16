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
import pandas as pd

"""Library for Telegram Bot"""
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, StringCommandHandler, Filters, CallbackContext, Handler
import threading
import datetime
import time

#from alarm import alarm_start

"""Local Libraries"""

""""============= GLOBAL VARIABLES ====================================================================================="""
chat_id_num = 5064819774
ticker_dict = {"VGX": "VGX-USD",
               "BTC": "BTC-USD",
               "BMY": "BMY"}
alarm_list = [] #List of alarms that will each run in their own thread
new_alarm = False
global notification_text
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

def alarm_manager(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=chat_id_num, text="Alarm has been set")
    extracted_time = update.message["text"].split(" ")[1]

    alarm_list.append(extracted_time)
    context.bot.send_message(chat_id=chat_id_num, text="current alarms are: {}".format(alarm_list))

    new_alarm = True

def alarm_added():
    extracted_time = alarm_list[0]
    hour = int(extracted_time.split(":")[0])
    minute = int(extracted_time.split(":")[1])

    print(hour, minute)
    th = threading.Thread(target=alarm_start, args=[hour, minute])
    th.start()
    th.join




def alarm_start(hour,minute):

    print("Alarm Set!")
    wait = True
    while wait == True:
        t = datetime.datetime.now()
        if t.hour == hour and t.minute == minute:
            print("Time to get up")
            wait = False

def price_change():

    threading.Timer(300.0, price_change).start()
    ticker_list = "VGX-USD"

    period = "1h"
    interval = "1mo"

    asset = yf.Ticker(ticker_list)  # fetch ticker price from Yahoo Finance


    asset_history = asset.history(period=period,interval=interval)  # Save the information about the ticker in a Dict
    asset_price = round(asset.info["regularMarketPrice"],2)

    history_df = pd.DataFrame.from_dict(asset_history)

    history_df["avg_price"] = (history_df["Low"] + history_df["High"]) / 2


    moving_avg = round(history_df["avg_price"].mean(),2)


    target_buy_price = round(moving_avg*.9,2)
    target_sell_price = round(moving_avg*1.1,2)

    print("The Target Sell Price is: ${}".format(target_sell_price))
    print("The Target Buy Price is: ${}".format(target_buy_price))


    if asset_price < target_buy_price:
        notification_text = "Your asset {} has decreased to ${}. Your buy price is currently calculated at ${}".format(result[3],result[0], result[2])
        select_function(updater,"buy_sell")
    elif asset_price > target_sell_price:
        notification_text = "Your asset {} has increased to ${}. Your sell price is currently calculated at ${}".format(result[3], result[0], result[1])
        select_function(updater,"buy_sell")
    else:
        perc_change = round(100*((asset_price-moving_avg)/moving_avg),2)
        notification_text = "Your asset {} is currently {}% from the moving average. Current Price is ${}. 1 month Moving Average is ${}".format(
            ticker_list, perc_change, asset_price, moving_avg)
        print(perc_change)
        if perc_change > 5.0 or perc_change < -5.0:
            select_function(updater, "buy_sell")

    return notification_text



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
    print(updater.update_queue.qsize())


#def Reminders(update: Update, context: CallbackContext) -> None:


def main() -> None:


    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    #test_bot_token 5088014861:AAFXKdqQQo7y4IpyFHKQB_isDf0mWWJa6dw
    #news_bot_toke 5098430589:AAHJkws6DDyv-GNoeHxSpv_svEu_a3cplz0
    updater = Updater("5098430589:AAHJkws6DDyv-GNoeHxSpv_svEu_a3cplz0")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    update_queue = updater.update_queue


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("alarm", alarm_manager,pass_args=False))
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
    print("Bot Reinitialized...")


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #updater.idle()

    return updater



def select_function(updater,func):
    update_queue = updater.update_queue
    update_queue.put_nowait("/{}".format(func))
    #print("Select Func:{} ".format(update_queue.get()))

if __name__ == '__main__':

    updater = main()

    select_function(updater,"reinit")
    notification_text = price_change()








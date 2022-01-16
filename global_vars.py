""""============= Global Variable ==============================================================================="""
#test_bot_token 5088014861:AAFXKdqQQo7y4IpyFHKQB_isDf0mWWJa6dw
#news_bot_toke 5098430589:AAHJkws6DDyv-GNoeHxSpv_svEu_a3cplz0

bot_token = "5088014861:AAFXKdqQQo7y4IpyFHKQB_isDf0mWWJa6dw"
chat_id_num = 5064819774
weather_API = "45e549ff6ec4bb4ca9220bfd6eab0c28"



ticker_dict = {"VGX": "VGX-USD",
               "BTC": "BTC-USD",
               "BMY": "BMY"}

ticker_list = ticker_dict.keys()

notification_text = "Initialized..."

weather_update_text = "Initialized..."

global message_sent



""""============= Variable Initial Condition ==============================================================================="""
message_sent = False

""""============= Library Imports ==============================================================================="""

" Logging Library"
import logging
"Fetch Data from Yahoo Finance"
import yfinance as yf #Fetch Data from Yahoo Finance
"Pandas Dataframe Library"
import pandas as pd

"""Library for Telegram Bot"""
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, StringCommandHandler, Filters, CallbackContext, Handler

"Creating threads to execute functions parallel to bot"
import threading

"Time Libraries"
import datetime
import time

"Online Requests??"
import requests, json

""" ========================== Start the bot ============================ """
# Create the Updater and pass it your bot's token.

updater = Updater(bot_token)
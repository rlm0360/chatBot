from global_vars import *
from function_selector import select_function

def price_change():

    global notification_text

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
        notification_text = "Your asset {} has decreased to ${}. Your buy price is currently calculated at ${}".format(ticker_list,asset_price, target_buy_price)
        select_function(updater,"buy_sell")
    elif asset_price > target_sell_price:
        notification_text = "Your asset {} has increased to ${}. Your sell price is currently calculated at ${}".format(ticker_list, asset_price, target_sell_price)
        select_function(updater,"buy_sell")
    else:
        perc_change = round(100*((asset_price-moving_avg)/moving_avg),2)
        notification_text = "Your asset {} is currently {}% from the moving average. Current Price is ${}. 1 month Moving Average is ${}".format(
            ticker_list, perc_change, asset_price, moving_avg)
        print(perc_change)
        if perc_change > 5.0 or perc_change < -5.0:
            select_function(updater, "buy_sell")

    return notification_text

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
    global notification_text
    context.bot.send_message(chat_id=chat_id_num,text=notification_text)

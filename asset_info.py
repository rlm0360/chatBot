import yfinance as yf #Fetch Data from Yahoo Finance
import pandas as pd
import threading


def price_change():
    threading.Timer(360.0, price_change).start()
    ticker_list = "VGX-USD"

    period = "1w"
    interval = "1m"

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

    return [asset_price,target_sell_price, target_buy_price, ticker_list]

result = price_change()

print("The Asset Price is ${} with a recommended sell price of ${} and buy price of ${}".format(result[0],result[1],result[2]))
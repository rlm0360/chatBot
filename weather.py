from global_vars import *
from function_selector import select_function

def Weather_Update():
    global message_sent
    global weather_update_text

    hour = 5
    minute = 30

    threading.Timer(30.0, Weather_Update).start()

    t = datetime.datetime.now()

    if t.hour == hour and t.minute == minute and message_sent == False:
        print("Post Weather Update")
        message_sent = True

        api_key = weather_API

        # base_url variable to store url
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        # Give city name
        city_name = "Aubrey,US"

        lat = "33.254200"
        long= "-96.942757"

        degree_sign = u"\N{DEGREE SIGN}"

        # complete_url variable to store
        # complete url address
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=imperial"

        # get method of requests module
        # return response object
        response = requests.get(complete_url)

        # json method of response object
        # convert json format data into
        # python format data
        x = response.json()

        print(x)
        # Now x contains list of nested dictionaries
        # Check the value of "cod" key is equal to
        # "404", means city is found otherwise,
        # city is not found
        if x["cod"] != "404":

            # store the value of "main"
            # key in variable y
            y = x["main"]

            print(y)

            # store the value corresponding
            # to the "temp" key of y
            curr_temp = y["temp"]

            feel_temp = y["feels_like"]

            min_temp = y["temp_min"]


            max_temp = y["temp_max"]


            # store the value corresponding
            # to the "pressure" key of y
            current_pressure = y["pressure"]

            # store the value corresponding
            # to the "humidity" key of y
            current_humidity = y["humidity"]

            # store the value of "weather"
            # key in variable z
            z = x["weather"]
            print(z)

            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            weather_description = z[0]["main"]

            # print following values
            weather_update_text = "Good Morning! Currently it is {}{}F and feels like {}{}F. The expected High for the day is {}{}F".format(curr_temp,degree_sign,feel_temp,degree_sign,max_temp,degree_sign)
            select_function(updater,"weather")

        else:
            print(" City Not Found ")
    elif t.hour == hour and t.minute == (minute + 1) and message_sent == True:
        weather_update_text = "No Update"

        message_sent = False
    else:
        weather_update_text = "No Update"

    return weather_update_text


def Weather_Notification(update: Update, context: CallbackContext) -> None:
    global weather_update_text
    context.bot.send_message(chat_id=chat_id_num,text=weather_update_text)
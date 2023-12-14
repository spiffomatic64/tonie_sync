from noaa_sdk import NOAA
import json
from gtts import gTTS
import shutil
from pprint import pprint
from datetime import datetime, timedelta


def get_temp(temp, low):
    temps = {100: "Very hot, Wear a Tshirt and shorts",
             85: "Hot, Wear a Tshirt and shorts",
             75: "Warm, Wear a Tshirt and shorts",
             65: "Nice, Wear a Tshirt and shorts",
             50: "Cool, Wear a Tshirt and pants",
             40: "Cold, Wear a Long Sleeves shirt and pants",
             30: "Very Cold, Wear a Long Sleeves shirt and pants"}

    for t in temps:
        if temp > t:
            if low < 65:
                temp_data = temps[t].replace("shorts","pants")
            return temp_data


def get_forcast(forecast_data, hourly_data):
    json_formatted_str = json.dumps(forecast_data, indent=2)
    print(json_formatted_str)

    tomorrow = datetime.now() + timedelta(1)
    tomorrow_string = tomorrow.strftime("%Y-%m-%d")
    # print(tomorrow_string)
    max = 0
    min = 100
    for hour_data in hourly_data:
        if hour_data['startTime'][:10] == tomorrow_string:
            hour = int(hour_data['startTime'][11:13])

            if hour > 6 and hour < 17:
                # print(hour)
                if hour_data['temperature'] > max:
                    max = hour_data['temperature']
                if hour_data['temperature'] < min:
                    min = hour_data['temperature']

    print(f"High: {max} Low: {min}")
    temp = get_temp(forecast_data['temperature'], min)
    forcast_string = (f"{forecast_data['name']} will be {temp}. " +
                      f"The forecast is {forecast_data['detailedForecast']} " +
                      f"The Low will be {min}")
    return forcast_string


n = NOAA()
res = n.get_forecasts('19067', 'US', type="forecast")
res2 = n.get_forecasts('19067', 'US', type="forecastHourly")
forecast = get_forcast(res[2], res2)
print(forecast)

myobj = gTTS(text=forecast, lang="en", slow=True)

# Saving the converted audio in a mp3 file named
# welcome
path = "I:\\audio\\weather"
filename = "weather"
ext = "mp3"

myobj.save(f"{path}\\{filename}0.{ext}")
for num in range(1, 3):
    shutil.copy(f"{path}\\{filename}0.{ext}", f"{path}\\{filename}{num}.{ext}")

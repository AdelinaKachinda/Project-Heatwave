import requests
import os
import pandas as pd
import sqlalchemy as db
import datetime 
from pytz import timezone
# Weather code


# FUNTION GET_FORECAST, RETURN JSON RESPONSE
class Weather:
    def __init__(self, city):
        self.city = city
        # self.date = datetime.datetime.today().date()
        # self.NextDay_Date = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
        # self.NextNextDay_Date = (datetime.datetime.today() + datetime.timedelta(days=2)).date()
    
    def get_forecast(self, city):
        params = {
            # 'key': os.environ.get('WEATHERAPI_API_KEY'),
            'key': '51872ff903844da98c321057220607',
            'q': str(self.city),
            'days': '3',
            'aqi': "yes",
            'alerts': "yes"}
        BASE_URL = 'https://api.weatherapi.com/v1/forecast.json?'
        r = requests.get(BASE_URL, params)
        return(r.json())

    #this is to help get specific weather date forecasts
    def weather_by_date(self, date, forecast_data):
        i = 0 
        date_forecast_info = None
        #print("Length of forecast_data: ", len(forecast_data))
        print(str(date))
        while i < len(forecast_data["forecast"]["forecastday"]):
            print(forecast_data["forecast"]["forecastday"][i]['date'])
            if forecast_data["forecast"]["forecastday"][i]['date'] == str(date):
                date_forecast_info = forecast_data["forecast"]["forecastday"][i]
            i += 1
        return date_forecast_info

    #gets the specific weather info on a day 
    def get_forecast_info(self, forecast_info):
        forecast_list = []
        if forecast_info is None:
            print("nothing in the forecast_info")
        else:
            count = 0
            for key in forecast_info['day']:
                if key == "condition":
                    val = str(key) + " : " + str(forecast_info['day']
                                                      ["condition"]
                                                      ["text"])
                    forecast_list.insert(count, val)
                else:
                    val = str(key) + " : " + str(forecast_info['day'][key])
                    forecast_list.insert(count, val)
        
                # print(departure_forecast[count])
                count += 1
        return forecast_list


    def retrieve_weather_data(self):
        eastern = timezone('US/Eastern')
        date = datetime.datetime.now(eastern).date()
        NextDay_Date = (datetime.datetime.now(eastern) + datetime.timedelta(days=1)).date()
        NextNextDay_Date = (datetime.datetime.now(eastern) + datetime.timedelta(days=2)).date()

        # date = datetime.datetime.today().date()
        # NextDay_Date = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
        # NextNextDay_Date = (datetime.datetime.today() + datetime.timedelta(days=2)).date()

        print(date)
        print(NextDay_Date)
        print(NextNextDay_Date)

        forecast_data = self.get_forecast(self.city)
        forecast_dict = {"today": [], "tommorrow": [], "day_after": []}

        #parses to forecast
        day_forecast_info = forecast_data["forecast"]["forecastday"][0]

        #obtain the weather data for that day
        day_forecast_info = self.weather_by_date(date, forecast_data)
        # print(len(day_forecast_info))
        tommorrow_forecast_info = self.weather_by_date(NextDay_Date, forecast_data)
        day_after_forecast_info = self.weather_by_date(NextNextDay_Date, forecast_data)

        print(len(day_forecast_info))
        print(len(tommorrow_forecast_info))
        print(len(day_after_forecast_info))

        today_forecast = self.get_forecast_info(day_forecast_info)
        #print(today_forecast)
        tommorrow_forecast = self.get_forecast_info(tommorrow_forecast_info)
        day_after_forecast = self.get_forecast_info(day_after_forecast_info)

        forecast_dict["today"] = today_forecast
        forecast_dict["tommorrow"] = tommorrow_forecast
        forecast_dict["day_after"] = day_after_forecast

        return self.create_database(forecast_dict)


    def create_database(self, forecast_info_dict):
        if forecast_info_dict is None:
            return None
        # create dataframe from the extracted records
        forecast_df = pd.DataFrame.from_dict(forecast_info_dict)

        # creating a database from dataframe
        # engine = db.create_engine('sqlite:///weather_forecast.db')
        # forecast_df.to_sql('forecast_info_dict',
        #                    con=engine,
        #                    if_exists='replace',
        #                    index=False)
        # query_result = engine.execute(
        #                             "SELECT * FROM" +
        #                             " forecast_info_dict;").fetchall()

        return forecast_df


    # print("This is the weather for city: ", self.city)
    # #print("date : " + day_forecast_info['date'])
    # print(create_database(forecast_dict))
    # #print((pd.DataFrame(query_result)))

example = Weather("New York")
print(example.retrieve_weather_data())

#timeZone handling
# zones = pytz.all_timezones
# num = 1
# us_zones = zones[577: 588]
# print()


# timezone = us_zones[int(1) - 1]
# print(timezone)
# pytz.timezone(timezone)
# print(pytz.timezone(timezone))

# eastern = timezone('US/Eastern')


# date = datetime.datetime.now(eastern).date()
# NextDay_Date = (datetime.datetime.now(eastern) + datetime.timedelta(days=1)).date()
# NextNextDay_Date = (datetime.datetime.now(eastern) + datetime.timedelta(days=2)).date()

# print(datetime.datetime.now())
# print(date)
# print(NextDay_Date)
# print(NextNextDay_Date)

# forecast_data = example.get_forecast("New York")
# forecast_dict = {"today": [], "tommorrow": [], "day_after": []}
# day_after_forecast_info = example.weather_by_date(NextNextDay_Date, forecast_data)
# print(day_after_forecast_info)

# Timezone handling
# name of airports and overall route


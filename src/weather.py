import requests
import os
import pandas as pd
import sqlalchemy as db
import datetime 
# Weather code


# FUNTION GET_FORECAST, RETURN JSON RESPONSE
class Weather():
    city = "New York"
    date = datetime.datetime.today().date()
    NextDay_Date = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
    NextNextDay_Date = (datetime.datetime.today() + datetime.timedelta(days=2)).date()
    print("Today date is: ", date)
    print("Tomorrow is: ", NextDay_Date)
    print("Day after Tomorrow is: ", NextNextDay_Date)

    def get_forecast(city):
        params = {
            # 'key': os.environ.get('WEATHERAPI_API_KEY'),
            'key': '51872ff903844da98c321057220607',
            'q': str(city),
            'days': '3',
            'aqi': "yes",
            'alerts': "yes"}
        BASE_URL = 'https://api.weatherapi.com/v1/forecast.json?'
        r = requests.get(BASE_URL, params)
        return(r.json())

    #this is to help get specific weather date forecasts
    def weather_by_date(date, forecast_data):
        i = 0 
        date_forecast_info = None
        #print("Length of forecast_data: ", len(forecast_data))
        while i < len(forecast_data["forecast"]["forecastday"]):
            if forecast_data["forecast"]["forecastday"][i]['date'] == str(date):
                date_forecast_info = forecast_data["forecast"]["forecastday"][i]
            i += 1
        return date_forecast_info

    #gets the specific weather info on a day 
    def get_forecast_info(forecast_info):
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

    #obtains the dictionary with all weather data for the next three days 
    forecast_data = get_forecast(city)

    forecast_dict = {"today": [], "tommorrow": [], "day_after": []}
    # holds the weather information in a dictionary in case we want to
    # include this information in the database



    #parses to forecast
    #day_forecast_info = forecast_data["forecast"]["forecastday"][0]

    # obtain the weather data for that day
    day_forecast_info = weather_by_date(date, forecast_data)
    # print(len(day_forecast_info))
    tommorrow_forecast_info = weather_by_date(NextDay_Date, forecast_data)
    day_after_forecast_info = weather_by_date(NextNextDay_Date, forecast_data)


    today_forecast = get_forecast_info(day_forecast_info)
    #print(today_forecast)
    tommorrow_forecast = get_forecast_info(tommorrow_forecast_info)
    day_after_forecast = get_forecast_info(day_after_forecast_info)



    forecast_dict["today"] = today_forecast
    forecast_dict["tommorrow"] = tommorrow_forecast
    forecast_dict["day_after"] = day_after_forecast


    def create_database(forecast_info_dict):
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


    # print("This is the weather for city: ", city)
    #print("date : " + day_forecast_info['date'])
    # print(create_database(forecast_dict))
    #print((pd.DataFrame(query_result)))

# weather = Weather()
# print(weather.forecast_dict)


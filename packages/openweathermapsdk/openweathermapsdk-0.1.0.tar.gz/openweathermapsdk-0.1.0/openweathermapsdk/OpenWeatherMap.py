import requests
from datetime import datetime


class OpenWeatherMap:
    def __init__(self,api_key):
        self.api_key = api_key
        self.daily_url = "https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=pt&appid={api_key}"
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pt&appid={api_key}"

    def get_daily_forecast(self, city=None, remove_yesterday=True):
        url = self.daily_url.format(city=city, api_key=self.api_key)
        response = requests.get(url)
        daily_forecast = []
        yesterday_date = datetime.now().strftime("%d/%m")
        if response.status_code == 200:
            data = response.json()
            temperatures_by_date = {}
            for forecast in data["list"]:
                date_time = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
                date = date_time.strftime("%d/%m")
                temperature = forecast["main"]["temp"]
                if date in temperatures_by_date:
                    temperatures_by_date[date].append(temperature)
                else:
                    temperatures_by_date[date] = [temperature]
            for date, temperatures in temperatures_by_date.items():
                average_temperature = sum(temperatures) / len(temperatures)
                daily_forecast.append(
                    {"date": date, "avg_temp": round(average_temperature, 1)}
                )
            if remove_yesterday:
                daily_forecast = [
                    i for i in daily_forecast if not (i["date"] == yesterday_date)
                ]
            return daily_forecast
        else:
            return response.json()

    def get_weather(self, city=None):
        url = self.weather_url.format(city=city, api_key=self.api_key)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_description = data["weather"][0]["description"]
            temp = round(data["main"]["temp"],1)
            date_time = datetime.fromtimestamp(data["dt"])
            date = date_time.strftime("%d/%m")
            return {"desc": weather_description, "temp": temp, "date": date}
        else:
            return response.json()

    def get_description(self, city=None):
        
        weather = self.get_weather(city=city)
        keys_set = {"desc","temp","date"}
        
        if keys_set== set(weather.keys()):
            text = "{average}°C e {status} em {city} em {date}. Média para os próximos dias: ".format(
                average=weather["temp"],
                status=weather["desc"],
                city=city,
                date=weather["date"],
            )
            daily_forecast = self.get_daily_forecast(city=city)
            if isinstance(daily_forecast,list):
                for forecast in daily_forecast[:-1]:
                    text += "{average}°C em {date}, ".format(
                        average=forecast["avg_temp"], date=forecast["date"]
                    )
                text = text[:-2]
                last_forecast = daily_forecast.pop()
                text+= " e {average}°C em {date}. ".format(
                        average=last_forecast["avg_temp"], date=last_forecast["date"]
                    )
        else: 
            text = None
        return text

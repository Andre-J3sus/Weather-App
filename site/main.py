from flask import Flask, request, render_template, redirect
import requests


# Config API
url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
api_key = "5d3247cdb8935e18e1d1f71e9423db2e"


# Get the weather from the url
def get_weather(city_searched):
    result = requests.get(url.format(city_searched, api_key))
    if result:
        json = result.json()
        # Getting the info that we want {City, Country, Temperatures, Icon, Weather Description}
        # Location
        city = json["name"]
        country = json["sys"]["country"]

        # Temperature
        temp_kelvin = json["main"]["temp"]
        temp_celsius = round(temp_kelvin - 273.15, 2)  # Converting kelvin to celsius
        min_temp_celsius = round(json["main"]["temp_min"] - 273.15, 2)
        max_temp_celsius = round(json["main"]["temp_max"] - 273.15, 2)

        # Weather description and icon
        icon = json["weather"][0]["icon"]
        weather_desc = json["weather"][0]["description"]

        return city, country, temp_celsius, icon, weather_desc, min_temp_celsius, max_temp_celsius
    else:
        return None


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST" and request.form["city"].strip() != "":
        city = request.form["city"]
        weather_info = get_weather(city)
        return render_template("base.html",
                               city=weather_info[0], country=weather_info[1],
                               icon=weather_info[3],
                               weather=weather_info[4].capitalize(), temp=weather_info[2]
                               )
    else:
        return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)

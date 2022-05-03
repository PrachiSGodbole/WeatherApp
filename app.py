from flask import Flask, render_template, request
import urllib.request, json
import os
from serpapi import GoogleSearch
import configparser


app = Flask(__name__)
cfg = configparser.ConfigParser()
cfg.read('settings.cfg')

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/", methods = ['GET','POST'])
def get_weather():
    if request.method == 'POST':
        if "city" in request.form:
            city = request.form['city']
        
        url = "http://api.openweathermap.org/geo/1.0/direct?q="+city+"&limit=5&appid={}".format(cfg.get('KEYS', 'WEATHER_API_KEY', raw=''))
        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)
        lat = dict[0].get('lat')
        lon = dict[0].get('lon')

        # # weather updates
        url = "https://api.openweathermap.org/data/2.5/onecall?lat="+str(lat)+"&lon="+str(lon)+"&exclude=hourly,daily&appid={}".format(cfg.get('KEYS', 'WEATHER_API_KEY', raw=''))
        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)

        # event updates
        params = {
            "engine": "google_events",
            "q": "Events in "+ city,
            "hl": "en",
            "gl": "us",
            "api_key": cfg.get('KEYS', 'EVENTS_API_KEY', raw='')
            }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        events_results = results['events_results']

        return render_template ("weather.html", weather=dict["current"],events=events_results )
    return render_template ("search.html",)

if __name__ == '__main__':
    app.run(debug=True)
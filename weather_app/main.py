from pathlib import Path
from flask import Flask, render_template
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<station>/<date>")
def weather(station: str, date: str):
    # Get the data of the station
    try:
        path_to_load = f"/home/API/weather_app/data/TG_STAID{int(station):06d}.txt"
        station_data = pd.read_csv(path_to_load, sep=",", skiprows=20, parse_dates=['    DATE'])
    except FileNotFoundError:
        return {"error": f"Station {station} not found"}, 404
    
    # Load the station data
    
    station_data.rename(columns={' SOUID':'SOUID', '    DATE':'DATE', '   TG':'TG', ' Q_TG':'Q_TG'}, inplace=True)
    station_data.replace({'TG': -9999}, np.nan, inplace=True)
    station_data.TG = station_data.TG/10
    
    # Get the temperature and refromat the date
    temperature = station_data.loc[station_data.DATE == date,'TG'].squeeze()
    if isinstance(temperature, pd.Series):
        return {"error": f"The entered date {date} is not available"}, 404
    reformat = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    
    # Get the station name
    stations = pd.read_csv("/home/API/weather_app/data/stations.txt", sep=",", skiprows=17)
    stations.rename(columns={"STANAME                                 ": "STANAME"}, inplace=True)
    station_name = stations.loc[stations['STAID'] == int('10'),'STANAME'].squeeze().strip()
    
    return {'station': f"{station_name} (ID: {station})", 'date': reformat, 'temperature': temperature}

if __name__ == "__main__":


    # print(list(Path("/home/API/weather_app/data").glob('TG*.txt')))
    app.run(debug=True)
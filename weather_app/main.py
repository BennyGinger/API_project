from pathlib import Path
from flask import Flask, render_template
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load the stations names txt file
stations = pd.read_csv("/home/API/weather_app/data/stations.txt", skiprows=17)
stations.rename(columns={"STANAME                                 ": "Station Name",'STAID':"ID"}, inplace=True)

@app.route("/")
def home():
    return render_template("home.html", stations=stations[['ID','Station Name']].to_html(index=False, justify='center'))

@app.route("/api/v1/<station>/<date>")
def one_sta_one_day(station: str, date: str):
    # Get the data of the station
    station_data = load_station_data(station)
    if isinstance(station_data, dict):
        return station_data, 404
    
    # Get the temperature and refromat the date
    temperature = station_data.loc[station_data.DATE == date,'TG'].squeeze()
    if isinstance(temperature, pd.Series):
        return {"error": f"The entered date {date} is not available"}, 404
    reformat = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    
    # Get the station name
    station_name = stations.loc[stations['STAID'] == int('10'),'STANAME'].squeeze().strip()
    
    return {'station': f"{station_name} (ID: {station})", 'date': reformat, 'temperature': temperature}


@app.route("/api/v1/<station>")
def one_sta_all_days(station: str):
    # Get the data of the station
    station_data = load_station_data(station)
    if isinstance(station_data, dict):
        return station_data, 404
    
    return station_data.to_dict(orient='records')

@app.route("/api/v1/yearly/<station>/<year>")
def one_sta_one_year(station: str, year: str):
    # Get the data of the station
    station_data = load_station_data(station)
    if isinstance(station_data, dict):
        return station_data, 404
    
    # Filter the data
    station_data = station_data.loc[station_data.DATE.dt.year == int(year)]
    
    return station_data.to_dict(orient='records')

def load_station_data(station: str)-> pd.DataFrame | dict:
    try:
        # Load the station data
        path_to_load = f"/home/API/weather_app/data/TG_STAID{int(station):06d}.txt"
        station_data = pd.read_csv(path_to_load, sep=",", skiprows=20, parse_dates=['    DATE'])
        # Filter the data and rename the columns
        station_data.rename(columns={' SOUID':'SOUID', '    DATE':'DATE', '   TG':'TG', ' Q_TG':'Q_TG'}, inplace=True)
        station_data.replace({'TG': -9999}, np.nan, inplace=True)
        station_data.TG = station_data.TG/10
        
        
        
        return station_data
    except FileNotFoundError:
        return {"error": f"Station {station} not found"}

 
if __name__ == "__main__":


    # print(list(Path("/home/API/weather_app/data").glob('TG*.txt')))
    app.run(debug=True)
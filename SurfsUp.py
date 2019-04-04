import numpy as np
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import datetime as dt

def get_date_prev_yr(last_date):
    yr = int(last_date.split("-")[0])
    mn = int(last_date.split("-")[1])
    dy = int(last_date.split("-")[2])
    return dt.date(yr, mn, dy) - dt.timedelta(days=365)
 
def get_last_date():
    return session.query(Measurement.date)\
        .order_by(Measurement.date.desc()).first()

def get_query_date():
    return get_date_prev_yr(get_last_date()[0])

# This function called `calc_temps` will accept start date 
# and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures
# for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    return session.query(func.min(Measurement.tobs),
                        func.avg(Measurement.tobs), 
                        func.max(Measurement.tobs))\
                        .filter(Measurement.date >= start_date)\
                        .filter(Measurement.date <= end_date).all()

def total_rain(station, start_date, end_date):
    """Total rainfall for the weather station for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        station (string): station id
    Returns:
        TotalRainfall
    """
    
    return session.query(func.sum(Measurement.prcp)).\
                filter(Measurement.station==station).\
                filter(Measurement.date >= start_date).\
                filter(Measurement.date <= end_date).first()
 
# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data
#  matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), 
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)]
    return session.query(*sel)\
        .filter(func.strftime("%m-%d", Measurement.date) == date).all()

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"/api/v1.0/trip/<start>/<end><br/>"
        f"/api/v1.0/rain/<station>/<start>/<end><br/>"
        f"/api/v1.0/rain/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary"""
    """using `date` as the key and `prcp` as the value."""
    """Return the JSON representation of your dictionary."""

    query_date = get_query_date()

    results = session.query(Measurement.date,
                            Measurement.prcp)\
                            .filter(Measurement.date >= query_date)\
                            .all()

    all_prcps = [{"DATE":"PRECIPITATION"}]
    for date, prcp in results:
        prcp_dict = {date:prcp}
        all_prcps.append(prcp_dict)

    return jsonify(all_prcps)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query all stations
    results = session.query(Station.station, 
                            Station.name).all()

    all_stations = []
    for station, name in results:
        station_dict = {}
        station_dict["WeatherStation"] = name
        station_dict["Station ID"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Convert the query results to a Dictionary"""
    """using `date` as the key and `tobs` as the value."""
    """Return the JSON representation of your dictionary."""

    query_date = get_query_date()

    results = session.query(Measurement.date,
                            Measurement.tobs)\
                            .filter(Measurement.date >= query_date)\
                            .all()

    all_tobs = [{"DATE":"TOBS"}]
    for date, tob in results:
        tobs_dict = {date:tob}
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
  # Return a JSON list of the minimum temperature, 
  # the average temperature, and the max temperature 
  # for a given start or start-end range.
  # When given the start only, 
  # calculate `TMIN`, `TAVG`, and `TMAX` for all 
  # dates greater than and equal to the start date.

    last_date = get_last_date()

    results = calc_temps(start, last_date[0])

    all_temps = [{'Start': start},
                {'End Date': last_date[0]}]
    for tmin, tave, tmax in results:
        temp_dict = {}
        temp_dict['TMIN'] = tmin
        temp_dict['TAVE'] = tave
        temp_dict['TMAX'] = tmax
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>/<end>")
def startToEnd(start,end):
  # Return a JSON list of the minimum temperature, 
  # the average temperature, and the max temperature 
  # for a given start or start-end range.
  # When given the start and the end date,
  #  calculate the `TMIN`, `TAVG`, and `TMAX` 
  # for dates between the start and end date inclusive.
    
    results = calc_temps(start, end)

    all_temps = [{'Start': start},
                 {'End Date': end}]
    for tmin, tave, tmax in results:
        temp_dict = {}
        temp_dict['TMIN'] = tmin
        temp_dict['TAVE'] = tave
        temp_dict['TMAX'] = tmax
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<trip>/<start>/<end>")
def trip(trip,start,end):
  # Return a JSON list of the minimum temperature, 
  # the average temperature, and the max temperature 
  # for a given start or start-end range.
  # When given the start and the end date,
  #  calculate the `TMIN`, `TAVG`, and `TMAX` 
  # for dates between the start and end date inclusive.
    
    results = calc_temps(get_date_prev_yr(start),
                        get_date_prev_yr(end))

    all_temps = [{'Start': start},
                 {'End Date': end}]
    for tmin, tave, tmax in results:
        temp_dict = {}
        temp_dict['TMIN'] = tmin
        temp_dict['TAVE'] = tave
        temp_dict['TMAX'] = tmax
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/rain/<station>/<start>/<end>")
def rain(station,start,end):
  # Return a JSON list of the minimum temperature, 
  # the average temperature, and the max temperature 
  # for a given start or start-end range.
  # When given the start and the end date,
  #  calculate the `TMIN`, `TAVG`, and `TMAX` 
  # for dates between the start and end date inclusive.
    
    results = total_rain(station, get_date_prev_yr(start),
                        get_date_prev_yr(end))

    all_prcps = [{'Start': start},
                 {'End Date': end}]
    for rain in results:
        rain_dict = {}
        rain_dict['RAINFALL'] = rain
        all_prcps.append(rain_dict)

    return jsonify(all_prcps)

@app.route("/api/v1.0/rain/<start>/<end>")
def rain_all_stations(start,end):

    results = session.query(Station.station, 
                            Station.name).all()

    all_stations = [{'Start': start},
                 {'End Date': end}]
    for station, name in results:
        station_dict = {}
        station_dict["WeatherStation"] = name
        station_dict["Station ID"] = station
        rainfall = total_rain(station, get_date_prev_yr(start),
                        get_date_prev_yr(end))
        station_dict['RAINFALL'] = rainfall.rain
        all_stations.append(station_dict)

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)

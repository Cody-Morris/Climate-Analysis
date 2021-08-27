import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Print all of the classes mapped to the Base
Base.classes.keys()

 # Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

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
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation:<br/>'
        f'/api/v1.0/stations:<br/>'
        f'/api/v1.0/tobs:<br/>'
        f'/api/v1.0/&lt;start&gt;:replace &lt;start&gt; with date format yyyy-mm-dd<br/>'
        f'/api/v1.0/&lt;start&gt;/&lt;end&gt;:replace &lt;start&gt; and &lt;end&gt; with date format yyyy-mm-dd<br/>'
    )

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    
    session = Session(engine)
    # Find the most recent date in the data set.
    strDate = session.query(func.max(Measurement.date)).first()[0]
    lastDate = dt.datetime.strptime(strDate, '%Y-%m-%d')
    lastDate

    prevYear = lastDate - dt.timedelta(days=366)

    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= prevYear).all()

    session.close()

     # Create a dictionary from the row data and append 
    all_weather = []
    for date,prcp in results:
        weather_dict = {}
        weather_dict["date"] = date
        weather_dict["prcp"] = prcp
        all_weather.append(weather_dict)

    return jsonify(all_weather)

@app.route("/api/v1.0/stations")
def station():

    session = Session(engine)

    result2 = session.query(Station.name)

    session.close()

    all_stations = []
    for station in result2:
        station_dict = {}
        station_dict['name'] = station.name
        all_stations.append(station_dict)
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    tobsresults = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').all()

    session.close()

    all_tobs = []
    for date,tobs in tobsresults:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_func(start):

    session = Session(engine)

    active = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),\
                       func.avg(Measurement.tobs)).\
                           order_by(Measurement.date).filter(Measurement.date >= start).all()    

    session.close()

    start_tobs = []
    for min,max,avg in active:
        start_dict = {}
        start_dict['min'] = min
        start_dict['max'] = max
        start_dict['avg'] = avg
        start_tobs.append(start_dict)

    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end_func(start,end):

    session = Session(engine)

    active = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),\
                       func.avg(Measurement.tobs)).\
                           order_by(Measurement.date).filter(Measurement.date >= start).filter(Measurement.date <= end).all()    

    session.close()

    start_end_tobs = []
    for min,max,avg in active:
        start_end_dict = {}
        start_end_dict['min'] = min
        start_end_dict['max'] = max
        start_end_dict['avg'] = avg
        start_end_tobs.append(start_end_dict)

    return jsonify(start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)
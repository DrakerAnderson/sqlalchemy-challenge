# Import the dependencies.
import numpy as np
from datetime import datetime, timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session()

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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Calculate the date 12 months ago
    date_12_months_ago = datetime.now() - timedelta(days=365.25)

    # Query the database for the last 12 months of precipitation data
    last_12_months_prcp = db.session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= date_12_months_ago).\
        all()

    # Convert the query results to a dictionary
    prcp_dict = {date: prcp for date, prcp in last_12_months_prcp}

    # Return the JSON representation of the dictionary
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query the database for a list of stations
    stations = active_stations.session.query(Station.name).all()

    # Convert the query results to a list
    station_list = [station[0] for station in stations]

    # Return the JSON representation of the list
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Identify the most-active station
    most_active_station = db.session.query(measurement.station, func.count(measurement.tobs)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.tobs).desc()).\
        first()

    # Query the dates and temperature observations for the most-active station
    # for the previous year of data
    previous_year = dt.date.today() - dt.timedelta(days=365)
    tobs_query = db.session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station[0]).\
        filter(measurement.date >= previous_year).\
        all()

    # Convert the query results to a list of dictionaries
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_query]

    # Return the JSON representation of the list
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Convert the start date to a datetime object
    start_date = datetime.strptime(start, "%Y-%m-%d")

    # Query the minimum, average, and maximum temperatures for all dates
    # greater than or equal to the start date
    temp_query = db.session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        all()

    # Convert the query results to a dictionary
    temp_dict = {
        "TMIN": temp_query[0][0],
        "TAVG": temp_query[0][1],
        "TMAX": temp_query[0][2]
    }

    # Return the JSON representation of the dictionary
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Convert the start and end dates to datetime objects
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    # Query the minimum, average, and maximum temperatures for the dates
    # from the start date to the end date, inclusive
    temp_query = db.session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).\
        all()

    # Convert the query results to a dictionary
    temp_dict = {
        "TMIN": temp_query[0][0],
        "TAVG": temp_query[0][1],
        "TMAX": temp_query[0][2]
    }

    # Return the JSON representation of the dictionary
    return jsonify(temp_dict)

# Import the dependencies.
import numpy as np 
import datetime as dt 
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create an engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a base class
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# All Dates to be provided in the YYYY-MM-DD format
@app.route("/")
def home(): 
    """ List all available api routes."""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/tour1<start_date><br>"
        f"/api/v1.0/tour2<start_date><end_date><br>"
    )
#Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Query the previous 12 months of data and provide daily precipitation across all stations    
    latest_date = dt.date(2017, 8, 23)
    # Calculate the date one year from the last date in data set [assuming 365 days]
    one_year_ago = latest_date - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    query_result = session.query(Measurement.date, Measurement.prcp).\
        filter(and_(Measurement.date >= one_year_ago, Measurement.date <= latest_date)).\
        order_by(Measurement.date.asc()).all()
    # Close the session
    session.close()

    # Convert query results to a dictionary using date as the key and prcp as the value
    prcp_values = []
    for date, prcp in query_result: 
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_values.append(prcp_dict)

    return jsonify(prcp_values)

#define the Stations route

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #query the stations and a measure of how active they are as measured by total count of rows
    active_stations = session.query(Measurement.station,func.count(Measurement.id)) \
                             .group_by(Measurement.station) \
                             .order_by(func.count(Measurement.id).desc()) \
                             .all()
    #close the session
    session.close()

    #convert list of tuples to regular list and jsonify
    active_stations_list = [{"station": station, "count": count} for station, count in active_stations]

    return jsonify(active_stations_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    session = Session(engine)
    latest_date = (dt.date(2017, 8, 23))
    # one year from the last date in data set [assuming 365 days]
    one_year_ago = latest_date - dt.timedelta(days=365)

    #queryd data
    active_tobs_data  = session.query(Measurement.date, Measurement.tobs).\
                   filter(Measurement.station == 'USC00519281').\
                   filter(and_(Measurement.date >= one_year_ago, Measurement.date <= latest_date)).\
                   order_by(Measurement.date.asc())
    session.close()

#convert query results to a list of dictionaries

    tobs_values = [] 

    for date, tobs in active_tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs 
        tobs_values.append(tobs_dict)

    return jsonify(tobs_values)                    


@app.route("/api/v1.0/tour1/<start_date>")
def tour1(start_date, end_date='2017-08-23'):
    # Accepts the start date as a parameter from the URL
    # Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
    # If no end date is provided, the function defaults to 2017-08-23.

    #start session
    session = Session(engine)

    query_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    tour_stats = []
    for min, avg, max in query_result:
        tour_dict = {}
        tour_dict["Min"] = min
        tour_dict["Average"] = avg
        tour_dict["Max"] = max
        tour_stats.append(tour_dict)

    # If the query returned non-null values return the results,
    # otherwise return an error message
    if tour_dict['Min']: 
        return jsonify(tour_stats)
    else:
        return jsonify({"error": f"Date {start_date} not found or not formatted as YYYY-MM-DD."}), 404

@app.route("/api/v1.0/tour2/<start_date>/<end_date>")
@app.route("/api/v1.0/tour2/<start_date>", defaults={'end_date': '2017-08-23'})
def tour2(start_date, end_date='2017-08-23'):
    # Accepts the start and end dates as parameters from the URL
    # Returns the min, max, and average temperatures calculated from the given start date to the given end date
    # If no valid end date is provided, the function defaults to 2017-08-23.

    session = Session(engine)
    query_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    # loop through and assign stats to a dictionary, and then append said dictionary to a list
    tour_stats = []
    for min, avg, max in query_result:
        tour_dict = {}
        tour_dict["Min"] = min
        tour_dict["Average"] = avg
        tour_dict["Max"] = max
        tour_stats.append(tour_dict)

    # If the query returned non-null values return the results,
    # otherwise return an error message
    if tour_dict['Min']: 
        return jsonify(tour_stats)
    else:
        return jsonify({"error": f"Date(s) not found, invalid date range or dates not formatted correctly."}), 404

if __name__ == '__main__':
    app.run(debug=True)
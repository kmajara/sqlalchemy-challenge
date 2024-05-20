# Import the dependencies.
import numpy as np 
import datetime as dt 
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
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
# Measurement = Base.metadata.tables['measurement']
# Station = Base.metadata.tables['station']

Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session
Session = sessionmaker(bind=engine)
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
    """ List all available api routes."""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
    )
#defining the precipitation route

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the previous 12 months of data and provide daily precipitation across all stations    
    latest_date = dt.date(2017, 8, 23)
    # Calculate the date one year from the last date in data set [assuming 365 days]
    one_year_ago = latest_date - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    query_result = session.query(Measurement.date, Measurement.prcp).\
        filter(and_(Measurement.date >= one_year_ago, Measurement.date <= latest_date)).\
        order_by(Measurement.date.asc()).all()
    
    # Close the session here
    session.close()

    # Convert query results to a dictionary using date as the key and prcp as the value
    prcp_values = []

    for date, prcp in query_result: 
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_values.append(prcp_dict)

    return jsonify(prcp_values)

#defining the Stations route

@app.route("/api/v1.0/stations")
def stations():
    #query the stations and a measure of how active they are as measured by total count of rows
    active_stations = session.query(Measurement.station,func.count(Measurement.id)) \
                             .group_by(Measurement.station) \
                             .order_by(func.count(Measurement.id).desc()) \
                             .all()
    #close the session
    session.close()

    #convert list of tuples to regular list and jsonify
    active_stations_list = list(np.ravel(active_stations))
   
    return jsonify(active_stations)



if __name__ == '__main__':
    app.run(debug=True)

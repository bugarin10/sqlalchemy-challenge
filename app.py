import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
import dateparser


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


Measurments=Base.classes.measurement
Station=Base.classes.station

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
        f"/api/v1.0/&lt star &gt <br/>"
        f"/api/v1.0/&lt star &gt/&lt end &gt<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitations in inches"""
    # Query all passengers
    results = session.query(Measurments.date,Measurments.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = [dict(results)]

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitations in inches"""
    # Query all passengers
    results = session.query(Station.name,Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = [dict(results)]

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitations in inches"""
    
    recent_d=session.query(Measurments.date).order_by(Measurments.date.desc()).first()[0]
    # Calculate the date one year from the last date in data set.
    query_date = datetime.strptime(recent_d,'%Y-%m-%d') - dt.timedelta(days=365)
    print("Query Date: ", query_date)
    # Perform a query to retrieve the data and precipitation scores
    sel=[Measurments.date,Measurments.prcp]
    results = session.query(*sel).filter(Measurments.date > query_date).all()
    session.close()

    # Convert list of tuples into normal list
    all_tobs = [dict(results)]

    return jsonify(all_tobs)


@app.route("/api/v1.0/<star>")
def tobs_star(star):
    try:
        star_date=dateparser.parse(star)
        star_date=star_date.strftime("%Y-%m-%d")
        # Create our session (link) from Python to the DB
        session = Session(engine)

        recent_d=session.query(Measurments.date).order_by(Measurments.date.desc()).first()[0]

        if star_date<recent_d:
        # Perform a query to retrieve the data and precipitation scores
            sel=[func.min(Measurments.tobs),func.max(Measurments.tobs),func.avg(Measurments.tobs)]
            results = session.query(*sel).filter(Measurments.date >= star_date).all()
            session.close()
            # Convert list of tuples into normal list
            sum_tobs=[{
                        'TMIN':results[0][0],
                        'TAVG':results[0][2],
                        'TMAX':results[0][1]
                        }]
            return jsonify(sum_tobs)
        else: 
            return jsonify({"error": f"{star} out of date."}), 404
    except:
        return jsonify({"error": f"{star} not valid as date."}), 404

@app.route("/api/v1.0/<star>/<end>")
def tobs_star_end(star,end):
    try:
        star_date=dateparser.parse(star)
        end_date=dateparser.parse(end)
        star_date=star_date.strftime("%Y-%m-%d")
        end_date=end_date.strftime("%Y-%m-%d")
        
        
        
        # Create our session (link) from Python to the DB
        session = Session(engine)

        recent_d=session.query(Measurments.date).order_by(Measurments.date.desc()).first()[0]

        if star_date<recent_d:
        # Perform a query to retrieve the data and precipitation scores
            sel=[func.min(Measurments.tobs),func.max(Measurments.tobs),func.avg(Measurments.tobs)]
            results = session.query(*sel).filter(Measurments.date >= star_date).filter(Measurments.date <= end_date).all()
            session.close()
            # Convert list of tuples into normal list
            sum_tobs=[{
                        'TMIN':results[0][0],
                        'TAVG':results[0][2],
                        'TMAX':results[0][1]
                        }]
            return jsonify(sum_tobs)
        else: 
            return jsonify({"error": f"{star} out of date."}), 404
    except:
        return jsonify({"error": f"{star} not valid as date."}), 404


if __name__ == '__main__':
    app.run(debug=True)
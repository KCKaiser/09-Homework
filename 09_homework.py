import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():

    return render_template('home.html')

@app.route("/api/v1.0/precipitation/")
def precipitation():

    session = Session(engine)

    prcp_ls = session.query(Measurement.date, Measurement.tobs).all()
    prcp_dict = dict(prcp_ls)

    return jsonify(prcp_dict)

@app.route("/api/v1.0/station/")
def station():

    session = Session(engine)

    station_ls = session.query(Station.name).all()
    station_ls = [station[0] for station in station_ls]
    return jsonify(station_ls)

@app.route("/api/v1.0/tobs/")
def tobs():

    session = Session(engine)

    tobs_ls = session.query(Measurement.tobs).all()
    tobs_ls = [tobs[0] for tobs in tobs_ls]
    return jsonify(tobs_ls)

@app.route("/api/v1.0/<start>/")
def start(start):
    session = Session(engine)
    start_ls = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    start_dict = {}
    start_dict["TMIN"] = start_ls[0][1]
    start_dict["TAVG"] = start_ls[0][2]
    start_dict["TMAX"] = start_ls[0][3]
        
    return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)

    start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date <= end).\
        filter(Measurement.date >= start).all()
  
    start_dict2 = {}
    start_dict2["TMIN"] = start_end[0][1]
    start_dict2["TAVG"] = start_end[0][2]
    start_dict2["TMAX"] = start_end[0][3]
           
    return jsonify(start_dict2)

if __name__ == '__main__':
    app.run(debug=True)


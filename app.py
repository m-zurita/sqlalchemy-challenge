import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return(f'''
        Available routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
    ''')

@app.route("/api/v1.0/precipitation")
def prcps():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_prcps = []
    for date, prcp in results:
        measurement_dic={}
        measurement_dic["date"] = date
        measurement_dic["prcp"] = prcp
        all_prcps.append(measurement_dic)
    return jsonify(all_prcps)

@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)
    results = session.query(Measurement.station).all()
    session.close()
    all_stat = list(np.ravel(results))
    return jsonify(all_stat)

@app.route("/api/v1.0/tobs")
def tempobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-18').all()
    session.close()
    all_tempobs = []
    for date, tobs in results:
        measurement_dic = {}
        measurement_dic["date"] = date
        measurement_dic["tobs"] = tobs
        all_tempobs.append(measurement_dic)
    return jsonify(all_tempobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    print(start)
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()       
    session.close()
    return jsonify({'results' : results})

@app.route("/api/v1.0/<start>/<end>")
def ranges(start, end):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    session.close()
    return jsonify({'results' : results})

if __name__=="__main__":
    app.run(debug=True)
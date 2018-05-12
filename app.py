import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///sql.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Meas = Base.classes.Measurements
Stat = Base.classes.Stations
last_12=dt.date(2017,8,23)-dt.timedelta(days=365)
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
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/range/start<start>/end<end>:<br>"
        f"Please provide a start date, for the end date, type in a date or latest to get the lates date"
        
    )


@app.route("/api/v1.0/percipitation")
def percipitation():
    results= session.query(Meas).filter(Meas.Date>=last_12).all()
    per=[]
    for re in results:
        dic={}
        dic[str(re.Date)]=re.Prcp
        per.append(dic)
    return jsonify(per)

@app.route("/api/v1.0/stations")
def stations():
    results=session.query(Stat.station).all()
    station=list(np.ravel(results))
    return jsonify(station)
@app.route("/api/v1.0/tobs")
def temp():
    result= session.query(Meas).filter(Meas.Date>=last_12).all()
    tob=[]
    for res in result:
        dics={}
        dics[str(res.Date)]=res.Tobs
        tob.append(dics)
    return jsonify(tob)
@app.route("/api/v1.0/range/<start>/<end>")
def calc_temp(start,end):

    TMin=func.min(Meas.Tobs)
    TAvg=func.avg(Meas.Tobs)
    TMax=func.max(Meas.Tobs)
    sel= [ 
       TAvg, 
       TMin, 
       TMax,
       ]
    st=dt.datetime.strptime(start, "%Y-%m-%d")
    if end!='latest':
        ed=dt.datetime.strptime(end, "%Y-%m-%d")
        results=session.query(*sel).filter(Meas.Date >= st).filter(Meas.Date<=ed).all()
    else:
        results=session.query(*sel).filter(Meas.Date >= st).all()

    temps=[]
    for ress in results:
        dicti={}
        dicti['Tmin']=ress[1]
        dicti['Tavg']=ress[0]
        dicti['Tmax']=ress[2]
        temps.append(dicti)
    return jsonify(temps)
    # Create a dictionary from the row data and append to a list of all_passengers
if __name__ == '__main__':
    app.run(debug=True)

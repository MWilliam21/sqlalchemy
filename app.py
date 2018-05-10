import datetime as dt
import numpy as np
import pandas as pd
import datetime as dtx
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
        
    )


@app.route("/api/v1.0/percipitation")
def percipitation():
    results= session.query(Meas).filter(Meas.Date>=last_12).all()
    per=[]
    for re in results:
        dic={}
        dic['Date']=Meas.Prcp
        per.append(dic)
    return jsonify(per)


    # Create a dictionary from the row data and append to a list of all_passengers
if __name__ == '__main__':
    app.run(debug=True)

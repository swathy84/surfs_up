import datetime as dt
import numpy as np 
import pandas as pd 

#import dependencies for SQLALchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import the Flask dependency.
from flask import Flask, jsonify
import app


#set up database engine
#grant access to the SQLite database and query SQlite database file
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into classes
Base = automap_base()

#reflect the tables in the database 
Base.prepare(engine, reflect=True)

#Create a variable for each of the classes (tables) in the database 
Measurement = Base.classes.measurement
Station = Base.classes.station


#Create a session link 
session = Session(engine)

#define Flask application 
#Create a new Flask app instance.
app = Flask(__name__)

#Create Flask routes.
#Define the starting point or root 
@app.route("/")

#Run a Flask app.
#create a function 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#creating the route for precipitation 
@app.route("/api/v1.0/precipitation")


#create a precipitation function 
def precipitation():
    
    #calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    #write a query to get the date and precipitation for the previous year.
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    
    #create a dictionary with the date as the key and the precipitation as the value.
    #To do this, we will "jsonify" Jsonify() is a function that converts the dictionary to a JSON file.
    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#creating the route for stations
@app.route("/api/v1.0/stations")

#create a function for stations
def stations():
    
    #create a query that will allow us to get all of the stations in our database.
    results = session.query(Station.station).all()
    
    #unraveling our results into a one-dimensional array. To do this, we want to use the function np.ravel(), with results.
    #Next, we will convert our unraveled results into a list.
    
    stations = list(np.ravel(results))
    
    return jsonify(stations = stations)


#create the route for temperature 
@app.route("/api/v1.0/tobs")



#create funtion temp_monthy()
def temp_monthly():
    
    #calculate the date one year ago from the last date in the database. 
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    
    
    # query the primary station for all the temperature observations from the previous year.
    results = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= prev_year).all()
    
    #unravel the results into a one-dimensional array and convert that array into a list. Then jsonify the list and return our       results, like this:
    temps = list(np.ravel(results))
    
    #we want to jsonify our temps list, and then return it
    return jsonify(temps = temps)


#add route for statistical analysis -min,max,avg
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


#create a function stats()
#add parameters to our stats()function: a start parameter and an end parameter. For now, set them both to None.

def stats(start =None , end =None):
    
    #create a query to select the minimum, average, and maximum temperatures from our SQLite 
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    #we need to determine the starting and ending date, by using if-not
    if not end: 
        
        #query our database using the list that we just made.
        #asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
        results = session.query(*sel).filter(Measurement.date >= start).all()
        
        
        #we'll unravel the results into a one-dimensional array and convert them to a list. Finally, we will jsonify our results         and return them.
        temps = list(np.ravel(results))
        return jsonify(temps = temps)
    
    results = session.query(*sel).filter(Measurement.date >= start). filter(Measurement.date <= end). all()
    temps = list(np.ravel(results))
    
    return jsonify(temps = temps)




#Import the Flask dependency.
from flask import Flask

#Create a new Flask app instance.
app = Flask(__name__)

#Create Flask routes.
#Define the starting point or root 
@app.route("/")

#Run a Flask app.
#create a function 
def hello_world():
    return "Hello World"
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Imports
from   flask import Flask                     # manage the app
from   sqlalchemy       import create_engine  # used to detect if table exists
from   flask_sqlalchemy import SQLAlchemy     # manage the database
import click                                  # used to load the data
import pandas            as pd                # process pandas

# Invoke Flask magic
app = Flask(__name__)

# App Configuration
app.config['SECRET_KEY'] = 'S_U_perS3crEt_KEY#9999'

# SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB Object = SQLAlchemy interface
db = SQLAlchemy (app)

# Define the storage
class Data(db.Model):

    passengerId  = db.Column(db.Integer,     primary_key=True )
    name         = db.Column(db.String(250), nullable=False   )
    survived     = db.Column(db.Integer,     nullable=False   )
    sex          = db.Column(db.String(10 ), default=None     )
    age          = db.Column(db.Integer,     default=-1       ) 
    fare         = db.Column(db.Float,       default=-1       )

    # Table constructor - called by the custom command 'load_data'
    def __init__(self, passengerId, name, survived, sex, age, fare):
        self.passengerId = passengerId
        self.name        = name
        self.survived    = survived
        self.sex         = sex
        self.age         = age
        self.fare        = fare

    # The string representation of the class
    def __repr__(self):
        return str(self.passengerId) + ' - ' + str(self.name) 

# Define the custom command
@app.cli.command("load-data")
@click.argument("fname")
def load_data(fname):
    ''' Load data from a CSV file '''
    print ('*** Load from file: ' + fname)

    # Build the Dataframe from pandas
    df = pd.read_csv( fname )

    # Iterate and load the data     
    for row in df.itertuples(index=False):

        print ( '************************************************' )

        v_passengerId = row[0]
        v_survived    = row[1]
        v_name        = row[3] 
        v_sex         = row[4] 
        v_age         = row[5] 
        v_fare        = row[9]

        print ( 'PassengerId = ' + str( v_passengerId ) )
        print ( 'Survived    = ' + str( v_survived    ) )
        print ( 'Name        = ' + str( v_name        ) )
        print ( 'Sex         = ' + str( v_sex         ) )   
        print ( 'Age         = ' + str( v_age         ) )
        print ( 'Fare        = ' + str( v_fare        ) )

        # def __init__(self, id, passengerId, name, survived, sex, age, fare):
        obj = Data(v_passengerId, v_name, v_survived, v_sex, v_age, v_fare)
        db.session.add( obj )

    # All good, commit changes
    db.session.commit( )

# Default Route 
@app.route('/')
def hello_world():
    retVal  = 'Hello, the database has ('+str( len(Data.query.all()) )+') rows' 
    retVal += '<br /> See loaded <a href="/data">data</a>.'

    return retVal

# Data Route - Shows the loaded information
@app.route('/data')
def data():

    retVal = 'Rows = ' + str( len(Data.query.all()) ) + '<br />' 

    for row in Data.query.all():
        retVal += '<br />' + str( row.__repr__() )             
    return retVal

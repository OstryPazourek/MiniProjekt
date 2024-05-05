from flask import Flask,render_template, jsonify, request  # Importing the Flask module from the flask package  
app = Flask(__name__)  # Creating an instance of the Flask class  
import sqlite3
from datetime import datetime, timedelta
import random
import os
import json
 

 
numRecords = 10
dbFile = os.path.join(os.getcwd(), 'databaseKur.db')
tableName = 'data'
minTemp = 20.0
maxTemp = 30.0
startDate = '2024-03-17 00:00:00'
period = 300
 
 
conn = sqlite3.connect(dbFile)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);
""")
#cursor.execute("INSERT INTO users (name, password) VALUES ('admin', 'admin')")



createQuery = f"""
CREATE TABLE IF NOT EXISTS {tableName} (
    id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    temp REAL NOT NULL
);
"""
cursor.execute(createQuery)
 
countQuery = f"SELECT COUNT(*) FROM {tableName}"
cursor.execute(countQuery)
count = cursor.fetchone()[0]
 
if count == 0:
    startTime = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
else:
    maxTimestampQuery = f"SELECT MAX(timestamp) FROM {tableName}"
    cursor.execute(maxTimestampQuery)
    maxTimestamp = cursor.fetchone()[0]
    maxTimestampDatetime = datetime.strptime(maxTimestamp, '%Y-%m-%d %H:%M:%S')
    startTime = maxTimestampDatetime + timedelta(seconds=period)
 
for i in range(numRecords):
    timestamp = startTime + timedelta(seconds=i*period)
    temperature = random.uniform(minTemp, maxTemp)
    insertQuery = f"INSERT INTO {tableName} (timestamp, temp) VALUES (?, ?)"
    cursor.execute(insertQuery, (timestamp.strftime('%Y-%m-%d %H:%M:%S'), temperature))
 
conn.commit()
conn.close()
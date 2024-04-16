
from flask import Flask,render_template, jsonify, request  # Importing the Flask module from the flask package  
app = Flask(__name__)  # Creating an instance of the Flask class  
import sqlite3
from datetime import datetime, timedelta
import random
import os
import json
 

 
numRecords = 10
dbFile = os.path.join(os.getcwd(), 'database.db')
tableName = 'data'
minTemp = 20.0
maxTemp = 30.0
startDate = '2024-03-17 00:00:00'
period = 300
 
 
conn = sqlite3.connect(dbFile)
cursor = conn.cursor()
 
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

'''''
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute(f"SELECT * FROM {tableName}")
rows = cursor.fetchall()
for row in rows:
    print(row)

def getTemps(connection):
    cursor = connection.cursor()
    cursor.execute()
'''''
def getTemps( json_str = False ):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    db = conn.cursor()

    rows = db.execute('''
    SELECT * from data
    ''').fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON

    return rows


temps = getTemps(json_str = True )
print(temps)
'''
temps = [
    {'id': 1, 'timestamp': '12:00', 'temp': 25},
    {'id': 2, 'timestamp': '12:01', 'temp': 24},
    {"id": 3, "timestamp": "12:02", "temp": 23},
    {"id": 4, "timestamp": "12:03", "temp": 26},
    {"id": 5, "timestamp": "2024-03-17 03:15:00", "temp": 27.653068415058094},
]

print(temps)
'''

Gpocet_vypis=2

@app.route('/api/temp/<int:pocet_vypis>', methods=['POST'])
def post_temp(pocet_vypis):
    global Gpocet_vypis
    Gpocet_vypis = pocet_vypis
    return jsonify(Gpocet_vypis), 200

@app.route('/api/temp/<int:pocet_vypis>', methods=['GET'])
def get_temp(pocet_vypis):
    global Gpocet_vypis
    Gpocet_vypis = pocet_vypis
    return jsonify(Gpocet_vypis), 200

@app.route('/api/temp', methods=['GET'])
def get2_temp():
    global Gpocet_vypis
    return jsonify(Gpocet_vypis), 200

@app.route('/api/temp/<int:mazani>', methods=['DELETE'])
def delete_temp(mazani):
    global temps
   # temps = temps[(mazani):]
    del temps [0:mazani]
    return jsonify(mazani), 200
   
@app.route('/')  # View function for endpoint '/'  
def helloNSI(name="Anonymous"):   
    global Gpocet_vypis
    if Gpocet_vypis > len(temps):
        Gpocet_vypis = len(temps)
    return render_template("base.html",name=name, temps=temps[(len(temps)-Gpocet_vypis):], temp1=temps[-1])  

@app.route('/<name>')  # View function for endpoint '/'  
def helloNSI4(name=""):   
    return render_template("base.html",name=name, temps=temps[(len(temps)-Gpocet_vypis):], temp1=temps[-1])  

@app.route('/login')  # View function for endpoint '/'  
def helloNSI2():  
    return render_template("login.html") 
@app.route('/register')  # View function for endpoint '/'  
def helloNSI3():  
    return render_template("register.html") 
# Starting a web application at 0.0.0.0.0:5000 with debug mode enabled  
if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)







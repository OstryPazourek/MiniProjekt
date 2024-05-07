
from flask import Flask,render_template,redirect, url_for, jsonify, request  # Importing the Flask module from the flask package  
from blueprintAPI import simple_page
import os
app = Flask(__name__)  # Creating an instance of the Flask class  
app.register_blueprint(simple_page)
app.config['RESTARTED'] = True 
dbFile = os.path.join(os.getcwd(), 'databaseKur.db')
from blueprintAPI import getName, getVypis, changeName, changeVypis, get_time_open, get_time_close, insert_timeclose, insert_timeopen, delete_time
import sqlite3
import json
import re
import string
import paho.mqtt.subscribe as subscribe
import json
import threading
import datetime
from datetime import datetime
import plotly.graph_objs as go
import numpy as np
import time
import serial
import sys
import paho.mqtt.publish as publish
import asyncio
import datetime
server = "test.mosquitto.org"
def otevri():
    print("Čas se shoduje, funkce otevri() byla zavolána.")
def zavri():
    print("Čas se shoduje, funkce zavri() byla zavolána.")

"""
def otevri():
    print(f"Oteviram : KURNIK/DVERE do {server}")
    publish.single("KURNIK/DVERE", 1 , hostname=server)
def zavri():
    print(f"Zaviram : KURNIK/DVERE do {server}")
    publish.single("KURNIK/DVERE", 0 , hostname=server)      
"""

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#ahoj
def print_msg(client, userdata, message):
    
    MSG = json.loads(message.payload.decode("utf-8"))
    print("%s : %s" % (message.topic, MSG))


chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
#key = chars.copy()
#random.shuffle(key)
key = ['a', 's', '$', 'P', ';', "'", 'D', '2', 'q', 'f', 'd', '5', '[', 'z', '(', 'G', '!', 'p', 'i', 'Y', '@', '?', ':', '}', 'I', ' ', 'B', 'Q', '>', '8', '^', 'b', ']', '{', ')', 'U', '0', 'm', '1', 'S', '`', 'v', '#', 'N', 'R', 'o', 'J', '&', 'l', '=', 'y', '.', 'T', '~', 'K', '-', '6', 'M', 'O', 't', 'A', 'k', 'w', '+', 'C', '*', '<', '9', 'h', '%', 'H', ',', 'x', 'W', '|', 'c', '7', 'r', 'E', '\\', 'F', 'u', 'X', 'Z', 'n', '3', 'e', '"', '/', '4', 'g', 'V', 'L', '_', 'j']




#print (ciphertext)
def deleteTemps(mazani):
    conn = sqlite3.connect("databaseKur.db")
    cur = conn.cursor()
    cur.execute(f"Delete from data WHERE id IN (SELECT id FROM data limit '{mazani}')")
    conn.commit()
    cur.close()
    return 0

def getTemps( json_str = False ):
    conn = sqlite3.connect("databaseKur.db")
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    db = conn.cursor()

    rows = db.execute('''
    SELECT * from data
    ''').fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.loads(json.dumps( [dict(ix) for ix in rows] )) #CREATE JSON
    return rows

def getUsers( json_str = False ):
    conn = sqlite3.connect("databaseKur.db")
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    db = conn.cursor()

    rows = db.execute('''
    SELECT * from users
    ''').fetchall() 

    conn.commit()
    conn.close()

    if json_str:
        return json.loads(json.dumps( [dict(ix) for ix in rows] )) #CREATE JSON
    return rows
# codování ze stránky https://stackoverflow.com/questions/73532164/proper-data-encryption-with-a-user-set-password-in-python3
def addUsers( name, password ):
    cipher_text = ""
    for letter in password:
        index = chars.index(letter)
        cipher_text += key[index]
    #encrypted = encrypted.decode("utf-8")
    conn = sqlite3.connect("databaseKur.db")
    db = conn.cursor()
    db.execute(f'''
    INSERT INTO users(name, password) VALUES ('{name}', '{cipher_text}');
    ''').fetchall() 

    conn.commit()
    conn.close()

    return 0


global temps
Gpocet_vypis=2
print(getName())
name = getName()
conectionDATA = "MQTT"




@app.route('/')  # View function for endpoint '/'  
def home():
    reset = app.config['RESTARTED']
    app.config['RESTARTED'] = False
    global Gpocet_vypis
    Gpocet_vypis = getVypis()
    global temps
    global name
    temps = getTemps(json_str = True )

    Grafdates = [datetime.datetime.strptime(d['timestamp'], '%Y-%m-%d %H:%M:%S') for d in temps]
    Graftemps = [d['temp'] for d in temps[-30240:]]
    graph = go.Figure(data=go.Scatter(x=Grafdates, y=Graftemps, mode='lines+markers'))

    graph.update_layout(
        title='Graf teploty',
        xaxis_title='Datum',
        yaxis_title='Teplota (°C)',
        xaxis=dict(
            tickformat='%Y-%m-%d %H:%M:%S',
            tickangle=45
        ),
        yaxis=dict(
        range=[-5, 40]  # Nastavení rozsahu osy Y od 15 do 30 stupňů Celsius
    )
    )

    graph_html = graph.to_html(full_html=False, default_width='100%', default_height='auto')

    delka = len(temps)    
    if Gpocet_vypis > delka:
        #Gpocet_vypis = delka
        changeVypis(delka)
    poradi = -1    
    if delka<1:
        temps = [{'id': 1, 'timestamp': '--', 'temp': 0}]
        poradi = 0
        #Gpocet_vypis=1
        changeVypis(1)
    print(Gpocet_vypis)
    open_time=get_time_open()
    close_time=get_time_close()
    print(open_time)
    print(close_time)
    casy = [d['timestamp'] for d in temps]
    teploty = [d['temp'] for d in temps]
    return render_template("base.html",graph_html=graph_html,name=getName(), temps=temps[(delka-getVypis()):], temp1=temps[poradi],reset=reset,open_time=open_time,close_time=close_time, casy=casy, teploty=teploty)  

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    users = getUsers(json_str = True )
    global key
    error = None
    if request.method == 'POST':
        for user in users:
            plain_text = ""
            for letter in user['password']:
                index = key.index(letter)
                plain_text += chars[index]

            if request.form['username'] == user['name'] and request.form['password'] == plain_text:
                #name = user['name']
                changeName(user['name'])
                return redirect(url_for('home'))               
            
        error = 'Chybné přihlašovací údaje. Zkuste to Znova.'
    return render_template('login.html', error=error)

@app.route("/logout/", methods = ["GET", "POST"])
def logout():
    #global name
    #name = "Anonymous"
   
    changeName()
    return redirect(url_for("home"))
@app.route("/MQTT/", methods = ["GET", "POST"])
def mqtt():
    global conectionDATA  
    conectionDATA = "MQTT"
    print (conectionDATA)
    mqtt_thread = threading.Thread(target=start_mqtt_subscriber)
    mqtt_thread.start()  # Spustí MQTT v samostatném vlákně
    return redirect(url_for("home"))
@app.route("/serial/", methods = ["GET", "POST"])
def serial():
    global conectionDATA  
    conectionDATA = "serial"
    print (conectionDATA)
    mqtt_thread = threading.Thread(target=start_serial_comunation)
    mqtt_thread.start()
    return redirect(url_for("home"))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE name = '{username}'")
        account = cursor.fetchone()
        if account:
            msg = 'Uživatel již existuje!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Uživatelské jméno musí být jen písmena a číslice'
        elif not username or not password:
            msg = 'Prosím vyplňte všechy položky!'
        else:
            name = getName()
            addUsers( name = username, password = password )
            msg = 'Úspěšně jste se zaregistroval!'
    elif request.method == 'POST':
        msg = 'Prosím vyplňte všechy položky!'
    return render_template('register.html', msg = msg)   
  
def insert_temperature(temp, timestamp):
    conn = sqlite3.connect("databaseKur.db")  # Připojení k databázi
    cursor = conn.cursor()
    cursor.execute('INSERT INTO data (timestamp, temp) VALUES (?, ?)', (timestamp, temp))
    conn.commit()  # Commit změn
    conn.close()  # Uzavření spojení s databází
    print(f"Inserted into database: Temperature = {temp}, Timestamp = {timestamp}")

def print_msg(client, userdata, message):
    if conectionDATA == "MQTT":
        data = json.loads(message.payload.decode("utf-8"))
        temperature = data['Temp']  # Získání teploty z MQTT zprávy
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Aktuální čas
        insert_temperature(temperature, timestamp)  # Vložení teploty a času do databáze
    

def start_mqtt_subscriber():
    subscribe.callback(print_msg, "KURNIK/DHT11", hostname=server)
 
def start_serial_comunation():
    while True:
        if conectionDATA == "serial":
            try:
                import serial
                ser = serial.Serial('COM5', 115200)
                ser.flushInput()
                while conectionDATA == "serial":
                    serDecode = ser.readline().decode()
                    print(serDecode)
                    temperature = json.loads(serDecode)
                    print(temperature["Temp"])
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Aktuální čas
                    insert_temperature(temperature["Temp"], timestamp)
            except Exception as e:
                print(e)
                print("unable to open COM port")
                time.sleep(2)
                #exit(-1)
def timeChecker():
    import paho.mqtt.publish as publish
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        print(f"cas ted {now} a csa open { get_time_open()}, a cas close { get_time_close()}")
        if now == get_time_open():
            print("cas se shoduje, funkce otevri() byla zavolana.") #open()
            publish.single("KURNIK/DVERE", 1 , hostname=server)
        if now == get_time_close():
            print("Cas se shoduje, funkce zavri() byla zavolana.") #zavri() 
            publish.single("KURNIK/DVERE", 0 , hostname=server) 
        time.sleep(60)

if __name__ == "__main__":
 
    time_thread = threading.Thread(target=timeChecker)
    time_thread.start() 
    #mqtt_thread = threading.Thread(target=start_serial_comunation)
    #mqtt_thread.start()
    #subscribe.callback(print_msg, "KURNIK/DHT11", hostname="test.mosquitto.org") 
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    # Starting a web application at 0.0.0.0.0:5000 with debug mode enabled
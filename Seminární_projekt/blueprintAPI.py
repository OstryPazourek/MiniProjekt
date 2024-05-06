from flask import Blueprint, render_template, abort, jsonify,redirect, url_for
from jinja2 import TemplateNotFound
import sqlite3
import json
from datetime import datetime
import os
#from main import put_Gpocet_vypis
dbFile = os.path.join(os.getcwd(), 'databaseKur.db')
conn = sqlite3.connect(dbFile)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS open (
    id INTEGER PRIMARY KEY,
    timeopen TEXT NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS close (
    id INTEGER PRIMARY KEY,
    timeclose TEXT NOT NULL
);
""")
#cursor.execute("INSERT INTO users (name, password) VALUES ('admin', 'admin')")



createQuery = f"""
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    temp REAL NOT NULL
);
"""
cursor.execute(createQuery)
name = "Anonymous"
Gpocet_vypis = 2
open = None
close = None

def deleteTemps(mazani):
    conn = sqlite3.connect("databaseKur.db")
    cur = conn.cursor()
    cur.execute(f"Delete from data WHERE id IN (SELECT id FROM data limit '{mazani}')")
    conn.commit()
    cur.close()
    return 0

def getName():
    global name
    return name

def changeName(NewName="Anonymous"):
    global name
    name = NewName
    return name

def getVypis():
    global Gpocet_vypis
    return Gpocet_vypis

def changeVypis(vypis=2):
    global Gpocet_vypis
    Gpocet_vypis = vypis
    return Gpocet_vypis

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
        return json.loads(json.dumps( [dict(ix) for ix in rows] )) #CREATE JSON
    return rows

def insert_timeopen(open_time):
    #open_time = '10:00'
    print(type(open_time)) 
    conn = sqlite3.connect("databaseKur.db")  # Připojení k databázi 
    cursor = conn.cursor()
    cursor.execute('DELETE FROM open')
    conn.commit() 
    conn.close() 
    conn = sqlite3.connect("databaseKur.db")  # Připojení k databázi 
    cursor = conn.cursor() 
    cursor.execute('INSERT INTO open (timeopen) VALUES (?)', (open_time,))
    conn.commit()  
    conn.close() 
    print(f"Inserted into database:  cas otevreni = {open_time}")


def insert_timeclose(close_time):
    #close_time = '18:00'
    print(type(close_time)) 
    conn = sqlite3.connect("databaseKur.db")  # Připojení k databázi 
    cursor = conn.cursor()
    cursor.execute('DELETE FROM close')
    conn.commit() 
    conn.close() 
    conn2 = sqlite3.connect("databaseKur.db")  # Připojení k databázi 
    cursor = conn2.cursor() 
    cursor.execute('INSERT INTO close (timeclose) VALUES (?)', (close_time,))
    conn2.commit()  
    conn2.close() 
    print(f"Inserted into database:  cas zavreni = {close_time}")

def delete_time(): 
    conn = sqlite3.connect("databaseKur.db")  # Připojení k databázi 
    cursor = conn.cursor()
    cursor.execute('DELETE FROM close')
    cursor.execute('DELETE FROM open')
    conn.commit() 
    conn.close() 
    print("Mazu casi otevirani a zavirani z kurniku")


def get_time_open():
    global open
    conn = sqlite3.connect("databaseKur.db")  # Připojení k databázi
    cursor = conn.cursor()
    cursor.execute("SELECT timeopen FROM open")
    hodnota = cursor.fetchone()
    if hodnota is not None:
     # Pokud byla hodnota nalezena, zapište ji do proměnné
        open = hodnota[0]
    else:
        open = None
    conn.commit()  
    conn.close() 
    print(f"Take out of database:  cas otevreni = {open}")
    return open
    
def get_time_close():
    global close
    conn = sqlite3.connect("databaseKur.db")  # Připojení k databázi
    cursor = conn.cursor()
    cursor.execute("SELECT timeclose FROM close")
    hodnota = cursor.fetchone()
    if hodnota is not None:
     # Pokud byla hodnota nalezena, zapište ji do proměnné
        close = hodnota[0]
    else:
        close = None
    conn.commit()  
    conn.close() 
    print(f"Take out of database:  cas zavreni = {close}")
    return close
open = get_time_open()
close = get_time_close()
print(f"Cas otevreni je = {open}")
print(f"Cas zavreni je = {close}")

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')


@simple_page.route('/api/temps', methods=['GET'])
def get3_temp():
    temps = getTemps(json_str = True )
    return jsonify(temps), 200

@simple_page.route('/api/temp/<int:pocet_vypis>', methods=['POST'])
def post_temp(pocet_vypis):
    global Gpocet_vypis
    Gpocet_vypis=pocet_vypis
   # Gpocet_vypis = pocet_vypis
    print(Gpocet_vypis)
    return jsonify(Gpocet_vypis), 200

@simple_page.route('/api/open/<string:POSTopen>', methods=['GET'])
def post_open(POSTopen):
    time_obj = datetime.strptime(POSTopen, '%H:%M')
    global open
    open = (time_obj.strftime('%H:%M'))
    insert_timeopen(open)
    #print(type(time_obj.strftime('%H:%M'))) 
    #print(time_obj.strftime('%H%M'))
    return jsonify(open), 200

@simple_page.route('/api/delete_time/', methods=["GET", "POST"])
def mazani_casu():
    delete_time()
    return redirect(url_for("home"))

@simple_page.route('/api/close/<string:POSTclose>', methods=['GET'])
def post_close(POSTclose):
    time_obj = datetime.strptime(POSTclose, '%H:%M')
    global close
    close = (time_obj.strftime('%H:%M'))
    insert_timeclose(close)
    #print(type(time_obj.strftime('%H:%M'))) 
    #print(time_obj.strftime('%H%M'))
    return jsonify(close), 200

   

@simple_page.route('/api/temp/<int:pocet_vypis>', methods=['GET'])
def get_temp(pocet_vypis):
    global Gpocet_vypis
    Gpocet_vypis = pocet_vypis
    print(Gpocet_vypis)
    return jsonify(Gpocet_vypis), 200

@simple_page.route('/api/temp', methods=['GET'])
def get2_temp():
    global Gpocet_vypis
    return jsonify(Gpocet_vypis), 200

@simple_page.route('/api/temp/<int:mazani>', methods=['DELETE'])
def delete_temp(mazani):
   
   # temps = temps[(mazani):]
    
    deleteTemps(mazani)
    #temps = getTemps(json_str = True )
    #del temps [0:mazani]
    return jsonify(mazani), 200




def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)
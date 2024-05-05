from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
import sqlite3
import json
#from main import put_Gpocet_vypis

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


name = "Anonymous"
Gpocet_vypis = 2


simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

'''
@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
'''


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
from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
import sqlite3
import json
from main import put_Gpocet_vypis

def deleteTemps(mazani):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"Delete from data WHERE id IN (SELECT id FROM data limit '{mazani}')")
    conn.commit()
    cur.close()
    return 0



simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

'''
@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
'''
@simple_page.route('/api/temp/<int:pocet_vypis>', methods=['POST'])
def post_temp(pocet_vypis):
    #put_Gpocet_vypis(pocet_vypis)
   # Gpocet_vypis = pocet_vypis
    return jsonify(Gpocet_vypis), 200

@simple_page.route('/api/temp/<int:pocet_vypis>', methods=['GET'])
def get_temp(pocet_vypis):
    global Gpocet_vypis
    Gpocet_vypis = pocet_vypis
    return jsonify(Gpocet_vypis), 200

@simple_page.route('/api/temp', methods=['GET'])
def get2_temp():
    global Gpocet_vypis
    return jsonify(Gpocet_vypis), 200

@simple_page.route('/api/temp/<int:mazani>', methods=['DELETE'])
def delete_temp(mazani):
    global temps
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
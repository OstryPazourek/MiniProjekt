
from flask import Flask,render_template,redirect, url_for, jsonify, request  # Importing the Flask module from the flask package  
app = Flask(__name__)  # Creating an instance of the Flask class  
import sqlite3
import json
import re
import string
import random
#from hashlib import sha256
#from cryptography.fernet import Fernet
#import base64
#from Crypto.Cipher import AES #pip3 install pycryptodome ukazka kodu https://stackoverflow.com/questions/15956952/how-do-i-decrypt-using-hashlib-in-python


chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
#key = chars.copy()
#random.shuffle(key)
key = ['a', 's', '$', 'P', ';', "'", 'D', '2', 'q', 'f', 'd', '5', '[', 'z', '(', 'G', '!', 'p', 'i', 'Y', '@', '?', ':', '}', 'I', ' ', 'B', 'Q', '>', '8', '^', 'b', ']', '{', ')', 'U', '0', 'm', '1', 'S', '`', 'v', '#', 'N', 'R', 'o', 'J', '&', 'l', '=', 'y', '.', 'T', '~', 'K', '-', '6', 'M', 'O', 't', 'A', 'k', 'w', '+', 'C', '*', '<', '9', 'h', '%', 'H', ',', 'x', 'W', '|', 'c', '7', 'r', 'E', '\\', 'F', 'u', 'X', 'Z', 'n', '3', 'e', '"', '/', '4', 'g', 'V', 'L', '_', 'j']

'''
entered_pw = "secretpw"
key = base64.b64encode(f"{entered_pw:<32}".encode("utf-8"))
encryptor = Fernet(key=key)
encrypted = encryptor.encrypt(
    "my super secret data with a password".encode("utf-8")
)
encrypted = encrypted.decode("utf-8")
print(encrypted)
#encrypted = encrypted.encode("utf-8")
print(encrypted)

print(encryptor.decrypt(encrypted).decode("utf-8"))

'''
#print (ciphertext)
def deleteTemps(mazani):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"Delete from data WHERE id IN (SELECT id FROM data limit '{mazani}')")
    conn.commit()
    cur.close()
    return 0

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

def getUsers( json_str = False ):
    conn = sqlite3.connect("database.db")
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
    conn = sqlite3.connect("database.db")
   
    db = conn.cursor()

    db.execute(f'''
    INSERT INTO users(name, password) VALUES ('{name}', '{cipher_text}');
    ''').fetchall() 

    conn.commit()
    conn.close()

    return 0
#temps = getTemps(json_str = True )

#print(temps)
'''
temps = [
    {'id': 1, 'timestamp': '12:00', 'temp': 25},
    {'id': 2, 'timestamp': '12:01', 'temp': 24},
    {"id": 3, "timestamp": "12:02", "temp": 23},
    {"id": 4, "timestamp": "12:03", "temp": 26},
    {"id": 5, "timestamp": "2024-03-17 03:15:00", "temp": 27.653068415058094},
]

print(temps)

users = [
    {'id': 1, 'name': 'admin', 'password': 'admin'},
    {'id': 2, 'name': 'user', 'password': 'user'},  
]
'''




global temps
name = "Anonymous"
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
    
    deleteTemps(mazani)
    #temps = getTemps(json_str = True )
    #del temps [0:mazani]
    return jsonify(mazani), 200
   
@app.route('/')  # View function for endpoint '/'  
def home():   
    global Gpocet_vypis
    global temps
    global name
    temps = getTemps(json_str = True )
    delka = len(temps)
    if Gpocet_vypis > delka:
        Gpocet_vypis = delka
    poradi = -1    
    if delka<1:
        poradi = 0
    return render_template("base.html",name=name, temps=temps[(delka-Gpocet_vypis):], temp1=temps[poradi])  

@app.route('/<name>')  # View function for endpoint '/'  
def helloNSI4(name=""):   
    return render_template("base.html",name=name, temps=temps[(len(temps)-Gpocet_vypis):], temp1=temps[-1])  
'''
@app.route('/login')  # View function for endpoint '/'  
def helloNSI2():  
    return render_template("login.html") 
'''
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    users = getUsers(json_str = True )
    global name
    global key
    error = None
    #uzivatel = 'admin'
    #heslo = 'admin'
    if request.method == 'POST':
        for user in users:
            
            #encryptor = Fernet(key=key)
            #encrypted =  user['password']

           #plaintext = cipher.decrypt(user['password'])
            #encrypted = user['password'].encode("utf-8")           
            #heslo = encryptor.decrypt(encrypted).decode("utf-8")
            #heslo = encryptor.decrypt(user['password'])
            #entered_pw = "secretpw"
            #key = base64.b64encode(f"{entered_pw:<32}".encode("utf-8"))
            #encryptor = Fernet(key=key)
            #heslo = encryptor.decrypt(user['password']).decode("utf-8")
            plain_text = ""

            for letter in user['password']:
                index = key.index(letter)
                plain_text += chars[index]

            if request.form['username'] == user['name'] and request.form['password'] == plain_text:
                name = user['name']
                return redirect(url_for('home'))               
            
        error = 'Chybné přihlašovací údaje. Zkuste to Znova.'
    return render_template('login.html', error=error)

@app.route("/logout/", methods = ["GET", "POST"])
def logout():
    global name
    name = "Anonymous"
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
            addUsers( name = username, password = password )
            msg = 'Úspěšně jste se zaregistroval!'
    elif request.method == 'POST':
        msg = 'Prosím vyplňte všechy položky!'
    return render_template('register.html', msg = msg)     
# Starting a web application at 0.0.0.0.0:5000 with debug mode enabled  
if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)







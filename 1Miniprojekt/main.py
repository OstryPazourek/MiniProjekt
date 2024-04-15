
from flask import Flask,render_template, jsonify, request  # Importing the Flask module from the flask package  
 
app = Flask(__name__)  # Creating an instance of the Flask class  
 

temps = [
    {"id": 1, "timestamp": "12:00", "temp": 25},
    {"id": 2, "timestamp": "12:01", "temp": 24},
    {"id": 3, "timestamp": "12:02", "temp": 23},
    {"id": 4, "timestamp": "12:03", "temp": 26},
    {"id": 5, "timestamp": "12:04", "temp": 25},
]

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







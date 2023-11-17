from flask import Flask
from flask import jsonify
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to hey cathay"
    
if __name__=="__main__":
    app.run(debug=True)
import time
import os
from flask import request

from flask import Flask

app = Flask(__name__)

@app.route("/log", methods=['POST'])
def main():
    log = request.json.get("log")
    with open("data/storagelogs.txt", "a") as myfile:
        return myfile.write(log)

    
    

@app.route("/log",methods=['GET'])
def get_log():
    with open("data/storagelogs.txt", "a") as myfile:
        pass
    with open("data/storagelogs.txt","r") as myfile:
        return myfile.read()
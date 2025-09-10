import psutil
import time
import os
import requests
from flask import Response
from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/status")
def main():
    # Get current timestamp
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Get system uptime
    boot_time = psutil.boot_time()   # seconds since epoch
    uptime_seconds = time.time() - boot_time
    uptime_hours = uptime_seconds / 3600

    # Get free disk space in root
    disk_usage = psutil.disk_usage(os.sep)  # root ("/" on Linux, "\" on Windows)
    free_disk_mb = disk_usage.free / (1024 * 1024)

    logstring = f"{timestamp} 1: uptime {uptime_hours:.2f} hours, free disk in root: {free_disk_mb:.2f} MBytes"+ "\n"
    with open("data/vstorage", "a") as myfile:
        myfile.write(logstring)


    url = 'http://storage:8198/log'
    myobj = {'log': logstring}

    requests.post(url, json = myobj)

    url = 'http://service2:8197/status'
    result = requests.get(url)
    logstring+=  result.text
    return Response(logstring, mimetype="text/plain")

@app.route("/log")
def get_log():
    result = requests.get('http://storage:8198/log')
    return Response(result.text, mimetype="text/plain")

@app.route("/test")
def test():
    return "Service1 is up and running"
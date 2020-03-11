from flask import Flask, jsonify, request, abort
import requests
import time
import sys

app = Flask(__name__)

port = 8084
scraper_host="scraper"
scraper_port=8083


@app.route("/healthcheck")
def healthcheck():
    check = {
        "status": "OK2",
        "port": port
    }
    return jsonify(check)

@app.route("/")
def index():
    return "This is the main index route. testing this"


def sync_predictions_db():
    try:
        result = requests.get("http://" + scraper_host + ":" + str(scraper_port) + "/predictions/db")
        if result.status_code != 200:
            raise Exception("Request status code is not 200")
    except Exception as e:
        print(e)

def sync_predictions_redis():
    try:
        result = requests.get("http://" + scraper_host + ":" + str(scraper_port) + "/predictions/redis")
        if result.status_code != 200:
            raise Exception("Request status code is not 200")
    except Exception as e:
        print(e)

def sync_standings_db():
    try:
        result = requests.get("http://" + scraper_host + ":" + str(scraper_port) + "/standings/db")
        if result.status_code != 200:
            raise Exception("Request status code is not 200")
    except Exception as e:
        print(e)

def sync_standings_redis():
    try:
        result = requests.get("http://" + scraper_host + ":" + str(scraper_port) + "/standings/redis")
        if result.status_code != 200:
            raise Exception("Request status code is not 200")
    except Exception as e:
        print(e)

def sync_head2heads_db():
    try:
        result = requests.get("http://" + scraper_host + ":" + str(scraper_port) + "/head2head/db")
        if result.status_code != 200:
            raise Exception("Request status code is not 200")
    except Exception as e:
        print(e)

def sync_head2heads_redis():
    try:
        result = requests.get("http://" + scraper_host + ":" + str(scraper_port) + "/head2head/redis")
        if result.status_code != 200:
            raise Exception("Request status code is not 200")
    except Exception as e:
        print(e)




if __name__ == "__main__":
    count_predictions = 0
    count_standings = 0

    while True:

        start = time.time()
        sync_standings_db()
        done = time.time()
        elapsed = done - start
        count_standings += 1
        print("Sync STANDINGS DB completed: " + str(elapsed) + " seconds")
        sys.stdout.flush()

        start = time.time()
        sync_standings_redis()
        done = time.time()
        elapsed = done - start
        count_standings += 1
        print("Sync STANDINGS REDIS completed: " + str(elapsed) + " seconds")
        sys.stdout.flush()

        start = time.time()
        sync_predictions_db()
        done = time.time()
        elapsed = done - start
        count_predictions += 1
        print("Sync PREDICTIONS DB completed: " + str(elapsed) + " seconds")
        sys.stdout.flush()

        start = time.time()
        sync_predictions_redis()
        done = time.time()
        elapsed = done - start
        count_predictions += 1
        print("Sync PREDICTIONS REDIS completed: " + str(elapsed) + " seconds")
        sys.stdout.flush()

        start = time.time()
        sync_head2heads_db()
        done = time.time()
        elapsed = done - start
        count_predictions += 1
        print("Sync HEAD2HEAD DB completed: " + str(elapsed) + " seconds")
        sys.stdout.flush()

        start = time.time()
        sync_head2heads_redis()
        done = time.time()
        elapsed = done - start
        count_predictions += 1
        print("Sync HEAD2HEAD REDIS completed: " + str(elapsed) + " seconds")
        sys.stdout.flush()

        time.sleep(1 * 60)


    app.run(host="0.0.0.0", port=port)
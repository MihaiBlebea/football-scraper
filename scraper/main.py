from flask import Flask, jsonify, request, abort
import requests
from datetime import date, timedelta
import sys

import database as db
import redis_client

app = Flask(__name__)

port = 8083
token = "36bb0160f14b1bcaa60fd41f7e98cb37fb9d2b01031d293c985d2861946b2e3f"
league = 262
base_url = "https://apiv2.apifootball.com/"

@app.route("/healthcheck")
def healthcheck():
    check = {
        "status": "OK",
        "port": port
    }
    return jsonify(check)


@app.route("/standings/db", methods = ["GET"])
def get_standings_db():
    url = base_url + "?action=get_standings&league_id=" + str(league) + "&APIkey=" + token

    res = requests.get(url)
    data = res.json()

    for raw in data:
        standing = {
            "country_name": raw["country_name"],
            "league_id": raw["league_id"],
            "league_name": raw["league_name"],
            "team_id": raw["team_id"],
            "team_name": raw["team_name"],
            "position": raw["overall_league_position"],
            "played": raw["overall_league_payed"],
            "league_W": raw["overall_league_W"],
            "league_D": raw["overall_league_D"],
            "league_L": raw["overall_league_L"],
            "league_GF": raw["overall_league_GF"],
            "league_GA": raw["overall_league_GA"],
            "league_PTS": raw["overall_league_PTS"],
            "team_badge": raw["team_badge"]
        }

        db.store_standing(standing)

    return jsonify(data)

@app.route("/predictions/db", methods = ["GET"])
def get_predictions_db():
    url = base_url + "?action=get_predictions&from=2020-03-13&to=2020-03-16&league_id=" + str(league) + "&APIkey=" + token

    res = requests.get(url)
    data = res.json()

    for raw in data:
        prediction = {
            "match_id": raw["match_id"],
            "country_id": raw["country_id"],
            "country_name": raw["country_name"],
            "league_id": raw["league_id"],
            "league_name": raw["league_name"],
            "match_date": raw["match_date"],
            "match_status": raw["match_status"],
            "match_time": raw["match_time"],
            "match_live": raw["match_live"],
            "match_hometeam_id": raw["match_hometeam_id"],
            "match_hometeam_name": raw["match_hometeam_name"],
            "match_hometeam_score": raw["match_hometeam_score"],
            "match_awayteam_id": raw["match_awayteam_id"],
            "match_awayteam_name": raw["match_awayteam_name"],
            "match_awayteam_score": raw["match_awayteam_score"],
            "match_hometeam_halftime_score": raw["match_hometeam_halftime_score"],
            "match_awayteam_halftime_score": raw["match_awayteam_halftime_score"],
            "match_hometeam_system": raw["match_hometeam_system"],
            "match_awayteam_system": raw["match_awayteam_system"],
            "prob_HW": raw["prob_HW"],
            "prob_D": raw["prob_D"],
            "prob_AW": raw["prob_AW"],
            "prob_HW_D": raw["prob_HW_D"],
            "prob_AW_D": raw["prob_AW_D"],
            "prob_HW_AW": raw["prob_HW_AW"]
        }

        db.store_prediction(prediction)

    return jsonify(data)

@app.route("/standings/redis", methods = ["GET"])
def standings_redis():
    standings = db.select_all_standings()
    for standing in standings:
        redis_client.store_standing(standing)
    return jsonify({ "result": True })

@app.route("/predictions/redis", methods = ["GET"])
def predictions_redis():
    predictions = db.select_all_predictions()
    for prediction in predictions:
        redis_client.store_prediction(prediction)
    return jsonify({ "result": True })

@app.route("/head2head/db", methods = ["GET"])
def head2head_db():
    predictions = db.select_all_predictions()
    for prediction in predictions:
        match_url = base_url + "?action=get_H2H&firstTeam=" + prediction["match_hometeam_name"] + "&secondTeam=" + prediction["match_awayteam_name"] + "&APIkey=" + token
        
        match_res = requests.get(match_url)
        match_data = match_res.json()

        match_list = match_data["firstTeam_VS_secondTeam"] + match_data["firstTeam_lastResults"] + match_data["secondTeam_lastResults"]
        for match_raw in match_list:

            match = {
                "match_id": match_raw["match_id"],
                "country_id": match_raw["country_id"],
                "match_date": match_raw["match_date"],
                "match_hometeam_id": match_raw["match_hometeam_id"],
                "match_hometeam_name": match_raw["match_hometeam_name"],
                "match_awayteam_id": match_raw["match_awayteam_id"],
                "match_awayteam_name": match_raw["match_awayteam_name"],
                "match_hometeam_score": match_raw["match_hometeam_score"],
                "match_awayteam_score": match_raw["match_awayteam_score"],
                "match_hometeam_halftime_score": match_raw["match_hometeam_halftime_score"],
                "match_awayteam_halftime_score": match_raw["match_awayteam_halftime_score"]
            }

            if db.valid_head2head(match) == True:
                db.store_head2head(match)

    return jsonify({ "result": True })

@app.route("/head2head/redis", methods = ["GET"])
def head2head_redis():
    head2heads = db.select_all_head2heads()
    for head2head in head2heads:
        redis_client.store_head2head(head2head)
    return jsonify({ "result": True })


if __name__ == "__main__":
    db.create_standings_table()
    db.create_predictions_table()
    db.create_head2heads_table()

    app.run(host="0.0.0.0", port=port)
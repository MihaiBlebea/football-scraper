from flask import Flask, render_template, jsonify, request
import redis_client
import sys

app = Flask(__name__)
port = 8081


@app.route("/")
def index():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route("/predictions", methods=["GET"])
def predictions():
    predictions = redis_client.fetch_predictions()
    return jsonify(predictions)

@app.route("/standings", methods=["GET"])
def standings():
    standings = redis_client.fetch_standings()
    return jsonify(standings)

@app.route("/head2head", methods=["GET"])
def head2head():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    head2heads = redis_client.fetch_head2heads()

    team1_matches = []
    team2_matches = []

    team1_form = []
    team2_form = []

    separator = "-"

    for match in head2heads:
        if len(team1_matches) < 5:
            if match["match_hometeam_name"] == team1:
                team1_matches.append(match)
                if match["match_hometeam_score"] > match["match_awayteam_score"]:
                    team1_form.append("W")
                elif match["match_hometeam_score"] < match["match_awayteam_score"]:
                    team1_form.append("L")
                else:
                    team1_form.append("D")

            if match["match_awayteam_name"] == team1:
                team1_matches.append(match)
                if match["match_hometeam_score"] < match["match_awayteam_score"]:
                    team1_form.append("W")
                elif match["match_hometeam_score"] > match["match_awayteam_score"]:
                    team1_form.append("L")
                else:
                    team1_form.append("D")

        if len(team2_matches) < 5:
            if match["match_hometeam_name"] == team2:
                team2_matches.append(match)
                if match["match_hometeam_score"] > match["match_awayteam_score"]:
                    team2_form.append("W")
                elif match["match_hometeam_score"] < match["match_awayteam_score"]:
                    team2_form.append("L")
                else:
                    team2_form.append("D")

            if match["match_awayteam_name"] == team2:
                team2_matches.append(match)
                if match["match_hometeam_score"] < match["match_awayteam_score"]:
                    team2_form.append("W")
                elif match["match_hometeam_score"] > match["match_awayteam_score"]:
                    team2_form.append("L")
                else:
                    team2_form.append("D")

    return jsonify({
        team1: {
            "matches": team1_matches,
            "form": separator.join(team1_form)
        },
        team2: {
            "matches": team2_matches,
            "form": separator.join(team2_form)
        }
    })
    

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=port)
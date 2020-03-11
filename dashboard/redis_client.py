import redis
from operator import itemgetter, attrgetter


def connect():
    r = redis.Redis(host='redis', port=6379, db=0)
    return r

def fetch_matches():
    r = connect()

    # Set a hash
    # HSET match:id1 hometeam "Ac Milan"
    # HSET match:id1 awayteam "Juventus"

    # HSET match:id2 hometeam "Dinamo"
    # HSET match:id2 awayteam "Steaua"

    # Add the key in a list
    # RPUSH matches match:id1 match:id2

    # Get all matches in the list
    # LRANGE matches 0 -1

    # keys = r.lrange("matches", 0, -1)
    keys = r.smembers("matches")

    matches = []

    for key in keys:
        res = r.hgetall(key)
        res = { k.decode("utf-8") : v.decode("utf-8") for k, v in res.items() }
        match = {
            "home_team_name": res["home:name"],
            "away_team_name": res["away:name"],
            "hometeam_halftime_score": int(res["home:score:halftime"]),
            "awayteam_halftime_score": int(res["away:score:halftime"]),
            "hometeam_score": int(res["home:score:final"]),
            "awayteam_score": int(res["away:score:final"]),
            "match_date": res["play:date"],
            "match_time": res["play:time"],
            "match_live": int(res["play:live"]),
            "league_id": res["league:id"],
            "league_name": res["league:name"],
            "country_id": res["country:id"],
            "country_name": res["country:name"]
        }
        matches.append(match)

    matches = sorted(matches, key=itemgetter("match_date", "match_time"), reverse=False)
    return matches

def fetch_predictions():
    r = connect()
    keys = r.smembers("predictions")
    predictions = []

    for key in keys:
        res = r.hgetall(key)
        prediction = { k.decode("utf-8").replace(":", "_") : v.decode("utf-8") for k, v in res.items() }
        predictions.append(prediction)

    # matches = sorted(matches, key=itemgetter("match_date", "match_time"), reverse=False)
    return predictions

def fetch_standings():
    r = connect()
    keys = r.smembers("standings")
    standings = []

    for key in keys:
        res = r.hgetall(key)
        standing = { k.decode("utf-8").replace(":", "_") : v.decode("utf-8") for k, v in res.items() }
        standings.append(standing)

    # standings = sorted(standings, key=itemgetter("team_position"), reverse=False)
    return standings

def fetch_head2heads():
    r = connect()
    keys = r.smembers("head2heads")

    head2heads = []

    for key in keys:
        res = r.hgetall(key)
        head2head = { k.decode("utf-8").replace(":", "_") : v.decode("utf-8") for k, v in res.items() }
        head2heads.append(head2head)

    head2heads = sorted(head2heads, key=itemgetter("match_date"), reverse=True)
    return head2heads
    

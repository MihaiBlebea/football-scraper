import redis

def connect():
    r = redis.Redis(host='redis', port=6379, db=0)
    return r

def store_standing(standing):
    r = connect()

    key = "standing:" + standing["team_id"]
    for k, value in standing.items():
        if k != "created_at":
            k = k.replace("_", ":")
            r.hset(key, k, value)

    r.sadd("standings", key)


def store_prediction(prediction):
    r = connect()

    key = "prediction:" + prediction["match_id"]
    for k, value in prediction.items():
        if k != "created_at":
            k = k.replace("_", ":")
            r.hset(key, k, value)

    r.sadd("predictions", key)

def store_head2head(match):
    r = connect()

    key = "head2head:" + match["match_id"]
    for k, value in match.items():
        if k != "created_at":
            k = k.replace("_", ":")
            r.hset(key, k, value)

    r.sadd("head2heads", key)
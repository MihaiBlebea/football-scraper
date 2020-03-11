import pymysql

def connect():
    conn = pymysql.connect(
        host="db",
        user="admin",
        password="pass",
        db="db",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def create_standings_table():
    conn = connect()

    cursor = conn.cursor()
    stm = """CREATE TABLE IF NOT EXISTS standings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_name VARCHAR(200),
            league_id VARCHAR(500),
            league_name VARCHAR(500),
            team_id VARCHAR(500),
            team_name VARCHAR(500),
            position VARCHAR(10),
            played VARCHAR(10),
            league_W VARCHAR(500),
            league_D VARCHAR(500),
            league_L VARCHAR(500),
            league_GF VARCHAR(500),
            league_GA VARCHAR(500),
            league_PTS VARCHAR(500),
            team_badge VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
    cursor.execute(stm) 
    conn.commit()
    conn.close()

def create_predictions_table():
    conn = connect()

    cursor = conn.cursor()
    stm = """CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            match_id VARCHAR(200),
            country_id VARCHAR(10),
            country_name VARCHAR(200),
            league_id VARCHAR(10),
            league_name VARCHAR(500),
            match_date VARCHAR(10),
            match_status VARCHAR(10),
            match_time VARCHAR(10),
            match_live VARCHAR(10),
            match_hometeam_id VARCHAR(500),
            match_hometeam_name VARCHAR(500),
            match_hometeam_score VARCHAR(500),
            match_awayteam_id VARCHAR(500),
            match_awayteam_name VARCHAR(500),
            match_awayteam_score VARCHAR(500),
            match_hometeam_halftime_score VARCHAR(500),
            match_awayteam_halftime_score VARCHAR(500),
            match_hometeam_system VARCHAR(500),
            match_awayteam_system VARCHAR(500),
            prob_HW VARCHAR(10),
            prob_D VARCHAR(10),
            prob_AW VARCHAR(10),
            prob_HW_D VARCHAR(10),
            prob_AW_D VARCHAR(10),
            prob_HW_AW VARCHAR(10),
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
    cursor.execute(stm) 
    conn.commit()
    conn.close()

def create_head2heads_table():
    conn = connect()

    cursor = conn.cursor()
    stm = """CREATE TABLE IF NOT EXISTS head2heads (
            id INT AUTO_INCREMENT PRIMARY KEY,
            match_id VARCHAR(200),
            country_id VARCHAR(10),
            match_date VARCHAR(10),
            match_hometeam_id VARCHAR(10),
            match_hometeam_name VARCHAR(500),
            match_awayteam_id VARCHAR(10),
            match_awayteam_name VARCHAR(10),
            match_hometeam_score VARCHAR(10),
            match_awayteam_score VARCHAR(10),
            match_hometeam_halftime_score VARCHAR(10),
            match_awayteam_halftime_score VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
    cursor.execute(stm) 
    conn.commit()
    conn.close()

def store_standing(standing):
    conn = connect()

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) AS count FROM standings WHERE team_id = %s", standing["team_id"])
    result = cursor.fetchone()
    
    if result["count"] == 0:

        cursor = conn.cursor()
        stm = """INSERT INTO standings (
                country_name, league_id, league_name, team_id, team_name,
                position, played, league_W, 
                league_D, league_L, league_GF,
                league_GA, league_PTS, team_badge) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        val = (standing["country_name"],
                standing["league_id"], 
                standing["league_name"], 
                standing["team_id"], 
                standing["team_name"], 
                standing["position"], 
                standing["played"], 
                standing["league_W"], 
                standing["league_D"], 
                standing["league_L"],
                standing["league_GF"],
                standing["league_GA"],
                standing["league_PTS"],
                standing["team_badge"])

        cursor.execute(stm, val)

    else:

        cursor = conn.cursor()
        stm = """UPDATE standings SET
                position = %s, 
                played = %s, 
                league_W = %s, 
                league_D = %s, 
                league_L = %s, 
                league_GF = %s,
                league_GA = %s, 
                league_PTS = %s
                WHERE team_id = %s;"""
        val = (
            standing["position"], 
            standing["played"], 
            standing["league_W"], 
            standing["league_D"], 
            standing["league_L"],
            standing["league_GF"],
            standing["league_GA"],
            standing["league_PTS"],
            standing["team_id"]
        )

        cursor.execute(stm, val)

    conn.commit()
    conn.close()

def store_prediction(standing):
    conn = connect()

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) AS count FROM predictions WHERE match_id = %s", standing["match_id"])
    result = cursor.fetchone()

    if result["count"] == 0:

        cursor = conn.cursor()

        values = []
        while len(values) < len(standing):
            values.append("%s")
            
        separator = ","

        stm = """INSERT INTO predictions (
                match_id, 
                country_id, 
                country_name, 
                league_id, 
                league_name,
                match_date, 
                match_status, 
                match_time, 
                match_live, 
                match_hometeam_id, 
                match_hometeam_name,
                match_hometeam_score, 
                match_awayteam_id,
                match_awayteam_name,
                match_awayteam_score,
                match_hometeam_halftime_score,
                match_awayteam_halftime_score,
                match_hometeam_system,
                match_awayteam_system,
                prob_HW,
                prob_D,
                prob_AW,
                prob_HW_D,
                prob_AW_D,
                prob_HW_AW) 
                VALUES (""" + separator.join(values) + """);"""

        val = list(standing.values())

        cursor.execute(stm, val)

    else: 

        cursor = conn.cursor()

        stm = """UPDATE predictions SET
                match_status = %s,
                match_live = %s, 
                match_hometeam_score = %s, 
                match_awayteam_score = %s,
                match_hometeam_halftime_score = %s,
                match_awayteam_halftime_score = %s,
                match_hometeam_system = %s,
                match_awayteam_system = %s,
                prob_HW = %s,
                prob_D = %s,
                prob_AW = %s,
                prob_HW_D = %s,
                prob_AW_D = %s,
                prob_HW_AW = %s
                WHERE match_id = %s;"""

        val = (
            standing["match_status"],
            standing["match_live"],
            standing["match_hometeam_score"],
            standing["match_awayteam_score"],
            standing["match_hometeam_halftime_score"],
            standing["match_awayteam_halftime_score"],
            standing["match_hometeam_system"],
            standing["match_hometeam_system"],
            standing["prob_HW"],
            standing["prob_D"],
            standing["prob_AW"],
            standing["prob_HW_D"],
            standing["prob_AW_D"],
            standing["prob_HW_AW"],
            standing["match_id"]
        )

        cursor.execute(stm, val)

    conn.commit()
    conn.close()

def valid_head2head(match):
    conn = connect()

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) AS count FROM head2heads WHERE match_id = %s", match["match_id"])
    result = cursor.fetchone()
    conn.close()
    
    if result["count"] == 0:
        return True
    else:
        return False 

def store_head2head(match):
    conn = connect()
    cursor = conn.cursor()

    values = []
    while len(values) < len(match):
        values.append("%s")
        
    separator = ","

    stm = """INSERT INTO head2heads (
            match_id,
            country_id,
            match_date,
            match_hometeam_id,
            match_hometeam_name,
            match_awayteam_id,
            match_awayteam_name,
            match_hometeam_score,
            match_awayteam_score,
            match_hometeam_halftime_score,
            match_awayteam_halftime_score) 
            VALUES (""" + separator.join(values) + """);"""

    val = list(match.values())

    cursor.execute(stm, val)
    conn.commit()

    conn.close()

def select_all_standings():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM standings")
    result = cursor.fetchall()
    conn.close()
    return result

def select_all_predictions():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions")
    result = cursor.fetchall()
    conn.close()
    return result

def select_all_head2heads():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM head2heads")
    result = cursor.fetchall()
    conn.close()
    return result






from thermostat import get_db

def get_info():
    db = get_db()
    cur = db.execute('SELECT * FROM info')
    return cur.fetchone()

def update_info_nickname(nickname):
    db = get_db()
    db.execute('UPDATE info SET nickname = ?', [nickname])
    db.commit()

def get_latest_target_temperature():
    db = get_db()
    cur = db.execute(
        'SELECT temperature '
        'FROM   target_temperatures '
        'ORDER BY id DESC '
        'LIMIT 1')
    return cur.fetchone()

def get_all_target_temperatures():
    db = get_db()
    cur = db.execute('SELECT temperature '
                     'FROM   target_temperatures '
                     'ORDER BY id ')
    return cur.fetchall()

def add_target_temperature(temperature):
    db = get_db()
    db.execute('INSERT INTO target_temperatures (temperature) VALUES (?)',
               [temperature])
    db.commit()

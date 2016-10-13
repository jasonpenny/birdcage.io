import random
from thermostat import app, get_db, jsonify, request

def get_current_temperature():
    """
    As there is no actual hardware available,
    simulate the current room temperature with a random value between 65-75F
    """
    return random.randint(65, 75)

@app.route('/')
def general_info():
    db = get_db()
    cur = db.execute('SELECT * FROM info')
    info = dict(cur.fetchone())

    info['current_temperature'] = get_current_temperature()

    cur = db.execute(
        'SELECT temperature '
        'FROM   target_temperatures '
        'ORDER BY id DESC '
        'LIMIT 1')
    rec = cur.fetchone()
    if rec:
        info['current_target_temperature'] = rec['temperature']

    return jsonify(info)

@app.route('/nickname', methods=['POST'])
def update_nickname():
    data = request.get_json()

    if not data or \
       not data.get('nickname'):
        return (
            jsonify(success=False,
                    error="'nickname' field is required"),
            400)

    db = get_db()
    db.execute('UPDATE info '
               '   SET nickname = ?',
               [data['nickname']])
    db.commit()

    return jsonify(success=True)

@app.route('/current_temperature')
def current_temperature():
    return jsonify(temperature=get_current_temperature())

@app.route('/target_temperatures/current', methods=['GET'])
def get_current_target_temperature():
    db = get_db()
    cur = db.execute(
        'SELECT temperature '
        'FROM   target_temperatures '
        'ORDER BY id DESC '
        'LIMIT 1')
    rec = cur.fetchone()
    if not rec:
        return jsonify(temperature=None)

    return jsonify(temperature=rec['temperature'])

@app.route('/target_temperatures/current', methods=['POST'])
def set_current_target_temperature():
    data = request.get_json()

    if not data or \
       not data.get('temperature'):
        return (
            jsonify(success=False,
                    error="'temperature' field is required"),
            400)

    db = get_db()
    db.execute('INSERT INTO target_temperatures (temperature)'
               'VALUES (?)',
               [data['temperature']])
    db.commit()

    return jsonify(success=True)

@app.route('/target_temperatures')
def get_target_temperature_history():
    db = get_db()
    cur = db.execute('SELECT temperature '
                     'FROM   target_temperatures '
                     'ORDER BY id ')
    entries = [dict(row) for row in cur.fetchall()]
    return jsonify(entries)

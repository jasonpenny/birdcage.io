import random
from thermostat import app, get_db, jsonify, request, IntegrityError

@app.route('/')
def general_info():
    db = get_db()
    cur = db.execute('SELECT * FROM info')
    info = cur.fetchone()
    return jsonify(dict(info))

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
    temp = random.randint(65, 75)
    return jsonify(temperature=temp)

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

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

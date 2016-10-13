from hub import app, get_db, jsonify, request, IntegrityError

@app.route('/v1/thermostats', methods=['GET'])
def list_thermostats():
    db = get_db()
    cur = db.execute('SELECT * FROM thermostats')
    entries = [dict(row) for row in cur.fetchall()]
    return jsonify(entries)

@app.route('/v1/thermostats', methods=['POST'])
def add_thermostat():
    data = request.get_json()

    if not data or \
       not data.get('id') or \
       not data.get('ip_address') or \
       not data.get('port'):
        return (
            jsonify(success=False,
                    error="'id', 'ip_address', and 'port' fields are required"),
            400)

    db = get_db()
    try:
        db.execute('INSERT INTO thermostats (id, ip_address, port, online) '
                   'VALUES (?, ?, ?, 1)',
                   [data['id'], data['ip_address'], data['port']])
        db.commit()
    except IntegrityError:
        return (
            jsonify(success=False,
                    error="'id' [%s] already exists" % data['id']),
            409)

    return (jsonify(success=True), 201)

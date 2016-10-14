from hub import app, get_db, jsonify, request, IntegrityError
from hub.thermostat_api import update_thermostat_target_temperature, \
        get_thermostat_current_temperature, get_thermostat_info

@app.route('/v1/thermostats', methods=['GET'])
def list_thermostats():
    db = get_db()
    cur = db.execute('SELECT * FROM thermostats')
    entries = [{"id": row['id'],
                "online": row['online']}
               for row in cur.fetchall()]
    return jsonify(entries)

@app.route('/v1/thermostats/<unique_id>', methods=['GET'])
def get_thermostat(unique_id):
    db = get_db()
    cur = db.execute('SELECT * FROM thermostats '
                     'WHERE  id = ?',
                     [unique_id])
    rec = cur.fetchone()
    if not rec:
        return (jsonify(success=False,
                        error='Not Found'),
                404)

    info = dict(rec)

    details = get_thermostat_info(rec['id'], rec['ip_address'], rec['port'])
    if details:
        fields_to_copy = {k:v for k, v in details.iteritems()
                          if k in ['nickname',
                                   'current_temperature',
                                   'current_target_temperature']}
        info.update(fields_to_copy)
    else:
        info['online'] = 0

    return jsonify(info)

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
    except IntegrityError:
        db.execute(
            'UPDATE thermostats '
            '   SET ip_address = ?, '
            '       port = ?, '
            '       online = 1 '
            'WHERE  id = ?',
            [data['ip_address'], data['port'],
             data['id']])

    db.commit()

    return (jsonify(success=True), 201)

@app.route('/v1/target_temperature/thermostats/<unique_id>', methods=['POST'])
def set_target_temperature_single(unique_id):
    data = request.get_json()

    if not data or \
       not data.get('temperature'):
        return (
            jsonify(success=False,
                    error="temperature field is required"),
            400)

    db = get_db()
    cur = db.execute('SELECT * FROM thermostats '
                     'WHERE  id = ?',
                     [unique_id])
    rec = cur.fetchone()
    if not rec:
        return (jsonify(success=False,
                        error='Not Found'),
                404)

    update_thermostat_target_temperature(data['temperature'],
                                         rec['id'],
                                         rec['ip_address'],
                                         rec['port'])

    return jsonify(success=True)

@app.route('/v1/target_temperature/thermostats', methods=['POST'])
def set_target_temperature_all():
    data = request.get_json()

    if not data or \
       not data.get('temperature'):
        return (
            jsonify(success=False,
                    error="temperature field is required"),
            400)

    db = get_db()
    cur = db.execute('SELECT * FROM thermostats '
                     'WHERE  online = 1 ')
    for rec in cur.fetchall():
        update_thermostat_target_temperature(data['temperature'],
                                             rec['id'],
                                             rec['ip_address'],
                                             rec['port'])

    return jsonify(success=True)

@app.route('/v1/current_temperature/thermostats')
def get_averate_thermostat_current_temperature():
    db = get_db()
    cur = db.execute('SELECT * FROM thermostats '
                     'WHERE  online = 1 ')

    all_temps = []
    for rec in cur.fetchall():
        temp = get_thermostat_current_temperature(rec['id'],
                                                  rec['ip_address'],
                                                  rec['port'])
        if temp is not None:
            all_temps.append(temp)

    avg_temp = sum(all_temps) / len(all_temps)
    return jsonify(average_temperature=avg_temp)

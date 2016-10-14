from hub import app, jsonify, request
from hub.thermostat_api import update_thermostat_target_temperature, \
        get_thermostat_current_temperature, get_thermostat_info
from hub.db import get_all_thermostats, get_thermostat_by_id, \
        add_or_update_thermostat

@app.route('/v1/thermostats', methods=['GET'])
def list_thermostats():
    entries = [{"id": row['id'],
                "online": row['online']}
               for row in get_all_thermostats()]
    return jsonify(entries)

@app.route('/v1/thermostats/<unique_id>', methods=['GET'])
def get_thermostat(unique_id):
    rec = get_thermostat_by_id(unique_id)
    if not rec:
        return (jsonify(success=False, error='Not Found'), 404)

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

    add_or_update_thermostat(data)

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

    rec = get_thermostat_by_id(unique_id)
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

    for rec in get_all_thermostats(online_only=True):
        update_thermostat_target_temperature(data['temperature'],
                                             rec['id'],
                                             rec['ip_address'],
                                             rec['port'])

    return jsonify(success=True)

@app.route('/v1/current_temperature/thermostats')
def get_averate_thermostat_current_temperature():
    all_temps = []
    for rec in get_all_thermostats(online_only=True):
        temp = get_thermostat_current_temperature(rec['id'],
                                                  rec['ip_address'],
                                                  rec['port'])
        if temp is not None:
            all_temps.append(temp)

    avg_temp = sum(all_temps) / len(all_temps)
    return jsonify(average_temperature=avg_temp)

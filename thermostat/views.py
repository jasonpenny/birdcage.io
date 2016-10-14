import random
from thermostat import app, jsonify, request
from thermostat.db import get_info, update_info_nickname, \
        get_latest_target_temperature, get_all_target_temperatures, \
        add_target_temperature

def get_current_temperature():
    """
    As there is no actual hardware available,
    simulate the current room temperature with a random value between 65-75F
    """
    return random.randint(65, 75)

@app.route('/')
def general_info():
    info = dict(get_info())

    info['current_temperature'] = get_current_temperature()

    rec = get_latest_target_temperature()
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

    update_info_nickname(data['nickname'])

    return jsonify(success=True)

@app.route('/current_temperature')
def current_temperature():
    return jsonify(temperature=get_current_temperature())

@app.route('/target_temperatures/current', methods=['GET'])
def get_current_target_temperature():
    rec = get_latest_target_temperature()
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

    add_target_temperature(data['temperature'])

    return jsonify(success=True)

@app.route('/target_temperatures')
def get_target_temperature_history():
    entries = [dict(row) for row in get_all_target_temperatures()]
    return jsonify(entries)

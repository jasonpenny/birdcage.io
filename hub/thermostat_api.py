from lib.http_requests import post_json, get_json, HTTPError, URLError
from hub.db import mark_thermostat_as_offline

def update_thermostat_target_temperature(target_temperature,
                                         thermostat_id,
                                         thermostat_ip_address,
                                         thermostat_port):
    url = 'http://{host}:{port}/target_temperatures/current' \
            .format(host=thermostat_ip_address,
                    port=thermostat_port)
    data = {"temperature": target_temperature}

    try:
        post_json(url, data)
        return True
    except (HTTPError, URLError):
        mark_thermostat_as_offline(thermostat_id)

        return False

def get_thermostat_current_temperature(thermostat_id,
                                       thermostat_ip_address,
                                       thermostat_port):
    url = 'http://{host}:{port}/current_temperature' \
            .format(host=thermostat_ip_address,
                    port=thermostat_port)

    try:
        data = get_json(url)
    except (HTTPError, URLError):
        mark_thermostat_as_offline(thermostat_id)

        return None

    return data.get('temperature')

def get_thermostat_info(thermostat_id,
                        thermostat_ip_address,
                        thermostat_port,
                        db=None):
    url = 'http://{host}:{port}/' \
            .format(host=thermostat_ip_address,
                    port=thermostat_port)

    try:
        return get_json(url)
    except (HTTPError, URLError):
        mark_thermostat_as_offline(thermostat_id, db=db)

        return None

from lib.http_requests import post_json, get_json, HTTPError, URLError

def update_thermostat_target_temperature(target_temperature,
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
        # TODO : mark thermostat as not online

        return False

def get_thermostat_current_temperature(thermostat_ip_address,
                                       thermostat_port):
    url = 'http://{host}:{port}/current_temperature' \
            .format(host=thermostat_ip_address,
                    port=thermostat_port)

    try:
        data = get_json(url)
    except (HTTPError, URLError):
        # TODO : mark thermostat as not online

        return None

    return data.get('temperature')

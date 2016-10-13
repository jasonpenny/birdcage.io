from lib.http_requests import post_json

def update_thermostat_target_temperature(target_temperature,
                                         thermostat_ip_address,
                                         thermostat_port):
    url = 'http://{host}:{port}/target_temperatures/current' \
            .format(host=thermostat_ip_address,
                    port=thermostat_port)
    data = {"temperature": target_temperature}

    post_json(url, data)

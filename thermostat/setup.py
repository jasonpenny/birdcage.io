import random
import socket

from lib.http_requests import post_json

def find_unused_port():
    while True:
        try:
            port = random.randint(8001, 8099)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', port))
            addr, _ = s.getsockname()
            s.close()

            return addr, port
        except socket.error:
            pass

def register_with_hub(hub_ip_address, hub_port,
                      thermostat_id, thermostat_ip_address, thermostat_port):
    url = 'http://{host}:{port}/v1/thermostats' \
            .format(host=hub_ip_address, port=hub_port)
    data = {"id": thermostat_id,
            "ip_address": thermostat_ip_address,
            "port": thermostat_port}

    post_json(url, data)

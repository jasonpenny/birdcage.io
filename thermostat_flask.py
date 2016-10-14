import json
import os
import sys

from thermostat.setup import find_unused_port, register_with_hub, safe_filename
from thermostat import app, init_db
from lib.http_requests import HTTPError

HUB_IP_ADDRESS = '127.0.0.1'
HUB_PORT = 3000

if len(sys.argv) < 2:
    print 'Usage: %s <unique_id>' % sys.argv[0]
    exit(1)

addr, port = find_unused_port()

unique_id = sys.argv[1]
try:
    register_with_hub(HUB_IP_ADDRESS, HUB_PORT,
                      unique_id, addr, port)
    print 'Registered thermostat {unique_id} with hub on {addr}:{port}' \
            .format(unique_id=unique_id, addr=addr, port=port)
except HTTPError as err:
    response = json.loads(err.read())
    print response['error']

    exit(2)

app.config.update(
    DATABASE=os.path.join(app.root_path, '%s.db' % safe_filename(unique_id)))

# create database if doesn't exist yet
if not os.path.isfile(app.config['DATABASE']):
    init_db(unique_id)

app.run(port=port)

# birdcage.io

This is a fake project to model a home thermostat automation system. The system consists of thermostat devices which expose an API and a 'hub' which exposes a separate API, and these two components communicate with each other.

Setup for test environment
--------------------------

The code is written for python 2.7

Both the hub project and thermostat project depend only on Flask, so first install with:

    pip install -r requirements.txt

##### Run hub:

    python hub_flask.py

##### Run two thermostat instances

    python thermostat_flask.py unique-id-1
    python thermostat_flask.py unique-id-2

##### Test that connections are working

> curl localhost:3000/v1/thermostats

    [{"id":"unique-id-1","online":1},{"id":"unique-id-2","online":1}]

> curl localhost:3000/v1/thermostats/unique-id-1

    {"current_temperature":71,"id":"unique-id-1","ip_address":"127.0.0.1","nickname":null,"online":1,"port":8071}

  * set the nickname of the first thermostat

> curl localhost:8071/nickname -X POST -H Content-Type:application/json -d '{"nickname": "first thermostat"}'

    {"success":true}

  * get the detailed info of the first thermostat from the hub, note the nickname is returned

> curl localhost:3000/v1/thermostats/unique-id-1

    {"current_temperature":75,"id":"unique-id-1","ip_address":"127.0.0.1","nickname":"first thermostat","online":1,"port":8071}

  * kill the first thermostat process with Ctrl-C
  * wait 2 minutes
  * the background thread should have marked `unique-id-1` as offline (online:0)

> curl localhost:3000/v1/thermostats

    [{"id":"unique-id-1","online":0},{"id":"unique-id-2","online":1}]


hub API
-------

#### GET /v1/thermostats

Returns a list of registered thermostats (including online status)

#### GET /v1/thermostats/:id

Returns detailed information about a registered thermostat for the given `:id` value

#### POST /v1/thermostats

Adds a new registered thermostat

**example request**

    { "id": "[unique_id]", "ip_address": "X.X.X.X", "port": 8044 }

#### POST /v1/target_temperature/thermostats

Sets the target temperature for all connected thermostats

**example request**

    { "temperature": 65 }

#### POST /v1/target_temperature/thermostats/:id

Sets the target temperature for a single thermostat for the given `:id` value

**example request**

    { "temperature": 65 }

#### GET /v1/current_temperature/thermostats

Returns the average current room temperature across all registered thermostats

thermostat API
--------------

#### GET /

Returns general thermostat information

#### POST /nickname

Sets the thermostat nickname

**example request**

    { "nickname": "[nickname]" }

#### GET /current_temperature

Gets the current room temperature (As there is no actual hardware available, simulate the current room temperature with a random value between 65­75F)

#### GET /target_temperature/current

Returns the current target temperature

#### POST /target_temperature/current

Sets the current target temperature

**example request**

    { "temperature": 65 }

#### GET /target_temperature

Returns the list of target temperatures (the temperature change history)

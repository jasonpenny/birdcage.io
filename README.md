# birdcage.io

This is a fake project to model a home thermostat automation system. The system consists of thermostat devices which expose an API and a 'hub' which exposes a separate API, and these two components communicate with each other.

Setup for test environment
--------------------------

TODO

hub API
-------

#### GET /v1/thermostats

Returns a list of registered thermostats (including online status)

#### GET /v1/thermostats/:id

Returns detailed information about a registered thermostat for the given `:id` value

#### POST /v1/thermostats

Adds a new registered thermostat

**example request**

    { "id": "[unique_id]", "ip": "X.X.X.X", "port": 8044 }

#### POST /v1/target_temperature/thermostats

Sets the target temperature for all connected thermostats

**example request**

    { "temperature": 65 }

#### POST /v1/target_temperature/thermostats/:id

Sets the target temperature for a single thermostat for the given `:id` value

**example request**

    { "temperature": 65 }

#### GET /v1/current_temperature

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

import os

from hub import app, init_db
from hub.background_update import CheckThermostatsConnectivity

# initialize database if it doesn't exist
if not os.path.isfile(app.config['DATABASE']):
    init_db()

# start background thread to periodicaly check connection with each registered
# thermostat and mark as offline if can't be reached
CheckThermostatsConnectivity(interval=120,
                             database=app.config['DATABASE'])

app.run(port=3000)

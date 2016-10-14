import threading
import time

from hub import connect_db
from hub.db import get_all_thermostats
from hub.thermostat_api import get_thermostat_info

class CheckThermostatsConnectivity(object):
    def __init__(self, interval, database):
        self.interval = interval
        self.database = database

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            db = connect_db()

            for thermostat in get_all_thermostats(db=db, online_only=True):
                # this will automatically mark the thermostat as offline
                # if the thermostat gives an error or is not accessible
                get_thermostat_info(thermostat['id'],
                                    thermostat['ip_address'],
                                    thermostat['port'],
                                    db=db)

            db.close()

            time.sleep(self.interval)
